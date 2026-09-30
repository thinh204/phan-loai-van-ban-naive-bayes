# Bộ câu hỏi phản biện bảo vệ đề tài (Defense Q&A)

Tài liệu này tổng hợp toàn bộ các câu hỏi phản biện chuyên sâu mà giảng viên và hội đồng chấm thi thường đặt ra, kèm theo câu trả lời chuẩn xác dựa trên hiện thực mã nguồn thực tế của dự án.

---

## 1. Cơ sở lý thuyết và Thuật toán

### Q1: Tại sao nhóm lại chọn thuật toán Multinomial Naive Bayes mà không dùng mô hình khác?
**Trả lời:**
- Multinomial Naive Bayes (MNB) là thuật toán xác suất kinh điển, có nền tảng toán học chặt chẽ và cực kỳ phù hợp với bài toán phân loại văn bản dạng Bag of Words hoặc TF-IDF.
- MNB có chi phí tính toán rất thấp (độ phức tạp tuyến tính $O(N \cdot V)$), tốc độ huấn luyện và suy luận nhanh (chỉ mất khoảng 2-3 ms trên CPU cho mỗi lượt dự đoán).
- Mô hình có tính giải thích cao (explainable): xác suất của từng đặc trưng từ vựng có thể tính toán và trực quan hóa minh bạch, rất phù hợp cho mục tiêu học tập và nghiên cứu bản chất mô hình trước khi chuyển sang các mạng nơ-ron phức tạp dạng "hộp đen".

---

### Q2: Thuật toán Naive Bayes hoạt động như thế nào? Tại sao gọi là "Naive" (Ngây thơ)?
**Trả lời:**
- **Nguyên lý:** Mô hình dựa trên định lý Bayes để tính xác suất hậu nghiệm:
  $$P(c | d) = \frac{P(d | c) P(c)}{P(d)}$$
  Do mẫu số $P(d)$ không đổi với mọi lớp $c$, mục tiêu là tìm lớp $c$ tối đa hóa $P(c) P(d | c)$.
- **Lý do gọi là "Ngây thơ" (Naive):** Mô hình đưa ra giả định đơn giản hóa cực đoan: **tất cả các từ trong văn bản đều độc lập có điều kiện khi đã biết lớp**. Trong thực tế, ngôn ngữ có cấu trúc ngữ pháp và sự tương quan mạnh giữa các từ (ví dụ "trí tuệ" thường đi kèm "nhân tạo"). Tuy giả định này sai so với thực tế, trong bài toán phân loại, việc ước lượng chính xác phân bố xác suất không quan trọng bằng việc bảo toàn thứ tự điểm số giữa các lớp, nên Naive Bayes vẫn hoạt động hiệu quả bất ngờ.

---

### Q3: Bản chất của biểu diễn TF-IDF là gì? So sánh với Bag of Words?
**Trả lời:**
- **Bag of Words (CountVectorizer):** Chỉ đếm số lần xuất hiện của từ ($TF$). Nhược điểm: những từ phổ biến xuất hiện nhiều lần (như 'the', 'is', 'say') sẽ chiếm trọng số rất lớn dù không có giá trị phân loại.
- **TF-IDF (Term Frequency - Inverse Document Frequency):**
  $$\text{TF-IDF}(t, d) = \text{TF}(t, d) \times \log\left(\frac{1 + N}{1 + \text{df}(t)}\right) + 1$$
  Thành phần $IDF$ giúp phạt nặng các từ xuất hiện trong hầu hết các văn bản và tăng điểm cho các từ chỉ xuất hiện tập trung ở một số tài liệu nhất định (mang tính phân biệt cao).
- **Kết quả thực nghiệm:** Trên cùng tập test 1.490 mẫu, TF-IDF đạt Accuracy 87.18% (so với 85.44% của Bag of Words), chứng minh tính hiệu quả của việc cân bằng trọng số từ.

---

## 2. Quy trình tiền xử lý và Chống rò rỉ dữ liệu (Data Leakage)

### Q4: Data Leakage (Rò rỉ dữ liệu) là gì? Tại sao tuyệt đối không được fit TF-IDF trên toàn bộ dataset trước khi chia train/test?
**Trả lời:**
- **Định nghĩa:** Data leakage là hiện tượng thông tin từ tập kiểm thử (test set) bị lộ hoặc thẩm thấu vào quá trình huấn luyện mô hình, khiến kết quả đánh giá quá lạc quan trên giấy tờ nhưng suy giảm khi chạy thực tế.
- **Nếu fit TF-IDF trên toàn dataset:**
  1. Bộ từ vựng (Vocabulary) sẽ chứa cả những từ độc nhất chỉ có trong tập test.
  2. Trọng số $IDF$ (tần số nghịch đảo của tài liệu) sẽ được tính toán dựa trên tổng số tài liệu của cả train lẫn test, làm sai lệch phân bố thực tế.
