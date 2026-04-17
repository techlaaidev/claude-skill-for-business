# Skill: CSKH Phân tích đơn hàng

Tác giả: **Techla** · Phiên bản: **1.0.0**

## Skill này làm gì

Bạn gửi file Excel đơn hàng (xuất từ Google Sheet, KiotViet, Sapo, file WECA bảng tần suất đặt hàng...), Claude đọc file và tự động:

- Liệt kê **khách sắp mất** (đặt đều đặn nhưng gần đây vắng)
- Xếp hạng **top VIP** theo doanh thu
- Chỉ ra **sản phẩm ngôi sao** (bán chạy + nhiều khách mua) và **sản phẩm xác sống** (ế)
- So sánh tháng này với tháng trước (**MoM**)
- Tìm **cặp sản phẩm hay được mua chung** (để push combo)
- Tổng hợp **action list** chăm sóc khách theo priority CAO / TRUNG BÌNH / THẤP

Xuất ra 2 file cùng nội dung: **`.docx`** (mở bằng Word/Google Docs) và **`.md`** (mở trong notepad/GitHub).

## Cách dùng

1. Cài skill vào Claude Desktop (xem `docs/02-CAI-SKILL.md` ở bundle ngoài)
2. Bật **Code execution** trong Settings > Skills của Claude
3. Chat với Claude: _"Phân tích file đơn hàng này cho tôi"_ rồi kéo file .xlsx vào
4. Claude sẽ trả về báo cáo Word + Markdown

## Các loại file Excel được hỗ trợ

### WECA-style (bảng ma trận tháng)
- Header ở dòng 5
- Các cột: `MÃ KH`, `TÊN KH`, `SĐT`, `ĐỊA CHỈ`, `MÃ SP`, `TÊN SP`, `GIÁ BÁN`...
- 12 cột tháng dạng `01/26`, `02/26`...
- Các ô cột tháng ghi ngày đặt: `datetime` hoặc string `"2;23/2"`, `"01,17/04"`...
- Thường có 3 sheet: bảng chính / Lịch sử chăm sóc KH / Danh sách KH

### Transaction log chuẩn
- Header ở dòng 1
- 1 dòng = 1 đơn hàng
- Các cột: `Ngày`, `Khách hàng`, `Sản phẩm`, `Số lượng`, `Đơn giá`, `Thành tiền`...
- Parser tự match alias tiếng Việt + Anh

## Tùy chỉnh (optional)

Đặt file `config.yaml` cạnh file Excel để chỉnh ngưỡng cảnh báo:

```yaml
churn_threshold_multiplier: 1.5    # KH vắng > 1.5 × nhịp TB → churn
vip_top_n: 10                      # hiển thị top 10 VIP
dead_product_days: 90              # SP > 90 ngày không đơn = xác sống
```

Xem `config.example.yaml` để biết tất cả tùy chọn.

## Sample

- `samples/sample_weca_format.xlsx` — file mẫu WECA, 8 quán cafe giả định
- `samples/sample_standard_format.xlsx` — cùng data nhưng dạng transaction log
- `samples/sample_report_output.docx` — mẫu báo cáo skill sinh ra

## Hỏi đáp nhanh

**File tôi không parse được?** → Kiểm tra có cột `Ngày`, `Khách`, `Sản phẩm` (hoặc dạng WECA với `MÃ KH` + cột tháng `MM/YY`) không. Gửi lại cho Claude, sẽ báo cụ thể thiếu cột nào.

**Số tiền hiển thị không đúng?** → File gốc có thể đang format text. Xuất lại Excel dạng số, hoặc chuyển cột về định dạng Currency / Number.

**Tôi muốn đổi màu/font báo cáo?** → Sửa `scripts/report_docx.py` (các biến `COLOR_PRIMARY`, `BASE_FONT` ở đầu file), re-upload skill.

**Có thể chạy tự động định kỳ không?** → Không tự làm được trong skill. Bạn có thể gọi scripts qua cron/Task Scheduler.

---

*Bản quyền © 2026 Techla — xem `LICENSE.md`*
