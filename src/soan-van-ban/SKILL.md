---
name: soan-van-ban
description: "Soạn 3 loại văn bản hành chính cho quán cafe / F&B nhỏ bằng tiếng Việt: (1) Hợp đồng thử việc pha chế / phục vụ, (2) Biên bản bàn giao ca sáng/chiều/tối (tồn quỹ + nguyên liệu + thiết bị), (3) Thông báo nội bộ (đổi ca, ra món mới, quy định, nghỉ lễ). Trigger khi user nói: 'soạn hợp đồng thử việc', 'làm hợp đồng cho nhân viên mới', 'viết biên bản bàn giao ca', 'tạo biên bản ca sáng/chiều/tối', 'soạn thông báo nội bộ', 'viết thông báo đổi ca', 'làm văn bản cho quán', 'soạn công văn nội bộ'. Output .docx chuẩn hành chính VN (A4, Times New Roman 13pt, Quốc hiệu, chữ ký)."
author: Techla
version: 1.0.0
license: xem LICENSE.md
---

# Skill: Soạn văn bản hành chính cho quán cafe

## Khi nào trigger skill này?

Khi user (chủ quán) yêu cầu soạn một trong 3 loại văn bản sau:

| Loại văn bản | Từ khoá trigger | File builder |
|---|---|---|
| **Hợp đồng thử việc** | "soạn hợp đồng thử việc", "hợp đồng cho nhân viên mới", "tuyển barista cần hợp đồng" | `scripts/builder_hop_dong.py` |
| **Biên bản bàn giao ca** | "biên bản bàn giao ca", "biên bản ca sáng", "ca chiều giao ca", "báo cáo cuối ca" | `scripts/builder_bien_ban_ca.py` |
| **Thông báo nội bộ** | "thông báo nội bộ", "soạn thông báo đổi ca", "viết công văn cho nhân viên", "thông báo ra món mới" | `scripts/builder_thong_bao.py` |

**Không trigger** cho: văn bản pháp lý phức tạp (đơn kiện, hợp đồng chính thức dài hạn, hợp đồng thuê mặt bằng...) — những cái này cần luật sư tư vấn, skill này chỉ phục vụ giấy tờ nội bộ hàng ngày.

## Quy trình sử dụng (4 bước)

### Bước 1 — Thu thập thông tin từ user

Hỏi user để lấy đủ các trường bắt buộc (xem "Schema dữ liệu" bên dưới). **Không được tự bịa thông tin** (tên nhân viên, số CCCD, lương, v.v.). Nếu user thiếu field nào — hỏi lại, không để trống.

### Bước 2 — Tạo file `data.json`

Với input từ user, tạo file JSON theo đúng schema của từng loại văn bản (xem từng builder để biết chi tiết).

### Bước 3 — Tạo / xác nhận `config.yaml`

Thông tin quán (tên, địa chỉ, MST, người đại diện) được truyền qua file `config.yaml`. Dùng chung cho cả 3 builder. Xem `config.example.yaml` làm mẫu. Chỉ cần tạo 1 lần, dùng lại mãi.

### Bước 4 — Chạy builder sinh ra .docx

```bash
# Hợp đồng thử việc
python scripts/builder_hop_dong.py --data hd.json --config config.yaml -o hop-dong-nguyen-van-an.docx

# Biên bản bàn giao ca
python scripts/builder_bien_ban_ca.py --data bb.json --config config.yaml -o bien-ban-ca-chieu-17-04.docx

# Thông báo nội bộ
python scripts/builder_thong_bao.py  --data tb.json --config config.yaml -o thong-bao-doi-ca.docx
```

Output là file `.docx` chuẩn hành chính Việt Nam: A4, margin 2cm, font Times New Roman 13pt, có quốc hiệu, đủ chữ ký.

## Schema dữ liệu (3 loại văn bản)

Xem comment ở đầu mỗi file builder (`scripts/builder_*.py`) để biết schema đầy đủ. Tóm tắt:

### 1. Hợp đồng thử việc — `builder_hop_dong.py`
- `employee_name`, `dob`, `id_number` (CCCD), `address`, `phone`, `position` (Barista / Phục vụ / Thu ngân)
- `salary_monthly` (số, đơn vị VND), `probation_months` (1–2), `start_date` (ISO date)
- `shift_description` (mô tả ca làm việc), `allowance` (phụ cấp, thưởng KPI)

Đầu ra gồm 6 điều khoản: (1) Công việc, (2) Lương + phụ cấp (có phần "đọc tiền bằng chữ"), (3) Thời gian thử việc, (4) **Bảo mật công thức pha chế & thông tin khách hàng**, (5) Trách nhiệm chung, (6) Hiệu lực hợp đồng.

