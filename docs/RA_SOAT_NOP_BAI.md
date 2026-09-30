# Rà soát đồ án môn Trí tuệ nhân tạo — 01/10/2026

## Nội dung đã sửa

- Bổ sung trường, lớp, tên và MSSV của ba thành viên vào README, báo cáo và bìa slide. MSSV của Nguyễn Trần Mạnh Dũng được giữ đúng thông tin nhóm gửi: `N23DVCN01`. Giảng viên để trống theo yêu cầu của nhóm.
- Slide v3 sửa biểu đồ baseline/tối ưu: Accuracy 87,18%/88,52%, Macro F1 86,87%/88,33%. Sửa số đếm nhầm lẫn Vũ trụ → Chính trị thành 25, chiều ngược lại thành 23; bỏ nhận xét từ phiên bản mô hình cũ.
- Báo cáo, kịch bản và hướng dẫn cập nhật 27 tests, bỏ tiêu đề lặp; phân biệt kết quả kiểm thử phần mềm với độ chính xác mô hình. Giữ nguyên mô hình và số liệu thực nghiệm.
- Xuất báo cáo PDF từ Markdown, có bìa, mục lục, công thức, bảng kết quả và nguồn tham khảo. Bản sửa PowerPoint là `presentation/phan-loai-van-ban-naive-bayes-v3.pptx`; v2 giữ làm bản cũ.
- Dùng chung `format_text_preview` từ service; bỏ reload service mỗi lần chạy. Giữ refresh cấu hình hiển thị để tương thích cách cập nhật Cloud hiện có.
- Sửa quy tắc đóng gói để không loại nhầm `.github` và `.gitignore` khi lọc `.git`.

## Xác minh và gói nộp

- Toàn bộ 27 tests đạt sau chỉnh sửa; slide được dựng thành ảnh để rà bố cục và kiểm tra cấu trúc file. PDF được render từng trang để kiểm tra hiển thị tiếng Việt và bảng.
- Biểu đồ mới có dữ liệu nhúng để chỉnh sửa trong PowerPoint; các giá trị nhập từ kết quả thực nghiệm. Chưa kiểm tra mở bằng ứng dụng PowerPoint bản desktop.
- Gói mới ở `submission/` tách biệt với tài sản Release v1.0.4. Manifest ghi commit nguồn, SHA-256 của ZIP và từng tệp; kiểm tra CRC và nội dung trước bàn giao.
- Trong gói, dùng báo cáo PDF và slide v3. Tài liệu kế hoạch/nghiệm thu cũ được giữ như lịch sử, không thay thế kết quả hiện tại.

## Trước khi nộp

1. Nhóm bổ sung tên giảng viên vào báo cáo Markdown và slide v3, rồi xuất lại PDF.
2. Nhóm kiểm tra lại MSSV của Nguyễn Trần Mạnh Dũng theo danh sách lớp; hiện tài liệu dùng `N23DVCN01` do nhóm cung cấp, không tự thêm chữ số.
3. Nếu sửa thông tin bìa, commit thay đổi nguồn trước rồi chạy `python scripts/build_submission_bundle.py` để cập nhật gói. Xuất PDF cần thư viện tùy chọn trong `scripts/requirements-docs.txt` và font Arial; ví dụ Windows: `python scripts/export_report_pdf.py`.
