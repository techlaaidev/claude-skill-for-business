# Skill: Soạn văn bản hành chính cho quán cafe

**Author:** Techla · **Version:** 1.0.0 · **License:** xem [LICENSE.md](./LICENSE.md)

Skill cho Claude Code dùng để soạn 3 loại văn bản hành chính tiếng Việt phổ biến nhất của một quán cafe / cơ sở F&B nhỏ:

1. **Hợp đồng thử việc** — cho barista, phục vụ, thu ngân.
2. **Biên bản bàn giao ca** — ca sáng / chiều / tối, có bảng nguyên liệu + thiết bị.
3. **Thông báo nội bộ** — đổi ca, ra món mới, quy định, nghỉ lễ.

Đầu ra là file `.docx` chuẩn hành chính Việt Nam: A4, Times New Roman 13pt, có quốc hiệu, đủ chữ ký.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng nhanh

### 1. Chuẩn bị `config.yaml` (1 lần)

Copy `config.example.yaml` thành `config.yaml`, điền thông tin quán:

```yaml
ten_quan: "Quán Cafe Sao Đêm"
dia_chi_quan: "Số 12 phố Hàng Bài, Hoàn Kiếm, Hà Nội"
ma_so_thue: "0109876543"
nguoi_dai_dien: "Trần Thị Chủ"
chuc_vu_dai_dien: "Chủ quán"
```

### 2. Chuẩn bị `data.json`

Copy 1 trong 3 file mẫu trong `templates/` về rồi chỉnh:

- `templates/hop_dong.example.json` — hợp đồng thử việc
- `templates/bien_ban_ca.example.json` — biên bản bàn giao ca
- `templates/thong_bao.example.json` — thông báo nội bộ

### 3. Chạy builder

```bash
# Hợp đồng
python scripts/builder_hop_dong.py --data hop_dong.json --config config.yaml -o hop-dong.docx

# Biên bản bàn giao ca
python scripts/builder_bien_ban_ca.py --data bien_ban.json --config config.yaml -o bien-ban.docx

# Thông báo nội bộ
python scripts/builder_thong_bao.py --data thong_bao.json --config config.yaml -o thong-bao.docx
```

## Cấu trúc thư mục

```
soan-van-ban/
├── SKILL.md                         # Manifest skill (Claude Code sẽ đọc file này)
├── README.md
├── LICENSE.md
├── CHANGELOG.md
├── config.example.yaml              # Mẫu config quán
├── requirements.txt
├── scripts/
│   ├── __init__.py
│   ├── doc_style.py                 # Style + helper chung (A4, font, quốc hiệu, footer)
│   ├── vn_format.py                 # Format số/tiền VN, đọc số thành chữ
│   ├── builder_hop_dong.py          # Builder hợp đồng thử việc
│   ├── builder_bien_ban_ca.py       # Builder biên bản bàn giao ca
│   └── builder_thong_bao.py         # Builder thông báo nội bộ
└── templates/
    ├── hop_dong.example.json
    ├── bien_ban_ca.example.json
    └── thong_bao.example.json
```

## Chuẩn format đầu ra

- Khổ **A4**, margin **2cm** tứ phía
- Font **Times New Roman 13pt** (chuẩn hành chính VN)
- Tiêu đề căn giữa, đậm
- Ngày tháng dạng "Ngày 01 tháng 05 năm 2026"
- Số tiền có phần đọc bằng chữ (cho hợp đồng): `8.000.000đ (Tám triệu đồng chẵn)`
- Footer: *Soạn bởi Techla — Skill Soạn văn bản v1.0.0*

## Không làm gì?

- Không soạn văn bản pháp lý phức tạp (đơn kiện, hợp đồng thuê mặt bằng dài hạn…) — những cái này nên qua luật sư.
- Không tự bịa thông tin. Thiếu field bắt buộc → dừng và hỏi user.
- Không thay thế cho kế toán / luật sư. Chỉ giúp soạn giấy tờ nội bộ hàng ngày.

## Liên quan

- Skill này thuộc **bộ "Techla Business Skills v1.0.0"** (4 skills).
- Các skill anh em: `cskh-phan-tich-don-hang`, `research-san-pham-moi`, `pancake-mcp-extension`.
