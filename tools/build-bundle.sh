#!/usr/bin/env bash
# Build toàn bộ bundle "Techla Business Skills v1.0.0".
# Author: Techla — v1.0.0 — License: xem LICENSE.md
#
# Output: build/Techla-Business-Skills-v1.0.0.zip
#
# Thành phần:
#   - skills/cskh-phan-tich-don-hang.skill
#   - skills/research-san-pham-moi.skill
#   - skills/soan-van-ban.skill
#   - extensions/techla-pancake-1.0.0.mcpb
#   - docs/*.md
#   - samples/*.xlsx
#   - README.md, LICENSE.md, CHANGELOG.md
#
# Yêu cầu:
#   - bash (Windows: Git Bash hoặc WSL)
#   - zip CLI
#   - node + npm (để install prod deps cho .mcpb)

set -e

# ═══════════════════════════════════════════════════════════════════
# Paths
# ═══════════════════════════════════════════════════════════════════

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$REPO_ROOT/build"
STAGE_DIR="$BUILD_DIR/stage"
OUT_NAME="Techla-Business-Skills-v1.0.0"
OUT_ZIP="$BUILD_DIR/${OUT_NAME}.zip"

SKILLS=(
    "cskh-phan-tich-don-hang"
    "research-san-pham-moi"
    "soan-van-ban"
)
PANCAKE_DIR="techla-pancake"
PANCAKE_VERSION="1.0.0"

# ═══════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════

log() { echo "[build-bundle] $*"; }

require_cmd() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "LỖI: thiếu lệnh '$1'. Cài trước khi chạy." >&2
        exit 1
    fi
}

# ═══════════════════════════════════════════════════════════════════
# Pre-flight check
# ═══════════════════════════════════════════════════════════════════

require_cmd zip
require_cmd node
require_cmd npm

log "REPO_ROOT=$REPO_ROOT"
log "Clean build/"
rm -rf "$BUILD_DIR"
mkdir -p "$STAGE_DIR/skills" "$STAGE_DIR/extensions" "$STAGE_DIR/docs" "$STAGE_DIR/samples"

# ═══════════════════════════════════════════════════════════════════
# 1. Build .skill files (zip của folder skill)
# ═══════════════════════════════════════════════════════════════════

for skill in "${SKILLS[@]}"; do
    src="$REPO_ROOT/src/$skill"
    if [ ! -d "$src" ]; then
        echo "LỖI: không tìm thấy skill dir '$src'." >&2
        exit 2
    fi
    out="$STAGE_DIR/skills/${skill}.skill"
    log "Build skill: $skill -> $(basename "$out")"

    (cd "$src" && zip -r -X "$out" . \
        -x "*.pyc" \
        -x "__pycache__/*" \
        -x "*/__pycache__/*" \
        -x ".pytest_cache/*" \
        -x "*.DS_Store" \
        -x ".venv/*" \
        -x "venv/*" \
        >/dev/null)
done

# ═══════════════════════════════════════════════════════════════════
# 2. Build .mcpb file (Pancake extension)
# ═══════════════════════════════════════════════════════════════════

log "Build Pancake extension..."
PANCAKE_SRC="$REPO_ROOT/src/$PANCAKE_DIR"
if [ ! -d "$PANCAKE_SRC" ]; then
    echo "LỖI: không tìm thấy '$PANCAKE_SRC'." >&2
    exit 3
fi

PANCAKE_BUILD="$BUILD_DIR/_pancake_build"
rm -rf "$PANCAKE_BUILD"
mkdir -p "$PANCAKE_BUILD"

