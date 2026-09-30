# Biên bản xác minh tài sản tải xuống từ GitHub Release (Asset Integrity Verification)

- **Repository**: [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)
- **Phiên bản kiểm tra**: `v1.0.2`
- **Tài sản kiểm tra**: `phan-loai-van-ban-naive-bayes-final-submission.zip`
- **URL tải xuống trực tiếp**: [https://github.com/thinh204/phan-loai-van-ban-naive-bayes/releases/download/v1.0.2/phan-loai-van-ban-naive-bayes-final-submission.zip](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/releases/download/v1.0.2/phan-loai-van-ban-naive-bayes-final-submission.zip)
- **Thời điểm kiểm tra**: 30/09/2026
- **Script tự động hóa**: [scripts/verify_release_asset.py](file:///d:/phan-loai-van-ban-naive-bayes/scripts/verify_release_asset.py)

---

## 1. Kết quả kiểm tra đối chiếu mã băm

| Tiêu chí đối chiếu | Giá trị xác thực | Trạng thái |
| :--- | :--- | :---: |
| **Dung lượng tệp tải về từ GitHub** | `673.099 bytes` (~657.3 KB) | **ĐẠT** |
| **SHA-256 tệp tải về từ GitHub** | `c23a328f48b01ebe4c6609a8a38b587e062f2a4dfa8983b5e9c3fd09457e1842` | **ĐẠT** |
| **SHA-256 tệp cục bộ (Local Package)** | `c23a328f48b01ebe4c6609a8a38b587e062f2a4dfa8983b5e9c3fd09457e1842` | **ĐẠT** |
| **SHA-256 trong release/CHECKSUMS.sha256** | `c23a328f48b01ebe4c6609a8a38b587e062f2a4dfa8983b5e9c3fd09457e1842` | **ĐẠT** |
| **Kiểm tra so khớp chéo** | Khớp tuyệt đối 100% giữa tài sản GitHub và bản nghiệm thu | **ĐẠT** |

---

## 2. Kết luận

Tài sản phát hành đính kèm trên GitHub Release hoàn toàn nguyên vẹn, không bị lỗi truyền tải, khớp từng byte và mã băm SHA-256 với gói nghiệm thu trong kho lưu trữ.
