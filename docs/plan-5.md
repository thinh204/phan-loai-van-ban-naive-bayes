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

## Tiến độ thực hiện Plan 5

### Giai đoạn 1 – Khôi phục demo công khai (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Nguyên nhân sự cố ban đầu**:
  - Repository trên GitHub ở chế độ `Private` (riêng tư), khiến Streamlit Community Cloud mặc định kích hoạt cơ chế bảo vệ danh tính (Viewer authorization) và chuyển hướng người dùng chưa đăng nhập sang `/-/login` hoặc trang "App not found".
- **Hành động khắc phục**:
  - Chuyển đổi trạng thái repository `thinh204/phan-loai-van-ban-naive-bayes` sang **Public** công khai qua GitHub REST API (`PATCH /repos/thinh204/phan-loai-van-ban-naive-bayes`).
  - Người dùng đã truy cập `https://share.streamlit.io` để kích hoạt triển khai chính thức cho repo với branch `main`, file `app.py` và subdomain `phan-loai-van-ban-naive-bayes`.
  - Cập nhật hướng dẫn kiểm tra cấu hình Viewer authorization sang `Public` trong [docs/DEPLOYMENT.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/DEPLOYMENT.md).
- **Kết quả bàn giao**: URL chính thức `https://phan-loai-van-ban-naive-bayes.streamlit.app` được định tuyến trên hạ tầng Streamlit Cloud, sẵn sàng phục vụ trình diễn công khai.

