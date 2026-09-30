# Release Notes - v1.0.0: Hệ Thống Phân Loại Văn Bản Multinomial Naive Bayes

Phiên bản chính thức **v1.0.0** đánh dấu sự hoàn thiện toàn diện của đề tài môn học Trí tuệ Nhân tạo: xây dựng hệ thống phân loại văn bản đa lớp bằng Multinomial Naive Bayes và TF-IDF trên bộ dữ liệu 20 Newsgroups (4 chủ đề).

---

## 🚀 Các tính năng nổi bật trong bản phát hành v1.0.0

### 1. Kiến trúc phân tầng và chuẩn hóa dịch vụ
- Tách biệt hoàn toàn tầng suy luận với `TextClassifierService` (`src/classifier_service.py`), giúp mã nguồn độc lập, dễ kiểm thử và sẵn sàng tích hợp API.
- Quản lý tập trung mọi đường dẫn, nhãn lớp và tham số hệ thống trong `src/config.py`.

### 2. Tối ưu hóa siêu tham số chuẩn mực
- Tối ưu hóa tham số làm trơn Laplace/Lidstone bằng **Stratified 5-Fold Cross-Validation** hoàn toàn trên tập train.
- Tìm ra giá trị tối ưu `alpha = 0.1` với điểm CV Macro F1 đạt **90.28%**.
- Nâng cao hiệu năng trên tập test 1.490 mẫu: **Test Accuracy đạt 88.52%** (+1.34%) và **Macro F1 đạt 88.33%** (+1.46%).

### 3. Cơ chế giải thích đặc trưng (Explainability) & Cảnh báo độ tin cậy
- Tính toán mức đóng góp log-odds của từng từ khóa đối với lớp được dự đoán, giúp người dùng hiểu rõ căn cứ đưa ra quyết định của mô hình.
- Tự động nhận diện các trường hợp biên: văn bản rỗng, văn bản quá ngắn, từ vựng ngoài từ điển (OOV) hoặc độ tin cậy thấp (< 60%) và hiển thị cảnh báo giao diện rõ ràng.

### 4. Giao diện Web tương tác Streamlit chuyên nghiệp
- Bố cục 4 Tab chuyên biệt phục vụ demo và thuyết trình:
  - **Tab 1 - Dự đoán & Giải thích:** Ô nhập văn bản, phân loại thời gian thực, đo độ trễ xử lý (ms), bảng/biểu đồ phân bố xác suất 4 lớp, bảng từ khóa đóng góp, lịch sử phiên và nút tải file CSV.
  - **Tab 2 - Giới thiệu mô hình:** Trình bày trực quan quy trình pipeline, cơ sở lý thuyết Bayes và nguyên tắc làm trơn.
  - **Tab 3 - Đánh giá thực nghiệm:** Nạp động kết quả từ `results/evaluation_summary.json` và bảng so sánh 8 giá trị alpha từ `results/alpha_tuning.json`.
  - **Tab 4 - Giới hạn & Lưu ý:** Nêu rõ các ranh giới phương pháp luận và lưu ý thực tiễn.
- Cấu hình sẵn sàng cho **Streamlit Community Cloud** (`.streamlit/config.toml`).

### 5. Kiểm thử tự động & Tích hợp liên tục (CI)
- Bộ kiểm thử tự động 16 test cases toàn diện với `pytest` (`tests/test_pipeline.py`).
- Pipeline GitHub Actions CI (`.github/workflows/ci.yml`) tự động kiểm tra cú pháp, import và chạy test trên cả Python 3.10 và 3.11 khi có `push` hoặc `pull_request`.

### 6. Bộ tài liệu bảo vệ đề tài hoàn chỉnh
- Kịch bản thuyết trình chi tiết 5–7 phút: `docs/DEMO_SCRIPT.md`.
- Bộ câu hỏi và câu trả lời phản biện chuyên sâu trước hội đồng: `docs/DEFENSE_QA.md`.
- Hướng dẫn triển khai trực tuyến Streamlit Cloud: `docs/DEPLOYMENT.md`.

---

## 📊 Bảng tổng hợp chỉ số thực nghiệm v1.0.0

| Chỉ số đánh giá | Kết quả thực tế |
| :--- | :---: |
| **Tập dữ liệu** | 20 Newsgroups (4 chủ đề: Graphics, Baseball, Space, Politics) |
| **Số lượng mẫu** | 2.239 mẫu train / 1.490 mẫu test |
| **Kích thước từ vựng TF-IDF** | 13.068 đặc trưng |
| **Siêu tham số tối ưu** | `alpha = 0.1` (chọn qua Stratified 5-Fold CV trên train) |
| **Test Accuracy** | **88.52%** (1.319 / 1.490 mẫu đúng) |
| **Test Macro F1** | **88.33%** |
| **Test Macro Precision** | **88.41%** |
| **Test Macro Recall** | **88.35%** |
| **Độ trễ suy luận trung bình** | ~2.5 ms / lượt dự đoán |
| **Kiểm thử tự động (pytest)** | **16 / 16 PASSED** |

---

## 🛠️ Hướng dẫn cài đặt và sử dụng

```powershell
# 1. Khởi tạo môi trường ảo
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Cài đặt phụ thuộc
pip install -r requirements.txt

# 3. Chạy kiểm thử tự động
pytest -v

# 4. Khởi chạy ứng dụng Streamlit
streamlit run app.py
```
