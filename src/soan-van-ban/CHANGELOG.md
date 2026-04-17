# CHANGELOG — Skill Soạn văn bản

Tất cả thay đổi đáng kể của skill này được ghi lại trong file này. Theo chuẩn [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/).

## [1.0.0] — 2026-04-17

### Thêm mới

- **Builder hợp đồng thử việc** (`scripts/builder_hop_dong.py`):
  - 6 điều khoản: Công việc — Lương & phụ cấp — Thời gian thử việc — Bảo mật công thức — Trách nhiệm chung — Hiệu lực
  - Tự sinh phần "đọc số tiền bằng chữ" (`8.000.000đ (Tám triệu đồng chẵn)`)
  - Điều khoản bảo mật công thức pha chế & thông tin khách hàng (đặc trưng F&B)
  - Hỗ trợ các vị trí: Barista / Phục vụ / Thu ngân / Pha chế

- **Builder biên bản bàn giao ca** (`scripts/builder_bien_ban_ca.py`):
  - 6 mục có đánh số: Tồn quỹ — Nguyên liệu — Thiết bị — Sự cố — Ý kiến KH — Việc bàn giao
  - Bảng nguyên liệu (tồn đầu / cuối ca) với màu header Techla xanh
  - Bảng thiết bị (tình trạng, ghi chú)
  - Tự tính chênh lệch quỹ trong ca
  - 3 loại ca: sáng / chiều / tối

- **Builder thông báo nội bộ** (`scripts/builder_thong_bao.py`):
  - 6 category: doi-ca / mon-moi / quy-dinh / nhac-nho / nghi-le / khac
  - Tự suy ra dòng "V/v …" từ category
  - Hỗ trợ nội dung nhiều đoạn + bullets + thời gian áp dụng
  - Quốc hiệu chuẩn hành chính + chữ ký người phát hành

- **Style & helper chung** (`scripts/doc_style.py`): A4 margin 2cm, Times New Roman 13pt, helper tạo paragraph căn giữa / căn trái, footer Techla, helper render quốc hiệu.

- **Format Việt Nam** (`scripts/vn_format.py`): tiền `8.000.000đ`, ngày `Ngày 01 tháng 05 năm 2026`, đọc số thành chữ (`money_to_words_vi`).

- **3 file template** trong `templates/` — copy về chỉnh theo nhu cầu.

- **Config chung** (`config.example.yaml`) — dùng 1 lần cho cả 3 builder.

### Ghi chú

- Version này chỉ hỗ trợ 3 loại văn bản phổ biến nhất của quán cafe/F&B nhỏ. Các loại khác (đơn xin nghỉ, hợp đồng thuê mặt bằng, v.v.) chưa được hỗ trợ.
- Mọi output đều có footer "*Soạn bởi Techla — Skill Soạn văn bản v1.0.0*" — đây là điều khoản license, không được xóa.
