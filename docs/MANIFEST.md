# Danh mục toàn vẹn và mã băm gói bài nộp (Submission Manifest & Checksums v1.0.2)

- **Tệp lưu trữ chính thức**: `release/phan-loai-van-ban-naive-bayes-final-submission.zip`
- **Phiên bản phát hành**: `v1.0.2` (Bản bảo vệ đề tài chính thức)
- **Tổng số tệp tin đóng gói**: 46 tệp tin (bao gồm toàn bộ mã nguồn, dữ liệu mô hình nạp sẵn, slide PowerPoint, tài liệu báo cáo và kết quả thực nghiệm).
- **Kiểm tra tính toàn vẹn (testzip)**: `VALID` (100% không lỗi dữ liệu, không hỏng CRC-32).
- **Danh mục chi tiết và mã băm từng tệp**: [release/MANIFEST.json](file:///d:/phan-loai-van-ban-naive-bayes/release/MANIFEST.json) và [release/CHECKSUMS.sha256](file:///d:/phan-loai-van-ban-naive-bayes/release/CHECKSUMS.sha256).

---

## 1. Bảng đối chiếu mã băm SHA-256 các tệp thành phần tiêu biểu

| Đường dẫn tệp trong gói | Dung lượng (bytes) | Trạng thái toàn vẹn |
| :--- | :---: | :---: |
| `.streamlit/config.toml` | 213 | ✅ Đã băm SHA-256 |
| `README.md` | 9.688 | ✅ Đã băm SHA-256 |
| `app.py` | 23.621 | ✅ Đã băm SHA-256 |
| `requirements.txt` | 107 | ✅ Đã băm SHA-256 |
| `models/naive_bayes_model.joblib` | 837.191 | ✅ Đã băm SHA-256 |
| `models/tfidf_vectorizer.joblib` | 270.438 | ✅ Đã băm SHA-256 |
| `models/class_names.joblib` | 86 | ✅ Đã băm SHA-256 |
| `presentation/phan-loai-van-ban-naive-bayes-v2.pptx` | 42.765 | ✅ Đã băm SHA-256 |
| `results/evaluation_summary.json` | 1.897 | ✅ Đã băm SHA-256 |
| `results/alpha_tuning.json` | 2.496 | ✅ Đã băm SHA-256 |
| `results/error_analysis.json` | 5.437 | ✅ Đã băm SHA-256 |
| `src/classifier_service.py` | 11.842 | ✅ Đã băm SHA-256 |
| `src/config.py` | 3.553 | ✅ Đã băm SHA-256 |
| `tests/test_pipeline.py` | 7.306 | ✅ Đã băm SHA-256 |
| `tests/test_inference.py` | 2.368 | ✅ Đã băm SHA-256 |
| `docs/bao-cao.md` | 14.951 | ✅ Đã băm SHA-256 |
| `docs/thuyet-trinh.md` | 4.193 | ✅ Đã băm SHA-256 |
| `docs/DIEN_TAP_BAO_VE.md` | 9.076 | ✅ Đã băm SHA-256 |
| `docs/DEMO_SCRIPT.md` | 8.470 | ✅ Đã băm SHA-256 |
| `docs/NGHIEM_THU.md` | 6.464 | ✅ Đã băm SHA-256 |
| `docs/CI_VERIFICATION.md` | 3.368 | ✅ Đã băm SHA-256 |
| `docs/CLEAN_ENV_TEST.md` | 3.302 | ✅ Đã băm SHA-256 |
| `docs/RELEASE_NOTES_v1.0.2.md` | 9.481 | ✅ Đã băm SHA-256 |

*(Chi tiết đầy đủ 46 tệp được lưu trữ đồng bộ tại `release/MANIFEST.json` và `release/CHECKSUMS.sha256`)*.

---

## 2. Hướng dẫn xác thực tính toàn vẹn độc lập

Người dùng hoặc hội đồng chấm thi có thể kiểm tra tính toàn vẹn của tệp tải về bằng công cụ dòng lệnh:

### Trên Windows PowerShell:
```powershell
Get-FileHash -Path release\phan-loai-van-ban-naive-bayes-final-submission.zip -Algorithm SHA256
```
So sánh chuỗi mã băm hiển thị với giá trị dòng đầu tiên trong `release/CHECKSUMS.sha256`.

### Trên Linux / macOS:
```bash
sha256sum -c release/CHECKSUMS.sha256
```
Kết quả mong đợi: `OK` cho mọi tệp tin thành phần.
