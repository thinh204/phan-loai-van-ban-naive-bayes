# Plan 9: Nghiệm thu website đang chạy và chốt bản nộp

## Trạng thái tiếp nhận

- Dự án: `D:\phan-loai-van-ban-naive-bayes`, GitHub: `thinh204/phan-loai-van-ban-naive-bayes`.
- Ngày 30/09/2026, kiểm tra trực tiếp xác nhận URL `https://phan-loai-van-ban-naive-bayes.streamlit.app/` đã mở được khi dashboard Streamlit vẫn yêu cầu đăng nhập. Giao diện hiển thị `v1.0.3 – Plan 6`.
- Đầu vào đã thử: `NASA launched a spacecraft into orbit to study distant planets and explore the solar system.` Kết quả quan sát: `sci.space`, xác suất 99,44%, 16,79 ms; có phân bố xác suất, giải thích từ khóa và một dòng lịch sử.
- Đây là kiểm tra ban đầu, chưa thay thế nghiệm thu đầy đủ. Chưa xác minh tải CSV, các ca biên hoặc commit nguồn Cloud đang sử dụng.
- Repo hiện còn biên bản Plan 8 ghi website chưa chạy. Release `v1.0.3` đã tồn tại. Lần chạy kiểm thử gần nhất đạt 21/21.

## Mục tiêu

Nghiệm thu đầy đủ trên website công khai, cập nhật trạng thái Plan 8 bằng bằng chứng mới, đồng bộ tài liệu và hoàn tất bản nộp có thể đối chiếu. Giữ phương pháp TF-IDF + Multinomial Naive Bayes, dataset và kết quả thực nghiệm đã chốt.

## Các bước AI cần thực hiện

### 1. Kiểm tra nguồn và truy cập công khai

- Đọc hướng dẫn repo và Plan 8; kiểm kê working tree, bảo toàn thay đổi có sẵn.
- Mở URL trực tiếp bằng phiên chưa đăng nhập Streamlit. Chờ tải giao diện và chạy dự đoán; không lấy HTTP 200 hoặc healthcheck làm bằng chứng thay thế.
- Nếu dashboard sẵn có quyền truy cập, ghi repository, branch, entrypoint, URL và commit triển khai khi có thông tin. Nếu cần đăng nhập, đề nghị chủ tài khoản thực hiện; không đoán thông tin dashboard.
- Nếu website lại lỗi, ghi thời điểm và lỗi thực tế, xử lý theo Plan 8 trước khi nghiệm thu tiếp.

### 2. Kiểm thử chức năng trên website

Lưu từng đầu vào, kết quả thực tế, thời điểm, trạng thái và bằng chứng vào `docs/NGHIEM_THU_PLAN_9.md`. Các câu dưới đây là đầu vào đề xuất; không ấn định trước nhãn hoặc xác suất thực tế.

| Ca | Đầu vào / thao tác | Kiểm tra |
| --- | --- | --- |
| Đồ họa | `The graphics software renders three dimensional images using polygons, textures and computer animation.` | Nhãn, xác suất, biểu đồ và giải thích |
| Bóng chày | `The baseball pitcher threw the ball and the batter hit a home run during the game.` | Nhãn, xác suất và lịch sử |
| Vũ trụ | Câu NASA trong phần trạng thái tiếp nhận | Chạy lại, lưu kết quả mới |
| Chính trị | `The government and parliament debated public policy, elections and political reform.` | Nhãn, xác suất và lịch sử |
| Rỗng | Chuỗi rỗng và chuỗi toàn khoảng trắng | Thông báo phù hợp, không crash hoặc thêm dự đoán giả vào lịch sử |
| Ngắn | `space` | Cảnh báo theo ngưỡng thực tế trong mã nguồn |
| OOV | `zxqvbnm qqqzxvv` | Cảnh báo từ ngoài từ điển, không crash |
| Tin cậy thấp | Thử văn bản trộn các chủ đề | Ghi xác suất quan sát; chỉ xác nhận cảnh báo khi thực sự dưới ngưỡng cấu hình |
| Giải thích | Sau một dự đoán hợp lệ | Đối chiếu từ khóa, TF-IDF và thông tin đóng góp hiển thị |
| Lịch sử | Sau ít nhất hai dự đoán hợp lệ | Số lượt, văn bản và nhãn khớp các thao tác |
| CSV | Bấm tải lịch sử, mở CSV tải thật từ Cloud | Số dòng, văn bản, nhãn và giá trị khớp lịch sử; ghi tên cột thực tế |
| Xóa lịch sử | Sau khi lưu CSV làm bằng chứng | Lịch sử phiên được xóa và có thông báo phù hợp |
| Tải lại | Mở lại URL, chạy một dự đoán mới | Website tiếp tục hoạt động; lịch sử theo hành vi phiên thực tế |

- Lưu ảnh và CSV thật trong `docs/evidence/plan-9/`; dùng văn bản thử nghiệm, che dữ liệu tài khoản riêng tư.
- Ghi nhãn sai hoặc cảnh báo không xuất hiện đúng như quan sát. Phân biệt giới hạn mô hình và lỗi ứng dụng; không sửa số liệu để đánh dấu đạt.
- Nếu có lỗi ứng dụng, sửa tối thiểu, bổ sung kiểm thử hồi quy phù hợp và thử lại chính ca lỗi trên Cloud sau redeploy.

