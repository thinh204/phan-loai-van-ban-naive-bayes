# Đồ án môn Trí tuệ nhân tạo

## Nghiên cứu và trình bày phương pháp phân loại văn bản bằng Multinomial Naive Bayes

Đồ án của nhóm **3 thành viên**, nghiên cứu cách kết hợp **TF-IDF** và **Multinomial Naive Bayes** để phân loại chủ đề văn bản. Dự án gồm cơ sở lý thuyết, mã nguồn thực nghiệm, kết quả đánh giá, giao diện web minh họa và tài liệu thuyết trình.

| Thông tin | Nội dung |
| --- | --- |
| Học phần | Trí tuệ nhân tạo |
| Bài toán | Phân loại văn bản nhiều lớp bằng học có giám sát |
| Phương pháp | TF-IDF + Multinomial Naive Bayes |
| Dữ liệu thực nghiệm | Văn bản tiếng Anh thuộc 4 chủ đề của 20 Newsgroups |
| Ngôn ngữ trình bày | Tiếng Việt |
| Giao diện demo | Streamlit |

**Học viện Công nghệ Bưu chính Viễn thông** · Lớp **D23VHCN01-N**

| Thành viên | MSSV |
| --- | --- |
| Lại Huy Thịnh | N23DVCN057 |
| Nguyễn Trần Mạnh Dũng | N23DVCN01 |
| Nguyễn Hữu Đức | N23DVCN012 |

Giảng viên: ........................................................

