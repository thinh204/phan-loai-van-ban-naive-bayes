#!/usr/bin/env python3
"""
Verify submission package in a completely clean and isolated environment.
Extracts the ZIP archive to a temporary directory, creates a fresh virtual environment,
installs dependencies strictly from requirements.txt, runs syntax compilation,
executes the full 16 pytest test suite, and tests end-to-end classification.
Strictly does NOT use the workspace's repository .venv.
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
WORKSPACE_VENV = ROOT / ".venv"


def verify_clean_package() -> dict:
    if not ZIP_PATH.exists():
        raise FileNotFoundError(f"Package ZIP not found: {ZIP_PATH}")

    # Create temporary directory for extraction
    temp_dir = Path(tempfile.mkdtemp(prefix="clean_pkg_test_"))
    # Create separate temporary directory for isolated venv
    venv_dir = Path(tempfile.mkdtemp(prefix="clean_pkg_venv_"))
    print(f"-> Thư mục giải nén độc lập: {temp_dir}")
    print(f"-> Thư mục môi trường ảo sạch: {venv_dir}")

    report = {
        "temp_dir": str(temp_dir),
        "venv_dir": str(venv_dir),
        "extracted_files_count": 0,
        "venv_created": False,
        "pip_installed": False,
        "isolated_python": None,
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

        # 2. Create fresh, isolated virtual environment
        print("-> Đang khởi tạo môi trường Python ảo mới hoàn toàn (python -m venv)...")
        # Use sys.executable as base python to create new venv
        res_venv = subprocess.run(
            [sys.executable, "-m", "venv", str(venv_dir)],
            capture_output=True,
            text=True,
        )
        if res_venv.returncode != 0:
            print(f"   Lỗi khởi tạo venv mới:\n{res_venv.stderr}")
            return report
        report["venv_created"] = True

        isolated_python = venv_dir / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
        if not isolated_python.exists():
            print(f"   Không tìm thấy Python trong venv mới: {isolated_python}")
            return report
        report["isolated_python"] = str(isolated_python)

        # Verify it is NOT the repository workspace .venv
        assert WORKSPACE_VENV not in isolated_python.parents, "LỖI: Môi trường ảo bị trùng với .venv của workspace!"
        print(f"   Đã tạo môi trường sạch thành công: {isolated_python}")
        print("   Xác nhận: Hoàn toàn độc lập, KHÔNG sử dụng .venv của workspace.")

        # 3. Install requirements.txt into the clean venv
        req_file = temp_dir / "requirements.txt"
        print(f"-> Đang cài đặt thư viện phụ thuộc từ {req_file.name} vào môi trường mới...")
        res_pip = subprocess.run(
            [str(isolated_python), "-m", "pip", "install", "-r", str(req_file)],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )
        if res_pip.returncode != 0:
            print(f"   Lỗi cài đặt pip dependencies:\n{res_pip.stderr}")
            return report
        report["pip_installed"] = True
        print("   Cài đặt thư viện phụ thuộc hoàn tất.")

        # 4. Syntax check with compileall using isolated_python
        print("-> Đang kiểm tra cú pháp toàn bộ tệp Python bằng Python của môi trường mới...")
        res_comp = subprocess.run(
            [str(isolated_python), "-m", "compileall", "-q", "app.py", "src", "tests"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )
        report["compileall_code"] = res_comp.returncode
        if res_comp.returncode != 0:
            print(f"   Lỗi compileall:\n{res_comp.stderr}")
            return report
        print("   Cú pháp hoàn toàn hợp lệ (returncode = 0).")

        # 5. Run full pytest suite (16 tests) with isolated_python
        print("-> Đang thực thi bộ kiểm thử tự động pytest bằng Python của môi trường mới...")
        res_pytest = subprocess.run(
            [str(isolated_python), "-m", "pytest", "-v"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
        )
        report["pytest_code"] = res_pytest.returncode
        report["pytest_output"] = res_pytest.stdout
        import re
        match = re.search(r"(\d+) passed", res_pytest.stdout)
        if res_pytest.returncode == 0 and match:
            report["pytest_passed"] = int(match.group(1))
            print(f"   Kết quả: {report['pytest_passed']} kiểm thử ĐẠT (passed)!")
        else:
            print(f"   pytest output:\n{res_pytest.stdout}")
            return report

        # 6. End-to-end inference test with ClassifierService using isolated_python
        print("-> Đang chạy kiểm thử suy diễn thực tế với ClassifierService bằng Python môi trường mới...")
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
            [str(isolated_python), "-c", code],
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
        # Clean up temp dirs
        shutil.rmtree(temp_dir, ignore_errors=True)
        shutil.rmtree(venv_dir, ignore_errors=True)
        print("-> Đã dọn dẹp các thư mục tạm sạch sẽ.")

    return report


def main() -> int:
    print("=" * 70)
    print("XÁC MINH GÓI BÀI NỘP TỪ MÔI TRƯỜNG GIẢI NÉN VÀ VENV ĐỘC LẬP HOÀN TOÀN")
    print("=" * 70)

    report = verify_clean_package()
    print("\n" + "=" * 70)
    print("TỔNG HỢP KẾT QUẢ XÁC MINH:")
    print(f"- Số tệp giải nén: {report['extracted_files_count']} tệp")
    print(f"- Môi trường ảo mới: {'ĐÃ TẠO' if report['venv_created'] else 'HỎNG'}")
    print(f"- Cài đặt dependencies: {'ĐẠT' if report['pip_installed'] else 'HỎNG'}")
    print(f"- Kiểm tra cú pháp (compileall): {'ĐẠT' if report['compileall_code'] == 0 else 'HỎNG'}")
    print(f"- Kiểm thử tự động (pytest): {report['pytest_passed']}/16 PASSED")
    print(f"- Kiểm thử phân loại suy diễn: {report['inference_test']}")
    print(f"- Trạng thái tổng thể: {report['status']}")
    print("=" * 70)

    return 0 if report["status"] == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
