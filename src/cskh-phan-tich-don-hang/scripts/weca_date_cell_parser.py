"""
Parse ô trong cột tháng của file WECA.
Author: Techla — v1.0.0 — License: xem LICENSE.md

Cell có thể là:
- datetime object (Excel) -> 1 ngày
- int đơn thuần "17" -> ngày 17 của tháng cột
- string "2;23/2" -> ngày 2 và 23 tháng 2
- string "01,17/04" -> ngày 1 và 17 tháng 4
- string "17/04" -> ngày 17 tháng 4 (có suffix override)
- None -> []
"""
from __future__ import annotations
from datetime import datetime, date
import re
import calendar


def parse_month_cell(value, col_month: int, col_year: int) -> list[str]:
    """Trả list ISO dates 'YYYY-MM-DD' parse được từ 1 cell.

    col_month/col_year: tháng + năm của cột này (để fallback khi value không ghi tháng)
    """
    if value is None or value == "":
        return []
    # datetime object
    if isinstance(value, datetime):
        return [value.date().isoformat()]
    if isinstance(value, date):
        return [value.isoformat()]
    # integer -> ngày trong tháng cột
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        day = int(value)
        return [_iso(col_year, col_month, day)] if 1 <= day <= 31 else []

    s = str(value).strip()
    if not s:
        return []

    # Nếu string kiểu '17/04/2026' hoặc '17-04-2026' (full date)
    full_match = re.fullmatch(r"(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})", s)
    if full_match:
        d, m, y = map(int, full_match.groups())
        if y < 100:
            y += 2000
        iso = _iso(y, m, d)
        return [iso] if iso else []

    # Tách thành các token bởi ',' hoặc ';'
    tokens = [t.strip() for t in re.split(r"[;,]", s) if t.strip()]
    if not tokens:
        return []

    # Tìm suffix override tháng — token cuối dạng "d/m" hoặc "d/mm"
    # Quy tắc: suffix áp dụng cho tất cả token trước đó nếu chúng là số đơn
    # vd "2;23/2" -> ngày 2 tháng 2 và ngày 23 tháng 2
    #     "01,17/04" -> ngày 1 và 17 tháng 4
    override_month = None
    last = tokens[-1]
    suffix_match = re.match(r"(\d{1,2})\s*[/\-.]\s*(\d{1,2})$", last)
    if suffix_match:
        d_last, m_override = map(int, suffix_match.groups())
        override_month = m_override
        # Token cuối đã có thông tin đầy đủ; xử lý đặc biệt
        tokens[-1] = str(d_last)

    out = []
    month_to_use = override_month if override_month else col_month
    for tok in tokens:
        # Token có thể dạng "17/04" bản thân nó
        inner = re.match(r"^(\d{1,2})\s*[/\-.]\s*(\d{1,2})$", tok)
        if inner:
            d_val, m_val = map(int, inner.groups())
            iso = _iso(col_year, m_val, d_val)
            if iso:
                out.append(iso)
            continue
        # Token chỉ số
        if tok.isdigit():
            d_val = int(tok)
            iso = _iso(col_year, month_to_use, d_val)
            if iso:
                out.append(iso)

    return out


def _iso(year: int, month: int, day: int) -> str | None:
    """Format thành ISO, trả None nếu invalid."""
    if not (1 <= month <= 12):
        return None
    try:
        last_day = calendar.monthrange(year, month)[1]
    except Exception:
        return None
    if not (1 <= day <= last_day):
        return None
    return f"{year:04d}-{month:02d}-{day:02d}"


def parse_column_header_to_month(header) -> tuple[int, int] | None:
    """Parse header cột tháng như '01/26', '1/26', 'T01/26', '01.2026' -> (month, year)."""
    if header is None:
        return None
    if isinstance(header, datetime):
        return (header.month, header.year)
    s = str(header).strip().upper().replace("T", "")
    m = re.match(r"(\d{1,2})\s*[/.\-]\s*(\d{2,4})$", s)
    if not m:
        return None
    month, year = int(m.group(1)), int(m.group(2))
    if year < 100:
        year += 2000
    if 1 <= month <= 12:
        return (month, year)
    return None


if __name__ == "__main__":
    # Sanity tests
    from datetime import datetime as dt
    assert parse_month_cell(dt(2026, 1, 22), 1, 2026) == ["2026-01-22"]
    assert parse_month_cell(17, 3, 2026) == ["2026-03-17"]
    assert parse_month_cell("2;23/2", 2, 2026) == ["2026-02-02", "2026-02-23"]
    assert parse_month_cell("01,17/04", 4, 2026) == ["2026-04-01", "2026-04-17"]
    assert parse_month_cell("17/04", 4, 2026) == ["2026-04-17"]
    assert parse_month_cell(None, 1, 2026) == []
    assert parse_column_header_to_month("01/26") == (1, 2026)
    assert parse_column_header_to_month("T04/26") == (4, 2026)
    assert parse_column_header_to_month("12/2026") == (12, 2026)
    print("weca_date_cell_parser OK")
