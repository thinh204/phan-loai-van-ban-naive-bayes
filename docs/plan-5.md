# Plan 5: Khắc phục nghiệm thu cuối và diễn tập bảo vệ

## Kết quả kiểm tra Plan 4

Plan 4 đã hoàn thành phần lớn mục tiêu về mã nguồn, CI, tài liệu, đóng gói và phát hành. Kết quả kiểm tra lại ngày 30/09/2026:

- `python -m pytest -q`: **16/16 kiểm thử đạt**.
- `python -m compileall -q app.py src tests`: **đạt**.
- GitHub Actions tại commit `dbca1f8` hoàn thành thành công trên Python 3.10 và 3.11.
- GitHub Release `v1.0.1` đã được xuất bản từ đúng commit `dbca1f8`.
- Tag `v1.0.0` và `v1.0.1` tồn tại, không di chuyển tag cũ.
- Gói nộp có 41 tệp, chứa mã nguồn, mô hình, kết quả, kiểm thử và PowerPoint.

Các điểm cần hoàn thiện tiếp:

1. URL `https://phan-loai-van-ban-naive-bayes.streamlit.app` chuyển đến trang **Not found** và yêu cầu đăng nhập; chưa đạt điều kiện demo công khai.
2. Chân trang trong `app.py` vẫn ghi `Plan 3 - Release v1.0.0` thay vì phiên bản nghiệm thu hiện tại.
3. Gói ZIP được tạo trước release notes nên chưa chứa `docs/RELEASE_NOTES_v1.0.1.md`.
4. Một số liên kết tệp trong phần mô tả GitHub Release thiếu thư mục `docs/`, vì vậy cần kiểm tra và sửa liên kết.
5. Cần chạy thử toàn bộ bài nộp từ một thư mục sạch, độc lập với môi trường phát triển hiện tại.

## Mục tiêu

Khắc phục các sai lệch còn lại của Plan 4, chứng minh bản nộp chạy độc lập và tổ chức một vòng diễn tập bảo vệ hoàn chỉnh cho ba thành viên. Giữ nguyên mô hình, tập dữ liệu, tham số và số liệu thực nghiệm đã được khóa.

## Các giai đoạn

| Giai đoạn | Công việc | Kết quả bàn giao | Commit đề xuất |
| --- | --- | --- | --- |
| 1. Khôi phục demo công khai | Kiểm tra Streamlit Community Cloud, quyền truy cập repository, tên ứng dụng và log triển khai; sửa cho đến khi URL mở được trong phiên chưa đăng nhập | URL công khai hiển thị ứng dụng và dự đoán được | `fix: khôi phục ứng dụng Streamlit công khai` |
| 2. Đồng bộ phiên bản | Sửa chân trang ứng dụng và mọi metadata còn ghi Plan 3 hoặc v1.0.0; dùng một nguồn cấu hình phiên bản duy nhất | Giao diện và tài liệu cùng ghi phiên bản hiện tại | `fix: đồng bộ thông tin phiên bản ứng dụng` |
| 3. Sửa liên kết phát hành | Kiểm tra từng liên kết trong release notes và GitHub Release, sửa đường dẫn thiếu `docs/` hoặc sai ref | Mọi liên kết trên trang phát hành mở đúng tệp | `docs: sửa liên kết tài liệu phát hành` |
| 4. Tự động hóa gói nộp | Viết script tạo ZIP từ danh sách tệp rõ ràng, bao gồm release notes mới; loại môi trường ảo, cache và dữ liệu tạm | Gói ZIP có thể tái tạo bằng một lệnh | `build: tự động hóa đóng gói bài nộp` |
| 5. Kiểm tra toàn vẹn | Tạo manifest gồm tên tệp, kích thước và SHA-256; kiểm tra ZIP không hỏng và không chứa tệp thừa | Manifest và checksum để đối chiếu bản nộp | `release: thêm manifest và checksum bài nộp` |
| 6. Chạy thử từ gói sạch | Giải nén sang thư mục tạm sạch, tạo môi trường mới, cài dependency, chạy 16 test và khởi động Streamlit | Biên bản tái lập từ đúng gói sẽ nộp | `test: xác minh gói nộp trong môi trường sạch` |
| 7. Diễn tập ba thành viên | Phân vai mở bài, phương pháp, thực nghiệm và demo; đo thời gian, chuẩn bị chuyển phần và xử lý lỗi mạng | Kịch bản bảo vệ 7–10 phút có thời lượng từng người | `docs: hoàn thiện kịch bản diễn tập nhóm` |
| 8. Đóng băng bản cuối | Rà soát CI, demo, ZIP, slide và tài liệu; tạo `v1.0.2` nếu có sửa lỗi, cập nhật GitHub Release và đính kèm đúng ZIP | Bản phát hành cuối đã được kiểm tra từ đầu đến cuối | `release: phát hành bản bảo vệ v1.0.2` |

