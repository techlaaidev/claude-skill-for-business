---
name: research-san-pham-moi
description: "Research trend sản phẩm mới cho quán cafe / F&B Việt Nam bằng web search realtime (VN + quốc tế). Tổng hợp thành báo cáo Markdown + Word + PowerPoint. Trigger khi user nói: 'research trend matcha 2026', 'tìm xu hướng đồ uống mới', 'phân tích menu đối thủ Phúc Long / Highlands / Katinat', 'nghiên cứu bao bì take-away', 'so sánh cafe Nhật Hàn Đài Loan', 'làm slide cho trend ngành', 'ý tưởng menu mới'. Output: 1 file .md + 1 file .docx + (optional) 1 file .pptx — có cite đầy đủ nguồn, paraphrase toàn bộ, tôn trọng copyright."
author: Techla
version: 1.0.0
license: xem LICENSE.md
---

# Skill: Research sản phẩm mới cho quán cafe VN

## Khi nào trigger skill này?

Khi user (chủ quán cafe / F&B) muốn tìm hiểu:

- **Xu hướng đồ uống / menu mới** (matcha, cold-brew, trà đặc sản, topping mới)
- **Trend bao bì** (cốc, ống hút, túi take-away thân thiện môi trường)
- **Chiến lược của chuỗi lớn** (Highlands, Phúc Long, Katinat, Starbucks VN…)
- **So sánh với thị trường quốc tế** (Nhật, Hàn, Đài Loan, Âu Mỹ)
- **Công thức / mô hình kinh doanh** (specialty coffee, dessert cafe, cold-brew bar)
- **Bất kỳ chủ đề nào liên quan đến ngành F&B** mà cần tổng hợp từ nhiều nguồn web

**Không trigger** khi: user hỏi thông tin chung chung không liên quan F&B, hoặc yêu cầu phân tích dữ liệu nội bộ (dùng skill `cskh-phan-tich-don-hang` thay vì skill này).

## Quy trình sử dụng (5 bước)

### Bước 1 — Làm rõ chủ đề với user

Lấy đủ 2 thông tin:
- **Topic cụ thể** (ví dụ: "Trend matcha 2026", không phải chỉ "trend cafe")
- **Phạm vi**: `vn` (chỉ VN) | `intl` (chỉ quốc tế) | `both` (mặc định)

Nếu user nêu mơ hồ → hỏi lại 1 câu ngắn để thu hẹp phạm vi.

### Bước 2 — Lập search plan 5–10 query

Claude tự lập. Ví dụ với "Trend matcha 2026 VN":
1. "trend matcha vietnam 2026"
2. "Phúc Long matcha menu 2026"
3. "matcha strawberry trend site:tiktok.com"
4. "specialty matcha Uji Nishio guide"
5. "roasted matcha Japan 2026"
6. "matcha market growth asia 2026"
7. "matcha cross-sell cafe"
8. "cold brew matcha trend"

### Bước 3 — Fetch + tổng hợp

Dùng `WebSearch` để tìm nguồn, `WebFetch` để lấy nội dung chi tiết. Với mỗi nguồn:
- **Paraphrase** (không copy nguyên văn)
- Mỗi nguồn chỉ `quote` tối đa **1 lần, dưới 15 từ** (giữ trong field `quote` của source)
- Ghi rõ URL, site, ngày xuất bản (nếu có)
- **Tối thiểu 8 nguồn** khác nhau (cấu hình ở `config.yaml: min_sources`)

### Bước 4 — Tạo file `research_data.json`

Theo schema (xem `templates/research.example.json`):

```json
{
  "topic": "Trend matcha 2026",
  "scope": "both",
  "generated_at": "2026-04-17",
  "summary": "3-5 câu tóm tắt...",
  "trends": [
    { "title": "...", "description": "...", "examples": [...], "source_refs": [1, 3] }
  ],
  "vn_intl_analysis": "...",
  "case_studies": [
    { "brand": "...", "highlight": "...", "learning": "...", "source_refs": [2] }
  ],
  "opportunities": ["...", "..."],
  "sources": [
    { "title": "...", "url": "...", "site": "...", "date": "...", "quote": "..." }
  ]
}
```

`source_refs` là index **1-based** vào mảng `sources`.

### Bước 5 — Build output

```bash
# Tạo md + docx cùng lúc
python scripts/build_report.py --data research_data.json --config config.yaml \
    --md research.md --docx research.docx

# (optional) convert sang pptx
python scripts/md_to_pptx.py --md research.md --pptx research.pptx
```

