# Plan 8: Khôi phục website công khai và nghiệm thu bằng bằng chứng thực tế

## Bối cảnh và mục tiêu

Repo: `thinh204/phan-loai-van-ban-naive-bayes`. Thư mục: `D:\phan-loai-van-ban-naive-bayes`.

Theo lần hậu kiểm gần nhất ngày 30/09/2026: 21 kiểm thử đạt, GitHub Actions thành công, Release `v1.0.3` tồn tại và SHA-256 của ZIP tải xuống khớp. Tuy nhiên URL `https://phan-loai-van-ban-naive-bayes.streamlit.app` chuyển đến trang **Not found**, với thông báo không có quyền truy cập hoặc ứng dụng không tồn tại. Các tài liệu ghi website đã đạt chưa phù hợp với quan sát này. AI phải kiểm tra lại trạng thái hiện tại trước khi sửa.

Mục tiêu: website mở được cho người xem chưa đăng nhập, thực hiện dự đoán và tải CSV thành công; tài liệu phản ánh đúng kết quả quan sát. Giữ Python, Pandas, TF-IDF, Multinomial Naive Bayes và Streamlit hiện có.

## Quy trình giao cho AI

### 1. Kiểm kê trạng thái

- Đọc hướng dẫn repo, `docs/plan-7.md`, tài liệu triển khai và các biên bản web hiện có.
- Kiểm tra branch, remote, working tree và commit gần nhất. Bảo toàn thay đổi đang làm dở, nếu có.
- Mở lại URL công khai và ghi thời điểm, URL cuối sau chuyển hướng, nội dung nhìn thấy. HTTP 200 hoặc trang đăng nhập không đủ chứng minh ứng dụng hoạt động.

### 2. Xác định nguyên nhân qua Streamlit Community Cloud

- Dùng phiên tài khoản chủ dự án trên dashboard Streamlit: xác minh ứng dụng tồn tại, URL thực tế, repository, branch `main`, entrypoint `app.py`, cấu hình người xem và trạng thái triển khai.
- Đọc log triển khai để xác định lỗi cụ thể. Phân biệt lỗi URL, quyền người xem, kết nối GitHub và lỗi chạy ứng dụng; không kết luận nguyên nhân từ phỏng đoán trong tài liệu cũ.
- Nếu cần đăng nhập, OAuth, mã xác minh hoặc thao tác chỉ chủ tài khoản làm được, yêu cầu đúng thao tác đó và ghi phần đang chờ. Tiếp tục phần độc lập; không tự ghi đã khắc phục.

### 3. Khắc phục và triển khai

- Sửa ứng dụng hiện có theo nguyên nhân quan sát. Chỉ tạo ứng dụng mới khi xác nhận ứng dụng cần dùng chưa tồn tại; tránh tạo nhiều bản trùng.
- Bật quyền xem công khai theo tùy chọn thực tế của dashboard; kiểm tra nguồn triển khai đúng repo, branch và file.
- Nếu URL cũ không thể sử dụng, lấy URL thật từ dashboard, kiểm thử URL mới và cập nhật mọi liên kết demo trong repo. Ghi rõ lý do đổi URL.
- Nếu log báo lỗi phụ thuộc, đường dẫn hoặc thiếu mô hình, sửa tối thiểu rồi redeploy; không huấn luyện lại hoặc thay đổi các kết quả thực nghiệm đã chốt.
- Ghi commit nguồn mà deployment sử dụng nếu dashboard cung cấp. Nếu không có thông tin này, ghi rõ chưa xác minh được thay vì đoán.

### 4. Nghiệm thu trực tiếp trên website công khai

Dùng phiên trình duyệt sạch, chưa đăng nhập Streamlit; mở URL trực tiếp. Phiên đã đăng nhập chủ ứng dụng và localhost không thay thế được bước này.

| Ca kiểm tra | Điều kiện đạt |
| --- | --- |
| Truy cập công khai | Hiển thị giao diện đầy đủ, không yêu cầu đăng nhập, không Not found hoặc lỗi ứng dụng |
| Bốn chủ đề | Chạy từng văn bản tiếng Anh cho `comp.graphics`, `rec.sport.baseball`, `sci.space`, `talk.politics.misc`; lưu đầu vào, nhãn dự đoán và xác suất thực tế |
| Rỗng và khoảng trắng | Thông báo nhập liệu rõ ràng, không crash |
| Văn bản ngắn | Cảnh báo phù hợp logic hiện có, không crash |
| OOV | Dùng chuỗi ngoài từ điển; kiểm tra cảnh báo thực tế |
| Độ tin cậy thấp | Dùng đầu vào tạo ra xác suất dưới ngưỡng cấu hình; ghi giá trị thực, chỉ đánh dấu đạt khi thực sự quan sát được |
| Giải thích | Từ khóa TF-IDF và xác suất hiển thị sau dự đoán |
| Lịch sử và CSV | Thực hiện ít nhất hai dự đoán, tải CSV và mở file để đối chiếu số dòng, văn bản, nhãn với lịch sử |
| Tải lại trang | Mở lại URL công khai và dự đoán thành công một lần nữa |

