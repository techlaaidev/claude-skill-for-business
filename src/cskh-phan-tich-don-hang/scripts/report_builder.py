"""
CLI wrapper: build báo cáo .docx + .md từ analysis.json.
Author: Techla — v1.0.0 — License: xem LICENSE.md

Usage:
    python scripts/report_builder.py analysis.json --docx out.docx --md out.md
"""
from __future__ import annotations
import os
import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from report_md import build_md
from report_docx import build_docx


def main():
    ap = argparse.ArgumentParser(description="Build report .docx + .md từ analysis.json")
    ap.add_argument("input", help="File analysis.json (từ analyzer.py)")
    ap.add_argument("--docx", default="bao-cao.docx", help="File .docx đầu ra")
    ap.add_argument("--md", default="bao-cao.md", help="File .md đầu ra")
    args = ap.parse_args()

    if not Path(args.input).exists():
        print(f"Lỗi: không tìm thấy '{args.input}'.", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        a = json.load(f)

    # Markdown
    md_text = build_md(a)
    with open(args.md, "w", encoding="utf-8") as f:
        f.write(md_text)
    print(f"OK: {args.md} ({len(md_text):,} bytes)")

    # Docx
    build_docx(a, args.docx)
    size = Path(args.docx).stat().st_size
    print(f"OK: {args.docx} ({size:,} bytes)")


if __name__ == "__main__":
    main()
