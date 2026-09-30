# Kịch bản thuyết trình và Demo đề tài (5–7 phút)

Tài liệu này cung cấp kịch bản chi tiết từng phút cho nhóm sinh viên khi bảo vệ đề tài trước hội đồng giảng viên. Kịch bản được phân chia thành 12 bước logic, có kèm lời thoại gợi ý và thao tác trực tiếp trên giao diện Streamlit.

---

## Bảng phân bổ thời gian (Tổng thời gian: 6 phút 30 giây)

| Thời gian | Mục | Nội dung trọng tâm | Thao tác minh họa |
| :---: | :--- | :--- | :--- |
| **0:00 - 0:30** | 1. Giới thiệu bài toán | Mục tiêu phân loại văn bản tự động, ý nghĩa thực tiễn. | Mở slide / Tab Giới thiệu |
| **0:30 - 1:00** | 2. Dữ liệu thực nghiệm | Bộ dữ liệu chuẩn 20 Newsgroups với 4 chủ đề. | Chỉ số 3.729 mẫu trên slide |
| **1:00 - 1:30** | 3. Tiền xử lý dữ liệu | Loại bỏ header, footer, quote để giảm rò rỉ metadata. | Giải thích lý do lọc dữ liệu |
| **1:30 - 2:00** | 4. Đặc trưng TF-IDF | Chuyển đổi văn bản thành véc-tơ 13.068 chiều. | Minh họa cơ chế TF và IDF |
| **2:00 - 2:45** | 5. Thuật toán MNB | Nguyên lý Bayes, tính toán miền Log và làm trơn Laplace. | Trình bày công thức trên Tab 2 |
| **2:45 - 3:15** | 6. Chống Data Leakage | `fit_transform` chỉ trên train, `transform` trên test. | Nhấn mạnh tính khách quan |
| **3:15 - 3:45** | 7. Tối ưu siêu tham số | Stratified 5-Fold CV trên train; chọn `alpha = 0.1`. | Bảng so sánh 8 giá trị alpha |
| **3:45 - 4:15** | 8. Kết quả thực nghiệm | Accuracy 88.52%, Macro F1 88.33%, ma trận nhầm lẫn. | Tab 3: Đánh giá thực nghiệm |
| **4:15 - 5:15** | 9. Demo Streamlit | Nhập văn bản trực tiếp, xem phân bố xác suất và độ trễ. | Tab 1: Thử nghiệm bài viết |
| **5:15 - 5:45** | 10. Giải thích đặc trưng | Bảng đóng góp log-odds và cảnh báo độ tin cậy thấp. | Xem bảng Explainability |
| **5:45 - 6:15** | 11. Hạn chế & Thách thức | Từ OOV, văn bản ngắn, giả định độc lập Naive Bayes. | Tab 4: Giới hạn mô hình |
| **6:15 - 6:30** | 12. Kết luận & Hướng tới | Tóm lược kết quả và hướng mở rộng tiếng Việt. | Chuyển sang phần Q&A |

---

## Chi tiết lời thoại và hành động theo từng bước

### 1. Giới thiệu bài toán (0:00 - 0:30)
> *"Kính thưa quý thầy cô trong hội đồng, đề tài của nhóm chúng em là: **Phân loại văn bản đa lớp bằng Multinomial Naive Bayes kết hợp trích xuất đặc trưng TF-IDF**. Mục tiêu của dự án là xây dựng một pipeline phân loại văn bản hoàn chỉnh, giải thích được cơ chế ra quyết định của thuật toán và triển khai ứng dụng web trực quan phục vụ người dùng cuối."*

### 2. Bộ dữ liệu thực nghiệm (0:30 - 1:00)
> *"Nhóm lựa chọn bộ dữ liệu chuẩn **20 Newsgroups** gồm 4 chủ đề có sự giao thoa ngữ nghĩa thực tế: Đồ họa máy tính (`comp.graphics`), Bóng chày (`rec.sport.baseball`), Khoa học vũ trụ (`sci.space`) và Chính trị tổng hợp (`talk.politics.misc`). Tổng số mẫu là 3.729 bài viết, được chia thành 2.239 mẫu huấn luyện và 1.490 mẫu kiểm thử độc lập."*

### 3. Tiền xử lý dữ liệu (1:00 - 1:30)
> *"Một vấn đề rất phổ biến trong phân loại văn bản là rò rỉ metadata (tiêu đề email, chữ ký, tên người gửi). Nếu giữ lại các phần này, mô hình sẽ học vẹt tên tác giả thay vì hiểu nội dung. Vì vậy, nhóm chủ động loại bỏ headers, footers và quotes, chỉ giữ lại phần nội dung bài đăng thực sự."*

### 4. Trích xuất đặc trưng TF-IDF (1:30 - 2:00)
> *"Máy học chỉ làm việc với số. Nhóm sử dụng TF-IDF để biến đổi văn bản thành véc-tơ số 13.068 chiều. TF giúp đếm tần suất từ trong bài, còn IDF giúp phạt các từ ngữ xuất hiện quá phổ biến như 'the', 'is', 'article', đồng thời tăng trọng số của các từ mang tính đặc trưng như 'telescope', 'pitcher', 'opengl'."*

