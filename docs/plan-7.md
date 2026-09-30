# Plan 7: Hoàn tất website công khai và phát hành v1.0.3

## Bối cảnh

Plan 6 đã hoàn thành phần lớn công việc kỹ thuật nhưng chưa thể đóng lại vì website Streamlit công khai vẫn trả về trang **Not found**. Repository hiện có các thay đổi bản `v1.0.3` chưa commit, 21 kiểm thử đang đạt và chưa có tag hoặc GitHub Release `v1.0.3`.

Plan 7 tiếp quản đúng trạng thái hiện tại để hoàn tất bản phát hành. Không tạo lại dự án, không huấn luyện lại mô hình và không bỏ các thay đổi Plan 6 đang có trong working tree.

## Mục tiêu

Đưa website Streamlit vào hoạt động công khai, nghiệm thu các chức năng chính trên chính website đó, hoàn tất các thay đổi đang chờ và phát hành `v1.0.3` có thể kiểm chứng.

## Các giai đoạn

| Giai đoạn | Công việc | Kết quả bàn giao | Commit đề xuất |
| --- | --- | --- | --- |
| 1. Bảo toàn trạng thái hiện tại | Kiểm kê toàn bộ tệp đã sửa và chưa theo dõi; phân loại thay đổi Plan 6; không reset, checkout hoặc xóa các tệp đang làm dở | Danh sách thay đổi cần hoàn tất, không mất công việc | `chore: rà soát trạng thái phát hành v1.0.3` |
| 2. Chẩn đoán Streamlit Cloud | Đăng nhập Streamlit Community Cloud, kiểm tra ứng dụng có tồn tại, repository, branch `main`, file `app.py`, quyền GitHub và log triển khai | Xác định nguyên nhân cụ thể của trang Not found | `docs: ghi nhận chẩn đoán triển khai Streamlit` |
| 3. Khôi phục website | Tạo mới hoặc sửa cấu hình ứng dụng trên Streamlit Cloud; redeploy và xử lý log cho đến khi ứng dụng tải hoàn chỉnh | URL công khai hiển thị giao diện `v1.0.3 – Plan 6` | `deploy: khôi phục website Streamlit công khai` |
| 4. Nghiệm thu trên web | Dùng phiên chưa đăng nhập để thử bốn chủ đề, đầu vào rỗng, văn bản ngắn, OOV, độ tin cậy thấp, giải thích từ khóa và tải CSV | Biên bản nghiệm thu website với trạng thái từng ca | `test: nghiệm thu website Streamlit công khai` |
| 5. Hoàn tất thay đổi Plan 6 | Rà soát các tệp đang sửa, chạy `git diff --check`, 21 kiểm thử, compileall, đóng gói và xác minh môi trường sạch; commit theo nhóm chức năng | Working tree sạch, toàn bộ kiểm tra đạt | `release: hoàn tất ứng viên phát hành v1.0.3` |
| 6. Tạo lại tài sản phát hành | Tạo ZIP bằng script, tạo lại manifest và checksum sau commit cuối; bảo đảm dữ liệu trong ZIP đúng với commit phát hành | ZIP, manifest và checksum đồng bộ | `build: tạo tài sản phát hành v1.0.3` |
| 7. Phát hành v1.0.3 | Push `main`, đợi CI xanh, tạo annotated tag `v1.0.3`, xuất bản GitHub Release và đính kèm ZIP cùng checksum | Release `v1.0.3` trỏ đúng commit và có đủ asset | `release: phát hành phiên bản v1.0.3` |
| 8. Kiểm tra sau phát hành | Tải ZIP từ GitHub Release, đối chiếu SHA-256, mở lại website bằng phiên chưa đăng nhập và chạy một dự đoán cuối | Biên bản hậu kiểm xác nhận bản phát hành sử dụng được | `docs: xác nhận hậu kiểm bản phát hành v1.0.3` |

## Điều kiện hoàn thành

1. URL `https://phan-loai-van-ban-naive-bayes.streamlit.app` mở được mà không yêu cầu đăng nhập.
2. Website hiển thị đúng phiên bản `v1.0.3 – Plan 6` và thực hiện dự đoán thành công.
3. Các ca nhập liệu chính, cảnh báo và tải CSV đều được kiểm tra trên website công khai.
4. `python -m pytest -q` đạt toàn bộ **21 kiểm thử** và `compileall` không báo lỗi.
5. Script kiểm tra gói chạy bằng virtual environment mới được tạo trong thư mục tạm.
6. Working tree sạch trước khi tạo tag.
7. CI của commit phát hành có trạng thái thành công.
8. Tag, GitHub Release, ZIP và SHA-256 cùng đại diện cho một commit `v1.0.3`.

## Prompt giao cho AI

> Hãy thực hiện Plan 7 trong repo `thinh204/phan-loai-van-ban-naive-bayes` từ đúng trạng thái working tree hiện tại. Trước tiên kiểm kê và bảo toàn mọi thay đổi Plan 6 đang chưa commit; không dùng `git reset`, `git checkout` hoặc xóa tệp để làm sạch repository. Kiểm tra Streamlit Community Cloud bằng tài khoản chủ repository: xác minh ứng dụng có tồn tại, kết nối GitHub còn hiệu lực, repository đúng, branch là `main`, entrypoint là `app.py` và xem deployment logs. Nếu ứng dụng không tồn tại thì tạo lại với subdomain phù hợp; nếu bị lỗi thì sửa theo log và redeploy. Chỉ công bố hoàn thành khi URL mở được trong một phiên chưa đăng nhập và hiển thị giao diện `v1.0.3 – Plan 6`. Trên website công khai, kiểm tra dự đoán bốn chủ đề, văn bản rỗng, quá ngắn, OOV, độ tin cậy thấp, phần giải thích và tải CSV; ghi kết quả thật vào biên bản. Sau đó rà soát các thay đổi đang chờ, chạy `git diff --check`, `python -m compileall -q app.py src tests scripts`, toàn bộ 21 kiểm thử và script xác minh môi trường sạch. Commit các thay đổi theo nhóm chức năng rõ ràng. Tạo lại ZIP, manifest và checksum sau commit cuối, chạy lại kiểm tra rồi push `main`. Chờ GitHub Actions thành công, tạo annotated tag `v1.0.3`, xuất bản GitHub Release và đính kèm ZIP cùng checksum. Cuối cùng tải lại asset từ Release, so sánh SHA-256 và kiểm tra thêm một dự đoán trên website bằng phiên chưa đăng nhập. Không huấn luyện lại, không đổi mô hình, không dùng tập test để chọn tham số và không ghi trạng thái hoàn thành khi chưa có bằng chứng trực tiếp.
