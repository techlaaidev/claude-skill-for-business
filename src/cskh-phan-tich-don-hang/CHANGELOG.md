# CHANGELOG

## v1.0.0 — 2026-04-17

Phiên bản đầu tiên.

- Parser WECA (bảng ma trận tháng, 3 sheet, merge cells forward-fill)
- Parser transaction log chuẩn (auto-detect cột VN + Anh)
- Analyzer 11 metrics: tổng quan, monthly, MoM, VIP, churn, decreasing rhythm, star products, dead products, cross-sell, basket pairs, action list
- Report builder .docx (A4, Arial 11pt, màu xanh #1F4E79, bảng màu #2E75B6) và .md đồng nội dung
- Config YAML tùy chỉnh các ngưỡng (churn multiplier, VIP top N, dead product days, enable basket)
- Format số/tiền/phần trăm kiểu VN (1.234.567đ, 1.234,5, +12,3%)
- Sample WECA 8 KH × 12 SP × 4 tháng + sample transaction log cùng data
