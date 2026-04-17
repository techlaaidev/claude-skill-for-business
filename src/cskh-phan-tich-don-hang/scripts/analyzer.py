"""
Analyzer: tính 11 metrics từ ParsedData -> analysis.json.
Author: Techla — v1.0.0 — License: xem LICENSE.md

Usage:
    python scripts/analyzer.py parsed.json --output analysis.json [--config config.yaml]
"""
from __future__ import annotations
import os
import sys
import json
import math
import argparse
from pathlib import Path
from datetime import datetime, date
from collections import defaultdict
from itertools import combinations

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from schema import ParsedData, now_iso

try:
    import yaml
except ImportError:
    yaml = None


DEFAULT_CONFIG = {
    "churn_threshold_multiplier": 1.5,
    "vip_top_n": 10,
    "dead_product_days": 90,
    "enable_basket_analysis": True,
    "reference_date": None,            # None -> dùng max order_date
    "min_orders_for_rhythm": 2,
    "decreasing_rhythm_threshold": 0.4,  # 40% giảm
    "decreasing_rhythm_min_orders": 4,
}


def load_config(path: str | None) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    if path and Path(path).exists() and yaml is not None:
        with open(path, "r", encoding="utf-8") as f:
            user = yaml.safe_load(f) or {}
        cfg.update({k: v for k, v in user.items() if k in DEFAULT_CONFIG})
    return cfg


def _iso_to_date(s: str) -> date:
    return date.fromisoformat(s)


def _vn_month_key(iso_date: str) -> str:
    """'2026-04-17' -> 'T4/2026'."""
    d = _iso_to_date(iso_date)
    return f"T{d.month}/{d.year}"


def analyze(parsed: ParsedData, cfg: dict) -> dict:
    customers_by_id = {c.customer_id: c for c in parsed.customers}
    products_by_id = {p.product_id: p for p in parsed.products}
    orders = parsed.orders

    if not orders:
        return _empty_result(parsed, cfg)

    # Reference date
    if cfg["reference_date"]:
        ref_date = _iso_to_date(cfg["reference_date"])
    else:
        ref_date = max(_iso_to_date(o.order_date) for o in orders)

    # ------- (1) Tổng quan -------
    overview = _overview(orders, parsed, ref_date)

    # ------- (2) Theo tháng -------
    monthly = _monthly_stats(orders)

    # ------- (3) MoM -------
    mom = _mom_compare(monthly)

    # ------- (4) VIP -------
    vip = _top_vip(orders, customers_by_id, cfg["vip_top_n"])

    # ------- (5) Churn -------
    churn = _churn_warnings(orders, customers_by_id, ref_date, cfg)

    # ------- (6) Decreasing rhythm -------
    decreasing = _decreasing_rhythm(orders, customers_by_id, cfg)

    # ------- (7) Star products -------
    stars = _star_products(orders, products_by_id)

    # ------- (8) Dead products -------
    dead = _dead_products(orders, products_by_id, ref_date, cfg)

    # ------- (9) Cross-sell opportunities -------
    cross_sell = _cross_sell(customers_by_id)

    # ------- (10) Basket analysis -------
    basket = []
    if cfg.get("enable_basket_analysis", True):
        basket = _basket_pairs(orders, products_by_id, top_n=10)

    # ------- (11) Action list -------
    actions = _action_list(churn, decreasing, cross_sell, vip)

    return {
        "generated_at": now_iso(),
        "source_file": parsed.source_file,
        "format": parsed.format,
        "reference_date": ref_date.isoformat(),
        "config_used": cfg,
        "overview": overview,
        "monthly": monthly,
        "mom_compare": mom,
        "top_vip": vip,
        "churn_warnings": churn,
        "decreasing_rhythm": decreasing,
        "star_products": stars,
        "dead_products": dead,
        "cross_sell_opportunities": cross_sell,
        "basket_pairs": basket,
        "action_list": actions,
    }


