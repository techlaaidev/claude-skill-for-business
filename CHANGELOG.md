# CHANGELOG — Techla Business Skills Bundle

Theo chuẩn [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/).

## [1.0.5] — 2026-04-17

### Sửa

- **Extension `techla-pancake`**: **convert server.js sang ESM** (`import`/`export`,
  `package.json "type": "module"`). SDK `@modelcontextprotocol/sdk@1.0.4` là
  ESM-only; trước đó dùng `require()` từ CJS nên module load fail silently trong
  Claude Desktop Electron UtilityProcess → `initialize` timeout 60s → lỗi
  *"Could not attach to MCP server"*.
- **Extension `techla-pancake`**: bỏ check `require.main === module` →
  `main()` chạy unconditional. Electron UtilityProcess không set `process.argv[1]`
  chuẩn nên check này trả false → transport không attach → client timeout.
  Test harness dùng env `PANCAKE_SKIP_MAIN=1` để gọi handlers trực tiếp.
- **Extension `techla-pancake`**: **sanitize env placeholder chưa substitute**.
  Claude Desktop quirk: khi optional `user_config.pancake_page_id` để trống,
  không truyền empty string mà truyền literal `"${user_config.pancake_page_id}"`
  vào env. Server giờ detect `${...}` → treat as empty → fallback về JWT decode.
  Trước đó URL gọi Pancake có `/pages/${user_config.pancake_page_id}/...` →
  Pancake trả 102 *"Invalid access_token"* (vì page_id sai).
- **Extension `techla-pancake`**: thêm diagnostic log ra `%TEMP%/techla-pancake-debug.log`
  (URL đã redact token, HTTP status, response body) để debug khi gặp lỗi.

## [1.0.4] — 2026-04-17

### Sửa

- **Extension `techla-pancake`**: **pin `@modelcontextprotocol/sdk` = `1.0.4`**
  (trước để `^1.0.4` → npm pull về `1.29.0` kéo theo 89 package / 14 MB deps
  gồm express, hono, ajv…). Built-in Node.js của Claude Desktop (MSIX Windows)
  hang 60s khi load lượng dep đó → lỗi *"Could not attach to MCP server"*.
  Bản này pin SDK nhẹ (13 package / 5.5 MB), attach tức thì.

## [1.0.3] — 2026-04-17

### Sửa

- **Extension `techla-pancake`**: `list_conversations` giờ dùng **Pancake Public
  API v2** — trả về cả **group Zalo** (trước đó v1 chỉ trả inbox 1-1 nên anh chị
  thấy danh sách trống khi page toàn group). Pagination đổi sang cursor
  `last_conversation_id` (60 conv/call).
- **Extension `techla-pancake`**: `get_messages` giữ **v1** (v2 không có endpoint
  này). Pagination theo `current_count` (offset) chuẩn spec Pancake. Tự lật
  trang đến khi đủ `limit` hoặc gặp `since`.
- **Extension `techla-pancake`**: tin nhắn trả về giờ **newest-first** (trước
  đó lấy nhầm tin cũ nhất trong batch).
- **Extension `techla-pancake`**: thêm **rate-limit throttle 220ms** giữa
  request (Pancake giới hạn 5 req/page/s).
- **Extension `techla-pancake`**: bắt lỗi `HTTP 200 + {"success": false}` của
  Pancake (trước đó silent-swallow thành empty list). Giờ throw rõ
  `"Sai Pancake API key"` để user biết đường cập nhật.

### Thay đổi

- Bỏ user_config `pancake_base_url` (không còn dùng — endpoint v1/v2 hard-code
  theo từng tool).

## [1.0.2] — 2026-04-17

### Thêm mới

- **Extension `techla-pancake`**: auto-detect Page ID từ JWT payload của API
  key — user chỉ cần điền 1 field thay vì 2. Field Page ID trở thành optional
  (để override nếu cần).

## [1.0.1] — 2026-04-17

### Sửa

