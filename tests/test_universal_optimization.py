from pathlib import Path
import shutil

from agent_guidance_mcp.catalog import build_catalog
from agent_guidance_mcp.server import register_handlers
from agent_guidance_mcp.token_optimizer import (
    ContentType,
    OptimizationConfig,
    OptimizationSettings,
    TokenOptimizer,
)


class FakeMCP:
    def __init__(self):
        self.resources = {}
        self.tools = {}
        self.prompts = {}

    def resource(self, uri, mime_type=None):
        def decorator(func):
            self.resources[uri] = {"func": func, "mime_type": mime_type}
            return func

        return decorator

    def tool(self):
        def decorator(func):
            self.tools[func.__name__] = func
            return func

        return decorator

    def prompt(self):
        def decorator(func):
            self.prompts[func.__name__] = func
            return func

        return decorator


def test_safe_defaults_from_empty_environment():
    settings = OptimizationSettings.from_env({})

    assert settings.enabled is True
    assert settings.level == "conservative"
    assert settings.max_tokens == 12000
    assert settings.cache_enabled is True
    assert settings.cache_ttl == 300
    assert settings.auto_detect is True
    assert settings.log_metrics is False


def test_env_parsing_and_invalid_level_fallback():
    settings = OptimizationSettings.from_env(
        {
            "RTK_OPTIMIZATION_ENABLED": "false",
            "RTK_OPTIMIZATION_LEVEL": "turbo",
            "RTK_MAX_TOKENS": "250",
            "RTK_CACHE_ENABLED": "no",
            "RTK_CACHE_TTL": "12",
            "RTK_AUTO_DETECT": "off",
            "RTK_LOG_METRICS": "yes",
        }
    )

    assert settings.enabled is False
    assert settings.level == "conservative"
    assert settings.max_tokens == 250
    assert settings.cache_enabled is False
    assert settings.cache_ttl == 12
    assert settings.auto_detect is False
    assert settings.log_metrics is True


def test_invalid_per_call_max_tokens_falls_back_to_current_default():
    settings = OptimizationSettings(max_tokens=321)

    overridden = settings.with_overrides(rtk_max_tokens="abc")

    assert overridden.max_tokens == 321


def test_invalid_mcp_rtk_max_tokens_does_not_crash():
    root = Path(__file__).resolve().parents[1]
    catalog = build_catalog(root)
    mcp = FakeMCP()
    register_handlers(mcp, catalog)

    result = mcp.tools["read_project_file"](
        str(root),
        "README.md",
        max_lines=1,
        rtk_max_tokens="abc",
    )

    assert result["content"]
    assert result["rtk"]["truncated"] is False


def test_content_type_detection_for_common_payloads():
    optimizer = TokenOptimizer()

    assert optimizer.optimize('{"ok": true}', "resource:json").content_type == ContentType.JSON
    assert (
        optimizer.optimize("def one():\n    pass\nclass Two:\n    pass", "resource:code").content_type
        == ContentType.CODE
    )
    assert (
        optimizer.optimize("ERROR failed\n2026-01-01 [ERROR] failed", "tool:test").content_type
        == ContentType.ERROR
    )
    assert (
        optimizer.optimize("- one\n- two\n- three", "resource:list").content_type
        == ContentType.LIST
    )


def test_cache_hit_for_safe_generated_tree():
    optimizer = TokenOptimizer(OptimizationConfig(max_tokens=10))
    payload = {
        "project_root": "x",
        "max_depth": 3,
        "tree": [
            {"path": f"src/module_{index}.py", "type": "file", "size_bytes": 10}
            for index in range(50)
        ],
    }

    first = optimizer.optimize(
        payload, "tool:get_project_tree", context={"mutation_policy": "safe_generated"}
    )
    second = optimizer.optimize(
        payload, "tool:get_project_tree", context={"mutation_policy": "safe_generated"}
    )

    assert first.modified is True
    assert first.truncated is True
    assert second.cache_hit is True
    assert second.optimized_content["rtk"]["cache_hit"] is True
    assert second.optimized_content["rtk"]["omitted_count"] > 0