def _empty_result(parsed: ParsedData, cfg: dict) -> dict:
    return {
        "generated_at": now_iso(),
        "source_file": parsed.source_file,
        "format": parsed.format,
        "reference_date": None,
        "config_used": cfg,
        "overview": {"total_customers": 0, "total_products": 0, "total_orders": 0,
                     "total_qty": 0, "total_revenue": 0, "period_start": None, "period_end": None},
        "monthly": [], "mom_compare": None, "top_vip": [], "churn_warnings": [],
        "decreasing_rhythm": [], "star_products": [], "dead_products": [],
        "cross_sell_opportunities": [], "basket_pairs": [], "action_list": [],
    }


def _overview(orders, parsed, ref_date):
    dates = [_iso_to_date(o.order_date) for o in orders]
    total_rev = sum(o.estimated_revenue or 0 for o in orders)
    total_qty = sum(o.qty or 0 for o in orders)
    return {
        "total_customers": len(parsed.customers),
        "total_products": len(parsed.products),
        "total_orders": len(orders),
        "total_qty": total_qty,
        "total_revenue": total_rev,
        "period_start": min(dates).isoformat(),
        "period_end": max(dates).isoformat(),
        "reference_date": ref_date.isoformat(),
    }


def _monthly_stats(orders):
    """List dict cho từng tháng (sort theo time)."""
    by_month: dict[str, dict] = defaultdict(lambda: {
        "orders": 0, "qty": 0.0, "revenue": 0.0, "customers": set()
    })
    for o in orders:
        key = _vn_month_key(o.order_date)
        d = _iso_to_date(o.order_date)
        by_month[key]["orders"] += 1
        by_month[key]["qty"] += o.qty or 0
        by_month[key]["revenue"] += o.estimated_revenue or 0
        by_month[key]["customers"].add(o.customer_id)
        by_month[key]["_sort"] = (d.year, d.month)

    rows = []
    for k, v in by_month.items():
        rows.append({
            "month": k,
            "sort_key": v["_sort"],
            "orders": v["orders"],
            "qty": v["qty"],
            "revenue": v["revenue"],
            "unique_customers": len(v["customers"]),
        })
    rows.sort(key=lambda r: r["sort_key"])
    for r in rows:
        r.pop("sort_key")
    return rows


def _mom_compare(monthly):
    if len(monthly) < 2:
        return None
    cur, prev = monthly[-1], monthly[-2]
    def pct(a, b):
        if b == 0:
            return None
        return (a - b) / b * 100
    return {
        "current_month": cur["month"],
        "previous_month": prev["month"],
        "orders_change_pct": pct(cur["orders"], prev["orders"]),
        "revenue_change_pct": pct(cur["revenue"], prev["revenue"]),
        "customers_change_pct": pct(cur["unique_customers"], prev["unique_customers"]),
        "qty_change_pct": pct(cur["qty"], prev["qty"]),
    }


def _top_vip(orders, customers_by_id, top_n):
    totals: dict[str, dict] = defaultdict(lambda: {"revenue": 0.0, "orders": 0, "qty": 0.0})
    for o in orders:
        t = totals[o.customer_id]
        t["revenue"] += o.estimated_revenue or 0
        t["orders"] += 1
        t["qty"] += o.qty or 0
    rows = []
    for cid, t in totals.items():
        c = customers_by_id.get(cid)
        if c is None:
            continue
        rows.append({
            "customer_id": cid,
            "name": c.name,
            "phone": c.phone,
            "total_revenue": t["revenue"],
            "total_orders": t["orders"],
            "total_qty": t["qty"],
        })
    rows.sort(key=lambda r: r["total_revenue"], reverse=True)
    return rows[:top_n]


def _avg_gap_days(dates: list[date]) -> float | None:
    if len(dates) < 2:
        return None
    dates = sorted(dates)
    gaps = [(dates[i + 1] - dates[i]).days for i in range(len(dates) - 1)]
    gaps = [g for g in gaps if g > 0]
    return sum(gaps) / len(gaps) if gaps else None


