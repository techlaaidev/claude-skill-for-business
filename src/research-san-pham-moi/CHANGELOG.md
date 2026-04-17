# CHANGELOG — Skill Research sản phẩm mới

Theo chuẩn [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/).

## [1.0.0] — 2026-04-17

### Thêm mới

- **Builder báo cáo** (`scripts/build_report.py`):
  - Nhận JSON schema chuẩn (topic / scope / summary / trends / case_studies / opportunities / sources)
  - Output song song `.md` (có footnote `[^n]`) và `.docx` (Calibri 11pt, title xanh navy, cite superscript `[n]`)
  - Báo cáo 6 phần: Tóm tắt / Xu hướng / Phân tích VN vs Quốc tế / Case study / Cơ hội / Nguồn
  - Tự tính số trend trong tiêu đề section 2

- **Converter md → pptx** (`scripts/md_to_pptx.py`):
  - Engine `auto`: dùng Marp CLI nếu có trong PATH, không thì fallback python-pptx
  - Engine `marp`: force Marp (cần `npm i -g @marp-team/marp-cli`)
  - Engine `pptx`: force python-pptx (luôn sẵn có)
  - Tự chia slide theo heading (H1/H2 = slide mới, H3 = section trong slide)
  - Hỗ trợ bullet, blockquote, text
  - Format 16:9, title xanh navy Techla, footer bản quyền

- **Config chung** (`config.example.yaml`):
  - `vn_brands_priority` — 8 chuỗi VN ưu tiên khi research
  - `international_markets` — 5 thị trường quốc tế ưu tiên
  - `min_sources` — số nguồn tối thiểu (default 8)
  - `auto_convert_pptx`, `pptx_engine`, `pptx_theme`

- **Template mẫu** (`templates/research.example.json`) — chủ đề "Trend matcha cho quán cafe VN 2026" với 5 trend, 2 case study, 5 cơ hội, 8 nguồn.

### Ghi chú

- Skill chỉ **format báo cáo**. Phần tìm nguồn web do Claude tự làm qua `WebSearch`/`WebFetch` trước khi gọi builder.
- Mọi output đều có footer "*Báo cáo tạo bởi Techla — Skill Research sản phẩm mới v1.0.0*" — không được xóa.
- Version này chưa support tự dịch nguồn tiếng Anh sang tiếng Việt — Claude tự paraphrase/dịch trong bước tổng hợp.
