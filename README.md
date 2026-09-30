# Phân loại văn bản bằng Naive Bayes đa thức (Multinomial Naive Bayes)

Đề tài môn Trí tuệ nhân tạo của nhóm 3 thành viên. Dự án giải thích phương pháp Multinomial Naive Bayes kết hợp trích xuất đặc trưng TF-IDF và kiểm chứng trên bài toán phân loại chủ đề văn bản (bộ dữ liệu 20 Newsgroups).

Hệ thống cung cấp pipeline xử lý dữ liệu hoàn chỉnh và **giao diện web trực quan bằng Streamlit** cho phép người dùng phân loại văn bản tức thì.

---

## Cấu trúc mã nguồn

- `src/prepare_data.py`: Đọc dataset bằng Pandas, kiểm tra phân bố nhãn, dữ liệu thiếu và trùng lặp.
- `src/tfidf_pipeline.py`: Chia tập train/test và trích xuất TF-IDF chuẩn xác, kiểm soát tuyệt đối không rò rỉ dữ liệu (chỉ `fit_transform` trên `X_train`, `transform` trên `X_test`).
- `src/train_evaluate.py`: Huấn luyện mô hình `MultinomialNB`, đánh giá toàn diện các chỉ số thực nghiệm và lưu trữ model.
- `app.py`: Giao diện ứng dụng web Streamlit phân loại văn bản trực tiếp.
- `models/`: Chứa mô hình Naive Bayes (`naive_bayes_model.joblib`) và bộ véc-tơ hóa (`tfidf_vectorizer.joblib`).
- `results/`: Báo cáo chỉ số thực tế (`metrics.json`, `evaluation_summary.json`, `confusion_tfidf.csv`).
- `docs/`: Báo cáo chi tiết lý thuyết, kịch bản thuyết trình và hướng dẫn thực nghiệm.

---

## Hướng dẫn cài đặt và sử dụng

### 1. Cài đặt môi trường

Khởi tạo môi trường ảo Python (khuyến nghị Python 3.10+) và cài đặt các phụ thuộc:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Thực thi pipeline dữ liệu và huấn luyện

Bạn có thể chạy kiểm tra từng giai đoạn hoặc chạy toàn bộ pipeline:

```powershell
# Giai đoạn 1: Chuẩn bị và kiểm tra dữ liệu bằng Pandas
python src/prepare_data.py

# Giai đoạn 2: Trích xuất đặc trưng TF-IDF chống rò rỉ dữ liệu
python src/tfidf_pipeline.py

# Giai đoạn 3: Huấn luyện và đánh giá mô hình Naive Bayes
python src/train_evaluate.py
```

### 3. Khởi chạy giao diện web Streamlit

Khởi chạy ứng dụng phân loại văn bản:

```powershell
streamlit run app.py
```

Ứng dụng sẽ mở giao diện tại: `http://localhost:8501`. Người dùng có thể nhập văn bản tùy ý hoặc chọn các đoạn văn mẫu để nhận dự đoán phân loại chủ đề kèm phân bố xác suất chi tiết.

---

## Kết quả thực nghiệm thực tế

Mô hình được đánh giá trên tập kiểm thử độc lập gồm **1.490 mẫu** (huấn luyện trên **2.239 mẫu**):

| Chỉ số đánh giá | Kết quả thực tế |
| :--- | :---: |
| **Accuracy (Độ chính xác tổng thể)** | **87.18%** (0.8718) |
| **Macro Precision** | **87.63%** (0.8763) |
| **Weighted Precision** | **87.42%** (0.8742) |
| **Macro Recall** | **86.57%** (0.8657) |
| **Weighted Recall** | **87.18%** (0.8718) |
| **Macro F1-Score** | **86.87%** (0.8687) |
| **Weighted F1-Score** | **87.09%** (0.8709) |

### Chi tiết từng lớp (Classification Report)

| Chủ đề (Class) | Precision | Recall | F1-Score | Số mẫu test (Support) |
| :--- | :---: | :---: | :---: | :---: |
| `comp.graphics` (Đồ họa máy tính) | 0.9141 | 0.9023 | 0.9082 | 389 |
| `rec.sport.baseball` (Bóng chày) | 0.8644 | 0.9471 | 0.9038 | 397 |
| `sci.space` (Khoa học không gian) | 0.8160 | 0.8553 | 0.8352 | 394 |
| `talk.politics.misc` (Chính trị) | 0.9109 | 0.7581 | 0.8275 | 310 |

---

## Tài liệu liên quan

- [Kế hoạch và phân công](docs/ke-hoach.md)
- [Báo cáo lý thuyết, ví dụ tính tay và kết quả](docs/bao-cao.md)
- [Hướng dẫn chạy thực nghiệm chi tiết](docs/chay-thu-nghiem.md)
- [Slide thuyết trình](presentation/phan-loai-van-ban-naive-bayes-v2.pptx) và [Kịch bản thuyết trình](docs/thuyet-trinh.md)
