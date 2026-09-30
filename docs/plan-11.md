# Plan 11: Đồng bộ phiên bản Cloud và chốt hậu kiểm v1.0.4

## Trạng thái tiếp nhận

Repo `thinh204/phan-loai-van-ban-naive-bayes`, thư mục `D:\phan-loai-van-ban-naive-bayes`.

Hậu kiểm ngày 01/10/2026 xác nhận:

- 27/27 tests đạt, compileall và `git diff --check` không lỗi, working tree sạch.
- CI commit `5616908` và commit phát hành `14e88a2` thành công.
- Release `v1.0.4` đã xuất bản; ZIP tải từ GitHub khớp local và checksum: `189918bdc3acaca2bc1e19f22ff370f475ad260b7b9b219ff9fe9ceb3a20d975`.
- Website công khai mở được, đã chặn đầu vào rỗng và không thêm lịch sử; CSV nghiệm thu Plan 10 đã sửa đoạn trích.
- Tuy nhiên sidebar và footer Cloud vẫn hiển thị `v1.0.3 – Plan 6`, trong khi `src/config.py` của repo là `v1.0.4`. Ảnh `tc18_post_release_v1_0_4.png` cũng hiển thị v1.0.3; tên file không chứng minh phiên bản.
- Biên bản Plan 10 còn ghi sẵn sàng phát hành thay vì kết quả phát hành thực tế.

## Mục tiêu

Xác minh và xử lý phiên bản hiển thị cũ trên Cloud; lưu hậu kiểm thật v1.0.4; đồng bộ tài liệu để đóng Plan 10. Giữ mô hình, số liệu và tag/asset đã phát hành. Không cần phát hành phiên bản mới nếu chỉ restart Cloud hoặc sửa tài liệu hậu kiểm.

## Quy trình cho AI

### 1. Kiểm kê và chẩn đoán

- Đọc hướng dẫn repo, Plan 10, cấu hình version và script hậu kiểm. Bảo toàn thay đổi có sẵn.
- Kiểm tra lại URL `https://phan-loai-van-ban-naive-bayes.streamlit.app/` bằng phiên chưa đăng nhập, ghi phiên bản sidebar/footer thực tế.
- Nếu có phiên chủ tài khoản trên Streamlit Cloud, kiểm tra đúng ứng dụng, repo, branch `main`, entrypoint `app.py`, logs và nguồn triển khai. Ghi commit SHA khi dashboard cung cấp; nếu không, ghi rõ chưa xác minh được.
- Kiểm tra các cách nạp `src.config`, cache resource, module và trạng thái deployment. Phiên bản cũ có thể do nguồn chưa cập nhật hoặc process/module cache; không khẳng định nguyên nhân khi chưa có bằng chứng.
- Nếu cần đăng nhập hoặc thao tác chỉ chủ tài khoản làm được, yêu cầu đúng thao tác đó, giữ phần phụ thuộc ở trạng thái chờ và tiếp tục rà soát tài liệu độc lập.

### 2. Đồng bộ ứng dụng Cloud

- Nếu nguồn đúng nhưng process chưa nhận cấu hình mới, dùng thao tác reboot/redeploy được dashboard cung cấp, đợi ứng dụng sẵn sàng rồi kiểm tra lại trong phiên mới.
- Nếu branch, entrypoint hoặc nguồn sai, sửa cấu hình ứng dụng theo thông tin đã xác minh. Không tạo thêm ứng dụng trùng khi ứng dụng hiện có vẫn hoạt động.
- Chỉ sửa mã khi quan sát được lỗi thực sự cần sửa; tiếp tục dùng version tập trung trong `src/config.py`, tránh hardcode version riêng trong nhiều tệp để che sai lệch.
- Không đổi Plan trên footer chỉ để khớp số kế hoạch mới. Yêu cầu bắt buộc là phiên bản v1.0.4 hiển thị nhất quán với cấu hình repo.
- Nếu sửa mã nguồn thuộc bản đã phát hành, không ghi đè tag/ZIP v1.0.4. Ghi rõ thay đổi mới và chỉ tạo bản vá v1.0.5 nếu thực sự cần gói nguồn mới, theo quy trình đóng gói hiện có.

### 3. Hậu kiểm trên website sau cập nhật

Tạo `docs/HAU_KIEM_V1.0.4.md` và lưu bằng chứng mới vào `docs/evidence/plan-11/`.