### 5. Thuật toán Multinomial Naive Bayes (2:00 - 2:45)
> *(Chuyển sang Tab 2 trên giao diện Streamlit)*  
> *"Dựa trên định lý Bayes, mô hình tính xác suất hậu nghiệm của từng lớp khi biết tài liệu. Áp dụng giả định độc lập có điều kiện giữa các từ, toàn bộ phép tính được đưa về miền log-sum để chống tràn số dưới. Để xử lý các từ chưa từng xuất hiện trong một lớp (tránh xác suất bằng 0), mô hình áp dụng kỹ thuật làm trơn với siêu tham số alpha."*

### 6. Nguyên tắc chống rò rỉ dữ liệu (2:45 - 3:15)
> *"Nhóm đặc biệt chú trọng tính toàn vẹn học máy: Bước `fit_transform` chỉ được chạy trên tập train để học bộ từ vựng và IDF. Tập kiểm thử chỉ được `transform`. Tuyệt đối không fit TF-IDF trên toàn bộ dữ liệu trước khi chia train/test. Trong bộ kiểm thử `pytest`, nhóm đã viết riêng test case xác thực không có từ vựng riêng của tập test lọt vào mô hình."*

### 7. Tối ưu hóa siêu tham số Alpha (3:15 - 3:45)
> *"Thay vì cố định alpha=1.0 hoặc thử sai trên tập test, nhóm thực hiện **Stratified 5-Fold Cross-Validation hoàn toàn trên tập train** để khảo sát 8 giá trị alpha từ 0.01 đến 2.0. Kết quả thực nghiệm cho thấy `alpha = 0.1` đạt điểm CV Macro F1 cao nhất là **90.28%**. Nhóm đã khóa alpha=0.1 và huấn luyện mô hình cuối cùng trên toàn bộ 2.239 mẫu train."*

### 8. Kết quả thực nghiệm thực tế (3:45 - 4:15)
> *(Chuyển sang Tab 3 - Đánh giá thực nghiệm)*  
> *"Khi đánh giá duy nhất một lần trên tập test 1.490 mẫu: Mô hình tối ưu đạt **Test Accuracy 88.52%** (tăng +1.34% so với mức 87.18% ban đầu) và **Macro F1 đạt 88.33%** (tăng +1.46%). Độ nhạy Recall của lớp Chính trị tăng mạnh từ 75.8% lên 85.16%."*

### 9. Thao tác Demo trực tiếp trên Streamlit (4:15 - 5:15)
> *(Chuyển sang Tab 1 - Dự đoán & Giải thích)*  
> *"Em xin phép thao tác trực tiếp trên ứng dụng Streamlit:
> 1. Đầu tiên, em chọn bài viết mẫu về khoa học vũ trụ: 'NASA and ESA announced a new deep space mission...'. Nhấn **🚀 Phân loại**.
> 2. Hệ thống xử lý trong **2.3 ms**, dự đoán chính xác nhãn `sci.space` với độ tin cậy **99.9%**.
> 3. Biểu đồ cột hiển thị rõ phân bố xác suất áp đảo của lớp vũ trụ so với 3 lớp còn lại."*

### 10. Giải thích đặc trưng và cảnh báo độ tin cậy (5:15 - 5:45)
> *"Tại cột bên phải, bảng Explainability chỉ ra các từ khóa đóng góp mạnh nhất: 'space' (+0.51), 'nasa' (+0.50), 'orbit' (+0.48).  
> Bây giờ, nếu em nhập một chuỗi vô nghĩa như: 'asdkfjhasdkljf xyz123', hệ thống sẽ không bị crash mà ngay lập tức kích hoạt cơ chế cảnh báo: 'Từ vựng nằm ngoài từ điển (OOV)' và 'Độ tin cậy thấp (< 60%)', giúp người dùng biết đây là dự đoán không chắc chắn."*

### 11. Hạn chế và thách thức (5:45 - 6:15)
> *(Chuyển sang Tab 4 - Giới hạn)*  
> *"Dù đạt kết quả tốt, mô hình vẫn tồn tại 3 hạn chế chính:
> - Giả định độc lập từ bỏ qua trật tự từ và ngữ cảnh sâu.
> - Phụ thuộc dữ liệu tiếng Anh đã học; chưa phân loại được các chủ đề ngoài 4 nhãn.
> - Văn bản quá ngắn (dưới 2 từ vựng) có tỷ lệ sai lên tới 53.33% do thiếu tín hiệu đặc trưng."*

### 12. Kết luận (6:15 - 6:30)
> *"Tóm lại, dự án đã hiện thực hóa thành công một hệ thống phân loại văn bản Naive Bayes chuẩn mực: không rò rỉ dữ liệu, tối ưu bằng cross-validation, kiểm thử tự động 16 test cases, có tính năng giải thích đặc trưng và sẵn sàng triển khai. Nhóm em xin cảm ơn quý thầy cô và kính mời thầy cô đặt câu hỏi ạ!"*
