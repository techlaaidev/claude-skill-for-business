"""
Format số kiểu Việt Nam.
Author: Techla — v1.0.0 — License: xem LICENSE.md
"""
from __future__ import annotations
from typing import Optional


def format_money(value: Optional[float]) -> str:
    """1234567 -> '1.234.567đ'. None/0 -> '0đ'."""
    if value is None:
        return "0đ"
    v = int(round(value))
    s = f"{abs(v):,}".replace(",", ".")
    return f"-{s}đ" if v < 0 else f"{s}đ"


def format_int(value: Optional[float]) -> str:
    """1234 -> '1.234'."""
    if value is None:
        return "0"
    v = int(round(value))
    s = f"{abs(v):,}".replace(",", ".")
    return f"-{s}" if v < 0 else s


def format_float(value: Optional[float], decimals: int = 1) -> str:
    """1234.5 -> '1.234,5' — chấm ngàn, phẩy thập phân."""
    if value is None:
        return "0"
    fmt = f"{{:,.{decimals}f}}".format(value)
    # swap separators: US (1,234.5) -> VN (1.234,5)
    return fmt.replace(",", "X").replace(".", ",").replace("X", ".")


def format_percent(value: Optional[float], decimals: int = 1) -> str:
    """0.123 -> '+12,3%'. Nhận giá trị đã tính % (vd 12.3), có dấu + nếu dương."""
    if value is None:
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{format_float(value, decimals)}%"


def money_to_words_vi(value: float) -> str:
    """Viết số tiền bằng chữ tiếng Việt, trả 'Tám triệu đồng chẵn' kiểu.
    Hỗ trợ đến hàng tỷ. Dùng cho hợp đồng / văn bản hành chính."""
    v = int(round(value))
    if v == 0:
        return "Không đồng"
    if v < 0:
        return "Âm " + money_to_words_vi(-v).lower()

    digits = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

    def read_triple(n: int, full: bool) -> str:
        """Đọc 1 nhóm 3 số. full=True => luôn đọc trăm (kể cả 0)."""
        h, t, u = n // 100, (n // 10) % 10, n % 10
        parts = []
        if h > 0 or full:
            parts.append(f"{digits[h]} trăm")
        if t == 0 and u > 0 and (h > 0 or full):
            parts.append("lẻ " + digits[u])
        elif t == 1:
            parts.append("mười" + ("" if u == 0 else (" một" if u == 1 else (" lăm" if u == 5 else f" {digits[u]}"))))
        elif t > 1:
            tens = f"{digits[t]} mươi"
            if u == 1:
                tens += " mốt"
            elif u == 5:
                tens += " lăm"
            elif u > 0:
                tens += f" {digits[u]}"
            parts.append(tens)
        elif u > 0 and not (h > 0 or full):
            parts.append(digits[u])
        return " ".join(parts).strip()

    billion = v // 1_000_000_000
    million = (v // 1_000_000) % 1000
    thousand = (v // 1000) % 1000
    unit = v % 1000

    chunks = []
    if billion > 0:
        chunks.append(read_triple(billion, full=False) + " tỷ")
    if million > 0:
        chunks.append(read_triple(million, full=billion > 0) + " triệu")
    if thousand > 0:
        chunks.append(read_triple(thousand, full=(billion > 0 or million > 0)) + " nghìn")
    if unit > 0:
        chunks.append(read_triple(unit, full=(billion > 0 or million > 0 or thousand > 0)))

    words = " ".join(chunks).strip()
    # Capitalize first letter
    words = words[0].upper() + words[1:]
    return f"{words} đồng chẵn"


if __name__ == "__main__":
    # Quick sanity check
    assert format_money(1234567) == "1.234.567đ"
    assert format_int(1234) == "1.234"
    assert format_float(1234.5) == "1.234,5"
    assert format_percent(12.3) == "+12,3%"
    assert format_percent(-5.0) == "-5,0%"
    print("OK:", format_money(1234567), "|", format_float(1234.56, 2), "|", format_percent(12.34))
    print("Money to words:", money_to_words_vi(8_000_000))
    print("Money to words:", money_to_words_vi(12_500_000))
    print("Money to words:", money_to_words_vi(1_050_000))
