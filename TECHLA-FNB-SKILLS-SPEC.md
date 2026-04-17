# Techla F&B Skills Bundle — Spec đầy đủ để build

Dùng prompt này với **Claude Code CLI** (hoặc Claude Desktop Code). Copy toàn bộ file này, đưa cho Claude Code với câu: *"Đọc spec này và build toàn bộ bundle theo thứ tự được chỉ định. Test từng skill trước khi sang skill tiếp theo. Có gì cần làm rõ thì hỏi tôi."*

---

## 0. Context tổng thể

### Mục tiêu

Build 1 **bundle 4 skill** để bán đứt cho chủ doanh nghiệp F&B/bán lẻ Việt Nam. Khách mua về, cài vào Claude Desktop app của họ, dùng để tự động hóa các việc:

1. Phân tích đơn hàng khách hàng (CSKH)
2. Research sản phẩm mới (trend đồ uống, bao bì, công thức...)
3. Giám sát nhóm Zalo qua Pancake API (phát hiện vấn đề cần xử lý)
4. Soạn các văn bản vận hành (hợp đồng, biên bản, thông báo)

### Quyết định đã chốt (KHÔNG cần hỏi lại)

| Mục | Giá trị |
|---|---|
| Tác giả / bản quyền | **Techla** (không kèm website/email) |
| Năm bản quyền | 2026 |
| Ngôn ngữ docs | **Tiếng Việt 100%** |
| Mô hình bán | Bán đứt, 1 lần thu tiền |
| Đối tượng khách | Chủ F&B/bán lẻ Việt Nam, biết chút kỹ thuật (copy-paste, sửa file config) |
| Môi trường chạy | **Claude Desktop app** (macOS + Windows), gói Free cũng chạy được |
| License | Nhẹ nhàng — cho phép phân phối lại, **bắt buộc giữ credit Techla** |
| Đóng gói | 3 file `.skill` + 1 file `.mcpb` trong 1 bundle zip |
| Code chính | Python cho scripts của skill, Node.js cho MCP extension |
| Report format | Đồng thời `.docx` (python-docx) và `.md` |
| Không làm | video hướng dẫn, installer `.exe`/`.dmg`, logo, license server, auto-update |

### Cấu trúc bundle

```
WECA-Business-Skills-v1.0.0/
├── skills/
│   ├── cskh-phan-tich-don-hang.skill      (Skill 1)
│   ├── research-san-pham-moi.skill        (Skill 2)
│   └── soan-van-ban.skill                 (Skill 3b)
├── extensions/
│   └── weca-pancake.mcpb                  (Skill 3a — extension)
├── docs/
│   ├── 01-BAT-DAU-TAI-DAY.md
│   ├── 02-CAI-SKILL.md
│   ├── 03-CAI-EXTENSION-PANCAKE.md
│   ├── 04-SU-DUNG.md
│   └── 05-HOI-DAP.md
├── samples/
│   ├── sample_weca_format.xlsx
│   ├── sample_standard_format.xlsx
│   └── sample_report_output.docx
├── LICENSE.md
├── CHANGELOG.md
└── README.md
```

### Cấu trúc của **mỗi** skill bên trong `.skill` file

```
skill-name/
├── SKILL.md                    # YAML frontmatter + instructions cho Claude
├── README.md                   # Hướng dẫn cho khách cuối (tiếng Việt)
├── LICENSE.md
├── CHANGELOG.md
├── config.example.yaml         # Config mẫu có comment chi tiết
├── requirements.txt
├── scripts/
│   └── *.py
├── templates/
│   └── *.docx (nếu cần)
└── samples/
    └── *.xlsx / *.docx (data mẫu)
```

### Thứ tự build

Build **tuần tự**, test xong mới sang skill tiếp theo:

1. **Skill 1 — CSKH Phân tích đơn hàng** (phức tạp nhất về logic, có data thật để test)
2. **Skill 3b — Soạn văn bản** (đơn giản, template-based)
3. **Skill 2 — Research sản phẩm mới** (web search dựa trên prompt)
4. **Skill 3a — Pancake MCP Extension** (phức tạp nhất về kỹ thuật, làm cuối)
5. Build `docs/`, `samples/`, `README.md` tổng, package bundle

---

## 1. Format chuẩn cho mỗi SKILL.md

Mọi file `SKILL.md` đều phải có YAML frontmatter như sau:

```yaml
---
name: <skill-id-kebab-case>
description: "Mô tả NHIỀU TRIGGER để skill dễ được kích hoạt. Phải có: (1) skill làm gì, (2) các cụm từ/ngữ cảnh để trigger, (3) output format. Viết bằng tiếng Việt, nên 'pushy' — 'Phải trigger bất cứ khi nào người dùng...'"
author: Techla
version: 1.0.0
license: Xem LICENSE.md — cho phép phân phối lại, yêu cầu giữ credit Techla
---

# Skill: <Tiêu đề>

<thân nội dung hướng dẫn Claude>
```