### 2. Biên bản bàn giao ca — `builder_bien_ban_ca.py`
- `shift` (sáng / chiều / tối), `shift_date`, `handover_by`, `receive_by`
- `cash_opening`, `cash_closing` (VND) — tự tính chênh lệch
- `materials[]` — bảng nguyên liệu (tên, đơn vị, tồn đầu ca, tồn cuối ca, ghi chú)
- `equipment[]` — bảng thiết bị (tên, tình trạng, ghi chú)
- `incidents`, `complaints`, `handover_notes` — text tự do

Đầu ra gồm 6 mục có đánh số: Tồn quỹ — Nguyên liệu — Thiết bị — Sự cố — Ý kiến khách hàng — Việc bàn giao. Cuối có 2 cột chữ ký (Người giao — Người nhận).

### 3. Thông báo nội bộ — `builder_thong_bao.py`
- `subject` (tiêu đề), `category` (doi-ca / mon-moi / quy-dinh / nhac-nho / nghi-le / khac)
- `recipient` (ai nhận: "toàn thể nhân viên", "ca sáng", "team pha chế"…)
- `content` (nội dung chính, có thể nhiều đoạn ngăn bằng `\n\n`)
- `bullets[]` (optional — danh sách gạch đầu dòng)
- `effective_from`, `effective_to` (optional — thời gian áp dụng)
- `signed_by`, `signed_title`, `signed_date`, `location`

Đầu ra gồm: Quốc hiệu — tiêu đề "THÔNG BÁO" — "V/v …" (tự suy ra từ `category`) — Kính gửi / Về việc — nội dung — thời gian áp dụng — lời kết — chữ ký.

## Tùy chỉnh qua `config.yaml`

Dùng chung cho cả 3 builder:

```yaml
ten_quan: "Quán Cafe Sao Đêm"
dia_chi_quan: "Số 12 phố Hàng Bài, Hoàn Kiếm, Hà Nội"
ma_so_thue: "0109876543"
dien_thoai: "024 3936 7890"
email: "contact@saodem.vn"
nguoi_dai_dien: "Trần Thị Chủ"
chuc_vu_dai_dien: "Chủ quán"
```

Xem `config.example.yaml`.

## Chuẩn format đầu ra

Tất cả 3 loại tuân thủ chuẩn hành chính Việt Nam:

- Khổ giấy **A4**, margin **2cm** tứ phía.
- Font **Times New Roman 13pt** (chuẩn công văn nhà nước).
- **Quốc hiệu** ở trên cùng (CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM / Độc lập — Tự do — Hạnh phúc) — trừ biên bản bàn giao ca thì thay bằng logo/tên quán.
- **Ngày tháng** ghi dạng "Ngày 01 tháng 05 năm 2026".
- **Số tiền** có phần đọc bằng chữ với hợp đồng ("Tám triệu đồng chẵn/tháng").
- Footer: "*Soạn bởi Techla — Skill Soạn văn bản v1.0.0*".

## Lưu ý quan trọng (cho Claude Code)

1. **Không bịa thông tin**: Tên, CCCD, số điện thoại, lương — phải hỏi user. Không được tự nghĩ ra dù chỉ là giá trị placeholder. Nếu thiếu field bắt buộc → dừng và hỏi lại.
2. **Ngày tháng định dạng ISO (`YYYY-MM-DD`)** trong JSON — builder sẽ tự convert sang "Ngày DD tháng MM năm YYYY".
3. **Số tiền dạng số nguyên VND** (không có dấu phẩy / đơn vị) — ví dụ `8000000`, không phải `"8.000.000đ"`.
4. **Hợp đồng thử việc 1–2 tháng** là phổ biến (theo Bộ luật Lao động 2019 với công việc không yêu cầu chuyên môn cao). Không gợi ý dài hơn trừ khi user yêu cầu.
5. **Không tự thêm điều khoản phạt / cam kết quá nặng** cho hợp đồng thử việc — skill này chỉ soạn hợp đồng chuẩn mực. Nếu user muốn thêm điều khoản đặc biệt → nói "phần đó cần luật sư xem giúp".
6. **Khi user yêu cầu loại văn bản nằm ngoài 3 loại trên** (đơn xin nghỉ, hợp đồng thuê mặt bằng, hợp đồng nhà cung cấp…) → nói thẳng "skill này chưa hỗ trợ, bạn có muốn mình soạn bản thô để bạn chỉnh lại không?", không tự chế ra builder mới.

## Phụ thuộc

```
python-docx >= 1.1.0
PyYAML >= 6.0
```

Xem `requirements.txt`.

## Tài liệu bổ sung

- `README.md` — hướng dẫn cài đặt, ví dụ nhanh.
- `templates/*.example.json` — dữ liệu mẫu cho cả 3 loại văn bản (copy về chỉnh lại).
- `config.example.yaml` — file config mẫu.
- `CHANGELOG.md` — lịch sử thay đổi.
