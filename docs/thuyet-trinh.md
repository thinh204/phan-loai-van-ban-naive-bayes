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
8. **Kết quả:** Accuracy là 85,44% với Bag of Words và 87,18% với TF-IDF. Macro F1 lần lượt là 85,20% và 86,87%. Số liệu lấy trực tiếp từ `results/metrics.json`.
9. **Phân tích lỗi:** TF-IDF giảm nhầm lẫn Không gian sang Chính trị từ 62 xuống 14, nhưng tăng nhầm lẫn chiều ngược từ 15 lên 45. Vì thế cần xem chỉ số từng lớp, không chỉ nhìn accuracy chung.
10. **Kết luận:** MNB dễ giải thích và cho kết quả hữu ích trong phạm vi thử nghiệm. Nhóm chưa kiểm tra trên tiếng Việt hay nhiều bộ dữ liệu; hướng tiếp theo là dùng dữ liệu tiếng Việt có nhãn và validation riêng.

## Câu hỏi có thể gặp

- **Vì sao gọi là “naive”?** Vì mô hình xấp xỉ các đặc trưng là độc lập khi đã biết lớp, dù từ ngữ thực tế có liên hệ với nhau.
- **Vì sao thêm `α=1`?** Để một từ chưa thấy ở một lớp không làm xác suất của cả tài liệu bằng 0.
- **Vì sao TF-IDF có điểm chung cao hơn nhưng lớp Chính trị giảm recall?** Trọng số đặc trưng thay đổi ranh giới dự đoán; ma trận nhầm lẫn cho thấy lỗi đã chuyển giữa hai lớp. Thử nghiệm này chưa đủ để khẳng định một nguyên nhân duy nhất.
- **Có thể áp dụng trực tiếp cho tiếng Việt không?** Thuật toán có thể dùng, nhưng cần dữ liệu tiếng Việt có nhãn và bước tách từ phù hợp để đánh giá riêng.

Tài liệu tham khảo và phương pháp chi tiết nằm trong [`bao-cao.md`](bao-cao.md).
