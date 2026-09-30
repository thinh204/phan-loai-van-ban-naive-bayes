# Phân loại văn bản bằng Naive Bayes đa thức (Multinomial Naive Bayes)

Đề tài môn Trí tuệ nhân tạo của nhóm 3 thành viên. Dự án nghiên cứu phương pháp Multinomial Naive Bayes kết hợp trích xuất đặc trưng TF-IDF trên bài toán phân loại chủ đề văn bản (bộ dữ liệu 20 Newsgroups).

Dự án đã hoàn thành toàn diện các giai đoạn phát triển và nghiệm thu: kiến trúc hướng dịch vụ tách biệt, tối ưu siêu tham số bằng Stratified 5-Fold Cross-Validation, kiểm thử tự động toàn diện với 21 ca kiểm thử `pytest`, tích hợp CI Pipeline trên GitHub Actions, chẩn đoán cảnh báo UX thông minh, giải thích đặc trưng TF-IDF và chuẩn bị triển khai trên nền tảng **Streamlit Community Cloud** kèm gói phát hành chính thức.

---

## Cấu trúc mã nguồn

- `src/config.py`: Quản lý tập trung đường dẫn, nhãn lớp và cấu hình hệ thống.
- `src/classifier_service.py`: Service dự đoán độc lập (nạp mô hình, tiền xử lý, trích xuất TF-IDF, tính xác suất `predict_proba`, trích xuất từ khóa tiêu biểu và chẩn đoán cảnh báo).
- `src/prepare_data.py`: Đọc dataset bằng Pandas, kiểm tra phân bố nhãn, dữ liệu thiếu và trùng lặp.
- `src/tfidf_pipeline.py`: Phân chia train/test và vector hóa TF-IDF nghiêm ngặt không rò rỉ dữ liệu (`fit_transform` chỉ trên train, `transform` trên test).
- `src/tune_alpha.py`: Tối ưu hóa siêu tham số `alpha` bằng Stratified 5-Fold Cross-Validation trên tập train và khóa tham số để đánh giá mô hình cuối cùng trên test set.
- `src/train_evaluate.py`: Huấn luyện và đánh giá mô hình Multinomial Naive Bayes cơ sở (`alpha=1.0`).
- `src/error_analysis.py`: Phân tích lỗi chuyên sâu trên tập test (độ tin cậy thấp, văn bản ít từ vựng, các cặp lớp nhầm lẫn).
- `app.py`: Giao diện web Streamlit nâng cao (phân loại tức thì, hiển thị xác suất, top từ khóa, cảnh báo thông minh, lịch sử phiên, tải file CSV).
- `tests/`: Bộ kiểm thử tự động toàn diện với `pytest` gồm 21 test cases (5 trong `test_pipeline.py`, 16 trong `test_inference.py`, tích hợp kiểm tra tính nhất quán số liệu và tính toàn vẹn phát hành).
- `results/`: Chứa các kết quả thực nghiệm động (`evaluation_summary.json`, `alpha_tuning.json`, `alpha_tuning.csv`, `error_analysis.json`, `confusion_tfidf.csv`).
- `docs/`: Báo cáo lý thuyết, kế hoạch thực hiện, biên bản nghiệm thu, bằng chứng CI, tài liệu triển khai và kịch bản thuyết trình.

---

## Hướng dẫn cài đặt và khởi chạy

### 1. Cài đặt môi trường chuẩn

Khởi tạo môi trường ảo Python (khuyến nghị Python 3.10+) và cài đặt phụ thuộc:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Chạy kiểm thử tự động với pytest

Kiểm tra toàn bộ 21 test cases cho pipeline, mô hình, độ trễ, trường hợp biên và tính nhất quán số liệu:

```powershell
pytest -v
```


### 3. Tối ưu hóa mô hình và phân tích lỗi

```powershell
# Chạy tối ưu hóa tham số alpha bằng Stratified 5-Fold Cross-Validation
python src/tune_alpha.py

# Chạy phân tích lỗi chi tiết trên tập kiểm thử test
python src/error_analysis.py
```

### 4. Khởi chạy giao diện web Streamlit

- **Trải nghiệm trực tuyến (Cloud Demo):** Truy cập trực tiếp tại [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)
  > [!TIP]
  > **Xác nhận nghiệm thu trực tuyến (30/09/2026 - Plan 9):**
  > Website công khai đã được nghiệm thu thực tế toàn diện trên phiên khách độc lập với 13/13 ca kiểm thử đạt (dự đoán 4 chủ đề, xử lý ca biên rỗng/ngắn/OOV, phân tích giải thích đặc trưng TF-IDF, bảng lịch sử và xuất tệp CSV). Chi tiết dữ liệu và ảnh chụp thực tế xem tại [`docs/NGHIEM_THU_PLAN_9.md`](docs/NGHIEM_THU_PLAN_9.md).

