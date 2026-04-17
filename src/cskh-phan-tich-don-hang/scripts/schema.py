"""
Schema dataclasses cho pipeline CSKH.
Author: Techla — v1.0.0 — License: xem LICENSE.md

Dùng chung giữa parser_weca, parser_standard, analyzer, report_builder.
Parser output -> JSON theo ParsedData; analyzer đọc vào bằng from_dict.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Optional
import json
from datetime import datetime


@dataclass
class Customer:
    customer_id: str
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    care_goal: Optional[str] = None              # sheet 2 - MỤC TIÊU CHĂM SÓC
    care_message_template: Optional[str] = None  # sheet 2 - Nội dung tin nhắn
    care_history: Optional[str] = None           # sheet 2 - LỊCH SỬ CHĂM SÓC
    opportunity: Optional[str] = None            # sheet 3 - Cơ hội
    action_needed: Optional[str] = None          # sheet 3 - Cần làm
    status: Optional[str] = None                 # sheet 3 - Hiện trạng chăm sóc


@dataclass
class Product:
    product_id: str
    name: str
    avg_qty_per_order: Optional[float] = None     # WECA: SỐ LƯỢNG BÁN TB/Lần
    avg_orders_per_month: Optional[float] = None
    unit_price: Optional[float] = None            # ưu tiên GIÁ BÁN MỚI


@dataclass
class OrderEvent:
    customer_id: str
    product_id: str
    order_date: str                                # ISO YYYY-MM-DD
    qty: Optional[float] = None
    estimated_revenue: Optional[float] = None


@dataclass
class ParsedData:
    source_file: str
    parsed_at: str
    format: str                                    # "weca" | "standard"
    year: int
    customers: list[Customer] = field(default_factory=list)
    products: list[Product] = field(default_factory=list)
    orders: list[OrderEvent] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def save_json(self, path: str) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load_json(cls, path: str) -> "ParsedData":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "ParsedData":
        return cls(
            source_file=data["source_file"],
            parsed_at=data["parsed_at"],
            format=data["format"],
            year=data["year"],
            customers=[Customer(**c) for c in data.get("customers", [])],
            products=[Product(**p) for p in data.get("products", [])],
            orders=[OrderEvent(**o) for o in data.get("orders", [])],
            warnings=list(data.get("warnings", [])),
        )


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
