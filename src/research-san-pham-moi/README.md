# Skill: Research sản phẩm mới

**Author:** Techla · **Version:** 1.0.0 · **License:** xem [LICENSE.md](./LICENSE.md)

Skill cho Claude Code giúp chủ quán cafe / F&B **research xu hướng sản phẩm mới** từ web (VN + quốc tế), tổng hợp thành báo cáo `.md` + `.docx`, và (option) slide `.pptx`.

## Cài đặt

```bash
pip install -r requirements.txt
# (optional) cài Marp CLI cho slide đẹp hơn:
npm install -g @marp-team/marp-cli
```

## Sử dụng nhanh

### 1. Claude research web (tự động)

Khi user nói *"research trend matcha 2026"*, Claude sẽ:
1. Lập search plan 5–10 query
2. Gọi `WebSearch` + `WebFetch` thu thập ≥8 nguồn
3. Paraphrase + cite đầy đủ
4. Tạo file `research_data.json` theo schema

### 2. Build báo cáo

```bash
python scripts/build_report.py \
    --data research_data.json \
    --config config.yaml \
    --md research.md \
    --docx research.docx
```

Output:
- `research.md` — Markdown có footnote `[^1]` cite nguồn.
- `research.docx` — Word A4 margin 2cm, title xanh navy, cite superscript.

### 3. (Optional) Convert sang slide

```bash
python scripts/md_to_pptx.py \
    --md research.md \
    --pptx research.pptx \
    --engine auto
```

Engine:
- `auto` (default) — dùng Marp nếu có, không thì python-pptx.
- `marp` — force Marp CLI (theme đẹp hơn).
- `pptx` — force python-pptx (đơn giản, không cần Node.js).

## Cấu trúc thư mục

```
research-san-pham-moi/
├── SKILL.md                 # Manifest + trigger descriptions
├── README.md, LICENSE.md, CHANGELOG.md
├── config.example.yaml      # Brand VN ưu tiên, min_sources, pptx engine
├── requirements.txt
├── scripts/
│   ├── __init__.py
│   ├── build_report.py      # Tạo .md + .docx từ research_data.json
│   └── md_to_pptx.py        # Convert .md -> .pptx (Marp / python-pptx)
└── templates/
    └── research.example.json
```

## Schema `research_data.json`

Xem đầy đủ trong `scripts/build_report.py` docstring. Ngắn gọn:

```json
{
    "topic": "...",
    "scope": "vn | intl | both",
    "generated_at": "YYYY-MM-DD",
    "summary": "...",
    "trends": [
        { "title": "...", "description": "...", "examples": [...], "source_refs": [1, 3] }
    ],
    "vn_intl_analysis": "...",
    "case_studies": [
        { "brand": "...", "highlight": "...", "learning": "...", "source_refs": [2] }
    ],
    "opportunities": ["..."],
    "sources": [
        { "title": "...", "url": "...", "site": "...", "date": "...", "quote": "..." }
    ]
}
```

`source_refs` là index **1-based** vào mảng `sources`.

## Lưu ý copyright

- **Paraphrase toàn bộ** — không copy nguyên văn.
- Mỗi nguồn chỉ quote tối đa **1 lần, ≤15 từ**.
- **Cite đầy đủ** URL + site + date — không bỏ sót nguồn.

## Không làm gì?

- Không research phi F&B (dùng Claude chat thay vì skill này).
- Không phân tích dữ liệu nội bộ của quán — dùng skill `cskh-phan-tich-don-hang`.
- Không fabricate số liệu — không tìm được trong nguồn thì **không ghi**.

## Liên quan

Skill này thuộc **bộ "Techla Business Skills v1.0.0"** (4 skills).
Các skill anh em: `cskh-phan-tich-don-hang`, `soan-van-ban`, `techla-pancake`.
