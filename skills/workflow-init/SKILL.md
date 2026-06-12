---
description: Khởi tạo dự án mới
---

# WORKFLOW: /init - Khởi Tạo Dự Án

**Vai trò:** Project Initializer
**Mục tiêu:** Capture ý tưởng và tạo workspace cơ bản. KHÔNG install packages, KHÔNG setup database.

**NGÔN NGỮ: Luôn trả lời bằng tiếng Việt.**

---

## Flow Position

```
[/init] ← BẠN ĐANG Ở ĐÂY
   ↓
/brainstorm (nếu chưa rõ ý tưởng)
   ↓
/plan (lên kế hoạch features)
   ↓
/design (thiết kế kỹ thuật)
   ↓
/code (viết code)
```

---

## Stage 1: Capture Vision (HỎI NGẮN GỌN)

### 1.1. Tên dự án
"Tên dự án là gì? (VD: my-coffee-app)"

### 1.2. Mô tả 1 câu
"Mô tả ngắn gọn app làm gì? (1-2 câu)"

### 1.3. Vị trí
"Tạo ở thư mục hiện tại hay chỗ khác?"

**XONG. Không hỏi thêm.**

---

## Stage 2: Tạo Workspace (CHỈ TẠO FOLDER)

Chỉ tạo cấu trúc folder cơ bản:

```
{project-name}/
├── .brain/
│   └── brain.json      # Project context (empty template)
├── docs/
│   └── ideas.md        # Ghi ý tưởng
└── README.md           # Tên + mô tả
```

### brain.json template:
```json
{
  "project": {
    "name": "{project-name}",
    "description": "{mô tả}",
    "created_at": "{timestamp}"
  },
  "tech_stack": [],
  "features": [],
  "decisions": []
}
```

### README.md template:
```markdown
# {Project Name}

{Mô tả 1 câu}

## Status: 🚧 Planning

Dự án đang trong giai đoạn lên ý tưởng.

## Next Steps

1. Gõ `/brainstorm` để explore ý tưởng
2. Hoặc `/plan` nếu đã rõ muốn làm gì
```

---

## Stage 3: Xác nhận & Hướng dẫn

```
✅ Đã tạo workspace cho "{project-name}"!

📁 Vị trí: {path}

🚀 BƯỚC TIẾP THEO:

Chọn 1 trong 2:

1️⃣ /brainstorm - Nếu chưa rõ muốn làm gì, cần explore ý tưởng
2️⃣ /plan - Nếu đã biết rõ features cần làm

💡 Tip: Newbie nên chọn /brainstorm trước!
```

---

## QUAN TRỌNG - KHÔNG LÀM

❌ KHÔNG install packages (để /code làm)
❌ KHÔNG setup database (để /design làm)
❌ KHÔNG tạo code files (để /code làm)
❌ KHÔNG chạy npm/yarn/pnpm
❌ KHÔNG hỏi về tech stack (AI sẽ tự quyết sau)

---

## First-time User

Nếu chưa có `.brain/preferences.json`:

```
👋 Chào mừng bạn đến với AI Agent Standards!

Đây là lần đầu dùng. Bạn muốn:
1️⃣ Dùng mặc định (Recommended)
2️⃣ Tùy chỉnh (/customize)
```

---

## Error Handling

### Folder đã tồn tại:
```
⚠️ Folder "{name}" đã có rồi.
1️⃣ Dùng folder này (có thể ghi đè)
2️⃣ Đổi tên khác
```

### Không có quyền tạo folder:
```
❌ Không tạo được folder. Kiểm tra quyền write nhé!
```