Thân nội dung cần có các section (không bắt buộc đủ hết, tùy skill):
- `## Khi nào trigger` — cụm từ/ngữ cảnh
- `## Quy trình thực hiện` — các bước Claude phải làm
- `## Tùy chỉnh qua config` — hành vi config điều khiển
- `## Lưu ý quan trọng` — edge cases, giới hạn
- `## Tài liệu bổ sung` — list các file trong skill

Giới hạn: SKILL.md **dưới 500 dòng**. Nếu dài hơn, tách ra file riêng trong `references/` và chỉ link từ SKILL.md.

---

## 2. SKILL 1 — CSKH Phân tích đơn hàng

### Đối tượng dữ liệu

Chủ F&B nhập file Excel đơn hàng đã export từ hệ thống (Google Sheet, KiotViet, Sapo…). Skill đọc file, phân tích, xuất báo cáo Word + Markdown.

### Hỗ trợ 2 format file (parser tự detect, hoặc hỏi user nếu không rõ)

#### **Format A — WECA-style (bảng ma trận tháng)**

Đặc điểm khó:
- Header ở **dòng 5** (dòng 1-4 là title/annotation)
- Các cột đầu: `STT`, `MÃ KH`, `TÊN KH`, `SĐT`, `ĐỊA CHỈ`, `MÃ SP`, `TÊN SP`, `SỐ LƯỢNG BÁN TB/Lần`, `SỐ LƯỢNG ĐƠN HÀNG/THÁNG`, `GIÁ BÁN`, `GIÁ BÁN MỚI`
- 12 cột tháng: tên cột dạng `01/26`, `02/26`, ..., `12/26` (format `MM/YY`)
- **Các ô trong cột tháng** chứa ngày khách đặt trong tháng đó. Format đa dạng:
  - Datetime object của Excel (1 ngày duy nhất) — ví dụ cell value là `datetime(2026, 1, 22)`
  - String nhiều ngày, phân tách bởi `;` hoặc `,`, có thể kèm suffix `/MM`:
    - `"2;23/2"` → ngày 2 và 23 của tháng 2
    - `"01,17/04"` → ngày 1 và 17 của tháng 4
    - `"17/04"` → ngày 17 tháng 4
  - Integer đơn thuần `17` → ngày 17 của tháng (của cột đó)
  - `None` → không đặt trong tháng đó
- **Thông tin KH merge dọc** trên file: dòng đầu có tên KH + SĐT + địa chỉ, các dòng tiếp theo (SP khác của cùng KH) để trống các cột đó. Parser phải forward-fill.

File WECA điển hình có **3 sheet**:

1. **Sheet chính** (tên như "Tần Suất đặt hàng 2026") — bảng ma trận nêu trên
2. **Sheet "Lịch sử chăm sóc KH"** — có các cột: `MÃ KH`, `TÊN KH`, `MỤC TIÊU CHĂM SÓC`, `Nội dung tin nhắn`, `LỊCH SỬ CHĂM SÓC`
3. **Sheet danh sách KH** (tên như "Trang tính1", "Danh sách khách hàng") — có các cột: `Tên khách hàng`, `Số điện thoại`, `Địa chỉ`, `Hiện trạng chăm sóc`, `Cơ hội`, `Cần làm`

Skill phải đọc **cả 3 sheet** nếu có — sheet 2 và 3 cung cấp context chăm sóc + cơ hội cross-sell.

**Lưu ý quan trọng khi classify sheet:** sheet "Lịch sử chăm sóc KH" cũng có cột `MÃ KH`/`TÊN KH`. Để không bị nhầm là sheet chính, phải check `MỤC TIÊU CHĂM SÓC`/`LỊCH SỬ CHĂM SÓC` **trước** — hints care sheet có priority cao hơn main.

Các cột có mã nội bộ như `4E-4`, `4E-2`, `3E-11`, `N1C-32 - CO` (sau 12 cột tháng) — **bỏ qua**, không dùng để phân tích.

#### **Format B — Transaction log chuẩn**

- Header ở dòng 1
- 1 dòng = 1 đơn hàng
- Các cột khác nhau tùy hệ thống — skill auto-detect theo alias:
  - **Ngày**: `Ngày`, `Ngày đặt`, `Date`, `Order Date`, `Ngày mua`, `Ngày bán`
  - **Khách**: `Tên khách`, `Khách hàng`, `Customer`, `Customer Name`, `Mã KH`
  - **SĐT**: `SĐT`, `Phone`, `Số điện thoại`
  - **Sản phẩm**: `Sản phẩm`, `Tên SP`, `Mặt hàng`, `Product`, `Mã SP`
  - **Số lượng**: `Số lượng`, `SL`, `Qty`, `Quantity`
  - **Đơn giá**: `Đơn giá`, `Giá`, `Price`, `Unit Price`
  - **Thành tiền** (optional): `Thành tiền`, `Doanh thu`, `Revenue`, `Total`

Parser normalize tên cột (lower, bỏ dấu tiếng Việt, strip) rồi match với alias list.

### Schema chuẩn hóa (output của parser, input của analyzer)

