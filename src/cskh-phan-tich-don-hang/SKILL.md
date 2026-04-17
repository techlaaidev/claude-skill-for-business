---
name: cskh-phan-tich-don-hang
description: "Phân tích file Excel đơn hàng của quán cafe / cửa hàng F&B và xuất báo cáo Word + Markdown có cảnh báo churn, top VIP, sản phẩm ngôi sao/xác sống, so sánh MoM, cặp SP hay mua cùng, và action list. PHẢI TRIGGER bất cứ khi nào người dùng: gửi file .xlsx đơn hàng; nói 'phân tích đơn hàng', 'báo cáo CSKH', 'khách nào sắp mất', 'top VIP', 'sản phẩm bán chạy', 'sản phẩm ế', 'cặp sản phẩm hay mua cùng', 'so sánh doanh thu tháng', 'action list chăm sóc khách'; hỏi về phân tích file WECA/KiotViet/Sapo/Google Sheet đơn hàng. Output: báo cáo .docx A4 màu xanh + .md cùng nội dung."
author: Techla
version: 1.0.0
license: Xem LICENSE.md — cho phép phân phối lại, yêu cầu giữ credit Techla
---

# Skill: CSKH Phân tích đơn hàng

Skill này đọc file Excel đơn hàng → phân tích → xuất báo cáo Word (.docx) và Markdown (.md) có đầy đủ cảnh báo churn, VIP, sản phẩm, action list chăm sóc khách.

## Khi nào trigger

Trigger ngay khi người dùng:

- Gửi/upload file `.xlsx` có dữ liệu đơn hàng
- Nói các cụm: "phân tích đơn hàng", "báo cáo CSKH", "khách sắp mất", "top VIP", "SP bán chạy", "SP ế", "cặp SP hay mua cùng", "so sánh tháng"
- Hỏi: "file này cho tôi thấy gì", "tóm tắt doanh số", "nên chăm sóc khách nào trước"
- Paste bảng đơn hàng dạng text/CSV

Không trigger khi:

- File là báo cáo tài chính thuần (không có cột khách + sản phẩm + ngày)
- User hỏi về trend sản phẩm ngoài thị trường (→ skill research)

## Quy trình thực hiện

1. **Nhận file**: Yêu cầu user gửi file `.xlsx`. Nếu file đã có trong conversation, dùng luôn.

2. **Auto-detect format**: Đọc file và chạy classifier:
   - **WECA format** (bảng ma trận tháng): header ở dòng 5, có các cột `MÃ KH`, `MÃ SP`, các cột tháng `MM/YY`, thường có 3 sheet (chính + lịch sử chăm sóc + danh sách KH).
   - **Standard format** (transaction log): header ở dòng 1, 1 dòng = 1 đơn, các cột `Ngày`, `Khách`, `Sản phẩm`, `Số lượng`, `Đơn giá`...

   Nếu không rõ → hỏi user.

3. **Parse** với script tương ứng:
   ```bash
   python scripts/parser_weca.py <file.xlsx> --output parsed.json
   # hoặc
   python scripts/parser_standard.py <file.xlsx> --output parsed.json
   ```

4. **Analyze**:
   ```bash
   python scripts/analyzer.py parsed.json --output analysis.json [--config config.yaml]
   ```

5. **Build report**:
   ```bash
   python scripts/report_builder.py analysis.json --docx bao-cao.docx --md bao-cao.md
   ```

6. **Trả kết quả cho user**:
   - Đính kèm file `.docx` + `.md`
   - Kèm tóm tắt 3-5 điểm nổi bật (churn cần xử lý, top VIP, SP ế...)
   - Nếu có warnings từ parser (vd: format ngày lạ), nêu ra

## Tùy chỉnh qua config

Đặt file `config.yaml` cạnh file Excel, hoặc user chỉ định qua `--config`:

```yaml
churn_threshold_multiplier: 1.5    # nhân với nhịp đặt TB của KH
vip_top_n: 10                      # số KH VIP hiển thị
dead_product_days: 90              # SP không đơn > 90 ngày = xác sống
enable_basket_analysis: true
reference_date: null               # null = ngày đơn mới nhất
min_orders_for_rhythm: 2
decreasing_rhythm_threshold: 0.4   # 40% giảm = cảnh báo
decreasing_rhythm_min_orders: 4
```

## 11 metrics skill tính

1. **Tóm tắt điều hành** — tổng KH/SP/đơn/doanh thu/SL, khoảng thời gian
2. **Khách sắp mất** — KH có nhịp đặt rõ ràng nhưng đơn cuối đã lâu (> nhịp × ngưỡng)
3. **Top VIP** — xếp theo total_revenue
4. **Cơ hội bán thêm** — KH có ghi chú opportunity/action trong sheet 3
5. **Sản phẩm ngôi sao** — rank theo `revenue × log(1 + num_customers)`
6. **Sản phẩm xác sống** — SP không có đơn hoặc đơn cuối quá lâu
7. **So sánh MoM** — % thay đổi tháng hiện tại so tháng trước
8. **Chi tiết theo tháng** — bảng đơn/SL/doanh thu/KH duy nhất từng tháng
9. **Khách giảm nhịp** — KH có ≥ 4 đơn, tháng cuối giảm > 40% so TB trước
10. **Cặp SP hay mua cùng** — basket analysis, top 10 cặp
11. **Action list** — tổng hợp churn + decreasing + cross-sell, phân priority

## Lưu ý quan trọng

- **WECA format có merge cells**: dòng 2, 3, 4... của cùng 1 KH để trống tên/SĐT/địa chỉ. Parser phải forward-fill.
- **Cột tháng WECA đa dạng format**: `datetime` object, `"2;23/2"`, `"01,17/04"`, số đơn `17`. Parser đã handle cả 4.
- **Sheet care history cũng có `MÃ KH`** — phải check hints care TRƯỚC khi classify main.
- **Standard format không có "dead product"**: chỉ WECA có product master đầy đủ.
- **reference_date**: nếu config null, dùng ngày đơn mới nhất. Với file cũ (toàn data 2024), đừng tính churn theo ngày hôm nay.
- **Báo cáo dùng Arial 11pt, A4, margin 2cm**. Footer "Báo cáo tạo bởi Techla" bắt buộc giữ.

## Tài liệu bổ sung

- `scripts/parser_weca.py` — parser bảng ma trận WECA
- `scripts/parser_standard.py` — parser transaction log
- `scripts/analyzer.py` — tính 11 metrics
- `scripts/report_builder.py` — build .docx + .md
- `scripts/vn_format.py` — format số/tiền kiểu VN
- `config.example.yaml` — mẫu config
- `samples/sample_weca_format.xlsx` — sample WECA 8 KH × 12 SP × 4 tháng
- `samples/sample_standard_format.xlsx` — sample transaction log cùng data
- `samples/sample_report_output.docx` — mẫu báo cáo output
- `README.md` — hướng dẫn khách cuối
