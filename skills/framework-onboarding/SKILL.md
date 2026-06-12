---
name: framework-onboarding
description: >-
  First-time user onboarding experience. Keywords: new, first, start, begin,
  welcome, tutorial, guide, learn, help me.
  Activates on first /init or when .brain/preferences.json doesn't exist.
version: 1.0.0
---

# AI Agent Standards Onboarding

Hướng dẫn người dùng mới làm quen với AI Agent Standards.

## Trigger Conditions

**Activates when:**
- User chạy `/init` lần đầu (không có `.brain/` folder)
- User chạy `/help` và chưa có preferences
- User nói "mới dùng", "hướng dẫn", "không biết bắt đầu"

**Check:**
```
if NOT exists(".brain/preferences.json") AND NOT exists("~/.ai-agent-standards/preferences.json"):
     Activate onboarding
else:
     Skip (returning user)
```

## Execution Logic

### Step 1: Welcome Message

```
👋 **CHÀO MỪNG ĐẾN VỚI AI Agent Standards!**

Em là trợ lý AI, sẽ giúp anh biến ý tưởng thành app thật.

🎯 AI Agent Standards có thể giúp anh:
   • Tạo app/website từ con số 0
   • Không cần biết code (em làm giùm!)
   • Nhớ mọi thứ giữa các lần làm việc

⏱️ Cho em 2 phút để hướng dẫn nhanh nhé?

1️⃣ Có, hướng dẫn em đi
2️⃣ Không cần, bắt đầu luôn
```

### Step 2: Quick Assessment (nếu chọn 1)

```
📊 **EM CẦN HIỂU ANH MỘT CHÚT:**

Anh đã từng làm app/website chưa?

1️⃣ Chưa bao giờ (newbie)
   → Em sẽ giải thích mọi thứ đơn giản

2️⃣ Có biết chút chút (basic)
   → Em giải thích khi cần

3️⃣ Dân IT rồi (technical)
   → Em nói chuyện như đồng nghiệp
```

### Step 3: 5 Commands Tour

```
🗺️ **5 LỆNH QUAN TRỌNG NHẤT:**

┌─────────────────────────────────────────┐
│ 1️⃣ /brainstorm                          │
│    "Tôi có ý tưởng nhưng chưa rõ"       │
│    → AI giúp làm rõ ý tưởng             │
├─────────────────────────────────────────┤
│ 2️⃣ /plan                                │
│    "Tôi biết muốn làm gì rồi"           │
│    → AI lên kế hoạch chi tiết           │
├─────────────────────────────────────────┤
│ 3️⃣ /code                                │
│    "Bắt đầu viết code đi"               │
│    → AI code theo kế hoạch              │
├─────────────────────────────────────────┤
│ 4️⃣ /run                                 │
│    "Chạy thử xem nào"                   │
│    → Khởi động app để xem kết quả       │
├─────────────────────────────────────────┤
│ 5️⃣ /debug                               │
│    "Có lỗi rồi, sửa giùm"               │
│    → AI tìm và sửa lỗi                  │
└─────────────────────────────────────────┘

💡 Mẹo: Không cần nhớ hết! Gõ /next bất cứ lúc nào
   để em gợi ý nên làm gì tiếp.
```

### Step 4: Quick Start Options

```
🚀 **BẮT ĐẦU THÔI!**

Anh muốn làm gì?

1️⃣ Tôi có ý tưởng app rồi → /plan
2️⃣ Chưa rõ, muốn bàn trước → /brainstorm
3️⃣ Hướng dẫn chi tiết hơn → /help
4️⃣ Tùy chỉnh cách AI nói chuyện → /customize
```

### Step 5: Initialize .brain/ Folder

**Tạo folder structure:**
```
.brain/
├── preferences.json
├── session.json
├── session_log.txt
└── brain.json
```

**preferences.json:**
```json
{
  "communication": {
    "tone": "friendly",
    "personality": "assistant"
  },
  "technical": {
    "technical_level": "[user_choice]",
    "detail_level": "simple",
    "autonomy_level": "ask_often"
  },
  "onboarding_completed": true,
  "onboarding_date": "[timestamp]"
}
```

**session.json:**
```json
{
  "updated_at": "[timestamp]",
  "working_on": {
    "feature": null,
    "task": null,
    "status": "idle"
  },
  "pending_tasks": [],
  "errors_encountered": [],
  "decisions_made": [
    {
      "decision": "Technical level set to [level]",
      "reason": "User selection during onboarding"
    }
  ],
  "skipped_tests": []
}
```

**session_log.txt:**
```
[YYYY-MM-DD HH:MM] ONBOARDING COMPLETE
[YYYY-MM-DD HH:MM] Technical level: [level]
[YYYY-MM-DD HH:MM] Ready for first project
```

**brain.json:**
```json
{
  "meta": {
    "schema_version": "1.0.0",
    "framework_version": "4.0.2",
    "created_at": "[timestamp]"
  },
  "project": {
    "name": null,
    "type": null,
    "status": "not_started"
  },
  "updated_at": "[timestamp]"
}
```

### Step 6: Save & Complete

```
✅ **HOÀN TẤT SETUP!**

Em đã tạo:
📁 .brain/
   ├── preferences.json  (cài đặt của anh)
   ├── session.json      (theo dõi tiến độ)
   ├── session_log.txt   (nhật ký)
   └── brain.json        (kiến thức dự án)

💾 Mọi thứ sẽ được tự động lưu từ giờ!

────────────────────────

Giờ anh muốn làm gì?

1️⃣ Tạo dự án đầu tiên → /init
2️⃣ Bàn ý tưởng trước → /brainstorm
3️⃣ Xem hướng dẫn chi tiết → /help
```

## Returning User Detection

```
if exists("preferences.json") AND preferences.onboarding_completed == true:

     Nếu > 7 ngày không dùng:
          "👋 Chào mừng anh quay lại! Gõ /recap để em nhắc lại đang làm gì nhé."

     Nếu < 7 ngày:
          Skip welcome, vào thẳng workflow
```

## Error Handling

```
If cannot create .brain/ folder:
    Try create in current directory
    If still fail:
        Warning: "⚠️ Em không tạo được folder lưu trữ, nhưng vẫn làm việc được!"
        Continue in-memory mode

If user skips all steps:
    Use defaults: technical_level = "basic"
    Mark onboarding_completed = true
```

## Integration

**Với /init:**
```
/init được gọi
    ↓
Check .brain/ folder
    ↓
├── Không có → Chạy onboarding TRƯỚC
└── Có rồi → Chạy /init bình thường
```

## Performance

- Total time: < 2 minutes
- No external API calls
- Minimal file I/O