def _churn_warnings(orders, customers_by_id, ref_date, cfg):
    by_cust: dict[str, list] = defaultdict(list)
    revenues: dict[str, float] = defaultdict(float)
    for o in orders:
        by_cust[o.customer_id].append(_iso_to_date(o.order_date))
        revenues[o.customer_id] += o.estimated_revenue or 0

    mult = cfg["churn_threshold_multiplier"]
    out = []
    for cid, dates in by_cust.items():
        if len(dates) < max(2, cfg["min_orders_for_rhythm"]):
            continue
        avg_gap = _avg_gap_days(dates)
        if avg_gap is None or avg_gap <= 0:
            continue
        last_order = max(dates)
        days_since = (ref_date - last_order).days
        if days_since > avg_gap * mult:
            c = customers_by_id.get(cid)
            if c is None:
                continue
            out.append({
                "customer_id": cid,
                "name": c.name,
                "phone": c.phone,
                "last_order_date": last_order.isoformat(),
                "days_since_last_order": days_since,
                "avg_gap_days": round(avg_gap, 1),
                "total_revenue": revenues[cid],
                "care_history": c.care_history,
                "care_goal": c.care_goal,
            })
    out.sort(key=lambda r: r["total_revenue"], reverse=True)
    return out


def _decreasing_rhythm(orders, customers_by_id, cfg):
    by_cust_month: dict[str, dict[tuple, int]] = defaultdict(lambda: defaultdict(int))
    revenues: dict[str, float] = defaultdict(float)
    for o in orders:
        d = _iso_to_date(o.order_date)
        by_cust_month[o.customer_id][(d.year, d.month)] += 1
        revenues[o.customer_id] += o.estimated_revenue or 0

    threshold = cfg["decreasing_rhythm_threshold"]
    min_orders = cfg["decreasing_rhythm_min_orders"]

    out = []
    for cid, months in by_cust_month.items():
        total = sum(months.values())
        if total < min_orders:
            continue
        sorted_months = sorted(months.items())
        if len(sorted_months) < 2:
            continue
        last_month, last_count = sorted_months[-1]
        prev_months = sorted_months[:-1]
        prev_avg = sum(cnt for _, cnt in prev_months) / len(prev_months)
        if prev_avg == 0:
            continue
        drop = (prev_avg - last_count) / prev_avg
        if drop > threshold:
            c = customers_by_id.get(cid)
            if c is None:
                continue
            out.append({
                "customer_id": cid,
                "name": c.name,
                "phone": c.phone,
                "prev_avg_orders_per_month": round(prev_avg, 1),
                "last_month": f"T{last_month[1]}/{last_month[0]}",
                "last_month_orders": last_count,
                "drop_pct": round(drop * 100, 1),
                "total_revenue": revenues[cid],
            })
    out.sort(key=lambda r: r["total_revenue"], reverse=True)
    return out


def _star_products(orders, products_by_id):
    by_prod: dict[str, dict] = defaultdict(lambda: {"revenue": 0.0, "qty": 0.0, "customers": set(), "orders": 0})
    for o in orders:
        t = by_prod[o.product_id]
        t["revenue"] += o.estimated_revenue or 0
        t["qty"] += o.qty or 0
        t["orders"] += 1
        t["customers"].add(o.customer_id)

    rows = []
    for pid, t in by_prod.items():
        p = products_by_id.get(pid)
        if p is None:
            continue
        unique_cust = len(t["customers"])
        score = t["revenue"] * math.log(1 + unique_cust)
        rows.append({
            "product_id": pid,
            "name": p.name,
            "revenue": t["revenue"],
            "qty": t["qty"],
            "orders": t["orders"],
            "unique_customers": unique_cust,
            "score": score,
        })
    rows.sort(key=lambda r: r["score"], reverse=True)
    return rows[:10]


def _dead_products(orders, products_by_id, ref_date, cfg):
    last_order_by_prod: dict[str, date] = {}
    for o in orders:
        d = _iso_to_date(o.order_date)
        last_order_by_prod[o.product_id] = max(last_order_by_prod.get(o.product_id, d), d)

    threshold = cfg["dead_product_days"]
    out = []
    for pid, p in products_by_id.items():
        last = last_order_by_prod.get(pid)
        if last is None:
            out.append({
                "product_id": pid,
                "name": p.name,
                "last_order_date": None,
                "days_since_last_order": None,
                "reason": "Không có đơn nào trong khoảng thời gian dữ liệu.",
            })
            continue
        days = (ref_date - last).days
        if days > threshold:
            out.append({
                "product_id": pid,
                "name": p.name,
                "last_order_date": last.isoformat(),
                "days_since_last_order": days,
                "reason": f"Đơn cuối cách {days} ngày (ngưỡng {threshold}).",
            })
    return out