**[Mở website demo](https://phan-loai-van-ban-naive-bayes.streamlit.app/)** · **[Đọc báo cáo PDF](docs/bao-cao-do-an.pdf)** · **[Tải slide thuyết trình](presentation/phan-loai-van-ban-naive-bayes-v3.pptx)**

## 1. Mục tiêu đề tài

- Trình bày định lý Bayes, giả định độc lập có điều kiện và cách làm trơn trong Naive Bayes.
- Biểu diễn văn bản dưới dạng đặc trưng số bằng TF-IDF.
- Xây dựng mô hình phân loại, lựa chọn tham số trên tập huấn luyện và đánh giá trên tập kiểm thử riêng.
- Phân tích kết quả, các trường hợp nhầm lẫn và giới hạn của phương pháp.
- Minh họa dự đoán bằng website để phục vụ trình bày và bảo vệ đồ án.

## 2. Phương pháp thực hiện

```text
Văn bản → Tiền xử lý → TF-IDF → Multinomial Naive Bayes → Nhãn dự đoán
```

1. **Tiền xử lý:** loại bỏ header, footer và trích dẫn trong dữ liệu nguồn để giảm tín hiệu nhận diện ngoài nội dung; kiểm tra dữ liệu thiếu, trùng và rỗng.
2. **TF-IDF:** chuyển văn bản thành vector trọng số từ. Bộ từ vựng và trọng số IDF được học trên tập huấn luyện; tập kiểm thử chỉ được biến đổi bằng vectorizer đã học.
3. **Multinomial Naive Bayes:** tính điểm cho mỗi chủ đề từ xác suất tiên nghiệm của lớp và các trọng số đặc trưng. Giả định các đặc trưng độc lập có điều kiện khi biết lớp.
4. **Lựa chọn tham số:** dùng Stratified 5-Fold Cross-Validation trên tập train; TF-IDF được fit riêng trong mỗi fold. Chọn `alpha = 0.1` theo CV Macro F1 rồi huấn luyện mô hình cuối trên toàn bộ tập train.
5. **Đánh giá:** dùng Accuracy, Precision, Recall, F1-score và ma trận nhầm lẫn trên tập test; không dùng tập test để chọn `alpha`.

Cơ sở lý thuyết, công thức và ví dụ tính toán được trình bày trong [báo cáo đề tài](docs/bao-cao.md).

## 3. Dữ liệu và công nghệ

### Dữ liệu thực nghiệm

| Nhãn | Chủ đề | Số mẫu test |
| --- | --- | ---: |
| `comp.graphics` | Đồ họa máy tính | 389 |
| `rec.sport.baseball` | Bóng chày | 397 |
| `sci.space` | Khoa học vũ trụ | 394 |
| `talk.politics.misc` | Chính trị | 310 |

- Tập huấn luyện: **2.239 mẫu**; tập kiểm thử: **1.490 mẫu**.
- Bộ từ vựng TF-IDF của mô hình cuối: **13.068 đặc trưng**.
- Mã tải và kiểm tra dữ liệu: [src/prepare_data.py](src/prepare_data.py).

### Công nghệ sử dụng

| Thành phần | Công nghệ |
| --- | --- |
| Ngôn ngữ | Python |
| Xử lý dữ liệu | Pandas, NumPy |
| TF-IDF, mô hình, chia dữ liệu và đánh giá | scikit-learn |
| Lưu mô hình | Joblib |
| Giao diện web | Streamlit |
| Kiểm thử | pytest, Streamlit AppTest |
| Kiểm tra tự động trên GitHub | GitHub Actions, Python 3.10 và 3.11 |

## 4. Kết quả thực nghiệm

### Đánh giá trên tập test

| Chỉ số | Baseline `alpha = 1.0` | Mô hình chọn `alpha = 0.1` |
| --- | ---: | ---: |
| Accuracy | 87,18% | **88,52%** |
| Macro Precision | 87,63% | **88,41%** |
| Macro Recall | 86,57% | **88,35%** |
| Macro F1-score | 86,87% | **88,33%** |
| Weighted F1-score | 87,09% | **88,49%** |

Mô hình cuối dự đoán đúng **1.319/1.490 mẫu**. So với baseline, Accuracy tăng **1,34 điểm phần trăm**, Macro F1 tăng **1,46 điểm phần trăm**.

### Kết quả theo từng chủ đề của mô hình cuối

| Chủ đề | Precision | Recall | F1-score |
| --- | ---: | ---: | ---: |
| `comp.graphics` | 0,9297 | 0,9177 | 0,9237 |
| `rec.sport.baseball` | 0,8685 | 0,9320 | 0,8991 |
| `sci.space` | 0,8865 | 0,8325 | 0,8586 |
| `talk.politics.misc` | 0,8516 | 0,8516 | 0,8516 |

**CV Macro F1 trên train:** 88,55% với `alpha = 1.0` và 90,28% với `alpha = 0.1`. Đây là kết quả cross-validation, tách biệt với kết quả test ở bảng trên.

Các số liệu có thể đối chiếu tại [evaluation_summary.json](results/evaluation_summary.json), [alpha_tuning.json](results/alpha_tuning.json), [ma trận nhầm lẫn](results/confusion_tfidf.csv) và [phân tích lỗi](results/error_analysis.json).

## 5. Chạy ứng dụng

### Xem demo trực tuyến

Truy cập **[website phân loại văn bản](https://phan-loai-van-ban-naive-bayes.streamlit.app/)**, nhập văn bản tiếng Anh hoặc chọn mẫu và bấm **Phân loại**.

Ứng dụng hiển thị nhãn dự đoán, xác suất của 4 lớp, từ khóa giải thích và lịch sử phiên; hỗ trợ tải lịch sử dưới dạng CSV. Đầu vào rỗng được chặn. Văn bản ngắn, ngoài từ điển hoặc có độ tin cậy thấp được cảnh báo.

### Chạy trên máy Windows

Cài Git và Python **3.10 hoặc 3.11**. Mở PowerShell và chạy:

```powershell
git clone https://github.com/thinh204/phan-loai-van-ban-naive-bayes.git
cd phan-loai-van-ban-naive-bayes
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Mở [http://localhost:8501](http://localhost:8501). Giữ cửa sổ terminal đang chạy; nhấn `Ctrl+C` để dừng. Repo có sẵn mô hình trong `models/`, không cần huấn luyện lại để demo. Cần mạng khi clone và cài thư viện; sau đó có thể dùng localhost làm phương án demo khi mất mạng.

Nếu đã clone, vào thư mục dự án và chạy `git pull origin main` để cập nhật trước khi khởi động. Trong VS Code, mở thư mục này và chọn Python interpreter `.venv`.

### Kiểm thử tự động

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Lần hậu kiểm ngày **01/10/2026** đạt **27/27 kiểm thử**, gồm pipeline, suy diễn, nhập liệu, lịch sử, CSV và tính nhất quán tài liệu phát hành. Xem [GitHub Actions](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/actions) và [biên bản hậu kiểm website](docs/HAU_KIEM_V1.0.4.md).

### Chạy lại thực nghiệm

Thực hiện trong một bản clone riêng nếu muốn đối chiếu kết quả, vì các lệnh sau có thể ghi lại mô hình và tệp kết quả. Lần tải dữ liệu đầu tiên cần Internet.

```powershell
.\.venv\Scripts\python.exe src/prepare_data.py
.\.venv\Scripts\python.exe src/tfidf_pipeline.py
.\.venv\Scripts\python.exe src/tune_alpha.py
.\.venv\Scripts\python.exe src/error_analysis.py
```

`src/train_evaluate.py` cung cấp thực nghiệm baseline. Quy trình lựa chọn tham số và huấn luyện mô hình cuối nằm trong `src/tune_alpha.py`.

## 6. Cấu trúc dự án

```text
phan-loai-van-ban-naive-bayes/
├── app.py              # Giao diện demo Streamlit
├── requirements.txt    # Thư viện cần cài
├── src/                # Xử lý dữ liệu, TF-IDF, huấn luyện và suy diễn
├── models/             # Mô hình, vectorizer và danh sách lớp đã lưu
├── results/            # Chỉ số đánh giá và phân tích lỗi
├── tests/              # Kiểm thử tự động
├── docs/               # Báo cáo, nghiệm thu và kịch bản bảo vệ
├── presentation/       # Slide PowerPoint
├── scripts/            # Đóng gói và xác minh phát hành
└── release/            # Gói nộp, manifest và checksum tại bản phát hành
```

## 7. Tài liệu nộp và bảo vệ đồ án

**Bản Word theo yêu cầu môn Trí tuệ nhân tạo:** [Báo cáo lý thuyết và thiết kế hệ thống của Nhóm 6](docs/BAO_CAO_NHOM_6_MUC_LUC_THEO_MAU_V3.docx). Bản 25 trang trình bày giải thuật, ý tưởng, chức năng, dữ liệu, logic xử lý, giao diện và thư viện; nội dung được đối chiếu với hệ thống hiện có. Giảng viên hướng dẫn còn để trống để nhóm bổ sung.

| Tài liệu | Đường dẫn |
| --- | --- |
| Báo cáo PDF để nộp | [docs/bao-cao-do-an.pdf](docs/bao-cao-do-an.pdf) |
| Báo cáo lý thuyết và thực nghiệm | [docs/bao-cao.md](docs/bao-cao.md) |
| Slide thuyết trình | [presentation/phan-loai-van-ban-naive-bayes-v3.pptx](presentation/phan-loai-van-ban-naive-bayes-v3.pptx) |
| Nội dung thuyết trình | [docs/thuyet-trinh.md](docs/thuyet-trinh.md) |
| Kịch bản demo | [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md) |
| Diễn tập nhóm 3 thành viên | [docs/DIEN_TAP_BAO_VE.md](docs/DIEN_TAP_BAO_VE.md) |
| Câu hỏi phản biện | [docs/DEFENSE_QA.md](docs/DEFENSE_QA.md) |
| Checklist nộp bài | [docs/CHECKLIST_NOP_BAI.md](docs/CHECKLIST_NOP_BAI.md) |
| Nghiệm thu bản sửa lỗi | [docs/NGHIEM_THU_PLAN_10.md](docs/NGHIEM_THU_PLAN_10.md) |
| Hậu kiểm website v1.0.4 | [docs/HAU_KIEM_V1.0.4.md](docs/HAU_KIEM_V1.0.4.md) |

**Phân công đề xuất:** thành viên 1 trình bày bài toán và lý thuyết; thành viên 2 trình bày dữ liệu, thực nghiệm và đánh giá; thành viên 3 demo ứng dụng, phân tích lỗi và giới hạn. Phân công chi tiết trong [kịch bản diễn tập](docs/DIEN_TAP_BAO_VE.md).

### Gói nộp hiện tại

[Gói nguồn và tài liệu đã rà soát](submission/phan-loai-van-ban-naive-bayes-nop-bai.zip) chứa báo cáo PDF, slide v3 và nguồn hiện tại; [manifest](submission/MANIFEST.json) ghi commit nguồn cùng SHA-256 từng tệp. [Checksum](submission/CHECKSUMS.sha256) dùng để kiểm tra gói nộp này. Giảng viên cần được bổ sung trước khi nộp; MSSV được giữ theo thông tin nhóm cung cấp.

### Phiên bản và gói phát hành trước

- [GitHub Release v1.0.4](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/releases/tag/v1.0.4) chứa ZIP, manifest và checksum của commit phát hành `14e88a2`.
- SHA-256 của ZIP: `189918bdc3acaca2bc1e19f22ff370f475ad260b7b9b219ff9fe9ceb3a20d975`.
- Nhánh `main` có thêm sửa xử lý cache trên Cloud, tài liệu hậu kiểm và README nộp đồ án sau bản phát hành. ZIP v1.0.4 không chứa các bổ sung này. Khi nộp nguồn hiện tại, dùng bản clone hoặc [Download ZIP của nhánh main](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/archive/refs/heads/main.zip); checksum Release ở trên chỉ áp dụng cho ZIP phát hành v1.0.4.
- Nhật ký kế hoạch phát triển được giữ trong [thư mục docs](docs/), tách khỏi nội dung chính phục vụ chấm đồ án.

## 8. Giới hạn của đề tài

- Mô hình học văn bản **tiếng Anh** và chỉ phân biệt 4 chủ đề đã chọn; chưa được đánh giá cho văn bản tiếng Việt hoặc chủ đề mới.
- Giả định độc lập của Naive Bayes là sự đơn giản hóa; mô hình chưa biểu diễn đầy đủ ngữ cảnh và quan hệ giữa các từ.
- Xác suất dự đoán là đầu ra của mô hình, không bảo đảm độ đúng tương ứng trên mọi đầu vào. Cảnh báo dưới 60% hỗ trợ người dùng kiểm tra kết quả.
- Văn bản ngắn, thiếu từ trong từ điển hoặc pha trộn chủ đề có thể bị phân loại sai. Từ khóa giải thích phản ánh đặc trưng của mô hình, không phải bằng chứng nhân quả.

## 9. Tài liệu tham khảo

- [Naive Bayes — scikit-learn](https://scikit-learn.org/stable/modules/naive_bayes.html).
- [Trích xuất đặc trưng văn bản — scikit-learn](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction).
- [Bộ dữ liệu 20 Newsgroups — scikit-learn](https://scikit-learn.org/stable/datasets/real_world.html#the-20-newsgroups-text-dataset).

Danh sách tham khảo và phần giải thích chi tiết nằm trong [báo cáo đề tài](docs/bao-cao.md).
