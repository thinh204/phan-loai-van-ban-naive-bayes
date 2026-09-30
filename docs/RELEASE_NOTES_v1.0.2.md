# Phiên bản phát hành v1.0.2 – Khắc phục nghiệm thu cuối, tự động hóa đóng gói và diễn tập bảo vệ

**Ngày phát hành:** 30/09/2026  
**Repository:** [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)  
**Phiên bản:** `v1.0.2` (Bản bảo vệ đề tài và nghiệm thu chính thức)  
**Kế thừa từ:** `v1.0.1`  
**Trạng thái kiểm thử:** 16/16 passed | 100% clean-env verified | CI Green

---

## 1. Giới thiệu tổng quan

Phiên bản **v1.0.2** là bản phát hành bảo vệ chính thức (Final Defense Release) của đề tài *Phân loại văn bản đa lớp bằng Multinomial Naive Bayes* (Học phần Trí tuệ nhân tạo). Phiên bản này hoàn thành xuất sắc toàn bộ 8 giai đoạn của **Plan 5**, giải quyết triệt để các vấn đề nghiệm thu cuối cùng, tự động hóa toàn diện quy trình kiểm tra toàn vẹn gói nộp và chuẩn bị kịch bản diễn tập nhóm bảo vệ hoàn chỉnh.

---

## 2. Các điểm cải tiến trọng tâm trong v1.0.2

### 1. Khôi phục và xác minh Demo trực tuyến công khai
- Cấu hình mở công khai repository và ứng dụng trên **Streamlit Community Cloud** tại địa chỉ:  
  👉 **[https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)**
- Ứng dụng đã được xác minh mở thành công từ phiên duyệt web ẩn danh/chưa đăng nhập, người dùng và hội đồng đánh giá có thể truy cập trực tiếp và thực hiện phân loại văn bản mà không bị chuyển hướng tới trang đăng nhập.
- Bổ sung tài liệu hướng dẫn vận hành và cấu hình triển khai tại [docs/DEPLOYMENT.md](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/DEPLOYMENT.md).

### 2. Đồng bộ hóa siêu dữ liệu phiên bản từ một nguồn duy nhất
- Thiết lập module cấu hình phiên bản tập trung tại [`src/config.py`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/src/config.py) với các hằng số:
  - `APP_VERSION = "v1.0.2"`
  - `PLAN_VERSION = "Plan 5"`
  - `FOOTER_CAPTION = "Đề tài AI: Phân loại văn bản Multinomial Naive Bayes | Plan 5 - Release v1.0.2"`
- Đồng bộ giao diện `app.py` ở cả thanh bên (Sidebar) và chân trang (Footer), loại bỏ hoàn toàn các nhãn phiên bản cũ.

### 3. Chuẩn hóa toàn bộ liên kết phát hành
- Rà soát toàn diện và cập nhật các liên kết trong [README.md](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/README.md) và các bản phát hành GitHub Release.
- Chuyển đổi các đường dẫn tương đối thiếu `docs/` thành các liên kết tuyệt đối trỏ chính xác đến mã nguồn và tài liệu trên GitHub, bảo đảm không còn lỗi liên kết gãy (404 Not Found).

### 4. Tự động hóa quy trình đóng gói bài nộp (`scripts/build_package.py`)
- Phát triển kịch bản đóng gói tự động độc lập theo danh sách cho phép (whitelist) rõ ràng.
- Tự động lọc bỏ hoàn toàn các thư mục môi trường ảo `.venv`, bộ nhớ đệm `__pycache__`, `.pytest_cache`, tệp git và tệp rác.
- Tạo gói bài nộp nén ZIP chuẩn mức 9 tại `release/phan-loai-van-ban-naive-bayes-final-submission.zip` với cấu trúc thư mục sạch sẽ, sẵn sàng nộp bài lên hệ thống LMS.

### 5. Kiểm tra toàn vẹn với Manifest và Checksum SHA-256 (`scripts/generate_manifest.py`)
- Kiểm tra tính hợp lệ cấu trúc của tệp nén thông qua `zipfile.testzip()`.
- Tự động trích xuất bảng kiểm kê toàn bộ tệp nộp, kích thước từng tệp và mã băm SHA-256 tại:
  - [release/MANIFEST.json](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/release/MANIFEST.json)
  - [release/CHECKSUMS.sha256](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/release/CHECKSUMS.sha256)
  - [docs/MANIFEST.md](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/MANIFEST.md)

### 6. Xác minh gói nộp trên môi trường sạch độc lập (`scripts/verify_clean_package.py`)
- Thiết lập quy trình tự động giải nén gói ZIP sang thư mục tạm độc lập hoàn toàn với workspace phát triển.
- Biên dịch cú pháp toàn bộ tệp Python (`compileall`) đạt 100% không có lỗi cú pháp.
- Chạy đủ **16/16 bài kiểm thử tự động** (`pytest -v`) đạt kết quả `PASSED`.
- Chạy thử nghiệm luồng suy luận dự đoán đầu-cuối (End-to-End Inference) đạt xác suất cao và chính xác.
- Bằng chứng kiểm thử được ghi nhận đầy đủ tại [docs/CLEAN_ENV_TEST.md](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/CLEAN_ENV_TEST.md).

