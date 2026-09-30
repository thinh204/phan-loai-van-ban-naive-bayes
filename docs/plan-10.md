# Plan 10: Sửa nhập liệu rỗng, lịch sử CSV và phát hành bản sửa lỗi

## Bối cảnh

Repo `thinh204/phan-loai-van-ban-naive-bayes`, thư mục `D:\phan-loai-van-ban-naive-bayes`.

Website `https://phan-loai-van-ban-naive-bayes.streamlit.app/` đang mở công khai. Hậu kiểm Plan 9 xác nhận 21/21 tests và CI commit `97d12cf` đạt, có ảnh và CSV nghiệm thu. Tuy nhiên còn hai lỗi:

1. `app.py` nối `(Rỗng)` vào mọi đoạn trích dài không quá 80 ký tự: CSV có `space(Rỗng)` và `zxqvbnm qqqzxvv(Rỗng)`.
2. Nhấn phân loại với đầu vào rỗng hoặc chỉ khoảng trắng vẫn tạo kết quả tiên nghiệm và thêm một dòng lịch sử, trái điều kiện Plan 9.

Biên bản ghi 13/13 đạt cần được đính chính. Báo cáo JSON còn đếm lịch sử thành 24 hàng do lấy cả các bảng khác; cần đếm riêng bảng lịch sử.

## Mục tiêu và phạm vi

Sửa hai lỗi giao diện, bổ sung kiểm thử hành vi, nghiệm thu lại trên Cloud và phát hành `v1.0.4` chứa bản sửa. Giữ thuật toán, vectorizer, mô hình và số liệu thực nghiệm. Không mở rộng tính năng.

## Các giai đoạn thực hiện

### 1. Kiểm kê và tái hiện

- Đọc hướng dẫn repo, Plan 9 và biên bản; kiểm tra working tree và bảo toàn thay đổi có sẵn.
- Tái hiện hai lỗi bằng ứng dụng thật và CSV tải xuống. Ghi đầu vào, kết quả và thời điểm; không chỉ đọc mã rồi đánh dấu đã thử.
- Xem scripts đóng gói, manifest, xác minh môi trường sạch và kiểm tra asset trước khi dùng; không đoán tham số CLI.

### 2. Sửa hành vi trong ứng dụng Streamlit

- Khi bấm phân loại, dùng chuỗi sau `strip()` để kiểm tra rỗng. Nếu rỗng, chỉ hiển thị yêu cầu nhập văn bản; không gọi dịch vụ phân loại, không thêm lịch sử và không tạo kết quả mới từ xác suất tiên nghiệm.
- Với đầu vào hợp lệ, đoạn trích bằng văn bản đã chuẩn hóa khoảng trắng ở hai đầu. Nếu dài hơn 80 ký tự, lấy 80 ký tự đầu và thêm `...`; nếu không, giữ nguyên. Không thêm `(Rỗng)` vào văn bản không rỗng.
- Không cần thay đổi khả năng xử lý chuỗi rỗng của service nếu đó là hợp đồng hiện có; kiểm soát yêu cầu người dùng tại giao diện.
- Giữ cảnh báo OOV, văn bản ngắn và tin cậy thấp cho đầu vào không rỗng. Những trường hợp này vẫn được phân loại và lưu lịch sử.
- CSV tiếp tục có các cột hiện có, giá trị khớp lịch sử. Không sửa bằng chứng CSV cũ để che lỗi.

### 3. Kiểm thử hồi quy có ý nghĩa

Ưu tiên Streamlit AppTest hoặc kiểm thử hành vi tương đương; có thể tách hàm tạo đoạn trích để kiểm thử nhưng vẫn cần kiểm tra luồng giao diện.

| Trường hợp | Kết quả bắt buộc |
| --- | --- |
| Chuỗi rỗng và toàn khoảng trắng ở phiên mới | Có thông báo, lịch sử vẫn 0 dòng, không tạo nhãn dự đoán mới |
| Đã có một lượt hợp lệ, sau đó gửi khoảng trắng | Lịch sử giữ nguyên số dòng, không thêm lượt rỗng |
| `space` | Đoạn trích đúng `space`, cảnh báo ngắn vẫn hoạt động |
| Văn bản đúng 80 ký tự | Không thêm dấu ba chấm hoặc `(Rỗng)` |
| Văn bản 81 ký tự | 80 ký tự đầu + `...` |
| OOV không rỗng | Có cảnh báo và lịch sử hợp lệ, không có hậu tố `(Rỗng)` |
| CSV | Đoạn trích, nhãn, số dòng khớp lịch sử sau chuỗi thao tác |

- Kiểm thử phải thất bại với lỗi cũ và đạt sau khi sửa. Không chỉ tìm chuỗi trong mã nguồn để kết luận hành vi đúng.
- Chạy toàn bộ tests, compileall và `git diff --check`. Ghi số kiểm thử thật; mốc trước sửa là 21.
- Commit sửa mã và kiểm thử với mô tả rõ ràng, rồi push để Cloud triển khai; đợi CI đạt.