- **Chạy cục bộ trên máy (Local Server):**
  ```powershell
  streamlit run app.py
  ```
  Truy cập ứng dụng tại: `http://localhost:8501`. Ứng dụng cung cấp:
  - Ô nhập văn bản tiếng Anh hoặc chọn bài viết mẫu theo 4 chủ đề.
  - Phân loại chủ đề và hiển thị phân bố xác suất trực quan (`predict_proba`).
  - Cảnh báo đầu vào thông minh (độ tin cậy thấp < 60%, văn bản quá ngắn, từ ngoài từ điển OOV).
  - Trích xuất top từ khóa TF-IDF tiêu biểu giải thích cho nhãn dự đoán.
  - Đo lường độ trễ suy diễn (ms) và lưu trữ lịch sử phiên làm việc.
  - Tải toàn bộ bảng lịch sử dự đoán dưới định dạng tệp CSV.


---

## Hướng dẫn chạy trên môi trường khác

### Chạy bằng Visual Studio Code (VS Code)
1. Mở thư mục dự án trong VS Code: `File -> Open Folder...`.
2. Mở Command Palette (`Ctrl + Shift + P`) -> chọn `Python: Select Interpreter` -> chọn trình thông dịch trong `.\.venv\Scripts\python.exe`.
3. Mở Terminal tích hợp (`Ctrl + ~`) và chạy:
   ```powershell
   pytest -v
   streamlit run app.py
   ```

### Chạy bằng Google Colab
1. Nén thư mục repo hoặc clone từ GitHub vào môi trường Colab:
   ```python
   !git clone https://github.com/thinh204/phan-loai-van-ban-naive-bayes.git
   %cd phan-loai-van-ban-naive-bayes
   !pip install -r requirements.txt
   !pip install localtunnel
   ```
2. Chạy kiểm thử và tối ưu:
   ```python
   !pytest -v
   !python src/tune_alpha.py
   ```
3. Chạy giao diện Streamlit với LocalTunnel:
   ```python
   !streamlit run app.py & npx localtunnel --port 8501
   ```

---

## Kết quả thực nghiệm thực tế

Mọi số liệu dưới đây được đo lường trực tiếp từ việc thực thi mã nguồn trên **1.490 mẫu test** (sau khi học từ **2.239 mẫu train**):

### 1. Quá trình chọn siêu tham số Alpha (Stratified 5-Fold CV trên tập Train)

| Giá trị Alpha | CV Accuracy trung bình | CV Macro F1 trung bình | Nhận xét |
| :---: | :---: | :---: | :--- |
| `0.01` | 89.82% (+/- 0.76%) | 89.77% (+/- 0.82%) | Độ trơn thấp |
| `0.05` | 90.26% (+/- 0.90%) | 90.23% (+/- 0.95%) | Hiệu năng cao |
| **`0.10`** | **90.26% (+/- 1.02%)** | **90.28% (+/- 1.07%)** | **Tối ưu nhất - Được chọn** |
| `0.20` | 90.17% (+/- 0.86%) | 90.18% (+/- 0.91%) | Ổn định |
| `0.50` | 89.73% (+/- 0.40%) | 89.73% (+/- 0.37%) | Giảm nhẹ |
| `1.00` | 88.61% (+/- 0.51%) | 88.55% (+/- 0.49%) | Mức Laplace mặc định |
| `1.50` | 87.40% (+/- 1.06%) | 87.25% (+/- 1.15%) | Quá trơn |
| `2.00` | 85.93% (+/- 1.23%) | 85.53% (+/- 1.35%) | Điểm số giảm rõ rệt |

### 2. Đánh giá mô hình tối ưu trên tập kiểm thử Test (Alpha = 0.1)

| Chỉ số đánh giá | Trước tối ưu (`alpha=1.0`) | **Sau tối ưu (`alpha=0.1`)** | Mức cải thiện |
| :--- | :---: | :---: | :---: |
| **Test Accuracy** | 87.18% | **88.52%** | **+1.34%** |
| **Macro Precision** | 87.63% | **88.41%** | **+0.78%** |
| **Weighted Precision** | 87.42% | **88.57%** | **+1.15%** |
| **Macro Recall** | 86.57% | **88.35%** | **+1.78%** |
| **Weighted Recall** | 87.18% | **88.52%** | **+1.34%** |
| **Macro F1-Score** | 86.87% | **88.33%** | **+1.46%** |
| **Weighted F1-Score** | 87.09% | **88.49%** | **+1.40%** |

