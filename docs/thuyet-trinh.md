# Kịch bản thuyết trình 10 slide

Tệp PowerPoint: [`presentation/phan-loai-van-ban-naive-bayes-v2.pptx`](../presentation/phan-loai-van-ban-naive-bayes-v2.pptx). Các slide có ghi chú người nói và nguồn tham khảo. Nhóm có thể thay tên ba thành viên trên slide bìa trước khi nộp.

## Phân chia lời nói đề xuất

| Thành viên | Slide | Trọng tâm |
| --- | --- | --- |
| 1 | 1–3 | Nêu bài toán, bốn nhãn và quy trình từ văn bản đến dự đoán |
| 2 | 4–6 | Giải thích biểu diễn từ, công thức MNB và ví dụ tính tay |
| 3 | 7–10 | Trình bày cách thử nghiệm, chỉ số, lỗi và giới hạn |

## Nội dung cần nói theo slide

1. **Giới thiệu:** Nhóm nghiên cứu một thuật toán phân loại văn bản, sau đó kiểm tra trên dữ liệu có nhãn.
2. **Bài toán:** Một bài đăng đầu vào được gán vào một trong bốn chủ đề của 20 Newsgroups. Dữ liệu thực nghiệm là tiếng Anh.
3. **Quy trình:** Tách train và test; học cách biến văn bản thành véc-tơ và học MNB trên train; test chỉ dùng để dự đoán và đánh giá.
4. **Đặc trưng:** Bag of Words đếm từ. TF-IDF giảm vai trò của từ xuất hiện trong nhiều tài liệu. Đây là hai cách biểu diễn của cùng thuật toán.
5. **Mô hình:** Điểm mỗi lớp gồm xác suất tiên nghiệm và đóng góp của các từ. Dùng log để tính ổn định; làm trơn `α=1` xử lý từ chưa xuất hiện ở lớp.
6. **Ví dụ tính tay:** Với câu “bóng đá mới”, điểm Thể thao `9/5488` lớn hơn Công nghệ `2/5488`, nên dự đoán Thể thao. Đây là ví dụ tự tạo để giải thích công thức.
7. **Thiết kế thực nghiệm:** 2.239 mẫu train, 1.490 mẫu test, bốn lớp, hai pipeline có cùng MNB. Loại header, chữ ký, phần trích dẫn để giảm tín hiệu nhãn ngoài nội dung.
8. **Kết quả:** Sau khi tối ưu siêu tham số bằng Stratified 5-Fold Cross-Validation trên tập train (chọn `alpha=0.1`), Accuracy trên tập test đạt 88,52% (tăng từ 87,18% ban đầu) và Macro F1 đạt 88,33% (tăng từ 86,87%). Số liệu lấy trực tiếp từ `results/evaluation_summary.json`.
9. **Phân tích lỗi:** Trên 1.490 mẫu test có 1.319 mẫu đúng và 171 mẫu sai. Các văn bản có ít từ vựng TF-IDF (<= 2 từ) có tỷ lệ sai lên tới 53,33%. Ngưỡng tin cậy thấp (< 60%) có tỷ lệ sai 44,36%, đóng vai trò cảnh báo quan trọng trong ứng dụng.
10. **Kết luận & Demo sản phẩm:** MNB học nhanh và dễ giải thích. Hệ thống đã chuẩn hóa kiến trúc hướng dịch vụ với `TextClassifierService`, bộ kiểm thử tự động 16 test cases (`pytest -v`), CI Pipeline tự động trên GitHub Actions, giải thích từ khóa đặc trưng TF-IDF, chẩn đoán cảnh báo UX thông minh, và giao diện web Streamlit triển khai trực tuyến trên Streamlit Cloud kèm tùy chọn chạy ngoại tuyến.

## Câu hỏi có thể gặp

- **Vì sao gọi là “naive”?** Vì mô hình xấp xỉ các đặc trưng là độc lập khi đã biết lớp, dù từ ngữ thực tế có liên hệ với nhau.
- **Vì sao thêm `α=1`?** Để một từ chưa thấy ở một lớp không làm xác suất của cả tài liệu bằng 0.
- **Vì sao TF-IDF có điểm chung cao hơn nhưng lớp Chính trị giảm recall?** Trọng số đặc trưng thay đổi ranh giới dự đoán; ma trận nhầm lẫn cho thấy lỗi đã chuyển giữa hai lớp. Thử nghiệm này chưa đủ để khẳng định một nguyên nhân duy nhất.
- **Có thể áp dụng trực tiếp cho tiếng Việt không?** Thuật toán có thể dùng, nhưng cần dữ liệu tiếng Việt có nhãn và bước tách từ phù hợp để đánh giá riêng.

Tài liệu tham khảo và phương pháp chi tiết nằm trong [`bao-cao.md`](bao-cao.md).
