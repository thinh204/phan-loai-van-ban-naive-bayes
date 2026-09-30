# Hướng dẫn chạy thực nghiệm và kiểm thử

Tài liệu này mô tả chi tiết quy trình chạy toàn diện các thành phần của hệ thống phân loại văn bản Naive Bayes đa thức, bao gồm kiểm thử tự động, tối ưu siêu tham số, phân tích lỗi và khởi chạy giao diện web.

## 1. Yêu cầu môi trường

- Python 3.10 trở lên.
- Bộ nhớ đệm dữ liệu 20 Newsgroups đặt tại `data/cache`.

Khởi tạo môi trường ảo và cài đặt thư viện:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Kiểm thử tự động với pytest

Hệ thống tích hợp bộ kiểm thử tự động 14 test cases kiểm tra từ việc nạp mô hình, trích xuất đặc trưng, tính xác suất đến xử lý ngoại lệ (văn bản rỗng, từ vựng ngoài từ điển OOV):

```powershell
pytest -v
```

Kết quả mong đợi: `14 passed`.

## 3. Xác thực khả năng tái lập độc lập (Reproducible Setup)

Dự án đã được kiểm chứng độc lập trên môi trường ảo sạch hoàn toàn (`clean environment`) mà không dựa vào bất kỳ thư viện nào cài đặt sẵn ngoài hệ thống:
- **Phiên bản Python xác thực:** Python `3.10.11` (tương thích Python 3.10+).
- **Cài đặt phụ thuộc:** Toàn bộ thư viện được cài đặt tự động từ `requirements.txt` (`scikit-learn==1.7.2`, `pandas>=2.2.0`, `streamlit>=1.40.0`, `pytest>=8.0.0`, `joblib>=1.4.0`, `numpy>=2.0.0`, `scipy>=1.14.0`).
- **Kiểm thử tự động:** `pytest -v` thực thi thành công 14/14 test cases.
- **Khởi động ứng dụng:** Nạp thành công mô hình (`naive_bayes_model.joblib`), vectorizer (`tfidf_vectorizer.joblib`) và tệp kết quả (`evaluation_summary.json`).

## 4. Quy trình thực nghiệm và tối ưu mô hình

### Bước 1: Khảo sát dữ liệu với Pandas
```powershell
python src/prepare_data.py
```
Kiểm tra số lượng mẫu, phân bố 4 lớp, kiểm tra dữ liệu thiếu Null/NaN và các văn bản rỗng sau khi loại bỏ metadata.

### Bước 2: Phân chia tập dữ liệu và trích xuất TF-IDF
```powershell
python src/tfidf_pipeline.py
```
Thực hiện chia dữ liệu và trích xuất đặc trưng TF-IDF đảm bảo nguyên tắc chống rò rỉ dữ liệu (`fit_transform` chỉ trên tập train, `transform` trên tập test).

### Bước 3: Tối ưu hóa siêu tham số Alpha bằng Stratified 5-Fold Cross-Validation
```powershell
python src/tune_alpha.py
```
- Quá trình tìm kiếm `alpha` được thực hiện hoàn toàn trên **tập train** (2.239 mẫu) bằng Stratified 5-Fold Cross-Validation.
- Mỗi fold trong CV đều fit TF-IDF riêng biệt để chống rò rỉ dữ liệu.
- Giá trị tối ưu được chọn là `alpha = 0.1` với điểm CV Macro F1 cao nhất (90.28%).
- Khóa `alpha = 0.1` và huấn luyện mô hình cuối cùng trên toàn bộ tập train, sau đó đánh giá đúng một lần trên tập test (1.490 mẫu), đạt Test Accuracy: **88.52%**, Macro F1: **88.33%**.

### Bước 4: Phân tích lỗi chi tiết trên tập kiểm thử
```powershell
python src/error_analysis.py
```
Xuất báo cáo phân tích lỗi chuyên sâu, khảo sát các mẫu nhầm lẫn, các văn bản có ít từ vựng và các dự đoán có độ tin cậy thấp (< 60%). Kết quả được lưu tại `results/error_analysis.json`.

## 4. Khởi chạy ứng dụng Web Streamlit

```powershell
streamlit run app.py
```

Truy cập địa chỉ cục bộ: `http://localhost:8501`.

Các tính năng nổi bật:
1. **Phân loại văn bản thời gian thực:** Nhập văn bản hoặc chọn bài viết mẫu, nhấn nút **🚀 Phân loại**.
2. **Hiển thị xác suất và độ tin cậy:** Trực quan hóa phân bố xác suất của 4 lớp bằng bảng và biểu đồ cột.
3. **Giải thích mô hình:** Liệt kê các từ khóa có trọng số TF-IDF cao nhất trong câu đầu vào.
4. **Lịch sử phiên làm việc:** Tự động ghi nhận lịch sử các lần phân loại kèm thời gian xử lý (độ trễ ms).
5. **Xuất dữ liệu:** Cho phép người dùng tải toàn bộ lịch sử phân loại về máy dưới dạng tệp CSV.
6. **Chỉ số thực nghiệm động:** Tự động đọc và hiển thị các metric mới nhất từ `results/evaluation_summary.json`.

## 5. Hướng dẫn chạy trên VS Code và Google Colab

### Chạy bằng Visual Studio Code
1. Mở thư mục dự án bằng VS Code (`File -> Open Folder...`).
2. Chọn Python Interpreter: Nhấn `Ctrl + Shift + P`, gõ `Python: Select Interpreter` và trỏ đến `.\.venv\Scripts\python.exe`.
3. Mở terminal tích hợp (`Ctrl + ~`) và chạy:
   ```powershell
   pytest -v
   streamlit run app.py
   ```

### Chạy bằng Google Colab
1. Tạo một notebook mới và clone repository:
   ```python
   !git clone https://github.com/thinh204/phan-loai-van-ban-naive-bayes.git
   %cd phan-loai-van-ban-naive-bayes
   !pip install -r requirements.txt
   !pip install localtunnel
   ```
2. Thực thi kiểm thử và tối ưu hóa:
   ```python
   !pytest -v
   !python src/tune_alpha.py
   ```
3. Chạy ứng dụng Streamlit qua LocalTunnel:
   ```python
   !streamlit run app.py & npx localtunnel --port 8501
   ```
   Mở liên kết `localtunnel.me` được in ra màn hình để truy cập giao diện.