### 3. Chi tiết Classification Report theo từng lớp (`alpha=0.1`)

| Chủ đề (Class) | Precision | Recall | F1-Score | Số mẫu test (Support) |
| :--- | :---: | :---: | :---: | :---: |
| `comp.graphics` | 0.9297 | 0.9177 | 0.9237 | 389 |
| `rec.sport.baseball` | 0.8685 | 0.9320 | 0.8991 | 397 |
| `sci.space` | 0.8865 | 0.8325 | 0.8586 | 394 |
| `talk.politics.misc` | 0.8516 | 0.8516 | 0.8516 | 310 |

---

## Phân tích lỗi thực nghiệm

Phân tích trên 1.490 mẫu test thực tế ([`results/error_analysis.json`](results/error_analysis.json)):
- **Dự đoán đúng:** 1.319 mẫu (**88.52%**)
- **Dự đoán sai:** 171 mẫu (**11.48%**)
- **Các cặp lớp thường nhầm lẫn nhất:**
  1. `sci.space` -> `rec.sport.baseball` (25 lần) & `sci.space` -> `talk.politics.misc` (25 lần)
  2. `talk.politics.misc` -> `sci.space` (23 lần) & `talk.politics.misc` -> `rec.sport.baseball` (19 lần)
  3. `sci.space` -> `comp.graphics` (16 lần)
- **Tác động của độ dài văn bản và từ vựng:** 60 mẫu có ít hơn hoặc bằng 2 từ vựng TF-IDF (do lọc bỏ header/footer/quote) có tỷ lệ lỗi lên tới **53.33%** (so với chỉ 9.72% ở các văn bản bình thường).
- **Phân tích độ tin cậy thấp (ngưỡng < 60%):** Có 266 mẫu có độ tin cậy < 60%; tỷ lệ dự đoán sai trong nhóm này lên đến **44.36%** (so với chỉ 4.33% ở nhóm có độ tin cậy >= 60%).

---

## Tài liệu liên quan
 
- [Kế hoạch và phân công](docs/ke-hoach.md)
- [Plan 3: Đóng gói, triển khai và chuẩn bị bảo vệ](docs/plan-3.md)
- [Plan 4: Nghiệm thu, triển khai chính thức và đóng gói bài nộp](docs/plan-4.md)
- [Plan 5: Khắc phục nghiệm thu cuối và diễn tập bảo vệ](docs/plan-5.md)
- [Plan 6: Sửa sai lệch cuối và khóa bản nộp có thể kiểm chứng](docs/plan-6.md)
- [Plan 7: Hoàn tất website công khai và phát hành v1.0.3](docs/plan-7.md)
- [Plan 8: Khôi phục website công khai và nghiệm thu bằng bằng chứng thực tế](docs/plan-8.md)
- [Plan 9: Nghiệm thu website đang chạy và chốt bản nộp](docs/plan-9.md)
- [Biên bản nghiệm thu website công khai Plan 9](docs/NGHIEM_THU_PLAN_9.md)
- [Biên bản nghiệm thu và chẩn đoán website công khai Plan 8](docs/NGHIEM_THU_PLAN_8.md)
- [Biên bản nghiệm thu chức năng Plan 4](docs/NGHIEM_THU.md)
- [Bằng chứng xác minh CI GitHub Actions](docs/CI_VERIFICATION.md)
- [Hướng dẫn triển khai Streamlit Cloud](docs/DEPLOYMENT.md)
- [Kịch bản Demo tương tác](docs/DEMO_SCRIPT.md)
- [Bộ câu hỏi và trả lời phản biện (Q&A)](docs/DEFENSE_QA.md)
- [Báo cáo lý thuyết và kết quả mở rộng](docs/bao-cao.md)
- [Kịch bản thuyết trình và slide bảo vệ](docs/thuyet-trinh.md)
- [Kịch bản diễn tập nhóm bảo vệ (7–10 phút)](docs/DIEN_TAP_BAO_VE.md)
- [Danh mục kiểm tra đóng gói bài nộp](docs/CHECKLIST_NOP_BAI.md)
- [Ghi chú phát hành phiên bản v1.0.1](docs/RELEASE_NOTES_v1.0.1.md)



