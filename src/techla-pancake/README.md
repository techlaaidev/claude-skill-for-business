# Techla Pancake — MCP Extension cho Claude Desktop

**Author:** Techla · **Version:** 1.0.0 · **License:** xem [LICENSE.md](./LICENSE.md)

Desktop Extension (`.mcpb` file) để **Claude Desktop** truy cập **Pancake API** và đọc tin nhắn từ các nhóm Zalo của chủ quán (qua nick Zalo cá nhân đã liên kết với Pancake).

Khi cài xong, bạn có thể **hỏi Claude** những câu như:
- *"Check nhóm nhân viên 3 ngày qua có vấn đề gì cần xử lý không"*
- *"Khách VIP có phàn nàn gì tuần này?"*
- *"Liệt kê câu hỏi chưa trả lời trong nhóm X"*
- *"Nhóm nào hôm nay nhiều tin nhất?"*

Claude sẽ tự gọi các tools của extension này để lấy dữ liệu, phân tích, và trả lời bằng tiếng Việt.

---

## Yêu cầu hệ thống

- **Claude Desktop** ≥ v0.10.0 (macOS hoặc Windows). **Không chạy** trên web/mobile/Linux.
- **Node.js** ≥ 18 (Claude Desktop bundle sẵn, không cần tự cài).
- **Pancake account** với page Zalo cá nhân của chủ quán đã được kích hoạt.

---

## Cài đặt (dành cho khách hàng)

### Bước 1 — Lấy thông tin Pancake

1. **Pancake API Key**:
   - Vào [Pancake admin](https://pages.fm/admin).
   - Chọn **Cấu hình → Webhook & API** (hoặc **Settings → API Access**).
   - Copy **API Access Token** (dài ~50 ký tự).
2. **Page ID**:
   - Cũng trong Pancake admin, vào page Zalo cá nhân.
   - Xem URL: `https://pages.fm/admin/pages/1234567/...` → `page_id = 1234567`.

### Bước 2 — Cài extension vào Claude Desktop

1. Mở **Claude Desktop** → **Settings** (⌘/Ctrl + `,`) → tab **Extensions**.
2. Bấm **Install from file** → chọn file `techla-pancake-1.0.0.mcpb`.
3. Trong dialog cấu hình:
   - **Pancake API Key**: dán key ở Bước 1.
   - **Page ID**: nhập ID page Zalo.
   - **Base URL**: để mặc định (`https://pages.fm/api/public_api/v1`).
4. Bấm **Save & Enable**. Restart Claude Desktop nếu được yêu cầu.

### Bước 3 — Dùng thử

Trong Claude Desktop chat, gõ:

> "Liệt kê 10 nhóm Zalo của tôi trong Pancake, sắp xếp theo thời gian tin nhắn gần nhất."

Claude sẽ gọi tool `list_conversations` và trả về bảng.

---

## Build từ source (dành cho developer)

```bash
cd src/techla-pancake

# 1. Cài deps
npm install

# 2. Test local (Ctrl+C để thoát)
PANCAKE_API_KEY=xxx PANCAKE_PAGE_ID=1234567 node server.js

# 3. Build .mcpb bundle
bash build.sh
# -> Output: techla-pancake-1.0.0.mcpb
```

Trên Windows, chạy `build.sh` qua **Git Bash** hoặc **WSL**.

---

## Tools mà extension cung cấp

| Tool | Input | Output |
|---|---|---|
| `list_conversations` | `limit?, page?` | List {id, title, member_count, last_message_at, unread_count, last_message_snippet} |
| `get_messages` | `conversation_id, since?, limit?` | List {id, from, content, attachments, sent_at} |
| `search_messages` | `keyword, conversation_id?, days_back?, max_results?` | List các message match keyword |
| `summarize_conversation` | `conversation_id, days_back?, max_messages?` | Dump tin N ngày qua để Claude tự phân tích |

Tất cả tool đều trả JSON. Claude sẽ tự format lại thành câu trả lời tiếng Việt.

---

## Cấu trúc bundle

```
techla-pancake/
├── manifest.json            # MCPB manifest (v0.2)
├── server.js                # MCP server (Node.js)
├── package.json
├── build.sh                 # Script đóng gói .mcpb
├── README.md                # (file này)
├── LICENSE.md
├── CHANGELOG.md
└── node_modules/            # Sau khi `npm install`
```

---

## Giới hạn version 1.0.0

- Chỉ **đọc** tin nhắn. Chưa hỗ trợ gửi / xóa / trả lời.
- Chỉ hỗ trợ **1 page** tại một thời điểm (nhiều page → cài nhiều instance extension).
- `search_messages` dùng client-side filter (có thể chậm nếu nhiều nhóm) — Pancake API chưa expose endpoint search chuẩn.
- Chưa có caching; mỗi lần gọi đều hit API. Cẩn thận rate limit (Pancake public API ~300 req/min).

---

## Troubleshooting

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| "Thiếu PANCAKE_API_KEY" | Extension chưa cấu hình | Settings → Extensions → Techla Pancake → điền API key |
| "Sai API key (401)" | Key hết hạn hoặc gõ sai | Regenerate ở Pancake admin, update lại |
| "Không tìm thấy page (404)" | Page ID sai | Kiểm tra URL admin Pancake, copy lại |
| "Pancake rate limit (429)" | Gọi quá nhiều | Chờ 1 phút, hoặc giảm `limit` trong câu hỏi |
| Claude không gọi tool | Extension disabled | Settings → Extensions → enable toggle |

---

## Liên quan

Extension này thuộc **bộ "Techla Business Skills v1.0.0"** (4 skills).

Các skill anh em:
- `cskh-phan-tich-don-hang` — Phân tích đơn hàng + CSKH
- `soan-van-ban` — Soạn 3 loại văn bản hành chính
- `research-san-pham-moi` — Research trend sản phẩm mới từ web
