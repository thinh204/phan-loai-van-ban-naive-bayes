#!/usr/bin/env python3
"""
Publish GitHub Release v1.0.4 and upload release assets.
"""

from __future__ import annotations

import json
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def get_github_token() -> str:
    p = subprocess.Popen(
        ["git", "credential", "fill"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    out, _ = p.communicate("protocol=https\nhost=github.com\n\n")
    for line in out.splitlines():
        if line.startswith("password="):
            return line.split("=", 1)[1]
    return ""


def main():
    token = get_github_token()
    if not token:
        print("Lỗi: Không tìm thấy GitHub token từ git credential helper.")
        return 1

    repo = "thinh204/phan-loai-van-ban-naive-bayes"
    tag_name = "v1.0.4"
    release_name = "v1.0.4 - Sửa nhập liệu rỗng, định dạng đoạn trích và hoàn thiện nghiệm thu"
    release_notes_file = ROOT / "docs" / "RELEASE_NOTES_v1.0.4.md"

    body = release_notes_file.read_text(encoding="utf-8")

    # Check or create release
    url = f"https://api.github.com/repos/{repo}/releases"
    payload = {
        "tag_name": tag_name,
        "target_commitish": "main",
        "name": release_name,
        "body": body,
        "draft": False,
        "prerelease": False,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        },
    )

    try:
        resp = urllib.request.urlopen(req)
        rel_data = json.loads(resp.read().decode("utf-8"))
        print(f"Khởi tạo GitHub Release thành công! ID: {rel_data['id']}")
        print(f"Release URL: {rel_data['html_url']}")
        upload_url = rel_data["upload_url"].split("{")[0]
    except Exception as e:
        print(f"Thông báo khi tạo release: {e}. Thử truy vấn release hiện có...")
        req_get = urllib.request.Request(
            f"https://api.github.com/repos/{repo}/releases/tags/{tag_name}",
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        resp = urllib.request.urlopen(req_get)
        rel_data = json.loads(resp.read().decode("utf-8"))
        print(f"Đã tìm thấy Release ID: {rel_data['id']}")
        upload_url = rel_data["upload_url"].split("{")[0]

    # Assets to upload
    assets = [
        ROOT / "release" / "phan-loai-van-ban-naive-bayes-final-submission.zip",
        ROOT / "release" / "MANIFEST.json",
        ROOT / "release" / "CHECKSUMS.sha256",
    ]

    for asset_path in assets:
        if not asset_path.exists():
            print(f"Cảnh báo: Không tìm thấy tệp {asset_path}")
            continue

        asset_name = asset_path.name
        upload_url_full = f"{upload_url}?name={urllib.parse.quote(asset_name)}"
        print(f"\n-> Đang tải lên tài sản {asset_name}...")
        asset_bytes = asset_path.read_bytes()

        if asset_name.endswith(".zip"):
            content_type = "application/zip"
        elif asset_name.endswith(".json"):
            content_type = "application/json"
        else:
            content_type = "text/plain"

        req_upload = urllib.request.Request(
            upload_url_full,
            data=asset_bytes,
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": content_type,
            },
        )

        try:
            resp_upload = urllib.request.urlopen(req_upload)
            asset_info = json.loads(resp_upload.read().decode("utf-8"))
            print(f"   [THÀNH CÔNG] Đã tải lên {asset_name} ({asset_info['size']:,} bytes)")
            print(f"   Tải xuống: {asset_info['browser_download_url']}")
        except Exception as e:
            print(f"   Lỗi khi tải lên {asset_name}: {e}")

    print("\nHoàn tất phát hành GitHub Release v1.0.4!")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
