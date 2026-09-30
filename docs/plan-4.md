# Plan 4: Nghiệm thu, triển khai chính thức và đóng gói bài nộp

## Kết quả kiểm tra Plan 3

Plan 3 đã hoàn thành phần triển khai trong mã nguồn: môi trường có thể chạy lại, GitHub Actions đã được cấu hình, giao diện có cảnh báo đầu vào và giải thích dự đoán, tài liệu demo đã được bổ sung, đồng thời tag `v1.0.0` đã được tạo. Kết quả kiểm tra tại máy ngày 30/09/2026:

- `python -m pytest -q`: **16/16 kiểm thử đạt**.
- `python -m compileall -q app.py src tests`: **đạt**.
- Mô hình giữ nguyên `MultinomialNB(alpha=0.1)` với Test Accuracy **88,52%** và Macro F1 **88,33%**.
- Chưa có URL Streamlit đã được xác minh trong tài liệu.
- Tag `v1.0.0` đã có, nhưng cần kiểm tra và xuất bản GitHub Release trên repository.
- Một số tài liệu cũ vẫn ghi Plan 1 & Plan 2 hoặc 14 kiểm thử, trong khi dự án hiện có 16 kiểm thử.

## Mục tiêu

Đưa dự án từ trạng thái hoàn thiện mã nguồn sang trạng thái có thể trình diễn, nghiệm thu và nộp bài. Plan này không huấn luyện lại, không thay đổi mô hình và không dùng tập test để lựa chọn thêm tham số.

## Các giai đoạn

| Giai đoạn | Công việc | Kết quả bàn giao | Commit đề xuất |
| --- | --- | --- | --- |
| 1. Đồng bộ GitHub | Push toàn bộ commit Plan 3, Plan 4 và tag `v1.0.0`; kiểm tra lịch sử commit trên GitHub | Nhánh `main` và tag trên GitHub khớp với máy | `chore: đồng bộ mã nguồn và tag phát hành` |
| 2. Xác minh CI | Mở GitHub Actions, xử lý lỗi nếu có và lưu bằng chứng workflow chạy thành công trên Python 3.10, 3.11 | Workflow CI có trạng thái xanh | `ci: hoàn tất xác minh quy trình kiểm thử` |
| 3. Triển khai trực tuyến | Triển khai repository trên Streamlit Community Cloud, kiểm tra ứng dụng và ghi URL thật vào README cùng hướng dẫn | URL demo Streamlit hoạt động | `deploy: công bố ứng dụng Streamlit trực tuyến` |
| 4. Nghiệm thu chức năng | Kiểm tra bốn lớp dự đoán, văn bản rỗng, văn bản ngắn, OOV, cảnh báo độ tin cậy thấp, giải thích từ khóa và tải CSV | Biên bản nghiệm thu có kết quả từng trường hợp | `test: nghiệm thu toàn bộ luồng ứng dụng` |
| 5. Đồng bộ tài liệu | Sửa các chỗ còn ghi Plan 1 & Plan 2 hoặc 14 kiểm thử; đối chiếu README, báo cáo, kịch bản và slide với kết quả thật | Tài liệu thống nhất: Plan 4, 16 kiểm thử và đúng số liệu | `docs: đồng bộ tài liệu và số liệu nghiệm thu` |
| 6. Rà soát slide bảo vệ | Kiểm tra slide có `alpha=0.1`, Accuracy 88,52%, Macro F1 88,33%, 16 kiểm thử và các chức năng mới của Plan 3 | Slide sẵn sàng thuyết trình | `docs: cập nhật slide bảo vệ bản cuối` |
| 7. Đóng gói bài nộp | Lập checklist gồm mã nguồn, báo cáo, slide, URL demo, hướng dẫn chạy và phương án demo ngoại tuyến; tạo gói nộp cuối | Bộ hồ sơ nộp có thể mở và chạy lại | `release: đóng gói hồ sơ nộp cuối` |
| 8. Phát hành | Xuất bản GitHub Release từ tag `v1.0.0`; nếu có sửa lỗi sau nghiệm thu thì tạo `v1.0.1` và ghi release notes mới | GitHub Release công khai, có mô tả và phiên bản rõ ràng | `release: phát hành phiên bản nghiệm thu` |

## Điều kiện hoàn thành

1. Nhánh `main`, tag và lịch sử commit hiển thị đầy đủ trên GitHub.
2. GitHub Actions chạy thành công cho phiên bản được nộp.
3. URL Streamlit mở được và thực hiện dự đoán thành công.
4. Các trường hợp chính và trường hợp biên trong biên bản nghiệm thu đều đạt.
5. README, báo cáo, slide và giao diện dùng cùng số liệu thực nghiệm.
6. Bộ bài nộp chứa đủ mã nguồn, tài liệu, slide, đường dẫn demo và hướng dẫn chạy ngoại tuyến.
7. GitHub Release được xuất bản từ đúng commit đã nghiệm thu.
8. Mỗi giai đoạn có commit riêng với chú thích nêu rõ thay đổi và kết quả kiểm tra.

## Prompt giao cho AI

> Hãy thực hiện Plan 4 trong repo `thinh204/phan-loai-van-ban-naive-bayes`. Trước tiên đồng bộ toàn bộ commit và tag `v1.0.0` lên GitHub, sau đó kiểm tra GitHub Actions chạy thành công trên Python 3.10 và 3.11. Triển khai ứng dụng trên Streamlit Community Cloud, tự kiểm tra URL thật và cập nhật URL đó vào README cùng tài liệu triển khai. Nghiệm thu đủ bốn lớp dự đoán và các trường hợp văn bản rỗng, quá ngắn, OOV, độ tin cậy thấp, giải thích từ khóa và tải CSV; ghi kết quả vào tài liệu nghiệm thu. Rà soát toàn bộ README, báo cáo, kịch bản và slide để sửa các nội dung cũ như “Plan 1 & Plan 2” và “14 test cases” thành trạng thái thực tế của dự án là Plan 4 và 16 kiểm thử. Đối chiếu slide với mô hình `MultinomialNB(alpha=0.1)`, Test Accuracy 88,52% và Macro F1 88,33%. Sau đó tạo checklist, đóng gói bộ bài nộp và xuất bản GitHub Release từ đúng commit đã nghiệm thu. Nếu phải sửa lỗi sau tag `v1.0.0`, hãy phát hành `v1.0.1`; không di chuyển tag cũ. Sau mỗi giai đoạn phải chạy kiểm tra phù hợp, commit và push với chú thích rõ ràng. Không huấn luyện lại, không thay đổi mô hình, không dùng tập test để chọn tham số và không tự tạo số liệu hoặc URL triển khai.
