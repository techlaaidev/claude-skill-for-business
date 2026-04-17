# Hỏi đáp (FAQ)

Tổng hợp các câu hỏi chủ quán thường gặp khi dùng bộ Techla Business Skills.

---

## Chung

### Bộ skill này chạy trên nền tảng nào?

- **Claude Desktop** (macOS + Windows): dùng được **cả 4 skill** (3 skill + 1 extension).
- **Claude Web** (claude.ai/code): dùng được **3 skill** đầu tiên. Extension Pancake **không chạy** trên web.
- **Claude Mobile**: **không chạy** skill/extension nào. Chỉ là chat bình thường.
- **Linux**: Claude Desktop chưa hỗ trợ chính thức (chỉ macOS + Windows).

### Cần gói Anthropic trả phí không?

**Không.** Gói **Free** dùng được tất cả skill. Nhưng quota request/ngày thấp — nếu bạn dùng nhiều (vài chục câu hỏi/ngày) → nên nâng lên **Pro** (~$20/tháng) hoặc **Team**.

### Skill hoạt động offline không?

- Skill 1 (CSKH): **Có thể** sau khi đã setup Claude Desktop lần đầu, vì xử lý file local bằng Python.
- Skill 2 (Research): **Không** — cần WebSearch/WebFetch.
- Skill 3b (Soạn VB): **Có** — local hoàn toàn.
- Extension Pancake: **Không** — cần internet để gọi Pancake API.

### Dữ liệu của tôi có bị gửi ra ngoài không?

- **File Excel / dữ liệu nội bộ**: Claude xử lý trong sandbox local, nhưng **câu hỏi + snippet ngữ cảnh** có gửi về Anthropic để Claude phản hồi (bình thường của mọi Claude session). Xem chính sách bảo mật Anthropic tại https://www.anthropic.com/privacy.
- **Pancake API key**: **Không gửi đi đâu cả.** Lưu trong Keychain (macOS) / Credential Manager (Windows). Chỉ Claude Desktop trên máy bạn đọc.

---

## Skill 1 — CSKH Phân tích đơn hàng

### File Excel của tôi không parse được — làm sao?

Kiểm tra theo thứ tự:

1. **File có đủ 3 sheet chưa?** (với format WECA matrix): sheet danh sách sản phẩm, sheet khách hàng (matrix), sheet lịch sử chăm sóc.
2. **Header có đúng tên Tiếng Việt chuẩn?** Ví dụ: "MÃ KH", "TÊN KHÁCH HÀNG", "SỐ ĐIỆN THOẠI"... — Claude parser nhận diện cả Tiếng Việt + English alias, nhưng sai chính tả thì không nhận.
3. **Định dạng ngày trong cột tháng**: chấp nhận `datetime`, `"17/04"`, `"2;23/2"`, `"01,17/04"`, số nguyên. Nếu dùng dạng khác → báo Claude, có thể cần cập nhật parser.
4. **File không có chống mật khẩu, không bị lỗi**: mở thử bằng Excel / LibreOffice xem có bị warning không.

Nếu vẫn lỗi → gửi **screenshot 5 dòng đầu của file** + thông báo lỗi của Claude, Techla sẽ hỗ trợ.

### Tôi muốn sửa template báo cáo — làm sao?

1. Tìm file `.skill` trong bundle.
2. Giải nén (file `.skill` thực chất là `.zip` → đổi đuôi hoặc dùng unzip).
3. Sửa file `scripts/report_docx.py` hoặc `scripts/report_md.py` theo ý.
4. Zip lại thành `.skill` mới.
5. Cài lại trong Claude Desktop (Remove bản cũ → Upload bản mới).

Nếu không rành code Python, tốt hơn là **hỏi Claude chỉnh template** trong cùng câu hỏi: *"Phân tích file này, nhưng ở phần top VIP, thêm cột "Sản phẩm mua nhiều nhất"."*

### Phân tích có bao nhiêu tháng dữ liệu?

Không giới hạn. Nhưng **trên 12 tháng** thì trend phân tích (churn, decrease) bắt đầu chính xác hơn. Dưới 3 tháng thì chỉ nên xem danh sách top VIP và sản phẩm bán chạy, phần churn/decrease chưa đáng tin.

### Tại sao báo cáo nói KH X "sắp churn" mà thực tế vẫn ổn?

Rule mặc định: `days_since_last_order > avg_gap × 1.5` là churn. Có thể bạn KH chỉ đang đi du lịch, không có ý nghỉ. **Không tự động gạch tên khách** — dùng report làm gợi ý để bạn gọi điện xác nhận.

---

## Skill 2 — Research sản phẩm mới

### Báo cáo có số liệu sai / nguồn cũ — sao vậy?

Research dựa trên **web search realtime**, nhưng web có thể lỗi thời. **Luôn kiểm tra lại nguồn gốc** (URL được cite trong báo cáo) trước khi đưa vào quyết định kinh doanh.

### Tôi không thấy file `.pptx` sau khi research — tại sao?

Claude chỉ tạo `.pptx` khi bạn **nói rõ "làm slide"** hoặc "xuất pptx". Mặc định chỉ tạo `.md` + `.docx`.

Nếu đã yêu cầu slide mà vẫn không có → check config `auto_convert_pptx: true` (trong file `config.yaml`), hoặc chạy thủ công:

```bash
python scripts/md_to_pptx.py --md research.md --pptx research.pptx
```

### Marp vs python-pptx?

- **Marp** (nếu cài): slide **đẹp hơn nhiều**, theme chuyên nghiệp. Cần `npm i -g @marp-team/marp-cli`.
- **python-pptx** (mặc định): đơn giản, đủ dùng, không cần Node.js.

Muốn force Marp: `--engine marp`. Muốn force python-pptx: `--engine pptx`.

---

## Skill 3b — Soạn văn bản

### Có đảm bảo hợp đồng đúng luật không?

**Không.** Template skill này là **mẫu tham khảo**, dựa trên Bộ luật Lao động 2019 VN và thực tiễn F&B phổ biến. **Với hợp đồng chính thức hoặc trường hợp đặc biệt**, bạn **nên nhờ luật sư** rà soát.

### Tôi muốn thêm điều khoản phạt — làm sao?

Không khuyến khích, nhưng nếu cần → hỏi Claude: *"Soạn hợp đồng ... + thêm điều khoản phạt 3 tháng lương nếu nghỉ việc sớm."* Claude sẽ thêm vào Điều 5 (Trách nhiệm chung).

### Biên bản bàn giao ca có thể thêm cột mới không?

Có. Sửa schema `materials` hoặc `equipment` trong file `data.json` (xem ví dụ trong `templates/bien_ban_ca.example.json`). Hoặc hỏi Claude: *"Thêm cột 'Ngày sản xuất' vào bảng nguyên liệu trong biên bản."*

---

## Skill 3a — Pancake Extension

### Pancake báo "sai API key" — làm sao?

1. Vào [Pancake admin](https://pages.fm/admin) → Cấu hình → Webhook & API.
2. Bấm **Regenerate Token** (token cũ sẽ vô hiệu hóa).
3. Copy token mới.
4. Mở Claude Desktop → Settings → Extensions → **Techla Pancake** → bấm **Configure** → paste token mới → Save.

### Extension disabled không gọi được tool — làm sao?

Settings → Extensions → Techla Pancake → bật toggle **Enabled**. Restart Claude Desktop nếu cần.

### Nhiều page Zalo khác nhau — cài được không?

Hiện tại extension chỉ support **1 page** tại một thời điểm. Nếu cần nhiều page:
- **Cách 1**: Đổi Page ID trong Settings mỗi lần cần check page khác.
- **Cách 2** (advanced): Build nhiều instance extension với tên khác nhau. Liên hệ Techla để được hướng dẫn.

### Pancake rate limit (429) — làm sao?

Pancake public API giới hạn ~300 req/phút. Nếu bạn gọi `search_messages` trên 50 nhóm cùng lúc → có thể bị 429.

Cách xử lý:
- Chờ 1 phút rồi hỏi lại.
- Giới hạn câu hỏi: *"Chỉ check 10 nhóm mới nhất"* thay vì *"Check tất cả"*.

### Extension có gửi tin / trả lời dùm tôi được không?

**Không trong version 1.0.0.** Chỉ đọc. Lý do: Techla tôn trọng chính sách Pancake và muốn chủ quán **luôn review** trước khi trả lời khách. Version 1.1.0 có thể mở tool `reply_message` nếu có nhu cầu.

---

## Skill nói chung

### Skill không tự trigger — làm sao?

Kiểm tra theo thứ tự:

1. **Settings → Skills → toggle đã ON** cho skill đó.
2. **Settings → Features → Code Execution đã ON**.
3. **Restart Claude Desktop** (đôi khi cache cần refresh).
4. **Câu hỏi có chứa từ khóa trigger không?** Ví dụ: "phân tích đơn hàng" dễ trigger skill CSKH hơn "xem giúp file này".

Xem thêm trigger keywords trong file `SKILL.md` của từng skill (giải nén `.skill` để xem).

### Tôi muốn custom skill cho quán của riêng mình — được không?

Có. License Techla cho phép:

- **Chỉnh sửa** code (ví dụ: sửa template .docx theo logo quán).
- **Đóng gói lại** với thông tin quán của bạn.

Nhưng **phải giữ credit Techla** ở các vị trí quy định (xem `LICENSE.md`). Không được xóa tên tác giả gốc.

### Có bảo hành không?

**Không.** Skill được cung cấp "nguyên trạng". Xem `LICENSE.md` mục **Miễn trừ trách nhiệm**. Techla không chịu trách nhiệm cho quyết định kinh doanh dựa trên output của skill.

### Muốn update lên version mới — làm sao?

Tải bundle mới → cài đè skill cũ (Remove rồi Upload lại). Config đã setup có thể mất, cần setup lại.

### Có hỗ trợ kỹ thuật không?

Liên hệ qua kênh bạn mua bundle này từ Techla. Các vấn đề thường gặp đã có trong file FAQ này và file README của từng skill.

---

## Tôi vẫn kẹt, làm sao?

1. Đọc lại file README trong từng skill folder (nếu đã giải nén `.skill`).
2. Đọc file `SKILL.md` của skill đó — phần "Lưu ý quan trọng" thường giải thích edge case.
3. Mô tả **lỗi cụ thể** + **screenshot** cho Techla support.

---

**© 2026 Techla.** Xem [LICENSE.md](../LICENSE.md) để biết điều khoản sử dụng.