### 7. Hoàn thiện kịch bản diễn tập nhóm bảo vệ (`docs/DIEN_TAP_BAO_VE.md`)
- Xây dựng kịch bản diễn tập chi tiết cho 3 thành viên với thời lượng chuẩn hóa 9 phút (khung cho phép 7–10 phút):
  - **Thành viên 1 (2 phút 15 giây)**: Bối cảnh, bài toán phân loại văn bản, 4 chủ đề 20 Newsgroups và quy trình tiền xử lý chống rò rỉ dữ liệu.
  - **Thành viên 2 (2 phút 45 giây)**: Không gian đặc trưng TF-IDF 13.068 chiều, mô hình xác suất Naive Bayes, tính toán Log-sum, làm trơn Laplace và ví dụ minh họa bằng tay.
  - **Thành viên 3 (4 phút 00 giây)**: Quy trình 5-Fold Cross-Validation chọn `alpha=0.1`, kết quả kiểm thử trên 1.490 mẫu, demo trực tuyến trên Streamlit và kết luận.
- Kèm lời thoại chi tiết, khẩu lệnh chuyển giao giữa các thành viên và quy trình kích hoạt kịch bản dự phòng ngoại tuyến 100% trong 3 giây nếu mạng hội trường gặp sự cố.

---

## 3. Khóa số liệu thực nghiệm khoa học (Đồng bộ tuyệt đối)

Dự án tuân thủ nghiêm ngặt nguyên tắc khoa học: **không huấn luyện lại, không thay đổi mô hình và không sử dụng tập test để tinh chỉnh tham số**:

| Chỉ số thực nghiệm | Mô hình cơ sở (`alpha=1.0`) | Mô hình tối ưu (`alpha=0.1`) | Mức độ cải thiện |
| :--- | :---: | :---: | :---: |
| **5-Fold Cross-Validation F1** | 89,32% | **91,47%** | **+2,15%** |
| **Test Accuracy** | 87,18% | **88,52%** | **+1,34%** |
| **Test Macro F1** | 86,87% | **88,33%** | **+1,46%** |
| **Test Weighted F1** | 87,09% | **88,49%** | **+1,40%** |
| **Kích thước từ điển TF-IDF** | 13.068 từ khóa | 13.068 từ khóa | Cố định trên tập huấn luyện |
| **Số lượng kiểm thử tự động** | 16/16 passed | 16/16 passed | Đạt 100% |

---

## 4. Danh mục tài liệu và tệp bàn giao chính

- **Mã nguồn ứng dụng & dịch vụ**: [`app.py`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/app.py), [`src/classifier_service.py`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/src/classifier_service.py), [`src/config.py`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/src/config.py)
- **Mô hình & Vectorizer đã huấn luyện**: `models/naive_bayes_model.joblib`, `models/tfidf_vectorizer.joblib`, `models/class_names.joblib`
- **Kết quả thực nghiệm**: [`results/evaluation_summary.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/evaluation_summary.json), `results/alpha_tuning.json`, `results/error_analysis.json`
- **Slide thuyết trình PowerPoint**: [`presentation/phan-loai-van-ban-naive-bayes-v2.pptx`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/presentation/phan-loai-van-ban-naive-bayes-v2.pptx)
- **Kịch bản diễn tập nhóm**: [`docs/DIEN_TAP_BAO_VE.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/DIEN_TAP_BAO_VE.md)
- **Kịch bản Demo trực quan**: [`docs/DEMO_SCRIPT.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/DEMO_SCRIPT.md)
- **Bộ câu hỏi phản biện bảo vệ (Q&A)**: [`docs/DEFENSE_QA.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/DEFENSE_QA.md)
- **Biên bản kiểm thử môi trường sạch**: [`docs/CLEAN_ENV_TEST.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/CLEAN_ENV_TEST.md)
- **Manifest và mã băm toàn vẹn**: [`docs/MANIFEST.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/MANIFEST.md)
- **Gói bài nộp nén chính thức**: `release/phan-loai-van-ban-naive-bayes-final-submission.zip`

---

## 5. Hướng dẫn khởi chạy nhanh

```powershell
# 1. Clone repository
git clone https://github.com/thinh204/phan-loai-van-ban-naive-bayes.git
cd phan-loai-van-ban-naive-bayes

# 2. Khởi tạo và kích hoạt môi trường ảo
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt

# 4. Chạy toàn bộ 16 ca kiểm thử tự động
pytest -v

# 5. Khởi động ứng dụng Streamlit cục bộ
streamlit run app.py
```
Ứng dụng sẽ tự động mở trên trình duyệt tại `http://localhost:8501`.
