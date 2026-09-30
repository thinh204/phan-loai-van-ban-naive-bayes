# Danh mục toàn vẹn và mã băm gói bài nộp (Submission Manifest & Checksums)

- **Tệp lưu trữ chính thức**: `release/phan-loai-van-ban-naive-bayes-final-submission.zip`
- **Dung lượng tệp nén**: `660.517 bytes` (~645.0 KB)
- **Mã băm SHA-256 tệp nén**:
  ```text
  1599c3e379f3af2df1059ed5ea6fb216da2d20a7e9f500a3b3e0a5b0b4f2be26
  ```
- **Tổng số tệp tin đóng gói**: 42 tệp tin (bao gồm toàn bộ mã nguồn, dữ liệu mô hình nạp sẵn, slide PowerPoint, tài liệu báo cáo và kết quả thực nghiệm).
- **Kiểm tra tính toàn vẹn (testzip)**: `VALID` (100% không lỗi dữ liệu, không hỏng CRC-32).

---

## 1. Bảng đối chiếu mã băm SHA-256 các tệp thành phần

| Đường dẫn tệp trong gói | Dung lượng (bytes) | Mã băm SHA-256 (Tóm lược 16 ký tự đầu) |
| :--- | :---: | :--- |
| `.streamlit/config.toml` | 213 | `21b5695beee3cff3...` |
| `README.md` | 9.600 | `f22f778d91b402eb...` |
| `app.py` | 23.621 | `d2d9ec224f8dbe8c...` |
| `requirements.txt` | 107 | `4f3ce23577319087...` |
| `models/naive_bayes_model.joblib` | 837.191 | `c5fae4ca58f553f4...` |
| `models/tfidf_vectorizer.joblib` | 270.438 | `e5bc68846fd253b2...` |
| `models/class_names.joblib` | 86 | `ef09a5bebe816823...` |
| `presentation/phan-loai-van-ban-naive-bayes-v2.pptx` | 42.765 | `63b8606ffc6b5412...` |
| `results/evaluation_summary.json` | 1.897 | `ba6f29910d6a4574...` |
| `results/alpha_tuning.json` | 2.496 | `321484be7b38d35e...` |
| `results/error_analysis.json` | 5.437 | `8e030b42fbb1bf4f...` |
| `src/classifier_service.py` | 11.842 | `001da66eb3e6d1eb...` |
| `src/config.py` | 3.553 | `1bfa11b93f77341d...` |
| `tests/test_pipeline.py` | 7.306 | `86ca8e14e134b225...` |
| `tests/test_inference.py` | 2.368 | `2e04e9c70014b2d5...` |
| `docs/bao-cao.md` | 14.951 | `ec62b083c5098ffb...` |
| `docs/thuyet-trinh.md` | 4.193 | `5f0b5d03831b7ad2...` |
| `docs/NGHIEM_THU.md` | 6.464 | `11603baefdfc1110...` |
| `docs/CI_VERIFICATION.md` | 3.368 | `a5f8ee4a938c5d2c...` |
| `docs/RELEASE_NOTES_v1.0.1.md` | 6.677 | `dd069612c9bf20c3...` |

*(Chi tiết đầy đủ 42 tệp được lưu trữ tại `release/MANIFEST.json` và `release/CHECKSUMS.sha256`)*.

---

## 2. Hướng dẫn xác thực tính toàn vẹn độc lập

Người dùng hoặc hội đồng chấm thi có thể kiểm tra tính toàn vẹn của tệp tải về bằng công cụ dòng lệnh:

### Trên Windows PowerShell:
```powershell
Get-FileHash -Path release\phan-loai-van-ban-naive-bayes-final-submission.zip -Algorithm SHA256
```
So sánh chuỗi mã băm hiển thị với giá trị đã công bố ở trên.

### Trên Linux / macOS:
```bash
sha256sum -c release/CHECKSUMS.sha256
```
Kết quả mong đợi: `OK` cho mọi tệp tin thành phần.