### 4. Nghiệm thu lại trên Cloud

- Dùng phiên chưa đăng nhập tại URL công khai, xác nhận deployment đã nhận bản sửa bằng phiên bản và hành vi thực tế. Nếu có thông tin commit trong dashboard thì ghi lại; nếu không, ghi chưa xác minh được commit triển khai.
- Thử bốn chủ đề, giải thích, ngắn, OOV và tin cậy thấp để kiểm tra hồi quy. Ghi nhãn/xác suất thật, không yêu cầu xác suất phải bằng lần cũ.
- Thử rỗng và khoảng trắng ở phiên mới, sau đó một lượt hợp lệ rồi khoảng trắng. Kiểm tra số dòng lịch sử không tăng sau yêu cầu rỗng.
- Thử đoạn trích 80 và 81 ký tự, tải CSV thật, mở file và đối chiếu từng dòng với thao tác. Đếm riêng dữ liệu lịch sử, không đếm hàng của bảng xác suất hoặc giải thích.
- Kiểm tra xóa lịch sử, tải lại trang và một dự đoán mới.
- Lưu ảnh, CSV và báo cáo vào `docs/evidence/plan-10/`; ghi biên bản `docs/NGHIEM_THU_PLAN_10.md` với đầu vào, thời điểm, mong đợi, kết quả thật, trạng thái và đường dẫn bằng chứng từng ca.

### 5. Đính chính và đồng bộ tài liệu

- Thêm ghi chú vào biên bản Plan 9: lần nghiệm thu trước có lỗi đoạn trích và lượt rỗng chưa đạt. Giữ ảnh/CSV cũ làm lịch sử, dẫn tới bằng chứng đã sửa trong Plan 10.
- Đính chính `history_rows_count: 24` bằng ghi chú giải thích sai phạm vi đếm; không thay báo cáo cũ thành bằng chứng giả của lần kiểm tra mới.
- Ghi rõ thông tin dashboard nào chưa xác minh. Cập nhật README, checklist, hướng dẫn triển khai và bản nộp với số tests, phiên bản và URL thật.
- Giữ số liệu mô hình: Accuracy 88,52%, Macro F1 88,33%, CV alpha=1.0 là 88,55%, alpha=0.1 là 90,28%; đối chiếu file kết quả hiện có.

### 6. Phát hành v1.0.4 và bàn giao

- Đồng bộ phiên bản tập trung và các tài liệu/kiểm thử liên quan thành `v1.0.4`. Giá trị Plan trong footer cập nhật nhất quán nếu đổi, không đổi rải rác từng chuỗi.
- Dùng script hiện có để tạo gói nộp, manifest và checksum; bảo đảm gói chứa bản sửa và tài liệu nghiệm thu mới. Chạy xác minh gói bằng môi trường sạch.
- Commit theo nhóm thay đổi, push và chờ CI của commit dùng để phát hành thành công. Bảo đảm working tree sạch trước tag; ghi rõ commit nguồn và commit chứa asset nếu quy trình dùng hai commit.
- Tạo annotated tag và GitHub Release mới `v1.0.4`, đính kèm ZIP, manifest và checksum. Giữ nguyên `v1.0.3`.
- Tải asset từ Release và đối chiếu SHA-256 với checksum; kiểm tra website hiển thị phiên bản mới và thử lại đầu vào rỗng cùng một dự đoán hợp lệ sau triển khai cuối.
- Báo cáo cuối: URL, trạng thái từng ca, số tests, commit/CI, Release, SHA-256 và đường dẫn bằng chứng. Nếu còn bước chờ quyền tài khoản, ghi chính xác bước đó.

## Điều kiện hoàn thành

Hai lỗi đã sửa cả trên local và Cloud; rỗng không tạo lượt dự đoán; đoạn trích và CSV đúng; kiểm thử hồi quy đạt; có bằng chứng thật; tài liệu đính chính; thay đổi đã push và CI đạt; Release v1.0.4 tải được với checksum khớp. Không ghi hoàn thành trước khi nghiệm thu Cloud sau sửa.

## Prompt giao cho AI

> Thực hiện toàn bộ `docs/plan-10.md` trong `D:\phan-loai-van-ban-naive-bayes`. Sửa đầu vào rỗng không được phân loại hoặc thêm lịch sử, và sửa đoạn trích ngắn bị thêm `(Rỗng)` vào lịch sử/CSV. Thêm kiểm thử hành vi tái hiện được lỗi cũ, chạy tests rồi push để triển khai. Kiểm thử lại website công khai và tải CSV thật, lưu bằng chứng, đính chính kết luận Plan 9. Giữ mô hình và số liệu thực nghiệm. Commit có chú thích sau từng nhóm thay đổi, đợi CI đạt, phát hành v1.0.4 với gói/manifest/checksum đồng bộ và tải lại asset để xác minh. Chỉ báo hoàn thành khi đủ các điều kiện trong plan.