def test_disabled_optimizer_leaves_payload_without_rtk_metadata():
    optimizer = TokenOptimizer(OptimizationConfig(enabled=False))
    payload = {"content": "unchanged"}

    result = optimizer.optimize(
        payload, "tool:read_project_file", context={"mutation_policy": "edit_critical"}
    )

    assert result.optimized_content == payload
    assert "rtk" not in result.optimized_content
    assert result.strategy_used == "disabled"


def test_modified_uses_content_equality_not_token_count():
    optimizer = TokenOptimizer(OptimizationConfig(max_tokens=1000))
    original = {
        "project_root": "x",
        "max_depth": 1,
        "tree": [{"path": "aaaaaaaa.py", "type": "file"}],
    }
    optimized = {
        "project_root": "x",
        "max_depth": 1,
        "tree": [{"path": "bbbbbbbb.py", "type": "file"}],
    }
    original_serialized = optimizer._serialize_content(original)
    optimized_serialized = optimizer._serialize_content(optimized)

    result = optimizer._finalize(
        optimized,
        optimizer.count_tokens(original_serialized),
        original_serialized,
        ["structural"],
        ContentType.TREE,
        "tool:get_project_tree",
        False,
        {},
        4000,
    )

    assert optimizer.count_tokens(optimized_serialized) == result.original_tokens
    assert result.modified is True
    assert result.optimized_content["rtk"]["modified"] is True


def test_structured_metadata_token_count_matches_final_payload():
    optimizer = TokenOptimizer(OptimizationConfig(max_tokens=10))
    payload = {
        "project_root": "x",
        "max_depth": 3,
        "tree": [
            {"path": f"src/module_{index}.py", "type": "file", "size_bytes": 10}
            for index in range(50)
        ],
    }

    result = optimizer.optimize(
        payload, "tool:get_project_tree", context={"mutation_policy": "safe_generated"}
    )
    serialized = optimizer._serialize_content(result.optimized_content)

    assert result.optimized_content["rtk"]["optimized_tokens"] == optimizer.count_tokens(serialized)
    assert result.optimized_tokens == optimizer.count_tokens(serialized)


def test_cap_exceeded_by_metadata_is_reported_for_tiny_caps():
    optimizer = TokenOptimizer(OptimizationConfig(max_tokens=1))

    result = optimizer.optimize(
        {"content": "abcd"},
        "tool:read_project_file",
        context={"mutation_policy": "edit_critical"},
    )

    assert result.optimized_content["rtk"]["cap_exceeded_by_metadata"] is True


def test_read_project_file_preserves_exact_content_under_normal_limits():
    root = Path(__file__).resolve().parents[1]
    catalog = build_catalog(root)
    mcp = FakeMCP()
    register_handlers(mcp, catalog)

    result = mcp.tools["read_project_file"](str(root), "README.md", max_lines=3)

    expected = "\n".join(
        Path(root / "README.md").read_text(encoding="utf-8").splitlines()[:3]
    )
    assert result["content"] == expected
    assert result["rtk"]["modified"] is False
    assert result["rtk"]["truncated"] is False


def test_read_project_file_forced_truncation_has_continuation_metadata():
    root = Path(__file__).resolve().parents[1]
    project = root / ".tmp_rtk_test_project"
    if project.exists():
        shutil.rmtree(project)
    project.mkdir()
    (project / "sample.txt").write_text(
        "\n".join(f"line {index:02d} has enough content" for index in range(20)),
        encoding="utf-8",
    )
    catalog = build_catalog(root)
    mcp = FakeMCP()
    register_handlers(mcp, catalog)

    try:
        result = mcp.tools["read_project_file"](
            str(project),
            "sample.txt",
            max_lines=20,
            rtk_max_tokens=8,
        )
    finally:
        shutil.rmtree(project)

    assert result["rtk"]["modified"] is True
    assert result["rtk"]["truncated"] is True
    assert result["rtk"]["omitted_lines"] > 0
    assert result["rtk"]["continuation"]["next_start_line"] > result["end_line"]
    assert result["rtk"]["continuation"]["suggested_tool"] == "read_project_file"


