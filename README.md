# Techla Business Skills v1.0.0

Bộ **4 công cụ AI** biến **Claude Desktop** thành trợ lý quản lý cho chủ quán cafe / cơ sở F&B nhỏ tại Việt Nam. Tất cả bằng tiếng Việt, chuẩn bối cảnh kinh doanh VN.

> **Không cần biết code.** Tải về → upload vào Claude Desktop → chat tiếng Việt.

---

## 4 module trong bộ

| # | Tên | Loại | Mô tả ngắn |
|---|---|---|---|
| 1 | **cskh-phan-tich-don-hang** | Claude Skill | Parse file Excel đơn hàng (WECA matrix hoặc log giao dịch), phân tích 11 metrics: top VIP, churn, sản phẩm chết, cross-sell, action list. Xuất `.docx` + `.md`. |
| 2 | **research-san-pham-moi** | Claude Skill | Research web realtime (VN + quốc tế) về trend đồ uống / bao bì / công thức. Xuất `.md` + `.docx` + (option) `.pptx`. Có cite nguồn. |
| 3 | **soan-van-ban** | Claude Skill | Soạn 3 loại văn bản hành chính: hợp đồng thử việc, biên bản bàn giao ca, thông báo nội bộ. Chuẩn hành chính VN. |
| 4 | **techla-pancake** | Desktop Extension (.mcpb) | Claude đọc tin nhắn từ nhóm Zalo qua Pancake API. 4 MCP tools: list / get / search / summarize. |

---

## Tải bundle

Vào mục **[Releases](https://github.com/techlaaidev/claude-skill-for-business/releases)** → tải file `Techla-Business-Skills-v1.0.0.zip` (~4 MB).

Giải nén sẽ có:

```
Techla-Business-Skills-v1.0.0/
├── README.md
├── LICENSE.md
├── CHANGELOG.md
├── docs/                                       ← 5 file hướng dẫn tiếng Việt
│   ├── 01-BAT-DAU-TAI-DAY.md
│   ├── 02-CAI-SKILL.md
│   ├── 03-CAI-EXTENSION-PANCAKE.md
│   ├── 04-SU-DUNG.md
│   └── 05-HOI-DAP.md
├── skills/
│   ├── cskh-phan-tich-don-hang.skill
│   ├── research-san-pham-moi.skill
│   └── soan-van-ban.skill
├── extensions/
│   └── techla-pancake-1.0.0.mcpb
└── samples/
    └── cskh-phan-tich-don-hang/
        ├── mau-don-hang-weca-matrix.xlsx
        └── mau-don-hang-standard.xlsx
```

---

## Yêu cầu hệ thống

- **Claude Desktop** ≥ v0.10.0 trên **macOS 11+** hoặc **Windows 10+**.
- Bật **Code Execution** trong Settings → Capabilities (bắt buộc cho 3 skill Python).
- **Gói Free trở lên** đều dùng được. Gói Pro đỡ bị limit quota hơn.
- (Chỉ cho extension Pancake): tài khoản **Pancake** + nick Zalo cá nhân đã link.

Skill 1–3 cũng chạy được trên **Claude Web** (claude.ai/code). Extension Pancake **chỉ chạy** trên Claude Desktop.

---

## Bắt đầu trong 15 phút

1. Tải bundle từ **[Releases](https://github.com/techlaaidev/claude-skill-for-business/releases)** → giải nén.
2. Đọc [`docs/01-BAT-DAU-TAI-DAY.md`](./docs/01-BAT-DAU-TAI-DAY.md) — welcome + tổng quan.
3. Cài Claude Desktop + bật Code Execution.
4. Cài 3 skill theo [`docs/02-CAI-SKILL.md`](./docs/02-CAI-SKILL.md).
5. (Optional) Cài Pancake extension theo [`docs/03-CAI-EXTENSION-PANCAKE.md`](./docs/03-CAI-EXTENSION-PANCAKE.md).
6. Xem ví dụ câu hỏi trong [`docs/04-SU-DUNG.md`](./docs/04-SU-DUNG.md).
7. Gặp vấn đề? [`docs/05-HOI-DAP.md`](./docs/05-HOI-DAP.md).

---

## Câu lệnh mẫu

- **CSKH**: kéo file Excel vào chat → *"Phân tích file đơn hàng này, xuất báo cáo docx cho tôi."*
- **Research**: *"Research xu hướng đồ uống matcha VN 2026, làm báo cáo docx và pptx."*
- **Soạn văn bản**: *"Soạn hợp đồng thử việc cho Nguyễn Văn A, pha chế, 6 triệu, 2 tháng."*
- **Pancake**: *"Tóm tắt 10 tin nhắn Zalo gần nhất từ nhóm khách VIP."*

---

## Build từ source (dành cho developer)

```bash
# clone
git clone https://github.com/techlaaidev/claude-skill-for-business.git
cd claude-skill-for-business

# yêu cầu: Python 3.10+, Node 18+, npm
python tools/build_bundle.py

# output: build/Techla-Business-Skills-v1.0.0.zip
```

Script build cross-platform (Windows/Mac/Linux), dùng Python `zipfile` stdlib — không cần `zip` CLI.

---

## Cấu trúc repository

```
claude-skill-for-business/
├── src/                          ← source của 4 module
│   ├── cskh-phan-tich-don-hang/
│   ├── research-san-pham-moi/
│   ├── soan-van-ban/
│   └── techla-pancake/
├── docs/                         ← 5 file hướng dẫn tiếng Việt
├── tools/
│   ├── build_bundle.py           ← build script cross-platform
│   └── build-bundle.sh           ← build script bash (Linux/Mac)
├── TECHLA-FNB-SKILLS-SPEC.md     ← spec gốc
├── README.md
├── LICENSE.md
└── CHANGELOG.md
```

---

## License ngắn gọn

- **Được dùng** thoải mái trong công việc của bạn, không giới hạn máy / người.
- **Được phân phối lại** cho nhân viên / đối tác / khách hàng (miễn phí hoặc thu phí).
- **Được chỉnh sửa** code, template, config.
- **Phải giữ credit Techla** ở các vị trí quy định trong `LICENSE.md`.
- **Không được ghi tên khác** làm tác giả gốc.
- **Không bảo hành**. Bạn tự chịu trách nhiệm kết quả kinh doanh.

Chi tiết xem [`LICENSE.md`](./LICENSE.md).

---

## Hỗ trợ

- **Tài liệu**: folder `docs/` (5 file tiếng Việt).
- **FAQ**: `docs/05-HOI-DAP.md` giải đáp 20+ tình huống thường gặp.
- **Bug / góp ý**: mở [Issue](https://github.com/techlaaidev/claude-skill-for-business/issues) trên GitHub.
- **Kỹ thuật**: liên hệ qua kênh bạn mua bundle từ Techla.

---

**© 2026 Techla — Đồng hành cùng chủ quán cafe Việt.**