- **Giải pháp của nhóm:** Nhóm áp dụng nguyên tắc nghiêm ngặt:
  - `fit_transform()` **chỉ chạy trên `X_train`**.
  - `transform()` **chạy trên `X_test` và văn bản mới**.
  - Nhóm đã xây dựng test case tự động `verify_no_data_leakage()` trong pytest để chứng minh 100% không có từ vựng riêng của tập test lọt vào từ điển mô hình.

---

### Q5: Tại sao nhóm lại loại bỏ headers, footers và quotes trong bộ dữ liệu 20 Newsgroups?
**Trả lời:**
- Headers của email thường chứa thông tin như tên nhóm tin (`Newsgroup: sci.space`), địa chỉ email của tổ chức (`nasa.gov`, `cmu.edu`) hoặc tiêu đề chủ đề.
- Chữ ký (footers) và trích dẫn (quotes) cũng chứa nhiều thông tin nhận diện tác giả.
- Nếu giữ lại, mô hình sẽ "học vẹt" quy luật: "cứ thấy tên tổ chức nasa.gov thì đoán là vũ trụ", thay vì học ngữ nghĩa của nội dung thảo luận. Việc loại bỏ giúp kiểm tra đúng năng lực phân loại dựa trên nội dung bài viết.

---

## 3. Siêu tham số Alpha và Tối ưu hóa (Hyperparameter Tuning)

### Q6: Tham số `alpha` trong MultinomialNB có tác dụng gì?
**Trả lời:**
- `alpha` là hệ số làm trơn (additive smoothing). Khi `alpha = 1.0`, đây là làm trơn Laplace; khi `0 < alpha < 1`, đây là làm trơn Lidstone.
- Công thức: $\theta_{c, i} = \frac{N_{c, i} + \alpha}{N_c + \alpha V}$.
- **Tác dụng:** Nếu một từ $w_i$ chưa từng xuất hiện trong lớp $c$ ở tập train ($N_{c, i} = 0$), không có làm trơn thì $\theta_{c, i} = 0$. Khi đó phép nhân tích xác suất sẽ khiến toàn bộ xác suất của tài liệu bằng 0 bất kể các từ còn lại có khớp đến đâu. Hệ số $\alpha > 0$ đảm bảo mọi từ vựng đều có xác suất khác 0.

---

### Q7: Vì sao nhóm lại chọn `alpha = 0.1`? Quy trình lựa chọn có khách quan không?
**Trả lời:**
- **Quy trình:** Nhóm thực hiện **Stratified 5-Fold Cross-Validation chỉ trên 2.239 mẫu của tập train**, khảo sát 8 giá trị: `[0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0]`. Trong mỗi fold, TF-IDF được fit độc lập bằng scikit-learn `Pipeline`.
- **Kết quả:** `alpha = 0.1` đạt điểm **CV Macro F1 cao nhất là 90.28%** (vượt trội so với mức mặc định alpha=1.0 chỉ đạt 88.55%).
- **Tính khách quan:** Nhóm tuyệt đối không xem điểm test để chọn alpha. Sau khi khóa `alpha = 0.1`, mô hình mới được đánh giá duy nhất một lần trên tập test 1.490 mẫu, đưa Accuracy từ 87.18% lên **88.52%** (+1.34%) và Macro F1 từ 86.87% lên **88.33%** (+1.46%).

---

### Q8: Tại sao lại dùng Stratified K-Fold mà không dùng K-Fold thông thường?
**Trả lời:**
- Stratified K-Fold đảm bảo tỷ lệ phần trăm giữa các lớp trong mỗi fold con giống hệt như phân bố của toàn bộ tập dữ liệu.
- Trong bộ dữ liệu này, số mẫu giữa các lớp có sự chênh lệch (lớp `talk.politics.misc` có 465 mẫu train, trong khi `rec.sport.baseball` có 597 mẫu). Stratified K-Fold giúp tránh tình trạng một fold nào đó ngẫu nhiên có quá ít mẫu của lớp nhỏ, giúp việc ước lượng điểm CV ổn định và đáng tin cậy hơn.

---

## 4. Đánh giá mô hình và Phân tích lỗi

### Q9: Accuracy và F1-Score khác nhau thế nào? Tại sao cần xem Macro F1?
**Trả lời:**
- **Accuracy (Độ chính xác tổng thể):** Tỷ lệ số mẫu đoán đúng trên tổng số mẫu $\frac{TP + TN}{Total}$. Accuracy có thể bị đánh lừa nếu dữ liệu mất cân bằng nghiêm trọng (ví dụ 95% lớp A, chỉ cần đoán toàn A là đạt 95% accuracy).
- **F1-Score:** Trung bình điều hòa giữa Precision (độ chuẩn xác) và Recall (độ nhạy bao phủ): $F1 = 2 \times \frac{P \times R}{P + R}$.
- **Macro F1:** Tính F1 riêng cho từng lớp rồi lấy trung bình cộng không trọng số giữa 4 lớp. Điều này đối xử công bằng với mọi lớp, ngăn không cho lớp có số mẫu lớn che lấp điểm yếu của lớp nhỏ (như lớp Chính trị).

