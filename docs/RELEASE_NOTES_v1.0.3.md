# Phiên bản phát hành v1.0.3 – Khóa bản nộp cuối có thể kiểm chứng

**Ngày phát hành:** 30/09/2026  
**Repository:** [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)  
**Phiên bản:** `v1.0.3` (Bản khóa nộp bài và bảo vệ đề tài chính thức)  
**Kế thừa từ:** `v1.0.2`  
**Trạng thái kiểm thử:** 21/21 passed (100% ĐẠT) | Môi trường ảo sạch 100% | CI Green | Checksum Verified

---

## 1. Giới thiệu tổng quan

Phiên bản **v1.0.3** là bản phát hành nghiệm thu và đóng băng cuối cùng (Final Locked Release) của đề tài *Phân loại văn bản đa lớp bằng Multinomial Naive Bayes* (Học phần Trí tuệ nhân tạo). Phiên bản này hoàn thành trọn vẹn toàn bộ 8 giai đoạn của **Plan 6**, khắc phục triệt để mọi sai lệch số liệu, kiểm chứng khả năng tái lập trong môi trường Python ảo mới hoàn toàn và thiết lập cơ chế kiểm tra nhất quán tự động trên CI.

---

## 2. Các cải tiến và nghiệm thu cốt lõi trong v1.0.3

### 1. Chuẩn hóa số liệu thực nghiệm khoa học từ dữ liệu gốc
- Rà soát và sửa đổi toàn bộ các tài liệu phát hành, đối chiếu trực tiếp từ tệp kết quả gốc [`results/alpha_tuning.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/alpha_tuning.json):
  - **Mô hình cơ sở (`alpha=1.0`)**: 5-Fold Cross-Validation Macro F1 đạt **88,55%** theo đúng dữ liệu gốc.
  - **Mô hình tối ưu (`alpha=0.1`)**: 5-Fold Cross-Validation Macro F1 đạt **90,28%** theo đúng dữ liệu gốc.
  - **Mức độ cải thiện thực tế**: **+1,73%** điểm Macro F1 trên tập huấn luyện 2.239 mẫu.
- Đồng bộ mô tả GitHub Release và các tài liệu liên quan.

### 2. Tái lập kiểm định gói nộp trong môi trường Python ảo hoàn toàn mới
- Nâng cấp kịch bản [`scripts/verify_clean_package.py`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/scripts/verify_clean_package.py):
  - Tự động tạo một virtual environment độc lập (`python -m venv`) trong thư mục tạm.
  - Kiểm tra điều kiện nghiêm ngặt: `assert WORKSPACE_VENV not in isolated_python.parents` (khẳng định tuyệt đối không dùng `.venv` của workspace).
  - Cài đặt toàn bộ thư viện phụ thuộc bằng `pip install -r requirements.txt`.
  - Thực thi biên dịch cú pháp (`compileall`), chạy toàn bộ bài kiểm thử tự động và thực hiện suy diễn phân loại câu mới (`sci.space`, độ tin cậy 99,96%).
  - Bằng chứng kiểm thử được ghi nhận tại [`docs/CLEAN_ENV_TEST.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/CLEAN_ENV_TEST.md).