- **Extension `techla-pancake`**: fix `list_conversations` trả về 0 do thiếu
  params bắt buộc của Pancake Public API. Giờ truyền đủ `since`, `until`,
  `page_number`, `page_size`. Default window = 30 ngày.
- Sửa `summarizeConversation` dùng `from.name` (đúng với schema Pancake Zalo).
- Sửa `handleGetMessages` truyền `page_number` bắt buộc. `since` filter
  client-side vì endpoint không hỗ trợ.
- Thêm `stripHtml()` làm sạch content tin nhắn Zalo (có HTML `<div>`, `<br>`).

## [1.0.0] — 2026-04-17

Phiên bản đầu tiên của bundle. Gồm 4 module:

### Thêm mới

- **Skill `cskh-phan-tich-don-hang`**
  - Parser WECA matrix (3 sheet, merge cells, 4 định dạng ngày)
  - Parser standard transaction log (alias header VN + English)
  - Analyzer 11 metrics: top VIP, churn warning, decreasing customers, dead products, cross-sell, MoM comparison, action list ưu tiên CAO/TRUNG/THẤP
  - Report `.docx` (Arial 11pt, title xanh navy, bảng màu Techla) + `.md` (emoji heading)
  - Synthetic samples (2 xlsx files) với 8 khách hàng, 12 sản phẩm, 4 tháng

- **Skill `research-san-pham-moi`**
  - Builder báo cáo từ JSON → `.md` (footnote `[^n]`) + `.docx` (Calibri, cite superscript)
  - Converter `.md` → `.pptx` với engine auto/marp/pptx
  - Báo cáo 6 phần: Tóm tắt / Xu hướng / VN vs Quốc tế / Case study / Cơ hội / Nguồn
  - Config brand VN ưu tiên + thị trường quốc tế

- **Skill `soan-van-ban`**
  - Builder hợp đồng thử việc (6 điều + bảo mật công thức + đọc tiền bằng chữ)
  - Builder biên bản bàn giao ca (6 mục + bảng nguyên liệu + bảng thiết bị)
  - Builder thông báo nội bộ (6 category: đổi ca / món mới / quy định / nhắc nhở / nghỉ lễ / khác)
  - Chuẩn hành chính VN: A4, Times New Roman 13pt, quốc hiệu, chữ ký

- **Extension `techla-pancake`** (.mcpb)
  - 4 MCP tools: `list_conversations`, `get_messages`, `search_messages`, `summarize_conversation`
  - Manifest v0.2 cho Claude Desktop ≥ 0.10.0 (macOS + Windows)
  - User config: `pancake_api_key` (sensitive), `pancake_page_id`, `pancake_base_url`
  - Error handling tiếng Việt (401 / 404 / 429 / network)
  - Build script `build.sh` đóng gói `.mcpb` với production deps

- **Docs tiếng Việt** (5 file trong `docs/`)
  - `01-BAT-DAU-TAI-DAY.md` — welcome + thứ tự cài
  - `02-CAI-SKILL.md` — cài 3 skill, 4 bước mỗi skill
  - `03-CAI-EXTENSION-PANCAKE.md` — cài Pancake extension, lấy API key + page ID
  - `04-SU-DUNG.md` — 40+ câu hỏi mẫu cho 4 skill
  - `05-HOI-DAP.md` — FAQ 20+ tình huống thường gặp

- **Bundle packaging**
  - 3 file `.skill` (zip của folder skill)
  - 1 file `.mcpb` (zip của folder extension với node_modules production)
  - 2 file Excel mẫu trong `samples/`
  - File `Techla-Business-Skills-v1.0.0.zip` tổng bundle

### Ghi chú

- Version 1.0.0 chưa hỗ trợ **Claude Mobile** (Anthropic chưa cho phép skill chạy mobile).
- Extension Pancake chỉ chạy **Claude Desktop** trên macOS + Windows.
- Tất cả skill có footer credit Techla — không được xóa theo license.
- Với hợp đồng lao động chính thức, **vẫn nên tham khảo luật sư** — skill chỉ hỗ trợ, không thay thế.
