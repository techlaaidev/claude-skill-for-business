"""
Build báo cáo dạng Markdown từ analysis.json.
Author: Techla — v1.0.0 — License: xem LICENSE.md
"""
from __future__ import annotations
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from vn_format import format_money, format_int, format_float, format_percent

FOOTER = "\n---\n\n*Báo cáo tạo bởi Techla — Skill CSKH Phân tích đơn hàng v1.0.0*\n"


def build_md(a: dict) -> str:
    out: list[str] = []
    out.append("# BÁO CÁO PHÂN TÍCH ĐƠN HÀNG & CHĂM SÓC KHÁCH HÀNG")
    out.append("")
    out.append(f"*Nguồn: {a.get('source_file', '-')} · Tạo lúc: {a['generated_at']}*")
    out.append(f"*Ngày tham chiếu: {a['reference_date']}*")
    out.append("")

    _section_overview(a, out)
    _section_churn(a, out)
    _section_vip(a, out)
    _section_cross_sell(a, out)
    _section_star(a, out)
    _section_dead(a, out)
    _section_mom(a, out)
    _section_monthly(a, out)
    _section_decreasing(a, out)
    if a["config_used"].get("enable_basket_analysis", True):
        _section_basket(a, out)
    _section_actions(a, out)

    out.append(FOOTER)
    return "\n".join(out)


def _section_overview(a, out):
    ov = a["overview"]
    out.append("## 1. Tóm tắt điều hành")
    out.append("")
    out.append("| Chỉ số | Giá trị |")
    out.append("|---|---|")
    out.append(f"| Khoảng thời gian | {ov['period_start']} → {ov['period_end']} |")
    out.append(f"| Tổng khách hàng | {format_int(ov['total_customers'])} |")
    out.append(f"| Tổng sản phẩm | {format_int(ov['total_products'])} |")
    out.append(f"| Tổng đơn hàng | {format_int(ov['total_orders'])} |")
    out.append(f"| Tổng số lượng | {format_float(ov['total_qty'])} |")
    out.append(f"| Doanh thu ước tính | {format_money(ov['total_revenue'])} |")
    out.append("")


def _section_churn(a, out):
    rows = a["churn_warnings"]
    out.append("## 2. ⚠️ Khách sắp mất")
    out.append("")
    if not rows:
        out.append("*Không có khách hàng nào có dấu hiệu churn.*")
        out.append("")
        return
    out.append("| Khách | SĐT | Đơn cuối | Đã lâu | Nhịp TB | Doanh thu | Gợi ý |")
    out.append("|---|---|---|---|---|---|---|")
    for r in rows:
        hint = (r.get("care_history") or r.get("care_goal") or "-").replace("\n", " ")
        out.append(
            f"| {r['name']} | {r.get('phone') or '-'} | {r['last_order_date']} | "
            f"{r['days_since_last_order']} ngày | {format_float(r['avg_gap_days'])} ngày | "
            f"{format_money(r['total_revenue'])} | {hint} |"
        )
    out.append("")


def _section_vip(a, out):
    rows = a["top_vip"]
    out.append("## 3. 👑 Top VIP")
    out.append("")
    if not rows:
        out.append("*Không có dữ liệu VIP.*"); out.append(""); return
    out.append("| # | Khách | SĐT | Doanh thu | Đơn | Số lượng |")
    out.append("|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        out.append(
            f"| {i} | {r['name']} | {r.get('phone') or '-'} | "
            f"{format_money(r['total_revenue'])} | {r['total_orders']} | {format_float(r['total_qty'])} |"
        )
    out.append("")


def _section_cross_sell(a, out):
    rows = a["cross_sell_opportunities"]
    out.append("## 4. 💡 Cơ hội bán thêm")
    out.append("")
    if not rows:
        out.append("*Chưa có ghi chú cơ hội nào.*"); out.append(""); return
    for r in rows:
        out.append(f"- **{r['name']}** — {r.get('phone') or '-'}")
        if r.get("opportunity"):
            out.append(f"  - Cơ hội: {r['opportunity']}")
        if r.get("action_needed"):
            out.append(f"  - Cần làm: {r['action_needed']}")
    out.append("")


