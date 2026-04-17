# Cài Techla Pancake Extension (cho Zalo qua Pancake)

Extension này giúp Claude đọc tin nhắn từ các **nhóm Zalo** mà bạn (nick phụ chủ quán) đã liên kết với **Pancake**. Khi cài xong, bạn có thể hỏi Claude:

- *"Check nhóm nhân viên 3 ngày qua có vấn đề gì cần xử lý không?"*
- *"Khách VIP có phàn nàn gì tuần này?"*
- *"Nhóm nào hôm nay nhiều tin nhất?"*

Extension **chỉ chạy trên Claude Desktop** (không chạy web/mobile).

---

## Yêu cầu trước khi cài

- **Claude Desktop** đã cài (xem file `01`).
- **Tài khoản Pancake** (https://pancake.vn) với page Zalo cá nhân đã bật.
- **Nick Zalo phụ** (thường là nick chủ quán) đã join các nhóm cần theo dõi, và nick này đã được link với page Pancake.

> ⚠️ Nếu bạn chưa dùng Pancake → **bỏ qua extension này**. 3 skill kia hoạt động độc lập.

---

## Bước 1 — Lấy Pancake API Key

1. Đăng nhập [https://pages.fm/admin](https://pages.fm/admin) (hoặc URL admin Pancake của bạn).
2. Chọn page Zalo cá nhân → vào **Cấu hình** (menu trái).
3. Tìm mục **Webhook & API** (hoặc **API Access**).
4. Bấm **Generate API Token** (nếu chưa có) hoặc copy token hiện có.
5. Dán tạm vào Notepad / note app — khoảng 50 ký tự dạng `lRkF...xT9z`.

> ⚠️ **Bảo mật**: API key này cho phép đọc toàn bộ tin nhắn của page. **Không share cho ai khác, không commit lên git.** Claude Desktop sẽ tự lưu vào Keychain/Credential Manager, không để plain text trong máy bạn.

> 📷 *(Placeholder screenshot: trang Webhook-API trong Pancake admin, highlight nút Generate Token)*

---

## Bước 2 — Cài file `.mcpb`

1. Trong bundle, vào `extensions/` → tìm file `techla-pancake-1.0.4.mcpb`.
2. **Cách 1**: Double-click file → Claude Desktop tự mở dialog cài đặt.
3. **Cách 2**: Mở Claude Desktop → Settings (`⌘/Ctrl + ,`) → tab **Extensions** → bấm **Install from file** → chọn `.mcpb`.

> 📷 *(Placeholder screenshot: dialog "Install Extension")*

---

## Bước 3 — Nhập credentials

Claude Desktop sẽ hỏi:

| Field | Giá trị |
|---|---|
| **Pancake API Key** | Paste token từ Bước 1 (hiển thị dạng `••••••••`) |
| **Page ID** (optional) | **Để trống** — extension tự detect từ token. Chỉ điền nếu cần override. |
| **Base URL** (optional) | Để mặc định: `https://pages.fm/api/public_api/v1` |

Bấm **Save & Enable**.

> Token Pancake là JWT chứa sẵn `page_id` trong payload, extension decode và tự dùng. Bạn không cần tìm page_id thủ công.

> 📷 *(Placeholder screenshot: dialog cấu hình extension với 2 field)*

---

## Bước 4 — Test thử

Mở cuộc trò chuyện mới, gõ:

> *"Liệt kê 5 nhóm Zalo mới nhất có tin nhắn trong Pancake."*

Claude sẽ gọi tool `list_conversations` và trả về bảng:

```
| # | Tên nhóm         | Số thành viên | Tin mới nhất       | Chưa đọc |
|---|------------------|---------------|--------------------|----------|
| 1 | Nhóm nhân viên   | 8             | 2026-04-17 14:23   | 3        |
| 2 | Khách VIP nhóm 1 | 12            | 2026-04-17 12:05   | 0        |
| ... |
```

**Nếu lỗi** → xem troubleshooting bên dưới.

---

## Troubleshooting

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| "Sai API key (401)" | Token hết hạn hoặc paste sai | Quay lại Pancake admin → Regenerate Token → update trong Settings → Extensions |
| "Không tìm thấy page (404)" | Page ID sai | Kiểm tra URL admin Pancake, copy lại phần số |
| "Pancake rate limit (429)" | Gọi quá nhiều trong 1 phút | Chờ 1 phút, rồi hỏi câu đơn giản hơn |
| Claude không gọi tool | Extension bị disabled | Settings → Extensions → Techla Pancake → bật toggle ON |
| "Không kết nối được Pancake" | Máy mất mạng / firewall chặn | Kiểm tra internet, thử mở `https://pages.fm` bằng browser |

---

## Bảo mật & quyền riêng tư

- API key **mã hóa** trong Keychain (macOS) hoặc Credential Manager (Windows). Không ở plain text.
- Claude Desktop **chỉ đọc** tin nhắn khi bạn hỏi. Không background polling.
- **Bạn tự chịu trách nhiệm** tuân thủ Luật An ninh mạng và Nghị định 13/2023 về dữ liệu cá nhân khi xuất tin nhắn ra ngoài.
- Xem thêm trong [LICENSE.md của extension](../src/techla-pancake/LICENSE.md) mục "Về quyền riêng tư & bảo mật".

---

## Gỡ cài đặt

Settings → Extensions → Techla Pancake → **⋯ → Remove**.

API key tự bị xóa khỏi Keychain.

---

## Bước tiếp theo

Sang [`04-SU-DUNG.md`](./04-SU-DUNG.md) để xem ví dụ câu hỏi hay dùng.

---

**© 2026 Techla.** Xem [LICENSE.md](../LICENSE.md) để biết điều khoản sử dụng.
