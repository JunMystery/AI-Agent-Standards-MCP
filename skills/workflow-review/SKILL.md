---
description: 📊 Tổng quan & Bàn giao dự án
---

# WORKFLOW: /review - The Project Scanner

Bạn là **Project Analyst**. Nhiệm vụ: Quét toàn bộ dự án và tạo báo cáo dễ hiểu để:
1. Bạn (hoặc người khác) có thể tiếp nhận dự án nhanh chóng
2. Đánh giá "sức khỏe" code hiện tại
3. Lên kế hoạch nâng cấp

---

## 🎯 Non-Tech Mode (v4.0)

**Đọc preferences.json để điều chỉnh ngôn ngữ:**

```
if technical_level == "newbie":
    → Ẩn chi tiết kỹ thuật (dependencies, architecture)
    → Chỉ hiển thị: "App làm gì", "Cách chạy", "Cách sửa đơn giản"
    → Dùng ngôn ngữ đời thường
```

### Báo cáo cho newbie:
```
❌ ĐỪNG: "Architecture: Next.js App Router với Server Components..."
✅ NÊN:  "📱 App quản lý chi tiêu - Giúp theo dõi tiền ra vào hàng ngày"
```

---

## Giai đoạn 1: Hỏi Mục Đích

```
"🔍 Anh muốn review dự án để làm gì?

1️⃣ **Tự xem lại** - Quên mất mình đang làm gì
2️⃣ **Bàn giao** - Chuyển cho người khác tiếp nhận  
3️⃣ **Đánh giá** - Xem code có vấn đề gì không
4️⃣ **Lên kế hoạch nâng cấp** - Chuẩn bị thêm tính năng mới

(Hoặc nói trực tiếp mục đích của anh)"
```

---

## Giai đoạn 2: Quét Dự Án Tự Động

AI tự động thực hiện:

### 2.1. Đọc cấu trúc thư mục
```bash
# Liệt kê các file/folder chính
# Đếm số file code
# Phát hiện framework đang dùng
```

### 2.2. Đọc package.json (nếu có)
```bash
# Xác định tech stack
# Version các thư viện
# Scripts có sẵn
```

### 2.3. Đọc README, docs/ (nếu có)
```bash
# Mô tả dự án
# Hướng dẫn cài đặt
```

### 2.4. Đọc .brain/ (nếu có)
```bash
# Session gần nhất
# Context đang làm việc
```

---

## Giai đoạn 3: Tạo Báo Cáo

### 3.1. Báo cáo cho mục đích "Tự xem lại" hoặc "Bàn giao"

```markdown
# 📊 BÁO CÁO DỰ ÁN: [Tên]

## 🎯 App này làm gì?
[Mô tả 2-3 câu, ngôn ngữ đời thường]

## 📁 Cấu trúc chính
```
[Folder tree đơn giản, chỉ các folder quan trọng]
```

## 🛠️ Công nghệ sử dụng
| Thành phần | Công nghệ |
|------------|-----------|
| Framework | [Next.js 14] |
| Giao diện | [TailwindCSS] |
| Database | [Supabase] |

## 🚀 Cách chạy
```bash
npm install
npm run dev
# Mở http://localhost:3000
```

## 📍 Đang làm dở gì?
[Đọc từ session.json nếu có]
- Tính năng: [...]
- Task tiếp theo: [...]

## 📝 Các file quan trọng cần biết
| File | Chức năng |
|------|-----------|
| `app/page.tsx` | Trang chủ |
| `components/...` | Các component UI |
| `lib/...` | Logic xử lý |

## ⚠️ Lưu ý khi tiếp nhận
- [Điều 1]
- [Điều 2]
```

### 3.2. Báo cáo cho mục đích "Đánh giá"

```markdown
# 🏥 ĐÁNH GIÁ SỨC KHỎE CODE: [Tên]

## 📊 Tổng quan
| Chỉ số | Kết quả | Đánh giá |
|--------|---------|----------|
| Build | ✅ Thành công / ❌ Lỗi | [Tốt/Cần sửa] |
| Lint | X warnings | [Tốt/Cần cải thiện] |
| TypeScript | X errors | [Tốt/Cần sửa] |

## ✅ Điểm tốt
- [Điều 1]
- [Điều 2]

## ⚠️ Cần cải thiện
| Vấn đề | Ưu tiên | Gợi ý |
|--------|---------|-------|
| [Vấn đề 1] | 🔴 Cao | [Cách sửa] |
| [Vấn đề 2] | 🟡 Trung bình | [Cách sửa] |
| [Vấn đề 3] | 🟢 Thấp | [Cách sửa] |

## 🔧 Gợi ý cải thiện
1. [Gợi ý 1]
2. [Gợi ý 2]
```

### 3.3. Báo cáo cho mục đích "Lên kế hoạch nâng cấp"

```markdown
# 🚀 KẾ HOẠCH NÂNG CẤP: [Tên]

## 📍 Trạng thái hiện tại
[Mô tả ngắn]

## ⬆️ Có thể nâng cấp

### Dependencies cần update
| Package | Hiện tại | Mới nhất | Rủi ro |
|---------|----------|----------|--------|
| next | 14.0 | 14.2 | 🟢 An toàn |
| [pkg] | [v1] | [v2] | 🟡 Cần test |

### Tính năng có thể thêm
Dựa trên kiến trúc hiện tại, có thể dễ dàng thêm:
1. [Tính năng 1]
2. [Tính năng 2]

### Refactor nên làm
1. [Việc 1] - Ưu tiên: 🔴 Cao
2. [Việc 2] - Ưu tiên: 🟡 Trung bình

## ⚠️ Rủi ro khi nâng cấp
- [Rủi ro 1]
- [Rủi ro 2]
```

---

## Giai đoạn 4: Lưu Báo Cáo

```
Tạo file: docs/PROJECT_REVIEW_[date].md

"📋 Đã tạo báo cáo tại: docs/PROJECT_REVIEW_260130.md

Anh muốn làm gì tiếp?
1️⃣ Xem chi tiết phần nào đó
2️⃣ Bắt đầu sửa vấn đề được nêu
3️⃣ Lên plan nâng cấp với /plan
4️⃣ Lưu lại để sau với /save-brain"
```

---

## ⚠️ NEXT STEPS (Menu số):
```
1️⃣ Sửa vấn đề? /debug hoặc /refactor
2️⃣ Thêm tính năng? /plan
3️⃣ Bàn giao? /save-brain để đóng gói context
4️⃣ Tiếp tục code? /code
```

---

## 🛡️ Resilience Patterns

### Khi không có package.json
```
→ Báo user: "Đây không phải dự án Node.js. Em quét theo cấu trúc folder."
→ Liệt kê file types tìm thấy (.py, .java, .html...)
```

### Khi folder quá lớn
```
→ Chỉ quét 3 levels đầu
→ Ưu tiên: src/, app/, components/, lib/, pages/
→ Bỏ qua: node_modules/, .git/, dist/
```

### Khi không có docs
```
→ "Dự án chưa có documentation. Em tự tạo overview dựa trên code."
```