```python
@dataclass
class Customer:
    customer_id: str
    name: str
    phone: str | None
    address: str | None
    care_goal: str | None          # từ sheet 2
    care_message_template: str | None
    care_history: str | None
    opportunity: str | None         # từ sheet 3
    action_needed: str | None
    status: str | None

@dataclass
class Product:
    product_id: str
    name: str
    avg_qty_per_order: float | None    # TB/lần (WECA) hoặc tự tính từ data (standard)
    avg_orders_per_month: float | None
    unit_price: float | None            # ưu tiên GIÁ BÁN MỚI, fallback GIÁ BÁN

@dataclass
class OrderEvent:
    customer_id: str
    product_id: str
    order_date: str                     # ISO "YYYY-MM-DD"
    qty: float | None                   # với WECA: suy ra từ avg_qty_per_order của SP
    estimated_revenue: float | None     # qty × unit_price

@dataclass
class ParsedData:
    source_file: str
    parsed_at: str
    format: str                         # "weca" | "standard"
    year: int
    customers: list[Customer]
    products: list[Product]
    orders: list[OrderEvent]
    warnings: list[str]
```

### Các phân tích analyzer phải tính

1. **Tổng quan:** tổng KH, SP, đơn, doanh thu ước tính, tổng SL, khoảng thời gian
2. **Theo tháng:** số đơn / SL / doanh thu / số KH duy nhất từng tháng
3. **MoM comparison:** % thay đổi của tháng hiện tại so với tháng trước (orders, revenue, customers, qty)
4. **Top VIP:** sort KH theo `total_revenue`, default top 10
5. **Churn warning (khách sắp mất):** với mỗi KH có >= 2 đơn, tính avg gap giữa các đơn. Nếu (ngày hiện tại - ngày đơn cuối) > `avg_gap × churn_threshold_multiplier` → cảnh báo. Default multiplier 1.5.
6. **Decreasing rhythm:** KH có >= 4 đơn, so sánh số đơn trong tháng gần nhất với trung bình các tháng trước. Nếu giảm > 40% → cảnh báo.
7. **Star products:** rank theo `revenue × log(1 + num_unique_customers)` — cân bằng doanh thu và độ phổ biến
8. **Dead products:** SP có trong products dict (nghĩa là có trong menu) nhưng:
   - 0 đơn trong toàn bộ khoảng thời gian, HOẶC
   - đơn cuối cách ngày tham chiếu > `dead_product_days` (default 90)
9. **Cross-sell:** list KH có `opportunity` hoặc `action_needed` được ghi trong sheet 3 (cho khách biết mà push)
10. **Basket analysis:** với mỗi (customer, date), nếu có >= 2 SP → đếm co-occurrence của các cặp. Top 10 cặp được mua cùng nhiều nhất.
11. **Action list:** tổng hợp churn + decreasing + cross-sell thành list việc cần làm, gắn priority CAO/TRUNG BÌNH/THẤP (CAO = churn của VIP, TRUNG BÌNH = churn thường hoặc decreasing, THẤP = cross-sell).

### Config (file `config.yaml` tùy chọn, khách đặt cạnh file Excel)

```yaml
churn_threshold_multiplier: 1.5   # nhân với avg_gap
vip_top_n: 10                     # số KH VIP hiển thị
dead_product_days: 90             # ngày không đơn thì xếp xác sống
enable_basket_analysis: true
reference_date: null              # null = dùng max(order_date), có thể set YYYY-MM-DD
min_orders_for_rhythm: 2          # cần ít nhất N đơn để tính nhịp
```

### Output report

