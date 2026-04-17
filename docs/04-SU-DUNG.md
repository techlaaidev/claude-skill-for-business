# Cách sử dụng — ví dụ câu hỏi cho từng skill

Sau khi cài skill, bạn chỉ cần **nói chuyện bình thường** với Claude — skill tự kích hoạt khi bạn nhắc đúng từ khóa. Không cần gõ lệnh đặc biệt.

Dưới đây là 40+ câu hỏi mẫu chia theo 4 skill.

---

## Skill 1 — Phân tích đơn hàng (`cskh-phan-tich-don-hang`)

**Input bạn cần chuẩn bị**: 1 file Excel đơn hàng (format WECA matrix hoặc transaction log thường).

### Câu hỏi mẫu

- *"Phân tích giúp tôi file đơn hàng tháng 4 này."* → kèm file Excel
- *"Check cho tôi khách nào sắp rời đi (churn) trong bảng này."*
- *"Liệt kê top 5 khách VIP, sắp xếp theo doanh thu."*
- *"Sản phẩm nào bán chậm / sắp chết trong 3 tháng qua?"*
- *"Có cơ hội bán chéo nào giữa các khách không?"*
- *"So sánh doanh thu tháng này vs tháng trước."*
- *"Vẽ cho tôi 5 action cụ thể cần làm cho tháng tới."*

### Kết quả

Claude sẽ trả file **.docx + .md** với:
- Top VIP (có tên, SĐT, tổng chi tiêu)
- Cảnh báo churn (khách đã lâu không quay lại)
- Khách giảm mua (giảm hơn 40% so với trung bình)
- Sản phẩm chết
- Cơ hội cross-sell
- Action list ưu tiên (CAO / TRUNG BÌNH / THẤP)

---

## Skill 2 — Research sản phẩm mới (`research-san-pham-moi`)

**Input**: chỉ cần 1 câu hỏi. Claude tự search web.

### Câu hỏi mẫu

- *"Research trend matcha cho quán cafe VN 2026."*
- *"So sánh bao bì take-away của Highlands và Phúc Long, có gì học được?"*
- *"Trend topping trà sữa Đài Loan 2026 có gì mới?"*
- *"Mô hình cafe dessert Hàn Quốc phù hợp quán nhỏ VN không?"*
- *"Tìm cho tôi 5 công thức cold-brew mới từ Nhật / Úc."*
- *"Ý tưởng menu Tết 2027 — xu hướng đồ uống lễ."*
- *"Phân tích chiến lược giá của Katinat, có gì đáng học?"*
- *"Làm slide 10 trang về trend matcha 2026."* → sẽ xuất file `.pptx`

### Kết quả

Claude sẽ:
1. Search web (5-10 query)
2. Tổng hợp thành báo cáo 6 phần (Tóm tắt / Trend / VN vs Quốc tế / Case study / Cơ hội áp dụng / Nguồn)
3. Xuất `.md` + `.docx` (và `.pptx` nếu bạn yêu cầu slide)
4. Cite đầy đủ nguồn, paraphrase toàn bộ (không copy)

---

## Skill 3b — Soạn văn bản (`soan-van-ban`)

**Input**: bạn kể thông tin cụ thể, Claude tự format thành văn bản hành chính.

### Hợp đồng thử việc

- *"Soạn hợp đồng thử việc cho bạn Nguyễn Văn An, barista, 8tr/tháng, thử việc 2 tháng, bắt đầu 01/05."*
- *"Làm hợp đồng cho chị Trần Bình làm phục vụ, 7.5tr + phụ cấp ăn trưa 30k/ngày."*
- *"Tuyển thu ngân mới — tên Lê Hoa, thử việc 1 tháng, 7tr/tháng."*

### Biên bản bàn giao ca

- *"Tạo biên bản bàn giao ca chiều 17/04: quỹ đầu 2tr, cuối 3.8tr, mất điện 30 phút, không sự cố khác."*
- *"Làm biên bản ca sáng hôm nay, bàn giao cho ca chiều — ghi cả tình trạng máy pha La Marzocco."*
- *"Soạn biên bản ca tối, có 1 khách phàn nàn matcha đắng."*

