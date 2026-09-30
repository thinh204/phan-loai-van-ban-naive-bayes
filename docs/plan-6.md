# Plan 6: Sửa sai lệch cuối và khóa bản nộp có thể kiểm chứng

## Kết quả kiểm tra Plan 5

Plan 5 đã hoàn thành phần mã nguồn, đóng gói và phát hành, nhưng chưa đạt toàn bộ điều kiện đã đặt ra. Kết quả kiểm tra trực tiếp ngày 30/09/2026:

- `python -m pytest -q`: **16/16 kiểm thử đạt**.
- `python -m compileall -q app.py src tests scripts`: **đạt**.
- Gói ZIP có **46 tệp**, vượt qua kiểm tra CRC và suy diễn `sci.space` với độ tin cậy 99,96%.
- SHA-256 thực tế của ZIP là `c23a328f48b01ebe4c6609a8a38b587e062f2a4dfa8983b5e9c3fd09457e1842`, khớp `MANIFEST.json` và `CHECKSUMS.sha256`.
- Tag và GitHub Release `v1.0.2` tồn tại, trỏ đến commit `b00015c`.
- GitHub Actions của Plan 5 đã được cấu hình và các commit trước bản phát hành chạy thành công.

Ba vấn đề cần sửa:

1. Truy cập `https://phan-loai-van-ban-naive-bayes.streamlit.app` trong phiên chưa đăng nhập vẫn chuyển đến trang **Not found**; nội dung công bố “đã mở công khai” chưa đúng với kiểm tra thực tế.
2. Release notes v1.0.2 ghi CV Macro F1 là **89,32%** và **91,47%**, trong khi dữ liệu gốc `results/alpha_tuning.json` cho `alpha=1.0` là **88,55%** và `alpha=0.1` là **90,28%**.
3. `scripts/verify_clean_package.py` giải nén vào thư mục sạch nhưng vẫn chạy bằng `.venv` của repository; script chưa tạo môi trường mới và chưa cài lại `requirements.txt` như tài liệu tuyên bố.

## Mục tiêu

Sửa các tuyên bố không khớp bằng chứng, triển khai website thật sự công khai và chứng minh gói nộp có thể cài đặt lại trong môi trường Python mới. Sau Plan 6, dự án được đóng băng để nộp và không mở thêm plan phát triển nếu không phát hiện lỗi mới.

## Các giai đoạn

| Giai đoạn | Công việc | Kết quả bàn giao | Commit đề xuất |
| --- | --- | --- | --- |
| 1. Sửa số liệu khoa học | Đọc số liệu trực tiếp từ JSON kết quả, sửa release notes, tài liệu và mô tả GitHub Release | CV Macro F1 thống nhất: 88,55% và 90,28% | `fix: sửa số liệu cross validation trong bản phát hành` |
| 2. Triển khai Streamlit thật | Kiểm tra bảng điều khiển Streamlit, tạo hoặc sửa ứng dụng trỏ tới `main/app.py`, xem log cho đến khi health check đạt | URL công khai trả về giao diện ứng dụng | `deploy: hoàn tất triển khai Streamlit công khai` |
| 3. Kiểm thử như khách truy cập | Mở URL trong phiên chưa đăng nhập, thử một mẫu dự đoán, tải CSV và lưu bằng chứng có thời điểm kiểm tra | Biên bản kiểm thử web công khai | `test: xác minh demo công khai từ phiên ẩn danh` |
| 4. Tái lập môi trường thật | Sửa script để tạo virtual environment mới trong thư mục tạm, cài đúng `requirements.txt`, rồi mới chạy compile, pytest và suy diễn | Không còn sử dụng `.venv` của workspace khi xác minh | `test: tái lập gói nộp bằng môi trường Python mới` |
| 5. Kiểm tra phát hành tải xuống | Tải asset ZIP từ GitHub Release, tính SHA-256 và so sánh với checksum trong repository | Asset trên GitHub khớp chính xác gói đã nghiệm thu | `release: xác minh tài sản tải xuống và checksum` |
| 6. Chống sai lệch tài liệu | Thêm kiểm tra tự động cho phiên bản, số liệu chính và URL; CI báo lỗi khi tài liệu khác JSON hoặc cấu hình | Các sai lệch quan trọng được phát hiện tự động | `test: thêm kiểm tra nhất quán tài liệu phát hành` |
| 7. Kiểm tra trước buổi bảo vệ | Chạy thử slide, demo online, demo offline, thời lượng ba thành viên và bộ câu hỏi phản biện trên đúng máy trình chiếu | Checklist ngày bảo vệ đã ký xác nhận | `docs: chốt checklist trước buổi bảo vệ` |
| 8. Khóa bản nộp cuối | Tạo lại ZIP, manifest và checksum; chạy toàn bộ CI; phát hành `v1.0.3` và đính kèm asset đã đối chiếu | Bản cuối có thể kiểm chứng từ mã nguồn đến website và tệp tải về | `release: khóa bản nộp cuối v1.0.3` |