### 3. Tự động xác minh tài sản tải xuống từ GitHub Release (`scripts/verify_release_asset.py`)
- Xây dựng công cụ kiểm tra tự động tải gói nén trực tiếp từ GitHub Release qua giao thức HTTPS.
- Tính toán mã băm SHA-256 của tệp tải về và đối chiếu tự động với gói nộp trong kho lưu trữ và [`release/CHECKSUMS.sha256`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/release/CHECKSUMS.sha256).
- Kết quả kiểm chứng xác nhận khớp từng byte và trùng khớp 100% mã băm SHA-256 tại [`docs/RELEASE_ASSET_VERIFICATION.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/RELEASE_ASSET_VERIFICATION.md).

### 4. Tích hợp kiểm tra tính nhất quán tài liệu tự động trên CI (`tests/test_release_consistency.py`)
- Bổ sung 5 bài kiểm thử tự động kiểm tra tính nhất quán số liệu và cấu trúc phát hành (nâng tổng số test cases lên **21 bài kiểm thử**):
  - `test_version_configuration_consistency`: Kiểm tra biến phiên bản tập trung giữa `src/config.py` và `app.py`.
  - `test_ground_truth_metrics_integrity`: Đối chiếu số liệu trong mã nguồn với `results/evaluation_summary.json` và `results/alpha_tuning.json`.
  - `test_no_stale_cv_metrics_in_release_notes`: Ngăn chặn mọi sai lệch số liệu CV Macro F1 trong tài liệu phát hành.
  - `test_manifest_and_checksums_sync`: Đảm bảo mọi tệp ghi trong `MANIFEST.json` đều tồn tại và hợp lệ.
  - `test_deployment_url_consistency`: Xác minh định dạng URL triển khai thống nhất.
- Bất kỳ sự sai lệch nào giữa tài liệu và số liệu gốc sẽ làm quy trình CI báo lỗi (Fail) ngay lập tức.

### 5. Hoàn thiện Checklist trước ngày bảo vệ đề tài (`docs/CHECKLIST_NGAY_BAO_VE.md`)
- Kiểm tra toàn diện trên máy trình chiếu bảo vệ:
  - 10 slide PowerPoint chuẩn hóa ([`presentation/phan-loai-van-ban-naive-bayes-v2.pptx`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/presentation/phan-loai-van-ban-naive-bayes-v2.pptx)).
  - Phân bổ thời lượng chuẩn hóa 9 phút cho 3 thành viên (khung 7–10 phút).
  - Phương án dự phòng ngoại tuyến (Offline Contingency Plan) sẵn sàng chuyển sang `http://localhost:8501` trong 3 giây khi hội trường gặp sự cố mạng.
  - Bộ câu hỏi phản biện 12 nhóm chuyên sâu ([`docs/DEFENSE_QA.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/DEFENSE_QA.md)).

---

## 3. Khóa số liệu thực nghiệm khoa học chính thức

| Chỉ số thực nghiệm | Mô hình cơ sở (`alpha=1.0`) | Mô hình tối ưu (`alpha=0.1`) | Mức độ cải thiện | Nguồn dữ liệu gốc |
| :--- | :---: | :---: | :---: | :--- |
| **5-Fold Cross-Validation Macro F1** | **88,55%** | **90,28%** | **+1,73%** | [`results/alpha_tuning.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/alpha_tuning.json) |
| **5-Fold Cross-Validation Accuracy** | 88,61% | 90,26% | +1,65% | [`results/alpha_tuning.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/alpha_tuning.json) |
| **Test Accuracy** | 87,18% | **88,52%** | +1,34% | [`results/evaluation_summary.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/evaluation_summary.json) |
| **Test Macro F1** | 86,87% | **88,33%** | +1,46% | [`results/evaluation_summary.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/evaluation_summary.json) |
| **Test Weighted F1** | 87,09% | **88,49%** | +1,40% | [`results/evaluation_summary.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/evaluation_summary.json) |
| **Không gian đặc trưng TF-IDF** | 13.068 đặc trưng | 13.068 đặc trưng | Cố định trên tập train | [`models/tfidf_vectorizer.joblib`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/models/tfidf_vectorizer.joblib) |
| **Số lượng kiểm thử tự động** | 21/21 passed | 21/21 passed | Đạt 100% | [`tests/`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/tests/) |

---

## 4. Hướng dẫn cài đặt và xác minh nhanh

```powershell
# 1. Clone repository
git clone https://github.com/thinh204/phan-loai-van-ban-naive-bayes.git
cd phan-loai-van-ban-naive-bayes

# 2. Khởi tạo môi trường ảo mới
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Cài đặt các gói phụ thuộc
pip install -r requirements.txt

# 4. Chạy toàn bộ 21 ca kiểm thử tự động (100% passed)
pytest -v

# 5. Khởi chạy ứng dụng Streamlit cục bộ
streamlit run app.py
```
Ứng dụng sẽ tự động mở trên trình duyệt tại `http://localhost:8501`.
