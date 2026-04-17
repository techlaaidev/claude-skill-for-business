# LICENSE — Techla Business Skills v1.0.0

**Bản quyền © 2026 Techla. Bảo lưu mọi quyền.**

---

## Phạm vi

License này áp dụng cho **toàn bộ bundle** "Techla Business Skills v1.0.0", bao gồm:

- 3 Claude Skills (`cskh-phan-tich-don-hang`, `research-san-pham-moi`, `soan-van-ban`)
- 1 Desktop Extension (`techla-pancake`)
- 5 file docs trong `docs/`
- Tài liệu bundle (`README.md`, `LICENSE.md`, `CHANGELOG.md`)
- File dữ liệu mẫu (`samples/`)

Mỗi skill / extension bên trong bundle có `LICENSE.md` riêng — nội dung tương thích với file này, có chi tiết hơn về từng module.

---

## Bạn được phép

- **Sử dụng** bundle trong công việc kinh doanh của bạn, không giới hạn số máy, số người dùng, số quán.
- **Phân phối lại** bundle (nguyên bản hoặc đã chỉnh sửa) cho nhân viên, đối tác, khách hàng, hoặc cộng đồng — miễn phí hoặc thu phí.
- **Chỉnh sửa** code (Python, JavaScript), template, config để phù hợp nhu cầu riêng của bạn.
- **Đóng gói lại** bundle (hoặc một phần) thành một phần của sản phẩm/dịch vụ của bạn.

---

## Bạn cần làm (điều kiện sử dụng)

### 1. Giữ credit Techla

Không được xóa hay thay tên tác giả ở các vị trí sau:

- YAML frontmatter `author: Techla` trong mọi file `SKILL.md`.
- `"author": { "name": "Techla" }` trong `manifest.json` của extension.
- Footer "Báo cáo tạo bởi Techla — Skill ... v1.0.0" trong mọi output `.docx`, `.md`, `.pptx` sinh ra từ skill.
- Dòng "© 2026 Techla" / "Bản quyền Techla" trong mọi file docs (`README.md`, `LICENSE.md`, ...).
- Docstring "Author: Techla" ở đầu các file `.py`, `.js`.

### 2. Ghi nhận công khai

Khi viết bài giới thiệu bundle (blog, mạng xã hội, báo chí, slide bán hàng) — ghi nhận **Techla** là tác giả gốc. Tối thiểu 1 câu dạng *"Bộ công cụ dựa trên Techla Business Skills v1.0.0"* hoặc tương đương.

---

## Bạn không được

- **Xóa credit** Techla khỏi bất kỳ vị trí nào nêu trên.
- **Ghi tên khác** làm tác giả gốc.
- **Đăng ký bản quyền** bundle hoặc bất kỳ skill nào (nguyên bản hoặc chỉnh sửa) dưới tên bạn hoặc tổ chức khác.
- **Tuyên bố** rằng skill do bạn phát triển nếu chưa có sự cho phép bằng văn bản của Techla.

---

## Về dữ liệu của bạn (quan trọng)

Bundle xử lý **dữ liệu nhạy cảm của quán**: đơn hàng, thông tin khách hàng, tin nhắn Zalo, số điện thoại, CCCD nhân viên...

Bạn (người dùng bundle) **tự chịu trách nhiệm**:

- **Tuân thủ Luật An ninh mạng 2018, Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân** và các quy định pháp luật liên quan.
- **Có sự đồng ý** của khách hàng / nhân viên trước khi nhập dữ liệu của họ vào skill để phân tích / xuất báo cáo.
- **Bảo mật credentials** (Pancake API key, thông tin quán, file Excel chứa SĐT khách). Không commit vào git public, không share trong chat bừa bãi.
- **Xóa dữ liệu** đúng hạn theo cam kết với khách (ví dụ: 90 ngày sau khi khách hết quan hệ mua bán).
- **Không dùng dữ liệu sai mục đích**: lừa đảo, quấy rối, theo dõi trái phép, bán cho bên thứ ba.

---

## Về copyright của nguồn bên ngoài

Skill `research-san-pham-moi` tổng hợp thông tin từ các nguồn web bên thứ ba. Bạn tự chịu trách nhiệm:

- **Tôn trọng copyright** của nguồn gốc (paraphrase, không copy nguyên văn, cite đầy đủ).
- **Không đạo nhái / bắt chước trái phép** menu, thương hiệu, slogan của đối thủ dựa trên báo cáo research.
- **Xác minh lại số liệu** trước khi đưa vào quyết định kinh doanh.

---

## Miễn trừ trách nhiệm

Bundle được cung cấp **"NGUYÊN TRẠNG"** (AS IS), không kèm bảo hành dưới bất kỳ hình thức nào, bao gồm nhưng không giới hạn: tính thương mại, tính phù hợp cho một mục đích cụ thể, và không vi phạm quyền của bên thứ ba.

**Techla KHÔNG CHỊU TRÁCH NHIỆM** cho:

- **Quyết định kinh doanh** bạn đưa ra dựa trên output của skill (danh sách churn, top VIP, dự báo doanh số, action list, báo cáo research).
- **Độ chính xác** của thông tin trong báo cáo research (phụ thuộc nguồn web bên thứ ba, có thể lỗi thời).
- **Hậu quả pháp lý** phát sinh từ điều khoản hợp đồng, văn bản bạn ký kết dựa trên template của skill — **skill không thay thế tư vấn luật sư**.
- **Vi phạm pháp luật / đạo đức** phát sinh từ việc bạn sử dụng dữ liệu mà skill / extension lấy về.
- **Rò rỉ, mất mát dữ liệu** do lỗi bảo mật phía bạn (API key bị lộ, thiết bị bị hack).
- **Sự gián đoạn dịch vụ** do Claude, Pancake, hoặc các bên thứ ba thay đổi / ngừng hoạt động.
- **Thiệt hại trực tiếp hoặc gián tiếp** phát sinh từ việc sử dụng bundle.

Bạn tự chịu trách nhiệm rà soát output trước khi dùng để đưa ra quyết định kinh doanh hoặc ký kết pháp lý.

---

## Luật áp dụng

License này được giải thích theo **pháp luật Việt Nam**. Mọi tranh chấp phát sinh sẽ được giải quyết tại tòa án có thẩm quyền tại Việt Nam.

---

*Nếu có câu hỏi về license, liên hệ qua kênh bạn mua bundle này từ Techla.*

**© 2026 Techla.** Bảo lưu mọi quyền.