## Điều kiện hoàn thành

1. URL Streamlit mở được trong cửa sổ chưa đăng nhập và thực hiện được ít nhất một dự đoán.
2. Không còn nội dung Plan 3 hoặc v1.0.0 trong giao diện bản mới, trừ tài liệu lịch sử phát hành.
3. Tất cả liên kết trong README, release notes và GitHub Release mở đúng đích.
4. Gói ZIP được tạo lại bằng script, có release notes v1.0.1 hoặc mới hơn và không chứa `.venv`, cache hay thông tin nhạy cảm.
5. SHA-256 của gói nộp được ghi vào manifest và khớp với tệp đính kèm GitHub Release.
6. Cài đặt, 16 kiểm thử và ứng dụng Streamlit chạy thành công từ thư mục giải nén sạch.
7. Ba thành viên hoàn thành một lượt diễn tập trong thời lượng 7–10 phút và có phương án demo ngoại tuyến.
8. GitHub Actions xanh trên commit cuối; tag và Release trỏ đúng commit đó.

## Prompt giao cho AI

> Hãy thực hiện Plan 5 trong repo `thinh204/phan-loai-van-ban-naive-bayes`. Trước tiên kiểm tra URL Streamlit bằng một phiên chưa đăng nhập. Hiện URL công bố đang chuyển đến trang Not found hoặc yêu cầu đăng nhập, vì vậy hãy kiểm tra cấu hình Streamlit Community Cloud, quyền truy cập repository và log triển khai, sau đó sửa cho đến khi ứng dụng mở công khai và dự đoán được. Đồng bộ thông tin phiên bản trong `app.py` và tài liệu bằng một nguồn cấu hình duy nhất; giao diện không được tiếp tục ghi Plan 3/v1.0.0. Kiểm tra và sửa mọi liên kết trong README, release notes và GitHub Release, đặc biệt các đường dẫn thiếu thư mục `docs/`. Viết script tạo lại gói ZIP từ danh sách tệp cho phép, bảo đảm có release notes mới nhất và không chứa môi trường ảo, cache hoặc thông tin nhạy cảm. Tạo manifest tên tệp, kích thước, SHA-256 rồi giải nén gói sang thư mục sạch để cài dependency, chạy đủ 16 kiểm thử và khởi động Streamlit. Cập nhật kịch bản diễn tập 7–10 phút cho ba thành viên, gồm chuyển phần, demo trực tuyến và phương án ngoại tuyến. Sau khi toàn bộ điều kiện đạt, tạo phiên bản `v1.0.2`, push tag, xuất bản GitHub Release và đính kèm đúng gói ZIP đã kiểm tra. Sau mỗi giai đoạn phải chạy kiểm tra phù hợp, commit và push với chú thích rõ ràng. Không huấn luyện lại, không thay đổi mô hình, không dùng tập test để chọn tham số và không tự ghi trạng thái hoàn thành nếu chưa có bằng chứng kiểm tra trực tiếp.
