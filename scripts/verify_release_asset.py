#!/usr/bin/env python3
"""
Verify that the release asset uploaded to GitHub Release matches the local submission package
and the documented SHA-256 checksum exactly.
"""

from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL_ZIP = ROOT / "release" / "phan-loai-van-ban-naive-bayes-final-submission.zip"
CHECKSUMS_FILE = ROOT / "release" / "CHECKSUMS.sha256"


def verify_release_asset(tag: str = "v1.0.2") -> bool:
    print("=" * 70)
    print(f"XÁC MINH TÀI SẢN TẢI XUỐNG TỪ GITHUB RELEASE ({tag})")
    print("=" * 70)

    asset_url = (
        f"https://github.com/thinh204/phan-loai-van-ban-naive-bayes/releases/download/{tag}/"
        f"phan-loai-van-ban-naive-bayes-final-submission.zip"
    )
    print(f"-> Đang tải tài sản kiểm thử từ: {asset_url}")

    req = urllib.request.Request(asset_url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
    except Exception as e:
        print(f"Lỗi khi tải tài sản từ GitHub: {e}")
        return False

    downloaded_size = len(data)
    downloaded_hash = hashlib.sha256(data).hexdigest()
    print(f"-> Dung lượng tải về: {downloaded_size:,} bytes")
    print(f"-> SHA-256 tải về:    {downloaded_hash}")

    if not LOCAL_ZIP.exists():
        print(f"Lỗi: Không tìm thấy gói local tại {LOCAL_ZIP}")
        return False

    local_bytes = LOCAL_ZIP.read_bytes()
    local_size = len(local_bytes)
    local_hash = hashlib.sha256(local_bytes).hexdigest()
    print(f"-> SHA-256 tệp local: {local_hash}")

    # Check against CHECKSUMS.sha256
    expected_hash = None
    if CHECKSUMS_FILE.exists():
        for line in CHECKSUMS_FILE.read_text(encoding="utf-8").splitlines():
            if "phan-loai-van-ban-naive-bayes-final-submission.zip" in line:
                expected_hash = line.split()[0].strip()
                break
    print(f"-> SHA-256 kỳ vọng:  {expected_hash}")

    if downloaded_hash == local_hash and (expected_hash is None or downloaded_hash == expected_hash):
        print("\n[THÀNH CÔNG] Tài sản trên GitHub Release khớp chính xác 100% với gói nghiệm thu!")
        return True
    else:
        print("\n[THẤT BẠI] Phát hiện sai lệch mã băm giữa GitHub Release và kho lưu trữ!")
        return False


if __name__ == "__main__":
    tag = sys.argv[1] if len(sys.argv) > 1 else "v1.0.2"
    success = verify_release_asset(tag)
    sys.exit(0 if success else 1)