### 3. Cập nhật tài liệu và đóng Plan 8

- Thêm ghi chú có ngày vào `docs/NGHIEM_THU_PLAN_8.md`, dẫn tới bằng chứng Plan 9. Chỉ đổi trạng thái Plan 8 thành hoàn thành khi các điều kiện của nó đã được xác minh; nêu rõ phần nào chưa xác minh nếu có.
- Cập nhật README, `docs/DEPLOYMENT.md`, `docs/CHAN_DOAN_STREAMLIT.md`, `docs/NGHIEM_THU_WEB_CONG_KHAI.md`, `docs/HAU_KIEM_V1.0.3.md` và checklist bản nộp để không còn khẳng định website hiện đang lỗi nếu kiểm tra mới đã đạt.
- Giữ lịch sử quan sát lỗi cũ; phân biệt thời điểm lỗi với thời điểm đã chạy được. Không khẳng định nguyên nhân lỗi cũ là quyền xem nếu chưa có bằng chứng dashboard.
- Đồng bộ số kiểm thử thực tế, URL demo và cách clone/cài đặt/chạy. Không đổi phiên bản ứng dụng chỉ để số Plan trên footer trùng số kế hoạch.
- Giữ số liệu chốt: Accuracy 88,52%, Macro F1 88,33%; CV alpha=1.0 là 88,55%, alpha=0.1 là 90,28%. Kiểm tra từ file kết quả hiện có.

### 4. Kiểm tra kỹ thuật

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m compileall -q app.py src tests scripts
git diff --check
```

- Ghi kết quả thật và thời điểm. Mốc hiện tại 21 kiểm thử; giải thích nếu có thêm kiểm thử.
- Nếu chỉ đổi tài liệu, không cần chạy lại huấn luyện hoặc tối ưu alpha. Nếu sửa mã, kiểm tra hồi quy và deployment sử dụng thay đổi đó.

### 5. Commit, push và quyết định gói phát hành

- Commit từng nhóm thay đổi có ý nghĩa và push lên GitHub, ví dụ `test: nghiệm thu website công khai Plan 9`, `docs: đồng bộ trạng thái triển khai và bản nộp`. Ghi chú rõ nội dung, không tạo commit rỗng.
- Chờ CI của commit cuối thành công; ghi SHA và liên kết workflow vào biên bản.
- Giữ nguyên tag và asset `v1.0.3`. Nếu bản nộp tiếp tục dùng ZIP này, ghi rõ đó là gói tại commit phát hành cũ và cung cấp riêng tài liệu nghiệm thu mới.
- Nếu cần ZIP chứa nguồn/tài liệu mới, phát hành `v1.0.4`: cập nhật version và kiểm thử nhất quán, tạo gói bằng script hiện có, kiểm tra môi trường sạch, đồng bộ manifest/checksum, push và chờ CI rồi tạo tag/release mới. Tải lại asset từ GitHub và đối chiếu SHA-256. Không sửa checksum bằng tay hoặc ghi đè release cũ.
- Nếu script kiểm tra nhất quán version thất bại, sửa nguyên nhân, không bỏ qua kiểm thử để phát hành.

### 6. Bàn giao cho nhóm

- Báo cáo cuối gồm URL công khai, trạng thái từng ca, kết quả tests/CI, đường dẫn bằng chứng, commit đã push và release dùng để nộp.
- Rà soát kịch bản demo nhóm 3 người hiện có: lý thuyết, thực nghiệm, demo web; bổ sung phương án chạy localhost khi mất mạng.
- Liệt kê rõ phần chưa đạt hoặc cần chủ tài khoản thao tác. Không ghi hoàn thành nếu chưa tải và kiểm tra CSV thật.

## Điều kiện hoàn thành

Website truy cập không cần đăng nhập; toàn bộ ca kiểm thử có kết quả và bằng chứng, lỗi ứng dụng đã xử lý; lịch sử và CSV được đối chiếu; tài liệu hiện tại nhất quán; tests và CI đạt; thay đổi được push; bản nộp xác định rõ phiên bản. Thông tin dashboard chưa xác minh phải được ghi rõ, không dùng suy đoán làm kết luận.

## Prompt giao cho AI

> Thực hiện `docs/plan-9.md` trong `D:\phan-loai-van-ban-naive-bayes`. Website công khai đã mở được và dự đoán thử NASA thành công, nhưng chưa nghiệm thu đầy đủ. Kiểm thử trực tiếp bằng phiên chưa đăng nhập, lưu bằng chứng thật, tải và đối chiếu CSV. Đính chính tài liệu trạng thái cũ và hoàn tất các điều kiện còn thiếu của Plan 8. Giữ mô hình và số liệu thực nghiệm; chỉ sửa lỗi được quan sát. Commit và push sau từng nhóm thay đổi, đợi CI đạt. Giữ nguyên Release v1.0.3; nếu cần gói mới thì phát hành phiên bản mới theo quy trình trong plan. Báo cáo rõ phần đã đạt và phần còn chờ, không công bố hoàn thành khi thiếu bằng chứng.
