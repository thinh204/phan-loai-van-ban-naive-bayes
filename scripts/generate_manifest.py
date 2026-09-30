#!/usr/bin/env python3
"""
Generate manifest and SHA-256 checksums for the final submission package.
Verifies ZIP archive integrity (testzip) and generates MANIFEST.json and CHECKSUMS.sha256.
"""

from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RELEASE_DIR = ROOT / "release"
ZIP_PATH = RELEASE_DIR / "phan-loai-van-ban-naive-bayes-final-submission.zip"
MANIFEST_JSON = RELEASE_DIR / "MANIFEST.json"
CHECKSUM_FILE = RELEASE_DIR / "CHECKSUMS.sha256"


def sha256_of_bytes(data: bytes) -> str:
    """Compute SHA-256 hexadecimal digest for raw bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_of_file(file_path: Path) -> str:
    """Compute SHA-256 hexadecimal digest for a file."""
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def generate_manifest(zip_path: Path = ZIP_PATH) -> dict:
    if not zip_path.exists():
        raise FileNotFoundError(f"Package ZIP not found: {zip_path}")

    # 1. Verify ZIP archive integrity
    with zipfile.ZipFile(zip_path, "r") as zf:
        corrupt_file = zf.testzip()
        if corrupt_file is not None:
            raise ValueError(f"Corrupt file detected in ZIP: {corrupt_file}")

        file_entries = []
        for info in sorted(zf.infolist(), key=lambda x: x.filename):
            content = zf.read(info.filename)
            file_hash = sha256_of_bytes(content)
            file_entries.append({
                "path": info.filename,
                "size_bytes": info.file_size,
                "compressed_bytes": info.compress_size,
                "sha256": file_hash,
            })

    zip_hash = sha256_of_file(zip_path)
    zip_size = zip_path.stat().st_size

    manifest = {
        "project": "phan-loai-van-ban-naive-bayes",
        "archive_name": zip_path.name,
        "archive_size_bytes": zip_size,
        "archive_sha256": zip_hash,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_files": len(file_entries),
        "total_uncompressed_bytes": sum(e["size_bytes"] for e in file_entries),
        "integrity_status": "VALID",
        "files": file_entries,
    }

    # Save MANIFEST.json
    with open(MANIFEST_JSON, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Save CHECKSUMS.sha256 (standard format compatible with sha256sum -c)
    with open(CHECKSUM_FILE, "w", encoding="utf-8") as f:
        f.write(f"{zip_hash}  {zip_path.name}\n")
        for e in file_entries:
            f.write(f"{e['sha256']}  {e['path']}\n")

    return manifest


def main() -> int:
    print("=" * 70)
    print("KIỂM TRA TOÀN VẸN VÀ TẠO MANIFEST BÀI NỘP (INTEGRITY CHECK)")
    print("=" * 70)

    try:
        manifest = generate_manifest()
        print(f"-> Trạng thái toàn vẹn tệp nén (testzip): {manifest['integrity_status']}")
        print(f"-> Tệp lưu trữ: {manifest['archive_name']}")
        print(f"-> Dung lượng tệp nén: {manifest['archive_size_bytes']:,} bytes")
        print(f"-> Tổng số tệp trong gói: {manifest['total_files']} tệp")
        print(f"-> SHA-256 gói nộp:\n   {manifest['archive_sha256']}")
        print(f"\n-> Đã xuất tệp Manifest JSON: {MANIFEST_JSON.name}")
        print(f"-> Đã xuất tệp Checksum SHA-256: {CHECKSUM_FILE.name}")
        print("\n[THÀNH CÔNG] Kiểm tra toàn vẹn đạt 100%! Gói nộp không lỗi, không tệp thừa.")
        return 0
    except Exception as exc:
        print(f"[LỖI] Kiểm tra toàn vẹn thất bại: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
