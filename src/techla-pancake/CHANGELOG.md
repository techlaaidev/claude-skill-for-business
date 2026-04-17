# CHANGELOG — Techla Pancake MCP Extension

Theo chuẩn [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/).

## [1.0.0] — 2026-04-17

### Thêm mới

- **MCP server** (`server.js`) chạy trên Node.js 18+, stdio transport.
- **Manifest v0.2** (`manifest.json`) tương thích Claude Desktop ≥ 0.10.0 trên macOS + Windows.
- **4 MCP tools**:
  - `list_conversations` — liệt kê nhóm/cuộc trò chuyện với paging
  - `get_messages` — lấy tin nhắn theo `conversation_id`, filter `since` + `limit`
  - `search_messages` — tìm tin theo keyword (client-side, hỗ trợ scope 1 nhóm hoặc toàn page)
  - `summarize_conversation` — shortcut dump tin N ngày qua để Claude phân tích
- **User config** với 2 field bắt buộc (`pancake_api_key` sensitive, `pancake_page_id`) + 1 optional (`pancake_base_url`).
- **Error handling**: validate input, bắt HTTP 401/404/429, message tiếng Việt rõ ràng hướng dẫn user fix (ví dụ: "Mở Settings → Extensions → Techla Pancake → cập nhật API key").
- **Build script** (`build.sh`) đóng gói thành `.mcpb` bundle (zip) với production deps only.
- **Logging** qua stderr để Claude Desktop log viewer debug được.

### Ghi chú

- Chỉ đọc tin nhắn. Chưa hỗ trợ gửi / trả lời / xóa.
- Mỗi instance extension gắn với 1 page Pancake. Nhiều page cần cài nhiều instance.
- `search_messages` dùng client-side filter vì Pancake public API chưa expose endpoint search chuẩn — có thể chậm nếu >50 nhóm.
- Không có caching — mỗi câu hỏi trong Claude hit API mới.
- Version tiếp theo (1.1.0) dự kiến: caching conversation list (5 phút TTL), tool `reply_message` (optional, cần Pancake cho phép write permission).
