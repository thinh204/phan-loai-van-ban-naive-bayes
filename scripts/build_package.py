#!/usr/bin/env python3
"""
Automated packaging script for Naive Bayes Text Classification project.
Builds a clean, reproducible submission ZIP archive from an explicit whitelist of files.
Strictly excludes virtual environments (.venv), caches, and temporary files.
"""

from __future__ import annotations

import os
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RELEASE_DIR = ROOT / "release"
OUTPUT_ZIP = RELEASE_DIR / "phan-loai-van-ban-naive-bayes-final-submission.zip"

# Explicit whitelist of directories to include (relative to repo root)
ALLOWED_DIRS = [
    "src",
    "models",
    "results",
    "docs",
    "tests",
    "presentation",
    ".streamlit",
    ".github",
    "scripts",
]

# Explicit whitelist of root files to include
ALLOWED_ROOT_FILES = [
    "app.py",
    "requirements.txt",
    "README.md",
    ".gitignore",
]

# Patterns and substrings strictly excluded
EXCLUDED_PATTERNS = [
    "__pycache__",
    ".pytest_cache",
    ".venv",
    ".git",
    ".build",
    ".codex",
    "scratch",
    ".env",
    "desktop.ini",
    ".DS_Store",
]


def is_excluded(path: Path) -> bool:
    """Check if a given path contains any excluded pattern or extension."""
    parts = set(path.parts)
    for p in EXCLUDED_PATTERNS:
        if p in parts:
            return True
    if path.suffix in [".pyc", ".pyo", ".pyd", ".tmp", ".log"]:
        return True
    return False


def collect_submission_files() -> list[Path]:
    """Collect and sort all allowed submission files."""
    files: list[Path] = []

    # Root files
    for fname in ALLOWED_ROOT_FILES:
        fpath = ROOT / fname
        if fpath.exists() and fpath.is_file() and not is_excluded(fpath):
            files.append(fpath)

    # Directory files
    for dir_name in ALLOWED_DIRS:
        dir_path = ROOT / dir_name
        if not dir_path.exists():
            continue
        for item in dir_path.rglob("*"):
            if item.is_file() and not is_excluded(item):
                files.append(item)

    # Deterministic sort
    files.sort(key=lambda p: str(p.relative_to(ROOT)))
    return files


def build_package(output_path: Path = OUTPUT_ZIP) -> tuple[Path, int, int]:
    """Build the clean submission zip archive."""
    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    files = collect_submission_files()

    total_uncompressed = 0
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for f in files:
            arcname = str(f.relative_to(ROOT)).replace("\\", "/")
            zf.write(f, arcname=arcname)
            size = f.stat().st_size
            total_uncompressed += size

    compressed_size = output_path.stat().st_size
    return output_path, len(files), compressed_size


def main() -> int:
    print("=" * 70)
    print("XÂY DỰNG GÓI BÀI NỘP CHÍNH THỨC (AUTOMATED PACKAGING)")
    print("=" * 70)

    output_path, file_count, comp_size = build_package()
    print(f"-> Gói nén đầu ra: {output_path.name}")
    print(f"-> Đường dẫn tuyệt đối: {output_path}")
    print(f"-> Số lượng tệp đóng gói: {file_count} tệp")
    print(f"-> Dung lượng tệp nén: {comp_size:,} bytes (~{comp_size / 1024:.1f} KB)")
    print("\nDanh sách các tệp đã đóng gói:")
    with zipfile.ZipFile(output_path, "r") as z:
        for info in z.infolist():
            print(f"  [{info.file_size:>8,} bytes]  {info.filename}")

    print("\n[THÀNH CÔNG] Gói bài nộp đã được tạo tự động và sẵn sàng bàn giao!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