def _cross_sell(customers_by_id):
    out = []
    for c in customers_by_id.values():
        if c.opportunity or c.action_needed:
            out.append({
                "customer_id": c.customer_id,
                "name": c.name,
                "phone": c.phone,
                "opportunity": c.opportunity,
                "action_needed": c.action_needed,
                "status": c.status,
            })
    return out


def _basket_pairs(orders, products_by_id, top_n=10):
    by_day: dict[tuple, set] = defaultdict(set)
    for o in orders:
        by_day[(o.customer_id, o.order_date)].add(o.product_id)

    pair_count: dict[tuple, int] = defaultdict(int)
    for prods in by_day.values():
        if len(prods) < 2:
            continue
        for a, b in combinations(sorted(prods), 2):
            pair_count[(a, b)] += 1

    rows = []
    for (a, b), count in pair_count.items():
        pa = products_by_id.get(a)
        pb = products_by_id.get(b)
        rows.append({
            "product_a_id": a, "product_a_name": pa.name if pa else a,
            "product_b_id": b, "product_b_name": pb.name if pb else b,
            "count": count,
        })
    rows.sort(key=lambda r: r["count"], reverse=True)
    return rows[:top_n]


def _action_list(churn, decreasing, cross_sell, vip):
    vip_ids = {v["customer_id"] for v in vip[:5]}
    out = []
    for c in churn:
        priority = "CAO" if c["customer_id"] in vip_ids else "TRUNG BÌNH"
        out.append({
            "priority": priority,
            "type": "Churn",
            "customer": c["name"],
            "phone": c.get("phone"),
            "detail": f"Không đặt {c['days_since_last_order']} ngày (nhịp TB {c['avg_gap_days']} ngày).",
            "care_hint": c.get("care_history") or c.get("care_goal"),
        })
    for d in decreasing:
        out.append({
            "priority": "TRUNG BÌNH",
            "type": "Giảm nhịp",
            "customer": d["name"],
            "phone": d.get("phone"),
            "detail": f"Tháng {d['last_month']} chỉ có {d['last_month_orders']} đơn (TB trước đó {d['prev_avg_orders_per_month']}, giảm {d['drop_pct']}%).",
            "care_hint": None,
        })
    for x in cross_sell:
        out.append({
            "priority": "THẤP",
            "type": "Cross-sell",
            "customer": x["name"],
            "phone": x.get("phone"),
            "detail": x.get("opportunity") or x.get("action_needed"),
            "care_hint": x.get("action_needed"),
        })
    priority_order = {"CAO": 0, "TRUNG BÌNH": 1, "THẤP": 2}
    out.sort(key=lambda a: priority_order.get(a["priority"], 99))
    return out


def main():
    ap = argparse.ArgumentParser(description="Analyzer: parsed.json -> analysis.json.")
    ap.add_argument("input", help="File parsed.json")
    ap.add_argument("--output", "-o", default="analysis.json")
    ap.add_argument("--config", "-c", default=None, help="config.yaml (optional)")
    args = ap.parse_args()

    if not Path(args.input).exists():
        print(f"Lỗi: không tìm thấy '{args.input}'.", file=sys.stderr)
        sys.exit(1)

    parsed = ParsedData.load_json(args.input)
    cfg = load_config(args.config)
    result = analyze(parsed, cfg)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)

    ov = result["overview"]
    print(f"OK: {ov['total_orders']} đơn, {ov['total_customers']} KH.")
    print(f"  Churn warnings: {len(result['churn_warnings'])}")
    print(f"  Decreasing:     {len(result['decreasing_rhythm'])}")
    print(f"  Dead products:  {len(result['dead_products'])}")
    print(f"  Cross-sell:     {len(result['cross_sell_opportunities'])}")
    print(f"  Basket pairs:   {len(result['basket_pairs'])}")
    print(f"  Actions:        {len(result['action_list'])}")
    print(f"Output: {args.output}")


if __name__ == "__main__":
    main()