---

### Q10: Confusion Matrix (Ma trận nhầm lẫn) phản ánh điều gì trong đề tài này?
**Trả lời:**
- Ma trận nhầm lẫn cho biết chính xác các lỗi dự đoán diễn ra giữa những cặp chủ đề nào.
- Phân tích lỗi thực tế trên 1.490 mẫu test cho thấy:
  1. `sci.space` thường bị nhầm sang `rec.sport.baseball` và `talk.politics.misc` (25 lần mỗi loại) khi bài viết vũ trụ thảo luận về phân bổ ngân sách nhà nước hoặc ngôn từ giao tiếp thông thường.
  2. `talk.politics.misc` nhầm sang `sci.space` (23 lần) khi các bài tranh luận đề cập tới chương trình không gian NASA.
  3. Hai lớp ít bị nhầm nhất là `comp.graphics` và `rec.sport.baseball` vì từ vựng giữa đồ họa máy tính và bóng chày gần như không có sự giao thoa ngữ nghĩa.

---

### Q11: Độ tin cậy (Confidence) của Naive Bayes có phải là xác suất chắc chắn đúng không?
**Trả lời:**
- **Hoàn toàn không.** Xác suất do Naive Bayes xuất ra là xác suất hậu nghiệm được tính toán dưới giả định các từ độc lập. Do giả định này không phản ánh cấu trúc tương quan thực tế, các xác suất của Naive Bayes thường có xu hướng bị cực đoan hóa (rất gần 0 hoặc rất gần 1).
- Trong ứng dụng, nhóm luôn nhấn mạnh: Confidence cao phản ánh sự phù hợp cao của từ khóa đối với từ điển đã học, chứ không đảm bảo 100% tính đúng đắn về mặt ngữ nghĩa thực tế. Nhóm đã đặt ngưỡng cảnh báo `LOW_CONFIDENCE_THRESHOLD = 0.60` (60%) để cảnh báo người dùng khi dự đoán không chắc chắn.

---

### Q12: Nếu người dùng nhập một văn bản chứa toàn các từ chưa từng xuất hiện (OOV) thì mô hình xử lý ra sao?
**Trả lời:**
- Khi gặp từ ngoài từ điển, véc-tơ TF-IDF sẽ là véc-tơ toàn số 0.
- Điểm log của mỗi lớp lúc này chỉ còn lại xác suất tiên nghiệm $\log P(c)$.
- Ứng dụng sẽ dự đoán lớp có số mẫu huấn luyện nhiều nhất trong tập train (`rec.sport.baseball`), nhưng hệ thống sẽ **bắt được sự kiện này và hiển thị cảnh báo rõ ràng:** *"Từ vựng nằm ngoài từ điển (OOV) - Dự đoán có độ tin cậy thấp dựa trên xác suất tiên nghiệm"*, hoàn toàn không gây crash ứng dụng.

---

## 5. Hướng mở rộng và Công nghệ tiên tiến

### Q13: Tại sao đề tài không sử dụng các mô hình ngôn ngữ lớn hoặc Deep Learning như BERT, RoBERTa?
**Trả lời:**
- Đề tài tập trung vào việc nghiên cứu sâu phương pháp học máy thống kê truyền thống **Multinomial Naive Bayes** theo đúng yêu cầu học phần Trí tuệ Nhân tạo.
- So với BERT: MNB có tốc độ huấn luyện tính bằng giây, không cần phần cứng GPU đắt tiền, kích thước file mô hình chỉ khoảng 1 MB (so với hàng trăm MB hoặc GB của BERT), suy luận cực nhanh (2-3 ms) và hoàn toàn giải thích được dựa trên trọng số từ vựng.
- MNB là mô hình cơ sở chuẩn mực (strong baseline) mà bất kỳ hệ thống phân loại văn bản nào cũng cần so sánh trước khi đầu tư hạ tầng nặng nề cho Deep Learning.

---

### Q14: Phương án dự phòng (Contingency Plan) nếu buổi bảo vệ bị mất mạng Internet hoặc lỗi Cloud?
**Trả lời:**
- Nhóm đã chuẩn bị phương án **chạy cục bộ 100% offline**:
  1. Toàn bộ mã nguồn, môi trường ảo Python và các tệp mô hình đã huấn luyện (`models/*.joblib`) đều nằm sẵn trên máy tính cá nhân.
  2. Chỉ cần mở terminal và gõ:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     streamlit run app.py
     ```
  3. Trình duyệt cục bộ mở ngay tại `http://localhost:8501` mà không cần bất kỳ kết nối Internet nào.
  4. Ngoài ra, nhóm đã chuẩn bị sẵn video quay lại màn hình thao tác demo và các tệp kết quả JSON/CSV xuất sẵn để trình chiếu slide trong trường hợp máy tính gặp trục trặc kỹ thuật.
