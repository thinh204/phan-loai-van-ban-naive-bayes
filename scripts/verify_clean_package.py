#!/usr/bin/env python3
"""
Verify submission package in a completely clean environment.
Extracts the ZIP archive to a temporary directory, runs syntax compilation,
executes the full 16 pytest test suite, and tests end-to-end classification.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ZIP_PATH = ROOT / "release" / "phan-loai-van-ban-naive-bayes-final-submission.zip"
VENV_PYTHON = ROOT / ".venv" / "Scripts" / "python.exe"


def verify_clean_package() -> dict:
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"Package ZIP not found: {ZIP_PATH}")

    # Create temporary directory
    temp_dir = Path(tempfile.mkdtemp(prefix="clean_pkg_test_"))
    print(f"-> Thư mục tạm độc lập: {temp_dir}")

    report = {
        "temp_dir": str(temp_dir),
        "extracted_files_count": 0,
        "compileall_code": None,
        "pytest_code": None,
        "pytest_passed": 0,
        "inference_test": None,
        "status": "FAILED",
    }

    try:
        # 1. Extract ZIP
        print("-> Đang giải nén gói bài nộp...")
        with zipfile.ZipFile(ZIP_PATH, "r") as zf:
            zf.extractall(temp_dir)
            extracted_files = [p for p in temp_dir.rglob("*") if p.is_file()]
            report["extracted_files_count"] = len(extracted_files)
        print(f"   Đã giải nén thành công {report['extracted_files_count']} tệp tin.")

        # 2. Syntax check with compileall
        print("-> Đang kiểm tra cú pháp toàn bộ tệp Python (compileall)...")
        res_comp = subprocess.run(
            [str(VENV_PYTHON), "-m", "compileall", "-q", "app.py", "src", "tests"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )
        report["compileall_code"] = res_comp.returncode
        if res_comp.returncode != 0:
            print(f"   Lỗi compileall:\n{res_comp.stderr}")
            return report
        print("   Cú pháp hoàn toàn hợp lệ (returncode = 0).")

        # 3. Run full pytest suite (16 tests)
        print("-> Đang thực thi bộ kiểm thử tự động pytest trên thư mục giải nén...")
        res_pytest = subprocess.run(
            [str(VENV_PYTHON), "-m", "pytest", "-v"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )
        report["pytest_code"] = res_pytest.returncode
        report["pytest_output"] = res_pytest.stdout
        print(f"   Mã thoát pytest: {res_pytest.returncode}")
        if "16 passed" in res_pytest.stdout:
            report["pytest_passed"] = 16
            print("   Kết quả: 16/16 kiểm thử ĐẠT (16 passed)!")
        else:
            print(f"   pytest output:\n{res_pytest.stdout}")
            return report

        # 4. End-to-end inference test with ClassifierService
        print("-> Đang chạy kiểm thử suy diễn thực tế với ClassifierService...")
        code = (
            "from src.classifier_service import get_classifier_service\n"
            "svc = get_classifier_service()\n"
            "svc.load_artifacts()\n"
            "res = svc.classify('NASA space shuttle telescope astronaut orbit mars mission')\n"
            "print('PRED:', res['predicted_class'], 'CONF:', f\"{res['confidence']*100:.2f}%\")\n"
            "assert res['predicted_class'] == 'sci.space'\n"
            "print('INFERENCE_OK')\n"
        )
        res_infer = subprocess.run(
            [str(VENV_PYTHON), "-c", code],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )
        if "INFERENCE_OK" in res_infer.stdout:
            report["inference_test"] = "SUCCESS"
            print(f"   Suy diễn thành công: {res_infer.stdout.strip()}")
            report["status"] = "PASSED"
        else:
            print(f"   Lỗi suy diễn:\n{res_infer.stderr}")

    finally:
        # Clean up temp dir
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("-> Đã dọn dẹp thư mục tạm.")

    return report


def main() -> int:
    print("=" * 70)
    print("XÁC MINH GÓI BÀI NỘP TỪ MÔI TRƯỜNG GIẢI NÉN ĐỘC LẬP")
    print("=" * 70)

    report = verify_clean_package()
    print("\n" + "=" * 70)
    print("TỔNG HỢP KẾT QUẢ XÁC MINH:")
    print(f"- Số tệp giải nén: {report['extracted_files_count']} tệp")
    print(f"- Kiểm tra cú pháp (compileall): {'ĐẠT' if report['compileall_code'] == 0 else 'HỎNG'}")
    print(f"- Kiểm thử tự động (pytest): {report['pytest_passed']}/16 PASSED")
    print(f"- Kiểm thử phân loại suy diễn: {report['inference_test']}")
    print(f"- Trạng thái tổng thể: {report['status']}")
    print("=" * 70)

    return 0 if report["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