| Ca | Điều kiện đạt |
| --- | --- |
| Truy cập công khai | Giao diện nạp không cần đăng nhập, không lỗi ứng dụng |
| Phiên bản | Sidebar và footer đều hiển thị v1.0.4; ảnh chụp đọc được giá trị thật |
| Rỗng ở phiên mới | Cảnh báo nhập văn bản, không có kết quả dự đoán mới, lịch sử 0 dòng |
| Dự đoán hợp lệ | Dùng câu NASA của Plan 10; ghi đầu vào, nhãn, xác suất, thời điểm và phiên bản |
| Khoảng trắng sau lượt hợp lệ | Có cảnh báo, lịch sử giữ nguyên 1 dòng |
| Đoạn trích ngắn | Phân loại `space`, lịch sử đúng `space`, không nối `(Rỗng)` |
| CSV thật | Tải CSV sau hai lượt hợp lệ, mở file; đúng 2 dòng dữ liệu, nhãn và đoạn trích khớp lịch sử, không có lượt rỗng |
| Tải lại | Mở lại URL, phiên bản vẫn v1.0.4, chạy thêm một dự đoán thành công |

- Chỉ lưu ảnh thực tế; không sửa chữ trên ảnh cũ. Giữ ảnh Plan 10 cũ làm lịch sử và chú thích nó chưa chứng minh v1.0.4.
- Mỗi ca ghi mong đợi, kết quả thật, thời điểm và đường dẫn bằng chứng. Nếu giá trị version chưa đúng thì không đánh dấu đạt.
- Cải thiện script hậu kiểm để trả mã thoát khác 0 khi phiên bản sai, truy cập lỗi, lịch sử tăng sau đầu vào rỗng hoặc CSV không khớp. Không chỉ in thông báo rồi tiếp tục công bố thành công.
- Kiểm tra cả sidebar/footer, không tìm chuỗi v1.0.4 ở tên file hoặc nội dung báo cáo để xác nhận deployment.

### 4. Đồng bộ tài liệu

- Cập nhật biên bản Plan 10: phân biệt nghiệm thu hành vi trước phát hành với hậu kiểm phiên bản sau cập nhật. Thay phần sẵn sàng phát hành bằng liên kết Release và kết quả đã xác minh.
- Thêm chú thích cho ảnh `tc18_post_release_v1_0_4.png` cũ: ảnh hiển thị v1.0.3, không phải bằng chứng version v1.0.4; dẫn tới ảnh mới.
- Ghi vào hậu kiểm: URL, phiên bản quan sát, thông tin nguồn deployment đã/chưa xác minh, commit repo, CI, Release, ZIP và SHA-256.
- Giữ ZIP v1.0.4 hiện có nếu không sửa mã: ghi rõ tài liệu Plan 11 được bổ sung sau commit phát hành và cung cấp riêng để nộp; không tuyên bố ZIP cũ chứa tài liệu mới.
- Cập nhật README, checklist và hướng dẫn demo ở những nơi cần thiết. Không ghi hoàn thành toàn bộ nếu có ca còn chờ.

### 5. Xác minh, commit và push

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m compileall -q app.py src tests scripts
git diff --check
.\.venv\Scripts\python.exe scripts\verify_release_asset.py v1.0.4
```

- Ghi số kiểm thử thực tế; mốc hiện tại 27. Nếu sửa script hậu kiểm, xác minh nó báo thất bại khi điều kiện không đạt.
- Commit từng nhóm thay đổi có ý nghĩa, ví dụ `test: kiểm tra nghiêm ngặt phiên bản Cloud`, `docs: xác nhận hậu kiểm v1.0.4 và đóng Plan 10`; push và chờ CI của commit cuối thành công.
- Không tạo commit rỗng cho thao tác chỉ diễn ra trên dashboard.
- Báo cáo cuối gồm trạng thái từng ca, URL, phiên bản thật, commit đã push, liên kết CI/Release và đường dẫn bằng chứng; nêu rõ phần còn chờ nếu có.

## Điều kiện hoàn thành

Website công khai hiển thị đúng phiên bản v1.0.4 trong sidebar/footer; các ca hậu kiểm đều đạt và có bằng chứng; CSV được tải và đối chiếu thật; tài liệu Plan 10 được đính chính; tests/CI đạt; checksum Release khớp; thay đổi được push. Không cần mở thêm kế hoạch nếu chỉ còn thao tác đăng nhập/reboot, tiếp tục Plan 11 cho đến khi hoàn tất hoặc ghi rõ bước đang chờ chủ tài khoản.

## Prompt giao cho AI

> Thực hiện toàn bộ `docs/plan-11.md` trong `D:\phan-loai-van-ban-naive-bayes`. Plan 10 đã sửa hành vi và phát hành v1.0.4, nhưng website và ảnh hậu kiểm vẫn hiển thị v1.0.3. Xác minh nguồn triển khai và xử lý cập nhật/reboot trên Cloud theo nguyên nhân thật. Kiểm thử bằng phiên chưa đăng nhập, xác nhận version sidebar/footer và tải CSV để đối chiếu. Lưu bằng chứng mới, đính chính ảnh cũ và biên bản, kiểm tra checksum Release. Giữ nguyên mô hình và tag/asset đã phát hành. Commit và push từng nhóm thay đổi, đợi CI đạt. Nếu cần chủ tài khoản thao tác, nêu chính xác phần đang chờ; không báo hoàn thành khi phiên bản thực tế chưa đúng.