def _section_star(a, out):
    rows = a["star_products"]
    out.append("## 5. ⭐ Sản phẩm ngôi sao")
    out.append("")
    if not rows:
        out.append("*Không có dữ liệu.*"); out.append(""); return
    out.append("| # | SP | Doanh thu | Đơn | KH mua | SL |")
    out.append("|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        out.append(
            f"| {i} | {r['name']} | {format_money(r['revenue'])} | "
            f"{r['orders']} | {r['unique_customers']} | {format_float(r['qty'])} |"
        )
    out.append("")


def _section_dead(a, out):
    rows = a["dead_products"]
    out.append("## 6. 💀 Sản phẩm xác sống")
    out.append("")
    if not rows:
        out.append("*Không có sản phẩm xác sống.*"); out.append(""); return
    out.append("| SP | Đơn cuối | Lý do |")
    out.append("|---|---|---|")
    for r in rows:
        out.append(f"| {r['name']} | {r['last_order_date'] or '-'} | {r['reason']} |")
    out.append("")


def _section_mom(a, out):
    mom = a["mom_compare"]
    out.append("## 7. 📊 So sánh MoM")
    out.append("")
    if not mom:
        out.append("*Chỉ có dữ liệu 1 tháng — không tính được MoM.*"); out.append(""); return
    out.append(f"So sánh **{mom['current_month']}** với **{mom['previous_month']}**:")
    out.append("")
    out.append(f"- Đơn hàng: {format_percent(mom['orders_change_pct'])}")
    out.append(f"- Doanh thu: {format_percent(mom['revenue_change_pct'])}")
    out.append(f"- Khách: {format_percent(mom['customers_change_pct'])}")
    out.append(f"- Số lượng: {format_percent(mom['qty_change_pct'])}")
    out.append("")


def _section_monthly(a, out):
    rows = a["monthly"]
    out.append("## 8. 📅 Chi tiết theo tháng")
    out.append("")
    if not rows:
        out.append("*Không có dữ liệu.*"); out.append(""); return
    out.append("| Tháng | Đơn | Số lượng | Doanh thu | KH duy nhất |")
    out.append("|---|---|---|---|---|")
    for r in rows:
        out.append(
            f"| {r['month']} | {r['orders']} | {format_float(r['qty'])} | "
            f"{format_money(r['revenue'])} | {r['unique_customers']} |"
        )
    out.append("")


def _section_decreasing(a, out):
    rows = a["decreasing_rhythm"]
    out.append("## 9. 📉 Khách giảm nhịp")
    out.append("")
    if not rows:
        out.append("*Không có khách nào giảm nhịp đột ngột.*"); out.append(""); return
    out.append("| Khách | SĐT | Tháng cuối | Đơn tháng cuối | TB trước đó | % giảm | Doanh thu |")
    out.append("|---|---|---|---|---|---|---|")
    for r in rows:
        out.append(
            f"| {r['name']} | {r.get('phone') or '-'} | {r['last_month']} | "
            f"{r['last_month_orders']} | {format_float(r['prev_avg_orders_per_month'])} | "
            f"-{format_float(r['drop_pct'])}% | {format_money(r['total_revenue'])} |"
        )
    out.append("")


def _section_basket(a, out):
    rows = a["basket_pairs"]
    out.append("## 10. 🛒 Cặp SP hay mua cùng")
    out.append("")
    if not rows:
        out.append("*Không tìm thấy cặp SP mua chung.*"); out.append(""); return
    out.append("| # | SP A | SP B | Số lần mua chung |")
    out.append("|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        out.append(f"| {i} | {r['product_a_name']} | {r['product_b_name']} | {r['count']} |")
    out.append("")


def _section_actions(a, out):
    rows = a["action_list"]
    out.append("## 11. 🎯 Action list")
    out.append("")
    if not rows:
        out.append("*Không có action cần làm.*"); out.append(""); return
    for r in rows:
        prio = r["priority"]
        marker = {"CAO": "🔴", "TRUNG BÌNH": "🟠", "THẤP": "🟢"}.get(prio, "")
        out.append(f"- {marker} **[{prio}]** {r['type']} — **{r['customer']}** ({r.get('phone') or '-'})")
        out.append(f"  - {r['detail']}")
        if r.get("care_hint"):
            out.append(f"  - Gợi ý: {r['care_hint']}")
    out.append("")
