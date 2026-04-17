# Bắt đầu tại đây

Chào mừng bạn đến với **Techla Business Skills v1.0.0** — bộ 4 công cụ AI dành riêng cho chủ quán cafe / F&B nhỏ tại Việt Nam. Bộ này biến Claude Desktop thành **"trợ lý quản lý"** giúp bạn:

1. **Phân tích đơn hàng** (`cskh-phan-tich-don-hang`) — đọc file Excel đơn hàng, đưa ra top khách VIP, khách sắp churn, sản phẩm chết, cơ hội cross-sell.
2. **Research sản phẩm mới** (`research-san-pham-moi`) — Claude search web, tổng hợp trend matcha / cafe / bao bì thành báo cáo `.docx` + slide `.pptx`.
3. **Soạn văn bản** (`soan-van-ban`) — hợp đồng thử việc, biên bản bàn giao ca, thông báo nội bộ — chuẩn hành chính VN, có chữ ký sẵn.
4. **Pancake Zalo Monitor** (`techla-pancake`) — Claude đọc tin nhắn từ các nhóm Zalo (qua Pancake) để bạn hỏi *"nhóm nhân viên 3 ngày qua có gì"*.

Ba module đầu tiên là **Claude Skills** (chạy trên Claude Desktop + Web). Module thứ 4 là **Desktop Extension** (chỉ chạy trên Claude Desktop).

---

## Thứ tự nên làm (15 phút setup)

### Bước 1 — Cài Claude Desktop

- Tải tại: https://claude.ai/download
- Hỗ trợ: **macOS 11+** hoặc **Windows 10+**.
- Đăng nhập bằng tài khoản Anthropic. **Gói Free trở lên đều dùng được.**

### Bước 2 — Bật Code Execution

Skills số 1, 2, 3 cần Claude chạy Python để xử lý file. Bật như sau:

1. Mở Claude Desktop → **Settings** (`⌘ + ,` trên macOS hoặc `Ctrl + ,` trên Windows).
2. Tab **Features** → bật toggle **Code execution**.
3. Bấm **Save**. Restart Claude Desktop.

### Bước 3 — Cài 3 Claude Skills

Mở thư mục `skills/` trong bundle, bạn sẽ thấy 3 file `.skill`:

- `cskh-phan-tich-don-hang.skill`
- `research-san-pham-moi.skill`
- `soan-van-ban.skill`

Xem hướng dẫn cài từng file trong [`02-CAI-SKILL.md`](./02-CAI-SKILL.md).

### Bước 4 — (Optional) Cài Pancake Extension

Nếu bạn dùng **Pancake** để quản lý chat Zalo → cài thêm extension. Nếu không dùng Pancake → **bỏ qua bước này**, 3 skill trên đã đủ dùng.

Xem hướng dẫn chi tiết trong [`03-CAI-EXTENSION-PANCAKE.md`](./03-CAI-EXTENSION-PANCAKE.md).

### Bước 5 — Bắt đầu hỏi Claude

Xem danh sách câu hỏi mẫu cho từng skill trong [`04-SU-DUNG.md`](./04-SU-DUNG.md).

---

## Bundle có gì?

```
Techla-Business-Skills-v1.0.0/
├── README.md                                    ← tổng quan
├── LICENSE.md                                   ← điều khoản sử dụng
├── CHANGELOG.md
├── docs/
│   ├── 01-BAT-DAU-TAI-DAY.md                    ← (file bạn đang đọc)
│   ├── 02-CAI-SKILL.md
│   ├── 03-CAI-EXTENSION-PANCAKE.md
│   ├── 04-SU-DUNG.md
│   └── 05-HOI-DAP.md
├── skills/
│   ├── cskh-phan-tich-don-hang.skill            ← Skill 1 (phân tích đơn hàng)
│   ├── research-san-pham-moi.skill              ← Skill 2 (research trend)
│   └── soan-van-ban.skill                       ← Skill 3b (soạn VB)
├── extensions/
│   └── techla-pancake-1.0.0.mcpb                ← Skill 3a (Pancake Zalo)
└── samples/
    └── cskh-phan-tich-don-hang/
        ├── mau-don-hang-weca-matrix.xlsx         ← file Excel mẫu format WECA
        └── mau-don-hang-standard.xlsx            ← file Excel mẫu format thường
```

---

## Có vấn đề?

- Xem FAQ trong [`05-HOI-DAP.md`](./05-HOI-DAP.md).
- Các skill có file `README.md` riêng trong folder gốc của `.skill` (unzip để xem).
- Nếu kẹt, liên hệ qua kênh bạn mua bundle này từ Techla.

---

**© 2026 Techla.** Bản quyền thuộc Techla. Xem [LICENSE.md](../LICENSE.md) để biết điều khoản sử dụng.
