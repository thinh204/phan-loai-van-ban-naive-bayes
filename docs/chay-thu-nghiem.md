# Cách chạy thực nghiệm và ứng dụng

Dự án yêu cầu Python 3.10 trở lên. Dữ liệu 20 Newsgroups được lưu trữ trong `data/cache` và không đưa lên Git.

## 1. Cài đặt môi trường

Trong thư mục gốc của repository:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Các bước chạy pipeline thực nghiệm

### Giai đoạn 1: Đọc và phân tích dữ liệu với Pandas
```powershell
python src/prepare_data.py
```
Lệnh này đọc dữ liệu, kiểm tra các nhãn, số lượng mẫu, đếm các bản ghi rỗng/khoảng trắng và kiểm tra dữ liệu trùng lặp.

### Giai đoạn 2: Phân chia tập dữ liệu và trích xuất TF-IDF
```powershell
python src/tfidf_pipeline.py
```
Thực hiện chia dữ liệu thành tập Train và Test. Khởi tạo `TfidfVectorizer` với nguyên tắc chống rò rỉ dữ liệu (data leakage) nghiêm ngặt:
- `fit_transform()` chỉ chạy trên `X_train`.
- `transform()` chạy trên `X_test`.
- Kiểm tra tự động không có từ vựng riêng của tập test lọt vào bộ từ vựng train.

### Giai đoạn 3: Huấn luyện và đánh giá Multinomial Naive Bayes
```powershell
python src/train_evaluate.py
```
Huấn luyện mô hình `MultinomialNB(alpha=1.0)` trên đặc trưng TF-IDF của tập train. Đánh giá toàn diện các chỉ số thực tế trên tập test:
- Accuracy, Precision (Macro/Weighted), Recall (Macro/Weighted), F1-Score (Macro/Weighted).
- Xuất Classification Report và Confusion Matrix lưu vào `results/evaluation_summary.json` và `results/confusion_tfidf.csv`.
- Lưu model và vectorizer vào thư mục `models/`.

## 3. Khởi chạy ứng dụng giao diện Web Streamlit
```powershell
streamlit run app.py
```
Truy cập địa chỉ cục bộ: `http://localhost:8501`.

Ứng dụng cho phép:
1. Nhập trực tiếp văn bản tiếng Anh bất kỳ hoặc chọn bài viết mẫu.
2. Nhấn nút **Phân loại**.
3. Chuyển đổi văn bản bằng bộ `TF-IDF` đã được fit từ tập train.
4. Dự đoán nhãn chủ đề và hiển thị biểu đồ phân bố xác suất cho cả 4 lớp.
5. Hiển thị danh sách các từ khóa có trọng số TF-IDF nổi bật nhất trong văn bản.