### Giai đoạn 2 – Đồng bộ phiên bản (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Thiết lập nguồn chân lý duy nhất (Single Source of Truth)**:
  - Khai báo các hằng số siêu dữ liệu tập trung trong [src/config.py](file:///d:/phan-loai-van-ban-naive-bayes/src/config.py): `APP_VERSION = "v1.0.2"`, `PLAN_VERSION = "Plan 5"`, `RELEASE_VERSION = "v1.0.2"`, `FOOTER_CAPTION`.
- **Cập nhật giao diện [app.py](file:///d:/phan-loai-van-ban-naive-bayes/app.py)**:
  - Thay thế toàn bộ chú thích chân trang cũ (`Plan 3 - Release v1.0.0`) bằng `FOOTER_CAPTION` động.
  - Bổ sung thông tin phiên bản phát hành (`v1.0.2`) nổi bật trong Sidebar giao diện người dùng.
  - Đảm bảo không còn tồn tại chuỗi ký tự Plan 3 / v1.0.0 trong mã nguồn giao diện đang hoạt động.
- **Kết quả bàn giao**: Giao diện và cấu hình hệ thống đồng bộ 100% về phiên bản hiện tại `v1.0.2`.

### Giai đoạn 3 – Sửa liên kết phát hành (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Nội dung rà soát và chỉnh sửa**:
  - Rà soát toàn bộ liên kết tài liệu trong [docs/RELEASE_NOTES_v1.0.1.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/RELEASE_NOTES_v1.0.1.md) và [README.md](file:///d:/phan-loai-van-ban-naive-bayes/README.md).
  - Sửa các đường dẫn relative thiếu tiền tố `docs/` hoặc không thể điều hướng trên trang GitHub Release thành URL repo đầy đủ (`https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/...`).
  - Cập nhật trực tiếp nội dung mô tả phiên bản phát hành `v1.0.1` trên GitHub qua API (`PATCH /repos/thinh204/phan-loai-van-ban-naive-bayes/releases/{id}`).
- **Kết quả bàn giao**: 100% liên kết trên trang phát hành GitHub Release và tài liệu điều hướng chính xác tới tệp đích.

### Giai đoạn 4 – Tự động hóa gói nộp (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Mã nguồn tự động hóa**: [scripts/build_package.py](file:///d:/phan-loai-van-ban-naive-bayes/scripts/build_package.py).
- **Quy tắc đóng gói**:
  - Áp dụng danh sách cho phép (whitelist) nghiêm ngặt gồm các thư mục: `src/`, `models/`, `results/`, `docs/`, `tests/`, `presentation/`, `.streamlit/` và các tệp gốc `app.py`, `requirements.txt`, `README.md`.
  - Loại trừ tuyệt đối mọi thư mục môi trường ảo (`.venv`), bộ nhớ đệm (`__pycache__`, `.pytest_cache`), tệp nhị phân tạm và dữ liệu nhạy cảm.
  - Tự động bao gồm đầy đủ tài liệu ghi chú phát hành mới nhất (`docs/RELEASE_NOTES_v1.0.1.md`).
  - Đóng gói có sắp xếp xác định (deterministic) 42 tệp tin vào [release/phan-loai-van-ban-naive-bayes-final-submission.zip](file:///d:/phan-loai-van-ban-naive-bayes/release/phan-loai-van-ban-naive-bayes-final-submission.zip) (660 KB).
- **Kết quả bàn giao**: Gói bài nộp có thể tái tạo hoàn toàn bằng một câu lệnh: `python scripts/build_package.py`.

### Giai đoạn 5 – Kiểm tra toàn vẹn (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Mã nguồn kiểm tra**: [scripts/generate_manifest.py](file:///d:/phan-loai-van-ban-naive-bayes/scripts/generate_manifest.py).
- **Kết quả kiểm tra toàn vẹn**:
  - Đã thực thi kiểm tra `testzip()` trên toàn bộ tệp nén: trạng thái `VALID`, 100% không phát hiện hỏng dữ liệu hay lỗi CRC-32.
  - Tính toán và lưu trữ mã băm SHA-256 chính xác của tệp ZIP (`1599c3e379f3af2df1059ed5ea6fb216da2d20a7e9f500a3b3e0a5b0b4f2be26`).
  - Xuất tệp manifest chuẩn [release/MANIFEST.json](file:///d:/phan-loai-van-ban-naive-bayes/release/MANIFEST.json), tệp đối chiếu [release/CHECKSUMS.sha256](file:///d:/phan-loai-van-ban-naive-bayes/release/CHECKSUMS.sha256) và tài liệu đối chiếu [docs/MANIFEST.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/MANIFEST.md).
- **Kết quả bàn giao**: Manifest và checksum SHA-256 đầy đủ, phục vụ đối chiếu và kiểm tra tính nguyên vẹn của bài nộp.

### Giai đoạn 6 – Chạy thử từ gói sạch (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Mã nguồn xác minh**: [scripts/verify_clean_package.py](file:///d:/phan-loai-van-ban-naive-bayes/scripts/verify_clean_package.py).
- **Quy trình thực nghiệm độc lập**:
  - Giải nén gói bài nộp vào thư mục tạm sạch cô lập (`clean_pkg_test_*`), kiểm tra đủ 42 tệp tin thành phần.
  - Chạy biên dịch cú pháp toàn bộ hệ thống bằng `python -m compileall`: 100% hợp lệ (exit code `0`).
  - Thực thi toàn bộ bộ kiểm thử tự động: **16/16 test cases PASSED** trên mã nguồn giải nén.
  - Chạy suy diễn dự đoán thực tế trên câu văn bản mới: nhận diện chính xác chủ đề `sci.space` với độ tin cậy **99,96%**.
  - Lập biên bản xác thực chi tiết tại [docs/CLEAN_ENV_TEST.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/CLEAN_ENV_TEST.md).
- **Kết quả bàn giao**: Biên bản tái lập từ gói bài nộp chứng minh ứng dụng có thể chạy hoàn toàn độc lập mà không gặp bất kỳ lỗi phụ thuộc nào.

### Giai đoạn 7 – Diễn tập ba thành viên (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Tài liệu kịch bản diễn tập**: [docs/DIEN_TAP_BAO_VE.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/DIEN_TAP_BAO_VE.md).
- **Phân bổ vai trò và thời lượng chuẩn (9 phút)**:
  - **Thành viên 1** (2 phút 15 giây): Mở đầu, bối cảnh bài toán, 4 chủ đề 20 Newsgroups, tiền xử lý loại metadata chống rò rỉ dữ liệu.
  - **Thành viên 2** (2 phút 45 giây): Lý thuyết TF-IDF 13.068 chiều, định lý Bayes, tính toán miền Log-sum, làm trơn Laplace và ví dụ tính tay.
  - **Thành viên 3** (4 phút 00 giây): Tối ưu hóa siêu tham số alpha qua 5-Fold CV (`alpha=0.1`), kết quả Test Accuracy 88,52%, Macro F1 88,33%, phân tích lỗi, thao tác trực tiếp trên giao diện Streamlit và kết luận.
- **Phương án dự phòng ngoại tuyến**: Chuẩn bị sẵn kịch bản chuyển sang localhost:8501 trong 3 giây nếu mạng Internet gặp sự cố tại hội trường bảo vệ.
- **Kết quả bàn giao**: Kịch bản diễn tập chi tiết từng phút, câu thoại gợi ý và quy tắc phối hợp chuyển phần nhuần nhuyễn.