**File `.docx`:**
- Page A4, margin 2cm
- Default font Arial 11pt
- Title page: "BÁO CÁO PHÂN TÍCH ĐƠN HÀNG & CHĂM SÓC KHÁCH HÀNG" màu xanh đậm (#1F4E79) căn giữa
- 11 section theo thứ tự (quan trọng — để cảnh báo trên đầu):
  1. Tóm tắt điều hành (bảng key-value)
  2. ⚠️ Khách sắp mất (bảng, màu đỏ ở tiêu đề)
  3. 👑 Top VIP (bảng)
  4. 💡 Cơ hội bán thêm (list có indent)
  5. ⭐ Sản phẩm ngôi sao (bảng)
  6. 💀 Sản phẩm xác sống (bảng)
  7. 📊 So sánh MoM (text)
  8. 📅 Chi tiết theo tháng (bảng)
  9. 📉 Khách giảm nhịp (bảng)
  10. 🛒 Cặp SP hay mua cùng (bảng, nếu `enable_basket_analysis` = true)
  11. 🎯 Action list — priority màu: CAO đỏ, TRUNG BÌNH cam, THẤP xanh
- Bảng có header màu xanh (#2E75B6) chữ trắng, dùng style "Light Grid Accent 1" hoặc "Table Grid"
- Footer cuối trang cuối: `"Báo cáo tạo bởi Techla — Skill CSKH Phân tích đơn hàng v1.0.0"` in nghiêng, xám nhạt, căn giữa, 9pt

**File `.md`:** cùng nội dung, dùng markdown tables. Footer cuối file tương tự.

### Format số (tiếng Việt)

- **Tiền:** `1.234.567đ` (dấu chấm ngăn cách ngàn, `đ` cuối)
- **Số nguyên:** `1.234`
- **Số thập phân:** `1.234,5` (chấm ngàn, phẩy thập phân)
- **Phần trăm:** `+12,3%` hoặc `-5,0%` (có dấu + nếu dương)

### Files cần tạo cho Skill 1

```
cskh-phan-tich-don-hang/
├── SKILL.md
├── README.md
├── LICENSE.md
├── CHANGELOG.md
├── config.example.yaml
├── requirements.txt                # openpyxl, python-docx, pyyaml
├── scripts/
│   ├── __init__.py
│   ├── parser_weca.py              # parse WECA format → JSON schema
│   ├── parser_standard.py          # parse transaction log → JSON schema
│   ├── analyzer.py                 # tính 11 metrics → analysis.json
│   └── report_builder.py           # build .docx + .md từ analysis.json
└── samples/
    ├── sample_weca_format.xlsx     # tạo bằng openpyxl, data ẩn danh
    └── sample_standard_format.xlsx
```

Mỗi script phải chạy được standalone với argparse:
```bash
python scripts/parser_weca.py input.xlsx --output parsed.json
python scripts/parser_standard.py input.xlsx --output parsed.json
python scripts/analyzer.py parsed.json --output analysis.json [--config config.yaml]
python scripts/report_builder.py analysis.json --docx out.docx --md out.md
```

### Sample data — yêu cầu ẩn danh

Tạo `sample_weca_format.xlsx` với ~8 khách hàng giả (tên kiểu "Quán Sao Đêm", "Coffee House Trúc Bạch", "The Local Brew Lab"…), ~12 sản phẩm giả (Cafe Robusta Premium, Trà Olong, Matcha Nhật…), data phủ 3-4 tháng năm 2026. Phải có:
- Ít nhất 2 KH trigger được churn warning (không đặt tháng cuối)
- Ít nhất 1 KH trigger decreasing rhythm
- Ít nhất 2 SP trigger dead product
- Ít nhất 2 KH có opportunity ghi trong sheet 3
- Nhiều format khác nhau ở các ô cột tháng (datetime, string 1 ngày, string nhiều ngày `;`)

Tạo `sample_standard_format.xlsx` cùng data đó nhưng dưới dạng transaction log (1 dòng = 1 đơn).

---

## 3. SKILL 3b — Soạn văn bản (làm trước Skill 2 vì đơn giản)

### Mục đích

Soạn nhanh các văn bản vận hành quán cafe theo mẫu chuẩn. Khách chỉ cần nói loại văn bản + thông tin cụ thể, skill tạo file `.docx` điền sẵn.

### 3 loại văn bản hỗ trợ

#### **1. Hợp đồng thử việc nhân viên** (pha chế / phục vụ)

Các điều khoản cần có:
- Thông tin 2 bên (quán + nhân viên)
- Vị trí công việc, mức lương (giờ/ca/tháng)
- Thời gian thử việc (thường 2 tháng)
- Giờ làm, ca làm, phụ cấp
- Quy định về đi trễ, nghỉ không phép, phạt
- Bảo mật công thức đồ uống (điều khoản quan trọng cho quán cafe)
- Chấm dứt hợp đồng

#### **2. Biên bản bàn giao ca**

Các mục:
- Ca (sáng/chiều/tối), ngày, người giao, người nhận
- Tồn quỹ đầu ca / cuối ca
- Tồn nguyên liệu: sữa tươi, kem, syrup, cafe các loại, trà... (bảng)
- Thiết bị: máy pha cafe, máy xay, tủ lạnh... tình trạng
- Sự cố trong ca (nếu có)
- Khách phàn nàn (nếu có)
- Việc bàn giao cho ca sau
- Chữ ký 2 bên

#### **3. Thông báo nội bộ**

Template chung, các loại thường dùng:
- Đổi lịch ca
- Ra món mới / đổi công thức
- Quy định mới
- Nhắc nhở (đồng phục, vệ sinh, thái độ)
- Thông báo nghỉ lễ

Trường cần:
- Kính gửi: toàn thể nhân viên / ca X / team Y
- Chủ đề (tiêu đề lớn)
- Nội dung chính
- Thời gian áp dụng
- Người ký (chủ quán / quản lý)

### Cách hoạt động

User nói kiểu: *"Soạn cho tôi hợp đồng thử việc cho bạn Nguyễn Văn A, vị trí pha chế, 8 triệu/tháng, thử việc 2 tháng, bắt đầu 01/05/2026."*

Skill:
1. Nhận dạng loại văn bản (hợp đồng / biên bản / thông báo) từ query
2. Extract thông tin từ query. Nếu thiếu trường quan trọng → hỏi user bổ sung (tối đa 3 câu hỏi 1 lúc).
3. Điền template tương ứng
4. Xuất file `.docx`

### Config

```yaml
ten_quan: "Quán Cafe XYZ"
dia_chi_quan: "123 Phan Đình Phùng, Hà Nội"
ma_so_thue: "0123456789"
nguoi_dai_dien: "Nguyễn Văn Chủ"
chuc_vu_dai_dien: "Chủ quán"
```

### Files cần tạo

```
soan-van-ban/
├── SKILL.md
├── README.md, LICENSE.md, CHANGELOG.md
├── config.example.yaml
├── requirements.txt               # python-docx, pyyaml
├── scripts/
│   ├── builder_hop_dong.py
│   ├── builder_bien_ban_ca.py
│   └── builder_thong_bao.py
└── templates/
    ├── hop_dong_thu_viec_template.docx   # (optional — có thể gen bằng code)
    ├── bien_ban_ban_giao_ca_template.docx
    └── thong_bao_template.docx
```

Mỗi builder nhận vào dict các trường + config → xuất `.docx`. Không dùng template file nếu gen bằng python-docx thuần đơn giản hơn.

### Yêu cầu quan trọng

- Văn phong **tiếng Việt hành chính, chuẩn mực**, không dùng emoji trong nội dung
- Footer mỗi file: `"Soạn bởi Techla — Skill Soạn văn bản v1.0.0"`
- Ngày tháng viết: `Ngày 01 tháng 05 năm 2026` (không viết `01/05/2026`)
- Số tiền viết bằng chữ sau khi viết bằng số: `8.000.000đ (Tám triệu đồng chẵn)`

---

## 4. SKILL 2 — Research sản phẩm mới

### Mục đích

Khách hỏi: *"Research cho tôi trend matcha 2026"* — skill search web realtime (VN + quốc tế), tổng hợp thành báo cáo `.md` + `.docx`, có sub-command convert `.md` → `.pptx`.

### Phạm vi research

- **Thị trường VN:** các chuỗi lớn (Highlands, Phúc Long, The Coffee House, Katinat, Starbucks VN), xu hướng quán độc lập, hashtag Vietnam trên social
- **Thị trường quốc tế:** Nhật (cafe specialty, matcha), Hàn (cafe dessert, topping), Đài Loan (trà), Âu Mỹ (specialty coffee)
- **Chủ đề rộng:** đồ uống (trà, cafe, topping, nguyên liệu mới), bao bì, công thức, mô hình kinh doanh, chiến lược giá

### Quy trình

1. User nêu chủ đề + (optional) phạm vi (VN / quốc tế / cả hai)
2. Nếu phạm vi không rõ, default **cả hai**
3. Skill tạo search plan: 5-10 query đa dạng
4. Chạy search_web, fetch top sources
5. Tổng hợp thành báo cáo có structure:
   - Tóm tắt (3-5 câu)
   - Xu hướng chính (top 5)
   - Phân tích VN vs quốc tế
   - Case study 2-3 brand nổi bật
   - Cơ hội áp dụng cho quán cafe tầm trung VN
   - Nguồn tham khảo (cite đầy đủ)
6. Xuất `.md` + `.docx` song song
7. Nếu user yêu cầu slide: convert `.md` → `.pptx` dùng **Marp** (preferred) hoặc `python-pptx`

### Lưu ý copyright

- **Paraphrase toàn bộ**, không copy nguyên văn
- Mỗi nguồn chỉ quote tối đa 1 lần, dưới 15 từ
- Cite nguồn đầy đủ (URL, tên site, ngày nếu có)

### Files cần tạo

```
research-san-pham-moi/
├── SKILL.md
├── README.md, LICENSE.md, CHANGELOG.md
├── config.example.yaml             # có thể chứa list brand VN ưu tiên, list nguồn quốc tế
├── requirements.txt                # python-docx, markdown-to-pptx (marp-cli optional)
├── scripts/
│   ├── build_report.py             # md + docx output
│   └── md_to_pptx.py               # dùng Marp CLI nếu có, fallback python-pptx
└── (không có samples — mỗi research là 1 chủ đề)
```

### Config example

```yaml
# Danh sách brand VN ưu tiên research khi không chỉ định
vn_brands_priority:
  - "Highlands Coffee"
  - "Phúc Long"
  - "The Coffee House"
  - "Katinat"
  - "Starbucks Vietnam"
  - "Cộng Cà Phê"
  - "Là Việt"

# Các thị trường quốc tế ưu tiên
international_markets:
  - "Japan specialty coffee"
  - "Korean dessert cafe"
  - "Taiwan bubble tea"
  - "Australia specialty coffee"

# Số nguồn tối thiểu để đưa vào báo cáo
min_sources: 8

# Có convert sang pptx không (sau khi tạo md)
auto_convert_pptx: false
```

---

## 5. SKILL 3a — Pancake MCP Extension

### Đây là gì

Desktop Extension (`.mcpb` file) cho Claude Desktop. KHÔNG phải skill truyền thống. Là 1 MCP server chạy local trong Claude Desktop, query Pancake API để lấy tin nhắn từ các nhóm Zalo mà chủ quán (nick phụ) đang tham gia.

### Môi trường chạy

- **Chỉ Claude Desktop app** (macOS + Windows). Không chạy trên web/mobile.
- Claude Desktop có sẵn Node.js runtime — **dùng Node.js**, không dùng Python (để không bắt khách cài thêm runtime).
- MCP server chạy như subprocess của Claude Desktop, **on-demand** (không cần background polling riêng).

### Credentials cần

- `pancake_api_key` (mark `"sensitive": true` trong manifest — Claude Desktop tự encrypt vào Keychain/Credential Manager)
- `pancake_page_id` (ID của page Zalo cá nhân trong Pancake — copy từ URL admin Pancake)

### Tools MCP cần expose

1. **`list_conversations`**
   - Input: `{ limit?: number, page?: number }`
   - Output: list conversation (id, name/title của nhóm, member count, last message time, unread count)
   - Endpoint: `GET https://pages.fm/api/public_api/v1/pages/{page_id}/conversations?access_token={token}`

2. **`get_messages`**
   - Input: `{ conversation_id: string, since?: ISO date, limit?: number }`
   - Output: list messages (sender_name, content, timestamp, attachments)
   - Endpoint: `GET https://pages.fm/api/public_api/v1/pages/{page_id}/conversations/{conversation_id}/messages?access_token={token}`

3. **`search_messages`** (nâng cao, optional v1.1)
   - Search tin nhắn theo keyword trong tất cả hoặc 1 nhóm cụ thể.

4. **`summarize_conversation`** (option)
   - Shortcut: gọi `get_messages` với `since` là X ngày trước, trả kết quả dạng tóm tắt sẵn.

### Use case Claude sẽ hỗ trợ (qua tools này)

- *"Check nhóm nhân viên 3 ngày qua có vấn đề gì cần xử lý không"*
- *"Có khách phàn nàn gì trong nhóm VIP tuần này không"*
- *"Liệt kê các câu hỏi chưa được trả lời trong nhóm X"*
- *"Nhóm nào hôm nay có nhiều tin nhắn nhất"*

Claude (trong chat) sẽ:
1. Gọi `list_conversations` để lấy danh sách nhóm
2. Gọi `get_messages` cho các nhóm relevant với query của user
3. Phân tích tin nhắn → tóm tắt các vấn đề cần xử lý

### Cấu trúc `.mcpb`

```
weca-pancake/
├── manifest.json               # MCPB manifest — xem spec
├── server.js                   # MCP server chính (Node.js)
├── package.json
├── README.md                   # hướng dẫn cài đặt
└── icon.png (optional)
```

### manifest.json template (quan trọng)

```json
{
  "manifest_version": "0.2",
  "name": "weca-pancake",
  "display_name": "WECA Pancake Zalo Monitor",
  "version": "1.0.0",
  "description": "Theo dõi và phân tích tin nhắn từ các nhóm Zalo của Pancake",
  "long_description": "...",
  "author": {
    "name": "Techla"
  },
  "license": "Xem LICENSE.md",
  "server": {
    "type": "node",
    "entry_point": "server.js",
    "mcp_config": {
      "command": "node",
      "args": ["${__dirname}/server.js"],
      "env": {
        "PANCAKE_API_KEY": "${user_config.pancake_api_key}",
        "PANCAKE_PAGE_ID": "${user_config.pancake_page_id}"
      }
    }
  },
  "user_config": {
    "pancake_api_key": {
      "type": "string",
      "title": "Pancake API Key",
      "description": "Lấy từ Pancake admin → Cấu hình → Webhook-API",
      "sensitive": true,
      "required": true
    },
    "pancake_page_id": {
      "type": "string",
      "title": "Page ID (Zalo cá nhân)",
      "description": "ID 7 chữ số của page Zalo cá nhân trong URL admin Pancake",
      "required": true
    }
  },
  "compatibility": {
    "claude_desktop": ">=0.10.0",
    "platforms": ["darwin", "win32"],
    "runtimes": {
      "node": ">=18.0.0"
    }
  }
}
```

### server.js template

```javascript
#!/usr/bin/env node
/**
 * WECA Pancake MCP Server
 * Author: Techla
 * License: Xem LICENSE.md
 */

const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { CallToolRequestSchema, ListToolsRequestSchema } = require("@modelcontextprotocol/sdk/types.js");

const API_KEY = process.env.PANCAKE_API_KEY;
const PAGE_ID = process.env.PANCAKE_PAGE_ID;
const BASE_URL = "https://pages.fm/api/public_api/v1";

// Implement list_conversations, get_messages, ...
// Dùng fetch (Node 18+ có sẵn)
// Handle errors gracefully — trả về message tiếng Việt rõ ràng
```

### Error handling

Tool nào cũng phải:
- Validate input (conversation_id format, limit range)
- Bắt lỗi HTTP từ Pancake (401 = sai API key, 404 = page_id sai, 429 = rate limit)
- Trả về message tiếng Việt: *"Sai API key. Vui lòng kiểm tra lại trong Settings > Extensions > WECA Pancake."*
- Log stderr cho debug (Claude Desktop có log viewer)

### Files cần tạo

```
weca-pancake/ (source, sẽ đóng thành .mcpb)
├── manifest.json
├── server.js
├── package.json                 # deps: @modelcontextprotocol/sdk, ...
├── README.md                    # hướng dẫn cho khách
├── LICENSE.md
├── CHANGELOG.md
└── build.sh                     # script tạo .mcpb bundle
```

Để đóng gói thành `.mcpb`:
```bash
npm install -g @anthropic-ai/mcpb
cd weca-pancake/
mcpb pack
# → tạo weca-pancake-1.0.0.mcpb
```

---

## 6. Docs tổng của bundle (`docs/`)

Viết 5 file markdown tiếng Việt, dành cho end-user (không phải technical):

### `01-BAT-DAU-TAI-DAY.md`
Chào mừng, giới thiệu bundle có gì, thứ tự nên làm:
1. Cài Claude Desktop (link download)
2. Bật code execution trong settings
3. Cài 3 skill
4. Cài extension Pancake (optional — chỉ nếu dùng Zalo qua Pancake)
5. Xem file 04-SU-DUNG.md để biết cách hỏi Claude

### `02-CAI-SKILL.md`
Hướng dẫn cài từng file `.skill`:
- Settings → Skills → Upload
- Kéo file vào
- Bật toggle
- Screenshot từng bước (chị tự chèn sau — để placeholder)

### `03-CAI-EXTENSION-PANCAKE.md`
Hướng dẫn cài `.mcpb`:
- Lấy Pancake API key (Cấu hình → Webhook-API)
- Lấy page_id (từ URL admin)
- Double-click file `.mcpb`
- Nhập credentials khi được hỏi

### `04-SU-DUNG.md`
Ví dụ câu hỏi cho từng skill:
- **CSKH:** *"Phân tích file đơn hàng này"*, *"Khách nào sắp mất"*, *"Top 5 VIP"*
- **Research:** *"Research trend matcha 2026"*, *"So sánh bao bì Highlands và Phúc Long"*
- **Soạn VB:** *"Soạn hợp đồng thử việc cho Nguyễn A, 8tr, 2 tháng"*, *"Tạo biên bản bàn giao ca chiều 17/04"*
- **Pancake:** *"Check nhóm nhân viên 2 ngày qua có gì"*

### `05-HOI-DAP.md`
FAQ:
- File Excel của tôi không parse được — làm sao? → hướng dẫn kiểm tra format
- Pancake báo sai API key — làm sao? → vào Settings > Extensions chỉnh lại
- Skill không tự trigger — làm sao? → kiểm tra toggle đã bật, code execution đã bật
- Tôi muốn sửa report template — làm sao? → chỉ file template trong skill, sửa và re-upload
- Skill chạy trên mobile không? → không, chỉ Desktop + Web, riêng extension chỉ Desktop
- Có bảo hành không? → xem LICENSE.md

---

## 7. File tổng của bundle

### `README.md` (ngoài cùng)

- Giới thiệu bundle (1-2 đoạn)
- 4 skill có trong bundle (liệt kê ngắn, mỗi cái 1-2 dòng)
- Yêu cầu hệ thống (Claude Desktop, macOS/Windows, gói Free trở lên)
- Link đến `docs/01-BAT-DAU-TAI-DAY.md` để bắt đầu
- Copyright Techla 2026

### `LICENSE.md` (ngoài cùng)

Điều khoản chung cho cả bundle (mỗi skill có LICENSE.md riêng bên trong, giống hệt):

- **Được phép:** sử dụng, phân phối lại, chỉnh sửa code
- **Cần làm:** giữ credit Techla trong SKILL.md, footer báo cáo, mọi file docs
- **Không được:** xóa credit, ghi tên khác làm tác giả gốc
- **Miễn trừ:** không bảo hành, Techla không chịu trách nhiệm cho quyết định kinh doanh dựa trên output của skill

### `CHANGELOG.md`

```
## v1.0.0 — <ngày build>
Phiên bản đầu tiên, gồm 4 module: CSKH / Research / Soạn VB / Pancake Extension.
```

---

## 8. Packaging

Sau khi build xong source code của 4 skill:

### Tạo các file `.skill`

Mỗi `.skill` = zip của folder skill đó:

```bash
cd cskh-phan-tich-don-hang/
zip -r ../cskh-phan-tich-don-hang.skill . -x "*.pyc" "__pycache__/*"
```

### Tạo file `.mcpb`

```bash
cd weca-pancake/
npm install
mcpb pack
# output: weca-pancake-1.0.0.mcpb
```

### Zip tổng bundle

```bash
WECA-Business-Skills-v1.0.0/
  skills/*.skill
  extensions/*.mcpb
  docs/*.md
  samples/*.xlsx
  README.md, LICENSE.md, CHANGELOG.md

zip -r WECA-Business-Skills-v1.0.0.zip WECA-Business-Skills-v1.0.0/
```

---

## 9. Testing checklist

### Skill 1 (CSKH)
- [ ] Parser WECA đọc được file có 3 sheet
- [ ] Parser tự forward-fill thông tin KH (merge cells)
- [ ] Parse đúng cả 3 format ngày trong cột tháng (datetime / "2;23" / "01,17/04")
- [ ] Parser standard đọc được file có header Vietnamese và English
- [ ] Analyzer trigger churn warning đúng (test case: KH đặt đều 10 ngày/lần, lần cuối 20 ngày trước)
- [ ] Report .docx mở được trong MS Word và Google Docs, không vỡ layout
- [ ] Report .md render đúng bảng trên GitHub
- [ ] Footer Techla xuất hiện ở cuối cả 2 format

### Skill 3b (Soạn VB)
- [ ] Tạo được cả 3 loại văn bản
- [ ] Số tiền có viết bằng chữ
- [ ] Văn phong đúng kiểu hành chính VN

### Skill 2 (Research)
- [ ] Output `.md` paraphrase toàn bộ, không có chuỗi > 15 từ giống nguồn
- [ ] Cite đầy đủ nguồn
- [ ] `.docx` xuất ra cùng nội dung
- [ ] Convert sang `.pptx` chạy được (nếu có Marp)

### Skill 3a (Pancake)
- [ ] `.mcpb` install được trong Claude Desktop
- [ ] Config screen hiện đúng 2 field (API key + page_id)
- [ ] `list_conversations` trả về danh sách nhóm (test với API key thật)
- [ ] `get_messages` trả đúng tin nhắn
- [ ] Error handling hiển thị message tiếng Việt rõ ràng

---

## 10. Những cạm bẫy đã biết — tránh từ đầu

1. **Classify sheet WECA sai:** sheet "Lịch sử chăm sóc" cũng có "MÃ KH" nên dễ bị nhầm là sheet chính. Phải check hints care **trước** main.

2. **Format ngày đa dạng trong cột tháng:** đừng chỉ handle datetime object — phải handle cả string `"2;23/2"`, `"01,17/04"`, integer đơn thuần, và trường hợp suffix `/MM` override tháng cột.

3. **Merge cells ở file WECA:** dòng 2, 3, 4... của cùng 1 KH không có ma_kh / ten_kh / sdt / dia_chi (vì merge). Phải forward-fill.

4. **openpyxl đọc merged cells:** chỉ ô trên-trái có value, các ô khác trong vùng merge trả None. Đây là expected behavior, không fix bằng `iter_merged_cells` mà fix bằng forward-fill ở tầng parser.

5. **Python-docx default page size là A4** — không cần set lại vì Việt Nam dùng A4. Nhưng phải set margin thủ công (2cm), không dùng default.

6. **python-docx emoji không render nice trong MS Word cũ** — OK, vẫn giữ emoji trong heading (📊 ⚠️ 👑...) vì bản Word mới đã hỗ trợ.

7. **Pancake API có rate limit** — gọi `get_messages` nhiều cuộc hội thoại cùng lúc có thể bị 429. Implement retry với exponential backoff trong MCP server.

8. **MCP server stdin/stdout:** phải dùng stderr để log (stdout dành cho protocol). Print debug ra console.error(), không console.log().

9. **Marp không có sẵn trong Claude sandbox** — fallback dùng python-pptx tự gen slide từ parsing markdown.

10. **`.mcpb` file extension mới** — trước là `.dxt`. Claude Desktop hỗ trợ cả hai nhưng nên dùng `.mcpb` cho version mới.

---

## 11. Quy tắc làm việc cho Claude Code

Khi build:

- **Test từng bước**. Sau mỗi file code quan trọng, chạy thử với sample data trước khi sang file tiếp.
- **Hỏi nếu thiếu thông tin**, không đoán. Nếu đoán, note rõ "tôi đang giả định X, nếu sai cho tôi biết."
- **Không over-engineer**. Skill này bán đứt cho chủ quán cafe, code cần đơn giản để dễ debug khi khách báo lỗi. Tránh metaclass, decorator phức tạp, dependency hiếm.
- **Viết comment tiếng Việt** cho phần business logic. Code structure/parameter name dùng tiếng Anh như thông thường.
- **Every single script** phải có:
  - Docstring ở đầu file (mô tả + author + license + version)
  - argparse nếu là script chạy standalone
  - Error message tiếng Việt khi raise cho end user

---

## 12. Khi nào báo cáo tôi

Claude Code báo tiến độ sau mỗi milestone:

1. ✅ Skill 1 — CSKH: build xong + test pass sample + test pass file WECA thật (nếu user có đưa)
2. ✅ Skill 3b — Soạn VB: build xong + 3 loại văn bản tạo được
3. ✅ Skill 2 — Research: build xong + chạy thử 1 chủ đề
4. ✅ Skill 3a — Pancake: `.mcpb` build xong (chưa test end-to-end cần API key)
5. ✅ Docs + samples + bundle zip cuối cùng

Mỗi milestone cần:
- Path đến file đã tạo
- Output demo (nếu có)
- Vấn đề gặp phải (nếu có)

---

## 13. Tài nguyên tham khảo

- **MCPB spec:** https://github.com/modelcontextprotocol/mcpb
- **Claude Desktop Extensions:** https://support.claude.com/en/articles/10949351
- **Pancake API:** https://developer.pancake.biz/
- **Pancake docs:** https://docs.pancake.vn/thai-new/developers/api-reference
- **Claude Skills:** https://support.claude.com/en/articles/12512180
- **Marp:** https://marp.app/
- **python-docx:** https://python-docx.readthedocs.io/
- **MCP SDK (Node):** https://www.npmjs.com/package/@modelcontextprotocol/sdk

---

Hết spec. Chúc build ngon miệng.
