"""
Parser utilities chung cho WECA + standard.
Author: Techla — v1.0.0 — License: xem LICENSE.md
"""
from __future__ import annotations
import unicodedata
import re


def normalize_header(s: str) -> str:
    """Chuẩn hóa tên cột: lower, bỏ dấu tiếng Việt, strip space."""
    if s is None:
        return ""
    s = str(s).strip().lower()
    # NFD decompose rồi bỏ combining marks
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    s = s.replace("đ", "d").replace("Đ", "D")
    s = re.sub(r"\s+", " ", s)
    return s


def to_float(v) -> float | None:
    """Cast linh hoạt sang float. Chấp nhận '1.234.567', '1,234.56', '1.234,5'."""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip()
    if not s:
        return None
    # Bỏ ký tự tiền tệ
    s = s.replace("đ", "").replace("VND", "").replace("vnđ", "").replace("vnd", "").strip()
    # Quyết định dấu ngăn nghìn vs thập phân
    # Nếu có cả chấm và phẩy: cái nào xuất hiện CUỐI là thập phân
    has_dot = "." in s
    has_comma = "," in s
    if has_dot and has_comma:
        if s.rfind(",") > s.rfind("."):
            # VN style: 1.234,5
            s = s.replace(".", "").replace(",", ".")
        else:
            # US style: 1,234.5
            s = s.replace(",", "")
    elif has_comma:
        # Chỉ comma: có thể là thousand sep (1,234) hoặc decimal (1,5)
        # Nếu sau comma cuối có <=2 digit thì decimal
        after = s.split(",")[-1]
        if len(after) <= 2 and s.count(",") == 1:
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
    elif has_dot:
        # Chỉ dot: nếu nhiều dot là thousand sep
        if s.count(".") > 1:
            s = s.replace(".", "")
        else:
            after = s.split(".")[-1]
            if len(after) == 3 and len(s.replace(".", "")) > 3:
                # '1.234' -> 1234 (VN thousand sep)
                s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def safe_str(v) -> str | None:
    if v is None:
        return None
    s = str(v).strip()
    return s if s else None


# Column aliases cho standard format
STANDARD_ALIASES = {
    "date": [
        "ngay", "ngay dat", "ngay mua", "ngay ban", "date", "order date",
    ],
    "customer_name": [
        "ten khach", "khach hang", "ten khach hang", "customer", "customer name",
    ],
    "customer_id": [
        "ma kh", "ma khach hang", "customer id", "customer_id",
    ],
    "phone": [
        "sdt", "phone", "so dien thoai", "dien thoai",
    ],
    "product_name": [
        "san pham", "ten sp", "ten san pham", "mat hang", "product", "product name",
    ],
    "product_id": [
        "ma sp", "ma san pham", "product id", "product_id", "sku",
    ],
    "qty": [
        "so luong", "sl", "qty", "quantity", "so luong ban",
    ],
    "unit_price": [
        "don gia", "gia", "gia ban", "price", "unit price",
    ],
    "revenue": [
        "thanh tien", "doanh thu", "revenue", "total", "tong tien",
    ],
    "address": [
        "dia chi", "address",
    ],
}


def match_column(header_normalized: str, field: str) -> bool:
    """Check header có khớp 1 alias của field không."""
    aliases = STANDARD_ALIASES.get(field, [])
    for alias in aliases:
        if header_normalized == alias or alias in header_normalized:
            return True
    return False


def build_column_map(headers: list) -> dict[str, int]:
    """Map field chuẩn -> column index từ list headers thực tế.
    Ưu tiên match chính xác hơn là substring match."""
    normalized = [normalize_header(h) for h in headers]
    out: dict[str, int] = {}
    for field in STANDARD_ALIASES:
        # Pass 1: exact match
        for idx, h in enumerate(normalized):
            if h in STANDARD_ALIASES[field]:
                out[field] = idx
                break
        if field in out:
            continue
        # Pass 2: substring
        for idx, h in enumerate(normalized):
            if any(alias in h for alias in STANDARD_ALIASES[field]):
                out[field] = idx
                break
    return out