## Điều kiện hoàn thành

1. Website Streamlit mở được trong phiên chưa đăng nhập và thực hiện dự đoán thành công.
2. Không còn tài liệu đang hoạt động ghi sai CV Macro F1 89,32% hoặc 91,47%.
3. Script xác minh tạo virtual environment mới, cài dependency từ `requirements.txt` và không gọi Python trong `.venv` của repository.
4. Toàn bộ kiểm thử đạt từ mã nguồn trong ZIP sau khi cài đặt mới.
5. SHA-256 của asset tải xuống từ GitHub Release khớp checksum đã công bố.
6. CI tự động kiểm tra phiên bản, số liệu và cấu trúc gói phát hành.
7. Demo online, demo offline, slide và phần trình bày ba thành viên được thử trên máy dùng để bảo vệ.
8. Tag `v1.0.3`, GitHub Release, commit và asset ZIP cùng thuộc một bản nghiệm thu.

## Prompt giao cho AI

> Hãy thực hiện Plan 6 trong repo `thinh204/phan-loai-van-ban-naive-bayes`. Trước tiên đọc số liệu từ `results/alpha_tuning.json` và sửa mọi tài liệu cùng mô tả GitHub Release đang ghi sai CV Macro F1; giá trị đúng của `alpha=1.0` là 88,55% và `alpha=0.1` là 90,28%. Không tự nhập số liệu nếu có thể đọc trực tiếp từ tệp kết quả. Tiếp theo mở Streamlit Community Cloud, kiểm tra ứng dụng trỏ đúng repository, branch `main` và file `app.py`; đọc log và xử lý cho đến khi URL công khai mở được trong phiên chưa đăng nhập. Thực hiện một dự đoán và thử tải CSV trên website rồi ghi bằng chứng có thời điểm kiểm tra. Sửa `scripts/verify_clean_package.py` để tạo virtual environment mới trong thư mục tạm, cài dependency từ `requirements.txt` và chạy compile, 16 kiểm thử cùng suy diễn bằng Python của môi trường mới; tuyệt đối không dùng `.venv` của workspace để gọi đó là kiểm tra sạch. Tải asset ZIP từ GitHub Release, tính SHA-256 và đối chiếu với checksum đã công bố. Thêm kiểm tra CI để phát hiện sai lệch giữa cấu hình phiên bản, JSON kết quả, tài liệu và cấu trúc gói. Sau khi chạy thử demo online, offline, slide và kịch bản ba thành viên trên máy bảo vệ, tạo lại ZIP, manifest, checksum và phát hành `v1.0.3` từ đúng commit cuối. Sau mỗi giai đoạn phải kiểm tra, commit và push với chú thích rõ ràng. Không huấn luyện lại, không đổi mô hình, không dùng tập test để chọn tham số và không ghi trạng thái hoàn thành nếu chưa xác minh trực tiếp.