Lưu bằng chứng vào `docs/evidence/plan-8/`: ảnh giao diện công khai, kết quả dự đoán, ảnh dashboard hoặc log đã che thông tin riêng tư và CSV thử nghiệm. Với mỗi ca ghi thời điểm, đầu vào, mong đợi, kết quả thực tế, trạng thái và đường dẫn bằng chứng trong `docs/NGHIEM_THU_PLAN_8.md`. Không tạo ảnh giả, không sao chép số liệu dự đoán từ biên bản cũ. Dự đoán sai phải được ghi thật, không sửa đầu ra để đạt nhãn mong muốn.

### 5. Đồng bộ tài liệu và kiểm tra hồi quy

- Đính chính các tuyên bố website đã hoàn thành trong README, `docs/CHAN_DOAN_STREAMLIT.md`, `docs/NGHIEM_THU_WEB_CONG_KHAI.md`, `docs/HAU_KIEM_V1.0.3.md` và checklist liên quan. Giữ lịch sử, thêm ghi chú đính chính có ngày và dẫn tới bằng chứng mới.
- Cập nhật README với URL đã kiểm chứng và số kiểm thử thực tế. Không ghi localhost thành URL công khai.
- Chạy bằng môi trường của dự án:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m compileall -q app.py src tests scripts
git diff --check
```

- Mốc hiện tại là 21 kiểm thử; nếu số lượng thay đổi, giải thích lý do. Chỉ bổ sung kiểm thử khi sửa lỗi hành vi có nguy cơ tái diễn.

### 6. Commit, push và chốt kết quả

- Sau mỗi giai đoạn có thay đổi tệp, commit với mô tả cụ thể và push lên GitHub. Không tạo commit rỗng chỉ để đánh dấu tiến độ.
- Ví dụ: `docs: ghi nhận nguyên nhân lỗi web Plan 8`, `fix: sửa lỗi triển khai Streamlit`, `docs: đính chính và nghiệm thu website Plan 8`.
- Chờ CI của commit nguồn cuối thành công; kiểm tra website sau khi Cloud cập nhật nguồn.
- Giữ nguyên tag và asset Release `v1.0.3`. Nếu cần phát hành gói nguồn mới do thay đổi mã hoặc tài liệu bản nộp, dùng phiên bản mới `v1.0.4`, đồng bộ version, ZIP, manifest, checksum, kiểm tra gói sạch và tải asset từ Release để đối chiếu. Không ghi đè lịch sử `v1.0.3`.
- Báo cáo cuối: URL thực tế, commit nguồn, liên kết CI, kết quả test, đường dẫn bằng chứng, commit đã push và phần còn chờ nếu có.

## Điều kiện đóng Plan 8

Chỉ đánh dấu **Hoàn thành** khi website công khai được kiểm tra trong phiên chưa đăng nhập, dự đoán và CSV hoạt động, các ca trên có kết quả thật, tài liệu đã đính chính, kiểm thử đạt và thay đổi đã push với CI thành công. Nếu thiếu quyền tài khoản hoặc không mở được website, ghi **Chưa hoàn thành** cùng thao tác cần chủ tài khoản thực hiện.

## Prompt để anh giao cho AI

> Hãy thực hiện toàn bộ `docs/plan-8.md` trong `D:\phan-loai-van-ban-naive-bayes`. Mục tiêu là khắc phục website Streamlit công khai đang chưa được nghiệm thu thành công. Kiểm tra trạng thái hiện tại, xác định nguyên nhân bằng dashboard và log thật, sửa rồi kiểm thử trên phiên chưa đăng nhập. Lưu bằng chứng từng ca, đính chính các biên bản cũ có tuyên bố chưa được xác minh. Giữ nguyên mô hình và số liệu thực nghiệm. Sau mỗi giai đoạn có thay đổi tệp hãy commit có chú thích rõ ràng và push lên GitHub, đợi CI thành công. Không ghi đè Release v1.0.3 và không báo hoàn thành chỉ vì localhost hoặc tests chạy được. Nếu cần chủ tài khoản đăng nhập hay xác minh, nêu chính xác thao tác còn thiếu và giữ trạng thái chưa hoàn thành cho đến khi có bằng chứng web thực tế.
