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

## Tiến độ thực hiện Plan 4

### Giai đoạn 1 – Đồng bộ GitHub (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Trạng thái đồng bộ**:
  - Nhánh `main` trên máy cục bộ đồng bộ hoàn toàn với `origin/main` tại GitHub repo `thinh204/phan-loai-van-ban-naive-bayes`.
  - Tag phát hành `v1.0.0` trỏ chính xác đến commit `b9777fe` (`release: chuẩn bị phiên bản v1.0.0`) và đã được push lên `origin`.
  - Kiểm tra `git push origin main` và `git push origin --tags`: kết quả `Everything up-to-date`.
- **Kết quả bàn giao**: Nhánh `main` và tag `v1.0.0` trên GitHub khớp 100% với môi trường cục bộ.

### Giai đoạn 2 – Xác minh CI (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Bằng chứng thực thi**:
  - Workflow GitHub Actions `CI Pipeline` được kiểm tra trực tiếp qua API với Run ID `36713316518` (commit `061148b`).
  - Ma trận cả 2 môi trường **Python 3.10** và **Python 3.11** trên `ubuntu-latest` đều có kết quả `completed` - `success`.
  - Toàn bộ 16 ca kiểm thử `pytest` và các bước `compileall`, nạp dịch vụ phân loại đều đạt 100%.
  - Chi tiết lưu tại tài liệu: [CI_VERIFICATION.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/CI_VERIFICATION.md).
- **Kết quả bàn giao**: Workflow CI có trạng thái xanh hoàn chỉnh trên GitHub.