Output sẽ:
- `.md`: báo cáo 6 phần, có footnote `[^1]` link đến sources.
- `.docx`: style Calibri 11pt, title xanh navy Techla, cite dạng superscript `[1]`.
- `.pptx`: tự chia slide theo H2 (mỗi xu hướng = 1 slide), dùng Marp nếu có hoặc python-pptx fallback.

## Cấu trúc báo cáo chuẩn (6 phần)

1. **Tóm tắt** — 3–5 câu đi thẳng vào insight chính.
2. **Xu hướng chính** — top 5 trend, mỗi trend có title + description + examples + source_refs.
3. **Phân tích VN vs Quốc tế** — so sánh giá, khẩu vị, kênh phân phối, cơ hội/thách thức.
4. **Case study** — 2–3 brand nổi bật, mỗi brand có `highlight` (điểm đáng chú ý) + `learning` (bài học áp dụng).
5. **Cơ hội áp dụng cho quán tầm trung VN** — 3–7 gợi ý cụ thể, đo được, có giá tham khảo.
6. **Nguồn tham khảo** — đánh số, cite đủ (URL, site, date, quote optional).

## Tùy chỉnh qua `config.yaml`

```yaml
vn_brands_priority:
  - "Highlands Coffee"
  - "Phúc Long"
  - "The Coffee House"
  - "Katinat Saigon Kafé"
  - "Starbucks Vietnam"
  - "Cộng Cà Phê"
  - "Là Việt Coffee"

international_markets:
  - "Japan specialty coffee & matcha"
  - "Korean dessert cafe"
  - "Taiwan bubble tea innovation"

min_sources: 8

auto_convert_pptx: false
pptx_engine: "auto"   # auto | marp | pptx
pptx_theme: "default" # default | gaia | uncover (Marp themes)
```

Xem `config.example.yaml`.

## Lưu ý copyright (cực quan trọng)

1. **Không copy nguyên văn** bất kỳ đoạn nào. Luôn paraphrase.
2. **Quote tối đa 1 lần / nguồn**, dưới **15 từ**. Không được tóm lại phần lớn bài viết.
3. **Cite đầy đủ** (URL + site + date) — không được bỏ nguồn dù là số liệu nhỏ.
4. **Không dùng ảnh / logo** của brand đối thủ trừ khi được phép (không có trong skill v1.0).
5. Nếu nguồn nói ý kiến trái chiều (ví dụ: 1 báo chí nói trend up, 1 nói down), **báo cáo cả hai** với cite riêng.

## Engine PPTX

- **Marp CLI** (nếu có): Cài `npm i -g @marp-team/marp-cli`. Kết quả đẹp, theme chuyên nghiệp.
- **python-pptx** (fallback): Luôn có sẵn sau `pip install -r requirements.txt`. Đủ dùng, không đẹp bằng Marp.

Skill tự chọn engine qua `--engine auto` (mặc định). Muốn force: `--engine marp` hoặc `--engine pptx`.

## Lưu ý quan trọng (cho Claude Code)

1. **Luôn search web trước khi viết báo cáo** — không được dùng "kiến thức cũ" vì trend thay đổi nhanh. Gọi `WebSearch` ít nhất 5 lần cho 1 research.
2. **Không fabricate số liệu** — nếu 1 số không tìm được trong nguồn nào, **không ghi** (đừng đoán).
3. **Nguồn VN + quốc tế cân bằng** (nếu scope=both): tối thiểu 3 VN + 3 quốc tế.
4. **Ngôn ngữ báo cáo = tiếng Việt**, kể cả khi nguồn là tiếng Anh. Tên brand quốc tế giữ nguyên.
5. **Cơ hội áp dụng phải cụ thể**: có giá tiền (VND), có thời gian triển khai gợi ý, có metric đo được — tránh chung chung kiểu "nên cải tiến menu".
6. Nếu topic quá rộng (ví dụ "trend cafe 2026") → chia làm 2–3 báo cáo nhỏ hơn thay vì 1 báo cáo khổng lồ.

## Phụ thuộc

```
python-docx >= 1.1.0
python-pptx >= 1.0.0
PyYAML >= 6.0
# optional: Marp CLI (npm i -g @marp-team/marp-cli) cho slide đẹp hơn
```

Xem `requirements.txt`.

## Tài liệu bổ sung

- `README.md` — cài đặt + ví dụ nhanh.
- `templates/research.example.json` — ví dụ đầy đủ chủ đề "Trend matcha 2026".
- `config.example.yaml` — mẫu config.
- `CHANGELOG.md` — lịch sử thay đổi.
