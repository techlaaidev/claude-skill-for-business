# Cài 3 Claude Skills

Bundle này có 3 file `.skill` trong folder `skills/`:

- `cskh-phan-tich-don-hang.skill` — phân tích đơn hàng
- `research-san-pham-moi.skill` — research trend sản phẩm mới
- `soan-van-ban.skill` — soạn hợp đồng / biên bản / thông báo

Cài 1 skill chỉ mất ~30 giây. Làm theo 4 bước dưới đây cho từng file.

---

## Yêu cầu trước khi cài

- Đã cài **Claude Desktop** (xem [`01-BAT-DAU-TAI-DAY.md`](./01-BAT-DAU-TAI-DAY.md) Bước 1).
- Đã bật **Code Execution** trong Settings → Features (Bước 2).

Nếu chưa — quay lại file `01` trước rồi mới tiếp.

---

## Cài từng file `.skill` (lặp lại cho cả 3)

### Bước 1 — Mở Settings → Skills

- macOS: bấm `⌘ + ,` → sang tab **Skills**
- Windows: bấm `Ctrl + ,` → sang tab **Skills**

> 📷 *(Placeholder screenshot: Settings panel mở ở tab "Skills")*

### Bước 2 — Bấm nút "Upload skill"

Ở góc trên phải tab Skills sẽ có nút **Upload skill** (hoặc **Install from file**).

> 📷 *(Placeholder screenshot: nút Upload skill trên UI)*

### Bước 3 — Chọn file `.skill` từ máy

Kéo thả hoặc browser chọn file:

- Lần 1: `cskh-phan-tich-don-hang.skill`
- Lần 2: `research-san-pham-moi.skill`
- Lần 3: `soan-van-ban.skill`

Claude Desktop sẽ **giải nén + xác thực** skill. Mất ~5-10 giây.

> 📷 *(Placeholder screenshot: dialog chọn file)*

### Bước 4 — Bật toggle

Sau khi cài, skill hiện trong danh sách. Bật toggle **bên phải** để Claude biết đã có skill này.

> 📷 *(Placeholder screenshot: toggle ON với tên skill)*

---

## Xác nhận đã cài đủ

Sau khi cài cả 3, tab Skills sẽ hiển thị:

| Tên | Trạng thái |
|---|---|
| `cskh-phan-tich-don-hang` | ✅ Enabled |
| `research-san-pham-moi` | ✅ Enabled |
| `soan-van-ban` | ✅ Enabled |

---

## Test thử

Mở một cuộc trò chuyện mới trong Claude Desktop, gõ:

> *"Skills nào đang bật cho tôi?"*

Claude sẽ trả lời tên 3 skill + mô tả ngắn. **Nếu Claude bảo không có skill nào** → quay lại kiểm tra:

1. Toggle đã bật (Bước 4)
2. Code Execution đã bật (xem file `01` Bước 2)
3. Đã restart Claude Desktop sau khi cài skill đầu tiên

---

## Update skill lên version mới

Khi Techla phát hành skill version mới:

1. Tải file `.skill` mới.
2. Vào Settings → Skills → tìm skill cũ → bấm **menu ⋯ → Remove**.
3. Upload file `.skill` mới theo 4 bước trên.

---

## Gỡ cài đặt

Settings → Skills → chọn skill → bấm **⋯ → Remove**.

Skill sẽ bị xóa khỏi Claude Desktop. Các file `.skill` vẫn còn trong bundle của bạn để cài lại sau.

---

## Bước tiếp theo

- Nếu bạn dùng **Pancake** để quản lý chat Zalo → cài extension Pancake theo [`03-CAI-EXTENSION-PANCAKE.md`](./03-CAI-EXTENSION-PANCAKE.md).
- Nếu không dùng Pancake → nhảy thẳng sang [`04-SU-DUNG.md`](./04-SU-DUNG.md) để bắt đầu hỏi Claude.

---

**© 2026 Techla.** Xem [LICENSE.md](../LICENSE.md) để biết điều khoản sử dụng.
