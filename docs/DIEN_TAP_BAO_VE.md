# Kịch bản diễn tập bảo vệ đề tài nhóm 3 thành viên (7–10 phút)

- **Đề tài**: Phân loại văn bản đa lớp bằng Multinomial Naive Bayes
- **Học phần**: Trí tuệ nhân tạo (AI)
- **Tổng thời lượng diễn tập chuẩn**: **9 phút** (Khung quy định: 7 – 10 phút)
- **Tệp trình chiếu**: [`presentation/phan-loai-van-ban-naive-bayes-v2.pptx`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/presentation/phan-loai-van-ban-naive-bayes-v2.pptx)
- **Ứng dụng Demo**: Trực tuyến tại [Streamlit Cloud](https://phan-loai-van-ban-naive-bayes.streamlit.app) / Ngoại tuyến tại `http://localhost:8501`

---

## 1. Bảng phân công vai trò và phân bổ thời gian

| Thành viên | Vai trò phụ trách | Slide trình bày | Thời lượng | Trọng tâm nội dung |
| :---: | :--- | :---: | :---: | :--- |
| **Thành viên 1** | Điều phối & Bối cảnh bài toán | Slide 1 – 3 | **2 phút 15 giây** | Giới thiệu đề tài, mục tiêu, dữ liệu 20 Newsgroups (4 lớp), kỹ thuật lọc metadata chống rò rỉ và quy trình phân loại tổng thể. |
| **Thành viên 2** | Cơ sở lý thuyết & Thuật toán | Slide 4 – 6 | **2 phút 45 giây** | Biểu diễn TF-IDF 13.068 chiều, công thức định lý Bayes, tính toán miền Log-sum, cơ chế làm trơn Laplace/Lidstone và ví dụ tính tay. |
| **Thành viên 3** | Thực nghiệm & Demo sản phẩm | Slide 7 – 10 | **4 phút 00 giây** | Stratified 5-Fold CV chọn `alpha=0.1`, Test Accuracy 88,52%, Macro F1 88,33%, phân tích lỗi, thao tác trực tiếp trên giao diện Streamlit và kết luận. |

---

## 2. Kịch bản chi tiết từng phút và lời thoại diễn tập

### Phần 1: Thành viên 1 – Đặt vấn đề và Thiết kế quy trình (0:00 – 2:15)

- **Slide 1: Bìa đề tài (0:00 - 0:30)**
  - *Lời thoại*: "Kính thưa quý thầy cô trong hội đồng và các bạn sinh viên, hôm nay nhóm 3 thành viên chúng em xin phép được báo cáo đề tài môn học Trí tuệ nhân tạo: **Phân loại văn bản đa lớp bằng Naive Bayes đa thức (Multinomial Naive Bayes)**."
  - *Mục tiêu*: Xây dựng trọn vẹn pipeline học máy từ thu thập, tiền xử lý, trích xuất đặc trưng TF-IDF đến mô hình hóa, giải thích quyết định và đóng gói giao diện web tương tác.

- **Slide 2: Bài toán và Dữ liệu thực nghiệm (0:30 - 1:15)**
  - *Lời thoại*: "Bài toán đặt ra là phân loại một văn bản tiếng Anh vào đúng một trong 4 chủ đề của bộ dữ liệu chuẩn **20 Newsgroups**: `comp.graphics` (Đồ họa máy tính), `rec.sport.baseball` (Bóng chày), `sci.space` (Khoa học vũ trụ) và `talk.politics.misc` (Chính trị tổng hợp). Tổng cộng 3.729 mẫu, phân chia thành 2.239 mẫu train và 1.490 mẫu test độc lập."
  - *Nhấn mạnh*: "Nhóm chủ động loại bỏ headers, footers và quotes để ngăn mô hình học vẹt tên tác giả hay địa chỉ email (chống data leakage)."

- **Slide 3: Quy trình phân loại học máy (1:15 - 2:00)**
  - *Lời thoại*: "Quy trình xử lý gồm 4 bước: Văn bản thô $\rightarrow$ Véc-tơ hóa $\rightarrow$ Tính điểm Naive Bayes $\rightarrow$ Nhãn dự đoán. Nguyên tắc vàng của nhóm: Bộ từ vựng và IDF chỉ được `fit` trên tập train; tập test chỉ được `transform`."

- **Câu chuyển phần (2:00 - 2:15)**:
  - *Lời thoại*: *"Tiếp theo, bạn [Tên Thành viên 2] sẽ trình bày chi tiết về cơ sở toán học và cơ chế tính toán xác suất của thuật toán Naive Bayes."*

---

### Phần 2: Thành viên 2 – Lý thuyết toán học và Cơ chế làm trơn (2:15 – 5:00)

- **Slide 4: Hai cách biểu diễn văn bản (2:15 - 3:00)**
  - *Lời thoại*: "Máy học chỉ làm việc với số. Nhóm nghiên cứu hai phương pháp biểu diễn: Bag of Words (đếm tần suất) và TF-IDF. TF-IDF có ưu thế vượt trội khi vừa ghi nhận tần suất từ cục bộ (TF), vừa phạt các từ xuất hiện đại trà trong nhiều tài liệu (IDF) để tôn vinh các từ khóa đặc trưng như *orbit*, *pitcher*, *polygon*."

- **Slide 5: Mô hình Multinomial Naive Bayes (3:00 - 3:45)**
  - *Lời thoại*: "Dựa trên định lý Bayes, mô hình tìm lớp $c$ tối đa hóa xác suất hậu nghiệm $P(c|d)$. Nhóm áp dụng giả định độc lập có điều kiện giữa các từ trong văn bản để chuyển phép nhân xác suất thành phép cộng trong miền log-sum: $\text{score}(c, x) = \log P(c) + \sum x_i \log \theta_{c,i}$. Kỹ thuật làm trơn Laplace với siêu tham số $\alpha$ giúp loại bỏ triệt để lỗi xác suất bằng 0 khi gặp từ mới."

- **Slide 6: Ví dụ tính tay minh họa (3:45 - 4:45)**
  - *Lời thoại*: "Để kiểm chứng công thức, nhóm xây dựng ví dụ tính tay với câu 'bóng đá mới'. Điểm Thể thao tính được là $9/5488$, lớn hơn Công nghệ $2/5488$, chứng minh mô hình hoạt động chính xác theo nguyên lý toán học."

- **Câu chuyển phần (4:45 - 5:00)**:
  - *Lời thoại*: *"Sau đây, bạn [Tên Thành viên 3] sẽ báo cáo kết quả thực nghiệm tối ưu siêu tham số, phân tích lỗi và trực tiếp demo ứng dụng sản phẩm."*

---

### Phần 3: Thành viên 3 – Thực nghiệm, Demo Streamlit và Kết luận (5:00 – 9:00)

- **Slide 7: Thiết kế thực nghiệm & Tối ưu Alpha (5:00 - 5:40)**
  - *Lời thoại*: "Nhóm không thử sai trên tập test mà áp dụng **Stratified 5-Fold Cross-Validation hoàn toàn trên 2.239 mẫu train** qua 8 giá trị alpha. Kết quả thực nghiệm khẳng định `alpha = 0.1` đạt điểm Macro F1 cao nhất là **90,28%**."

- **Slide 8: Kết quả đánh giá trên tập kiểm thử Test (5:40 - 6:20)**
  - *Lời thoại*: "Khi đánh giá mô hình cuối cùng trên 1.490 mẫu test: Mô hình đạt **Accuracy 88,52%** (tăng +1,34% so với mô hình cơ sở $\alpha=1.0$) và **Macro F1 đạt 88,33%** (tăng +1,46%). Độ nhạy Recall của lớp Chính trị tăng vọt từ 75,8% lên 85,16%."

- **Slide 9: Phân tích lỗi thực nghiệm (6:20 - 7:00)**
  - *Lời thoại*: "Phân tích 171 mẫu dự đoán sai chỉ ra: 60 văn bản quá ngắn (dưới 2 từ vựng TF-IDF) có tỷ lệ lỗi lên tới 53,33%. Đặc biệt, nhóm thiết lập ngưỡng cảnh báo độ tin cậy thấp (< 60%), nơi tỷ lệ lỗi chiếm tới 44,36% để cảnh báo người dùng cuối."

- **Trình diễn ứng dụng Demo thực tế (7:00 - 8:30)**:
  - *Thao tác*: Mở trình duyệt tại [Streamlit Cloud](https://phan-loai-van-ban-naive-bayes.streamlit.app) (hoặc localhost:8501).
  - *Bước 1 (Dự đoán chuẩn)*: Chọn bài mẫu 'Khoa học vũ trụ' $\rightarrow$ Bấm **🚀 Phân loại** $\rightarrow$ Hệ thống phản hồi tức thì trong **2,4 ms**, độ tin cậy **99,9%**.
  - *Bước 2 (Giải thích đặc trưng)*: Cuộn xuống bảng Explainability, chỉ cho hội đồng thấy các từ khóa đóng góp biên log-odds như `space`, `satellite`, `orbit`.
  - *Bước 3 (Cảnh báo thông minh)*: Thử nhập câu mơ hồ ngắn hoặc từ OOV để hệ thống hiển thị cảnh báo UX màu vàng.
  - *Bước 4 (Xuất dữ liệu)*: Nhấn nút **Tải file CSV lịch sử dự đoán**.

- **Slide 10: Kết luận & Đóng gói sản phẩm (8:30 - 9:00)**
  - *Lời thoại*: "Dự án đã vượt qua toàn bộ **16/16 kiểm thử tự động pytest**, tích hợp CI Pipeline xanh trên GitHub Actions, xuất bản phiên bản phát hành chính thức `v1.0.2` kèm gói nộp độc lập 660 KB. Nhóm em xin chân thành cảm ơn quý thầy cô và xin sẵn sàng lắng nghe câu hỏi phản biện!"

---

## 3. Quy trình chuyển đổi và xử lý sự cố mạng (Contingency Plan)

1. **Sự cố mất kết nối mạng hoặc Streamlit Cloud phản hồi chậm**:
   - Thành viên 3 giữ bình tĩnh, thông báo: *"Thưa thầy cô, để đảm bảo tốc độ phản hồi tối đa, em xin phép chuyển sang giao diện chạy trực tiếp trên máy cục bộ."*
   - Chuyển sang tab trình duyệt `http://localhost:8501` đã khởi động sẵn trong nền.
   - Thao tác tiếp tục diễn ra liền mạch, không bị gián đoạn thời gian bảo vệ.

2. **Quy tắc phối hợp giữa các thành viên**:
   - Khi một thành viên đang nói, thành viên kế tiếp đứng ở tư thế sẵn sàng, theo dõi thời gian qua đồng hồ bấm giờ.
   - Nếu thành viên trước nói quá thời gian quy định > 30 giây, thành viên điều phối ra hiệu tay kín đáo để tóm lược nhanh và chuyển phần.