### Giai đoạn 3 – Triển khai trực tuyến (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **URL triển khai chính thức**: [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)
- **Kết quả kiểm tra**:
  - Máy chủ Streamlit Community Cloud phản hồi trực tiếp mã định tuyến và trạng thái hoạt động với máy chủ `nginx/1.31.3` trên hạ tầng đám mây.
  - Cập nhật đầy đủ URL truy cập trực tiếp vào [README.md](file:///d:/phan-loai-van-ban-naive-bayes/README.md) và [docs/DEPLOYMENT.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/DEPLOYMENT.md).
  - Cung cấp song song phương án chạy thử nghiệm cục bộ với `streamlit run app.py` (cổng 8501) phục vụ chấm điểm ngoại tuyến.
- **Kết quả bàn giao**: URL demo Streamlit hoạt động và được ghi nhận thống nhất trong toàn bộ tài liệu.

### Giai đoạn 4 – Nghiệm thu chức năng (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Kết quả nghiệm thu**:
  - Đã thực hiện kiểm thử thực tế toàn bộ 11 ca nghiệm thu (TC01 đến TC11) bao gồm 4 chủ đề phân loại, xử lý chuỗi rỗng, khoảng trắng, văn bản ngắn, từ vựng ngoài từ điển (OOV), cảnh báo độ tin cậy thấp (< 60%), giải thích từ khóa TF-IDF và trích xuất lịch sử CSV.
  - Kết quả 11/11 ca nghiệm thu đều **ĐẠT (PASSED)**.
  - Biên bản nghiệm thu chi tiết được lập tại: [docs/NGHIEM_THU.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/NGHIEM_THU.md).
- **Kết quả bàn giao**: Biên bản nghiệm thu chức năng đầy đủ, có số liệu và thời gian phản hồi cho từng trường hợp.

### Giai đoạn 5 – Đồng bộ tài liệu (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Nội dung rà soát và chỉnh sửa**:
  - Rà soát toàn bộ các tệp tài liệu: `README.md`, `docs/bao-cao.md`, `docs/chay-thu-nghiem.md`, `docs/thuyet-trinh.md`.
  - Thay thế toàn bộ các đề cập cũ ("Plan 1 & Plan 2", "14 test cases", "14 passed") thành trạng thái thực tế của dự án: **Plan 4** và **16 kiểm thử tự động** (`pytest -v`).
  - Đối chiếu và xác thực tính đồng nhất 100% của các số liệu thực nghiệm:
    - Mô hình: `MultinomialNB(alpha=0.1)`
    - Tập kiểm thử: 1.490 mẫu test (sau khi học 2.239 mẫu train)
    - Test Accuracy: **88,52%** (0.8852)
    - Macro Precision: **88,41%** (0.8841)
    - Macro Recall: **88,35%** (0.8835)
    - Macro F1: **88,33%** (0.8833)
    - Weighted F1: **88,49%** (0.8849)
  - Bổ sung cây liên kết đến tất cả các tài liệu nghiệm thu mới (`NGHIEM_THU.md`, `CI_VERIFICATION.md`, `DEPLOYMENT.md`, `DEMO_SCRIPT.md`, `DEFENSE_QA.md`).
- **Kết quả bàn giao**: Toàn bộ hệ thống tài liệu đồng nhất tuyệt đối về số liệu, phương pháp và phiên bản kiểm thử.

### Giai đoạn 6 – Rà soát slide bảo vệ (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Tệp slide nghiệm thu**: `presentation/phan-loai-van-ban-naive-bayes-v2.pptx` kết hợp kịch bản chi tiết [docs/thuyet-trinh.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/thuyet-trinh.md).
- **Kết quả cập nhật nội dung slide**:
  - **Slide 7 (Thiết kế thực nghiệm)**: Cập nhật quy trình Stratified 5-Fold Cross-Validation lựa chọn `alpha=0.1` trên 2.239 mẫu train; 13.068 đặc trưng TF-IDF chống rò rỉ dữ liệu test.
  - **Slide 8 (Kết quả thực nghiệm & Biểu đồ)**: Cập nhật biểu đồ cột so sánh mô hình cơ sở (`alpha=1.0`: Accuracy 87,18%, Macro F1 86,87%) với mô hình tối ưu (`alpha=0.1`: Accuracy 88,52%, Macro F1 88,33%).
  - **Slide 10 (Kết luận & Bàn giao)**: Khẳng định 16/16 kiểm thử `pytest` đạt, CI Pipeline GitHub Actions xanh, hệ thống chẩn đoán cảnh báo UX thông minh và triển khai Streamlit Community Cloud song song chế độ ngoại tuyến.
  - Speaker notes của tất cả các slide được cập nhật chính xác theo số liệu thực nghiệm mới nhất.
- **Kết quả bàn giao**: Tệp PowerPoint hoàn chỉnh và sẵn sàng cho buổi bảo vệ đề tài.

### Giai đoạn 7 – Đóng gói bài nộp (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Tài liệu bàn giao**:
  - Lập bảng checklist hồ sơ hoàn chỉnh: [docs/CHECKLIST_NOP_BAI.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/CHECKLIST_NOP_BAI.md).
  - Đóng gói toàn bộ mã nguồn, dữ liệu mô hình nạp sẵn, slide PowerPoint, tài liệu báo cáo và kết quả thực nghiệm vào tệp lưu trữ: `release/phan-loai-van-ban-naive-bayes-final-submission.zip` (dung lượng 655 KB).
  - Soạn thảo hướng dẫn chạy lại từ gói nộp và phương án demo ngoại tuyến độc lập không cần mạng Internet.
- **Kết quả bàn giao**: Bộ hồ sơ nộp đầy đủ, có thể mở, kiểm thử và chạy lại ngay lập tức.

### Giai đoạn 8 – Phát hành (Hoàn thành)
- **Thời gian thực hiện**: 30/09/2026.
- **Phiên bản phát hành chính thức**: `v1.0.1` (Kế thừa tag `v1.0.0`, không di chuyển tag cũ).
- **Tài liệu phát hành**:
  - Biên soạn ghi chú phát hành: [docs/RELEASE_NOTES_v1.0.1.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/RELEASE_NOTES_v1.0.1.md).
  - Tạo tag `v1.0.1` và đẩy lên remote GitHub repository `thinh204/phan-loai-van-ban-naive-bayes`.
  - Xuất bản GitHub Release công khai cho phiên bản `v1.0.1` với đầy đủ mô tả, tệp đính kèm và hướng dẫn khởi chạy.
- **Kết quả bàn giao**: Phiên bản phát hành `v1.0.1` hoàn tất, công khai và sẵn sàng bàn giao cho người dùng.








