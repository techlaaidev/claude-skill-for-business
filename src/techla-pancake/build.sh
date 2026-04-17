#!/usr/bin/env bash
# Build script: đóng gói thành .mcpb bundle cho Claude Desktop.
# Author: Techla — v1.0.0 — License: xem LICENSE.md
#
# Usage: bash build.sh
# Output: techla-pancake-1.0.0.mcpb
#
# Yêu cầu:
#   - Node.js 18+ (để chạy `npm install --omit=dev`)
#   - zip CLI (có sẵn trên macOS; Windows: dùng Git Bash / WSL / 7z)

set -e

NAME="techla-pancake"
VERSION="1.0.0"
OUT="${NAME}-${VERSION}.mcpb"
TMP_DIR=".mcpb-build"

echo "[1/5] Làm sạch thư mục tạm..."
rm -rf "$TMP_DIR" "$OUT"
mkdir -p "$TMP_DIR"

echo "[2/5] Copy source files..."
cp manifest.json "$TMP_DIR/"
cp server.js "$TMP_DIR/"
cp package.json "$TMP_DIR/"
[ -f README.md ] && cp README.md "$TMP_DIR/"
[ -f LICENSE.md ] && cp LICENSE.md "$TMP_DIR/"
[ -f CHANGELOG.md ] && cp CHANGELOG.md "$TMP_DIR/"
[ -f icon.png ] && cp icon.png "$TMP_DIR/"

echo "[3/5] Cài production dependencies (không dev deps)..."
cd "$TMP_DIR"
npm install --omit=dev --no-audit --no-fund --silent
cd ..

echo "[4/5] Đóng gói .mcpb (thực chất là zip)..."
cd "$TMP_DIR"
# -X = không lưu extra file attributes (portable)
# -r = recursive
if command -v zip >/dev/null 2>&1; then
    zip -r -X "../$OUT" . -x "*.DS_Store" "*.git*" >/dev/null
else
    echo "LỖI: cần cài 'zip' CLI (macOS/Linux có sẵn; Windows dùng Git Bash hoặc WSL)." >&2
    exit 1
fi
cd ..

echo "[5/5] Dọn dẹp..."
rm -rf "$TMP_DIR"

SIZE=$(du -h "$OUT" | cut -f1)
echo ""
echo "OK: $OUT ($SIZE)"
echo "   -> Cài vào Claude Desktop: Settings -> Extensions -> Install from file -> chọn $OUT"
