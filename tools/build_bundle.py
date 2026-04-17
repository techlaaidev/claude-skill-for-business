"""
Build toàn bộ bundle "Techla Business Skills v1.0.0" — cross-platform (Win/Mac/Linux).
Author: Techla — v1.0.0 — License: xem LICENSE.md

Output: build/Techla-Business-Skills-v1.0.0.zip

Thành phần:
    - skills/cskh-phan-tich-don-hang.skill
    - skills/research-san-pham-moi.skill
    - skills/soan-van-ban.skill
    - extensions/techla-pancake-1.0.0.mcpb
    - docs/*.md
    - samples/*.xlsx
    - README.md, LICENSE.md, CHANGELOG.md

Usage:
    python tools/build_bundle.py
"""
from __future__ import annotations
import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = REPO_ROOT / "build"
OUT_NAME = "Techla-Business-Skills-v1.0.3"
OUT_ZIP = BUILD_DIR / f"{OUT_NAME}.zip"

SKILLS = [
    "cskh-phan-tich-don-hang",
    "research-san-pham-moi",
    "soan-van-ban",
]
PANCAKE_DIR = "techla-pancake"
PANCAKE_VERSION = "1.0.3"

EXCLUDE_NAMES = {".DS_Store", "__pycache__", ".pytest_cache", ".venv", "venv",
                 "node_modules", ".git", ".gitignore"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}


def log(msg: str):
    print(f"[build_bundle] {msg}")


def should_skip(path: Path, skip_node_modules: bool = True) -> bool:
    parts = path.parts
    for part in parts:
        if part in EXCLUDE_NAMES:
            if part == "node_modules" and not skip_node_modules:
                continue
            return True
    if path.suffix in EXCLUDE_SUFFIXES:
        return True
    return False


def zip_folder(src: Path, dst_zip: Path, skip_node_modules: bool = True):
    dst_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dst_zip, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src):
            dirs[:] = [
                d for d in dirs
                if not should_skip(Path(root) / d, skip_node_modules=skip_node_modules)
            ]
            for f in files:
                fp = Path(root) / f
                if should_skip(fp, skip_node_modules=skip_node_modules):
                    continue
                arcname = fp.relative_to(src).as_posix()
                zf.write(fp, arcname)


def check_commands():
    for cmd in ("node", "npm"):
        if shutil_which(cmd) is None:
            print(f"LỖI: thiếu lệnh '{cmd}'. Cài trước khi chạy.", file=sys.stderr)
            sys.exit(1)


def shutil_which(cmd: str):
    found = shutil.which(cmd)
    if found:
        return found
    # Windows fallback
    for ext in (".cmd", ".bat", ".exe"):
        found = shutil.which(cmd + ext)
        if found:
            return found
    return None


def run(cmd, cwd=None):
    r = subprocess.run(cmd, cwd=cwd, shell=False, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + "\n" + r.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return r


# ═══════════════════════════════════════════════════════════════════
# Build steps
# ═══════════════════════════════════════════════════════════════════

def clean_build():
    log("Clean build/")
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)


def build_skills(stage: Path):
    skills_dir = stage / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    for skill in SKILLS:
        src = REPO_ROOT / "src" / skill
        if not src.is_dir():
            raise FileNotFoundError(f"Không tìm thấy skill dir: {src}")
        out = skills_dir / f"{skill}.skill"
        log(f"Build skill: {skill} -> {out.name}")
        zip_folder(src, out, skip_node_modules=True)


def build_pancake(stage: Path):
    log("Build Pancake extension...")
    src = REPO_ROOT / "src" / PANCAKE_DIR
    if not src.is_dir():
        raise FileNotFoundError(f"Không tìm thấy: {src}")

    tmp = BUILD_DIR / "_pancake_build"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)

    for fname in ["manifest.json", "server.js", "package.json",
                  "README.md", "LICENSE.md", "CHANGELOG.md", "icon.png"]:
        fp = src / fname
        if fp.exists():
            shutil.copy2(fp, tmp / fname)

    log("  -> npm install --omit=dev")
    npm = shutil_which("npm")
    run([npm, "install", "--omit=dev", "--no-audit", "--no-fund", "--silent"], cwd=tmp)

    ext_dir = stage / "extensions"
    ext_dir.mkdir(parents=True, exist_ok=True)
    out = ext_dir / f"{PANCAKE_DIR}-{PANCAKE_VERSION}.mcpb"
    log(f"  -> pack .mcpb -> {out.name}")
    # .mcpb cần include node_modules
    zip_folder(tmp, out, skip_node_modules=False)

    shutil.rmtree(tmp)


def copy_docs(stage: Path):
    log("Copy docs/")
    src = REPO_ROOT / "docs"
    dst = stage / "docs"
    dst.mkdir(parents=True, exist_ok=True)
    for md in src.glob("*.md"):
        shutil.copy2(md, dst / md.name)


def copy_samples(stage: Path):
    log("Copy samples/")
    src = REPO_ROOT / "src" / "cskh-phan-tich-don-hang" / "samples"
    dst = stage / "samples" / "cskh-phan-tich-don-hang"
    dst.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        for xlsx in src.glob("*.xlsx"):
            shutil.copy2(xlsx, dst / xlsx.name)


def copy_root(stage: Path):
    log("Copy root README / LICENSE / CHANGELOG")
    for fn in ("README.md", "LICENSE.md", "CHANGELOG.md"):
        src = REPO_ROOT / fn
        if not src.exists():
            raise FileNotFoundError(f"Missing: {src}")
        shutil.copy2(src, stage / fn)


def make_final_zip(stage: Path):
    log(f"Zip bundle -> {OUT_ZIP.name}")
    wrap = BUILD_DIR / OUT_NAME
    if wrap.exists():
        shutil.rmtree(wrap)
    stage.rename(wrap)

    with zipfile.ZipFile(OUT_ZIP, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(wrap):
            dirs[:] = [d for d in dirs if d != ".DS_Store"]
            for f in files:
                if f == ".DS_Store":
                    continue
                fp = Path(root) / f
                arcname = fp.relative_to(BUILD_DIR).as_posix()
                zf.write(fp, arcname)


def print_summary():
    size_kb = OUT_ZIP.stat().st_size / 1024
    size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.2f} MB"

    print()
    print("=" * 64)
    print(" BUILD OK")
    print("=" * 64)
    print(f"  Output : {OUT_ZIP}")
    print(f"  Size   : {size_str}")
    print()
    print("  Nội dung:")
    wrap = BUILD_DIR / OUT_NAME
    for p in sorted(wrap.rglob("*")):
        if p.is_file():
            rel = p.relative_to(wrap).as_posix()
            depth = rel.count("/")
            if depth <= 2:
                print(f"    {rel}")
    print()
    print("  Upload bundle này lên kênh bán hàng của bạn!")
    print("=" * 64)


def main():
    check_commands()
    log(f"REPO_ROOT={REPO_ROOT}")
    clean_build()

    stage = BUILD_DIR / "stage"
    stage.mkdir(parents=True)

    build_skills(stage)
    build_pancake(stage)
    copy_docs(stage)
    copy_samples(stage)
    copy_root(stage)
    make_final_zip(stage)
    print_summary()


if __name__ == "__main__":
    main()