def test_stats_tools_report_and_reset():
    root = Path(__file__).resolve().parents[1]
    catalog = build_catalog(root)
    mcp = FakeMCP()
    register_handlers(mcp, catalog)

    mcp.tools["get_project_tree"](str(root), max_depth=1)
    stats = mcp.tools["get_rtk_stats"](detailed=True)

    assert stats["total_actions"] >= 1
    assert "by_action_type" in stats

    reset = mcp.tools["reset_rtk_stats"]()
    assert reset == {"status": "reset"}
    assert mcp.tools["get_rtk_stats"]()["total_actions"] == 0


def test_general_dict_pruning():
    from agent_guidance_mcp.token_optimizer.core import prune_structure
    data = {
        "key1": "value1",
        "key2": "value2",
        "nested_list": ["item1", "item2", "item3", "item4", "item5"],
        "nested_dict": {"k1": "v1", "k2": "v2", "k3": "v3"}
    }
    
    # Check that it returns unchanged if it fits in target_len
    pruned, meta, truncated = prune_structure(data, 1000)
    assert not truncated
    assert pruned == data

    # Prune nested collections
    pruned, meta, truncated = prune_structure(data, 100)
    assert truncated
    # Check that nested_list or nested_dict was pruned or keys omitted
    assert len(pruned.get("nested_list", [])) < 5 or len(pruned.get("nested_dict", {})) < 3 or "key2" not in pruned


def test_cache_hit_deepcopies_lists():
    # Set max_tokens to 1 to force truncation and cache entry
    optimizer = TokenOptimizer(OptimizationConfig(cache_enabled=True, max_tokens=1))
    payload = [{"name": "item1"}, {"name": "item2"}, {"name": "item3"}]
    
    first = optimizer.optimize(payload, "tool:list_entries", context={"mutation_policy": "safe_generated"})
    second = optimizer.optimize(payload, "tool:list_entries", context={"mutation_policy": "safe_generated"})
    
    assert second.cache_hit is True
    # Mutate the list returned by second call
    second.optimized_content.append({"name": "item4"})
    
    # Fetch third time, it should NOT contain the mutated item since it deepcopies from the cache
    third = optimizer.optimize(payload, "tool:list_entries", context={"mutation_policy": "safe_generated"})
    assert {"name": "item4"} not in third.optimized_content


def test_cache_key_varies_by_auto_detect():
    optimizer = TokenOptimizer()
    payload = "def test_func(): pass"
    
    # First config has auto_detect_type=True
    config1 = OptimizationConfig(auto_detect_type=True)
    key1 = optimizer._cache_key(payload, "tool:test", {}, config1)
    
    # Second config has auto_detect_type=False
    config2 = OptimizationConfig(auto_detect_type=False)
    key2 = optimizer._cache_key(payload, "tool:test", {}, config2)
    
    assert key1 != key2


def test_inline_repeated_error_collapsing():
    from agent_guidance_mcp.token_optimizer.strategies import SemanticCompression
    compressor = SemanticCompression()
    
    logs = (
        "normal log line 1\n"
        "ConnectionTimeoutError: attempt 1 failed\n"
        "ConnectionTimeoutError: attempt 2 failed\n"
        "ConnectionTimeoutError: attempt 3 failed\n"
        "ConnectionTimeoutError: attempt 4 failed\n"
        "ConnectionTimeoutError: attempt 5 failed\n"
        "normal log line 2"
    )
    
    compacted, meta = compressor.compress(logs, "error", 1000)
    
    expected = (
        "normal log line 1\n"
        "ConnectionTimeoutError: attempt 1 failed\n"
        "ConnectionTimeoutError: attempt 2 failed\n"
        "ConnectionTimeoutError: attempt 3 failed\n"
        "[RTK: 2 similar error lines collapsed]\n"
        "normal log line 2"
    )
    assert compacted == expected

