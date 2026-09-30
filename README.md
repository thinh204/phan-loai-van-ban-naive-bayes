# Phân loại văn bản bằng Naive Bayes đa thức

Đề tài môn Trí tuệ nhân tạo của nhóm 3 thành viên. Dự án giải thích phương pháp Multinomial Naive Bayes và kiểm chứng bằng bài toán phân loại chủ đề văn bản.

## Sản phẩm

- [Kế hoạch và phân công](docs/ke-hoach.md)
- Báo cáo lý thuyết và ví dụ tính tay
- Mã thực nghiệm có thể chạy lại trên bộ dữ liệu 20 Newsgroups
- Kết quả đánh giá và nội dung thuyết trình

## Nguyên tắc thực nghiệm

Sử dụng tập `train` và `test` có sẵn của 20 Newsgroups; học bộ từ vựng và trọng số văn bản **chỉ từ tập train**. Loại bỏ header, chữ ký và phần trích dẫn nhằm giảm thông tin tiết lộ nhãn. Không ghi số liệu vào báo cáo trước khi chạy mã.

Nguồn dữ liệu: [scikit-learn, 20 Newsgroups](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html).

## Nhật ký

Mỗi giai đoạn hoàn thành sẽ có một commit riêng. Xem lịch sử commit để biết nội dung và thời điểm cập nhật.