# Copy source files (không copy node_modules hay log)
cp "$PANCAKE_SRC/manifest.json" "$PANCAKE_BUILD/"
cp "$PANCAKE_SRC/server.js"     "$PANCAKE_BUILD/"
cp "$PANCAKE_SRC/package.json"  "$PANCAKE_BUILD/"
[ -f "$PANCAKE_SRC/README.md" ]    && cp "$PANCAKE_SRC/README.md"    "$PANCAKE_BUILD/"
[ -f "$PANCAKE_SRC/LICENSE.md" ]   && cp "$PANCAKE_SRC/LICENSE.md"   "$PANCAKE_BUILD/"
[ -f "$PANCAKE_SRC/CHANGELOG.md" ] && cp "$PANCAKE_SRC/CHANGELOG.md" "$PANCAKE_BUILD/"
[ -f "$PANCAKE_SRC/icon.png" ]     && cp "$PANCAKE_SRC/icon.png"     "$PANCAKE_BUILD/"

log "  → npm install --omit=dev (production deps only)"
(cd "$PANCAKE_BUILD" && npm install --omit=dev --no-audit --no-fund --silent)

MCPB_OUT="$STAGE_DIR/extensions/${PANCAKE_DIR}-${PANCAKE_VERSION}.mcpb"
log "  → pack .mcpb -> $(basename "$MCPB_OUT")"
(cd "$PANCAKE_BUILD" && zip -r -X "$MCPB_OUT" . \
    -x "*.DS_Store" \
    -x "*.git*" \
    >/dev/null)

rm -rf "$PANCAKE_BUILD"

# ═══════════════════════════════════════════════════════════════════
# 3. Copy docs
# ═══════════════════════════════════════════════════════════════════

log "Copy docs/"
cp "$REPO_ROOT/docs/"*.md "$STAGE_DIR/docs/"

# ═══════════════════════════════════════════════════════════════════
# 4. Copy samples (từ skill CSKH)
# ═══════════════════════════════════════════════════════════════════

log "Copy samples/"
SAMPLES_SRC="$REPO_ROOT/src/cskh-phan-tich-don-hang/samples"
SAMPLES_DST="$STAGE_DIR/samples/cskh-phan-tich-don-hang"
mkdir -p "$SAMPLES_DST"
if [ -d "$SAMPLES_SRC" ]; then
    cp "$SAMPLES_SRC/"*.xlsx "$SAMPLES_DST/" 2>/dev/null || true
fi

# ═══════════════════════════════════════════════════════════════════
# 5. Copy root files
# ═══════════════════════════════════════════════════════════════════

log "Copy root README / LICENSE / CHANGELOG"
cp "$REPO_ROOT/README.md"    "$STAGE_DIR/"
cp "$REPO_ROOT/LICENSE.md"   "$STAGE_DIR/"
cp "$REPO_ROOT/CHANGELOG.md" "$STAGE_DIR/"

# ═══════════════════════════════════════════════════════════════════
# 6. Zip bundle tổng
# ═══════════════════════════════════════════════════════════════════

log "Zip bundle -> $(basename "$OUT_ZIP")"
WRAP_DIR="$BUILD_DIR/$OUT_NAME"
rm -rf "$WRAP_DIR"
mv "$STAGE_DIR" "$WRAP_DIR"

(cd "$BUILD_DIR" && zip -r -X "$(basename "$OUT_ZIP")" "$OUT_NAME" \
    -x "*.DS_Store" \
    >/dev/null)

# ═══════════════════════════════════════════════════════════════════
# 7. Summary
# ═══════════════════════════════════════════════════════════════════

SIZE=$(du -h "$OUT_ZIP" | cut -f1)
echo ""
echo "════════════════════════════════════════════════════════════════"
echo " BUILD OK"
echo "════════════════════════════════════════════════════════════════"
echo "  Output : $OUT_ZIP"
echo "  Size   : $SIZE"
echo ""
echo "  Nội dung:"
(cd "$WRAP_DIR" && find . -maxdepth 2 -type f | sort | sed 's|^\./|    |')
echo ""
echo "  Upload bundle này lên kênh bán hàng của bạn!"
echo "════════════════════════════════════════════════════════════════"