### Thông báo nội bộ

- *"Soạn thông báo đổi lịch ca tuần 20-26/04 do khai trương chi nhánh mới."*
- *"Viết thông báo ra món mới 'Matcha Strawberry Latte' giá 59k, áp dụng từ 01/05."*
- *"Làm thông báo nghỉ lễ 30/04 – 01/05/2026 cho toàn bộ nhân viên."*
- *"Thông báo quy định mới về giữ vệ sinh quầy bar, gửi cho tất cả barista."*

### Kết quả

File `.docx` chuẩn hành chính:
- A4 margin 2cm, Times New Roman 13pt
- Quốc hiệu CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
- Ngày định dạng "Ngày 01 tháng 05 năm 2026"
- Số tiền đọc bằng chữ (hợp đồng)
- Đủ phần chữ ký

---

## Skill 3a — Pancake Zalo Monitor (`techla-pancake`)

**Input**: không cần upload file. Chỉ cần hỏi Claude.

> Extension này chỉ hoạt động sau khi bạn đã cài xong (xem `03-CAI-EXTENSION-PANCAKE.md`).

### Câu hỏi mẫu

- *"Liệt kê 10 nhóm Zalo có tin mới nhất trong Pancake."*
- *"Check nhóm 'Nhân viên ca sáng' 3 ngày qua có gì cần xử lý không?"*
- *"Nhóm nào có nhiều tin chưa đọc nhất hôm nay?"*
- *"Khách trong nhóm VIP tuần này có phàn nàn gì không? Tìm từ khóa 'phàn nàn', 'hủy đơn', 'đắng', 'nguội'."*
- *"Tóm tắt giúp tôi nhóm 'Team pha chế' tuần qua — ai báo cáo gì, có câu hỏi nào chưa trả lời?"*
- *"Trong 2 ngày qua, nhóm nào tôi chưa trả lời tin nào?"*

### Kết quả

Claude tự:
1. Gọi `list_conversations` lấy danh sách nhóm
2. Gọi `get_messages` / `search_messages` / `summarize_conversation` để lấy chi tiết
3. Phân tích + trả lời tiếng Việt kèm gợi ý hành động

---

## Kết hợp nhiều skill (power user)

Claude tự phối hợp các skill trong cùng 1 câu hỏi:

- *"Phân tích đơn hàng tháng 4 (đính kèm), rồi soạn thông báo nội bộ cảm ơn top 5 khách VIP."* → dùng Skill 1 + 3b
- *"Research trend matcha 2026, rồi đề xuất tôi nên soạn thông báo menu mới thế nào."* → Skill 2 + 3b
- *"Check nhóm VIP tuần qua có phàn nàn gì, rồi soạn thông báo xin lỗi + khuyến mãi bù."* → Skill 3a + 3b

---

## Mẹo đặt câu hỏi hiệu quả

1. **Gọi rõ hành động**: "soạn", "phân tích", "research", "liệt kê" — Claude nhận diện skill nhanh hơn.
2. **Cho context cụ thể**: số tiền, tên người, thời gian. Ví dụ "8tr/tháng" hơn "lương tầm trung".
3. **Đặt câu hỏi follow-up**: sau khi Claude trả báo cáo, hỏi thêm "Giải thích chi tiết action #2" hay "Cho tôi số liệu gốc cho phần churn".
4. **Yêu cầu format**: "xuất ra .docx" / "làm slide 10 trang" / "làm Excel" — Claude điều chỉnh output.
5. **Không đoán giúp Claude**: nếu Claude hỏi thiếu info (ví dụ "Bạn cần hợp đồng thử việc mấy tháng?") — trả lời rõ ràng, không bỏ qua.

---

**© 2026 Techla.** Xem [LICENSE.md](../LICENSE.md) để biết điều khoản sử dụng.
