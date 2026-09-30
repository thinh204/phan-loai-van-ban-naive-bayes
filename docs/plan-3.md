# Plan 3: Đóng gói, triển khai và chuẩn bị bảo vệ

## Mục tiêu

Hoàn thiện dự án thành phiên bản có thể cài đặt lại, kiểm thử tự động, trình diễn trực tuyến và sử dụng trong buổi bảo vệ. Plan 3 giữ nguyên mô hình và kết quả của Plan 2; không tiếp tục lựa chọn mô hình bằng tập test.

## Các giai đoạn

| Giai đoạn | Công việc | Kết quả bàn giao | Commit đề xuất |
| --- | --- | --- | --- |
| 1. Kiểm tra khả năng tái lập | Tạo môi trường Python sạch, cài từ `requirements.txt`, chạy pytest và pipeline | Biên bản kiểm tra và hướng dẫn tái lập | `chore: xác minh khả năng cài đặt và tái lập dự án` |
| 2. Tích hợp CI | Tạo GitHub Actions chạy kiểm tra cú pháp và pytest mỗi lần push hoặc pull request | Workflow CI và trạng thái kiểm thử | `ci: thêm kiểm thử tự động trên GitHub Actions` |
| 3. Kiểm soát đầu vào | Cảnh báo văn bản rỗng, quá ngắn, không có từ trong bộ từ vựng hoặc có độ tin cậy thấp | Kết quả dự đoán an toàn và dễ hiểu hơn | `feat: cảnh báo đầu vào và độ tin cậy thấp` |
| 4. Giải thích dự đoán | Hiển thị các từ khóa có ảnh hưởng đến lớp được chọn và giải thích giới hạn của xác suất | Khu vực giải thích trong Streamlit | `feat: bổ sung giải thích kết quả dự đoán` |
| 5. Hoàn thiện giao diện | Thêm trang giới thiệu quy trình, chỉ số từng lớp và ma trận nhầm lẫn | Ứng dụng trình diễn hoàn chỉnh | `feat: hoàn thiện trang thông tin và đánh giá mô hình` |
| 6. Triển khai | Chuẩn hóa cấu hình và triển khai trên Streamlit Community Cloud | Đường dẫn demo trực tuyến và hướng dẫn triển khai | `deploy: chuẩn hóa cấu hình triển khai Streamlit` |
| 7. Chuẩn bị bảo vệ | Viết kịch bản demo 5–7 phút, câu hỏi phản biện và phương án demo ngoại tuyến | Bộ tài liệu bảo vệ cho ba thành viên | `docs: thêm kịch bản demo và câu hỏi phản biện` |
| 8. Phát hành | Rà soát dữ liệu, dependency và tài liệu; tạo phiên bản `v1.0.0` | Bản phát hành ổn định để nộp | `release: chuẩn bị phiên bản v1.0.0` |

## Điều kiện hoàn thành

1. Một máy hoặc môi trường sạch có thể cài và chạy dự án theo README.
2. Toàn bộ kiểm thử vượt qua trên máy cá nhân và GitHub Actions.
3. Giao diện xử lý rõ ràng các trường hợp đầu vào không đủ thông tin.
4. Số liệu trên giao diện, báo cáo và slide đều đọc từ kết quả chạy thật.
5. Bản demo trực tuyến và phương án demo ngoại tuyến đều hoạt động.
6. Không dùng tập test để chọn thêm tham số hoặc mô hình.
7. Mỗi giai đoạn có commit riêng, nêu rõ thay đổi và kết quả kiểm tra.

## Prompt giao cho AI

> Hãy thực hiện Plan 3 trong repo `thinh204/phan-loai-van-ban-naive-bayes`. Giữ nguyên mô hình và kết quả đã hoàn thành ở Plan 2. Trước tiên kiểm tra khả năng cài đặt lại dự án từ `requirements.txt`. Sau đó thêm GitHub Actions để chạy pytest và kiểm tra cú pháp khi push. Nâng cấp Streamlit để cảnh báo văn bản rỗng, quá ngắn, không có từ trong bộ từ vựng hoặc có độ tin cậy thấp. Bổ sung phần giải thích dự đoán, thông tin mô hình, ma trận nhầm lẫn và kết quả từng lớp. Chuẩn bị cấu hình triển khai Streamlit Community Cloud, hướng dẫn demo, câu hỏi phản biện và phương án demo ngoại tuyến. Cuối cùng chuẩn bị bản phát hành `v1.0.0`. Sau mỗi giai đoạn phải kiểm thử, commit và push với chú thích rõ ràng. Không thay đổi hoặc tự tạo số liệu thực nghiệm. Không dùng tập test để tiếp tục lựa chọn mô hình.
