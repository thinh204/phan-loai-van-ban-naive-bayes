# Danh mục kiểm tra trước ngày bảo vệ đề tài (Pre-Defense Checklist)

- **Học phần**: Trí tuệ nhân tạo (AI)
- **Đề tài**: Phân loại văn bản đa lớp bằng Multinomial Naive Bayes
- **Nhóm sinh viên**: 3 thành viên
- **Thời gian diễn tập & kiểm tra chéo**: 30/09/2026
- **Thiết bị trình chiếu**: Laptop Windows 11 (kết nối HDMI/Type-C)
- **Phiên bản mã nguồn**: `v1.0.4` (Commit cuối nhánh `main`)

---

## 1. Bảng kiểm tra điều kiện kỹ thuật trước giờ bảo vệ

| Hạng mục kiểm tra | Tiêu chuẩn đánh giá | Kết quả thực tế trên máy trình chiếu | Xác nhận (Ký duyệt) |
| :--- | :--- | :--- | :---: |
| **1. Slide PowerPoint** | Tệp [`presentation/phan-loai-van-ban-naive-bayes-v2.pptx`](file:///d:/phan-loai-van-ban-naive-bayes/presentation/phan-loai-van-ban-naive-bayes-v2.pptx) hiển thị trọn vẹn 10 slide; đồ thị kết quả rõ nét; font chữ không lỗi Unicode tiếng Việt. | Đạt 10/10 slide, tỷ lệ 16:9, hình ảnh sắc nét, speaker notes đầy đủ. | **ĐÃ DUYỆT** |
| **2. Demo Trực tuyến (Online)** | Mở ứng dụng trên nền tảng [Streamlit Community Cloud](https://phan-loai-van-ban-naive-bayes.streamlit.app); giao diện hiển thị phiên bản `Plan 10 - Release v1.0.4`. | Thử nghiệm dự đoán tức thì câu văn bản mẫu, thời gian phản hồi < 0,5 giây. | **ĐÃ DUYỆT** |
| **3. Demo Ngoại tuyến (Offline Fallback)** | Khởi động Streamlit cục bộ tại `http://localhost:8501`; tự chủ nạp mô hình từ `models/naive_bayes_model.joblib`. | Chạy độc lập 100% không cần kết nối Internet, thời gian chuyển đổi khi mất mạng < 3 giây. | **ĐÃ DUYỆT** |
| **4. Kiểm thử tự động (pytest)** | Chạy toàn bộ bộ kiểm thử tự động `pytest -v` (gồm 16 test cốt lõi + 5 test tính nhất quán + 6 test hành vi người dùng/CSV = 27 tests). | **27/27 passed (100% ĐẠT)**, không có cảnh báo hay lỗi phụ thuộc. | **ĐÃ DUYỆT** |
| **5. Cú pháp toàn diện (compileall)** | Chạy lệnh `python -m compileall -q app.py src tests scripts`. | Return code: `0`, không có lỗi cú pháp hay import sai đường dẫn. | **ĐÃ DUYỆT** |
| **6. Gói bài nộp & Checksum** | Tệp `release/phan-loai-van-ban-naive-bayes-final-submission.zip` khớp SHA-256 với `CHECKSUMS.sha256` và asset GitHub Release. | Mã băm SHA-256 khớp tuyệt đối 100%, cấu trúc 46+ tệp sạch, không chứa `.venv` hay cache. | **ĐÃ DUYỆT** |

---

## 2. Bảng kiểm tra kịch bản và phân bổ thời lượng 3 thành viên

| Vai trò | Thành viên phụ trách | Nhiệm vụ chính & Nội dung trình bày | Thời lượng chuẩn | Giới hạn tối đa | Trạng thái diễn tập |
| :---: | :---: | :--- | :---: | :---: | :---: |
| **Phần 1** | **Thành viên 1** | Mở đầu, bối cảnh bài toán, 4 chủ đề 20 Newsgroups, tiền xử lý và nguyên tắc chống rò rỉ dữ liệu test. | **2 phút 15 giây** | 2 phút 30 giây | **HOÀN THÀNH** |
| **Phần 2** | **Thành viên 2** | Không gian đặc trưng TF-IDF 13.068 chiều, định lý Bayes, tính toán Log-sum tránh underflow, làm trơn Laplace và ví dụ tính tay. | **2 phút 45 giây** | 3 phút 00 giây | **HOÀN THÀNH** |
| **Phần 3** | **Thành viên 3** | Tối ưu hóa siêu tham số alpha qua 5-Fold CV (`alpha=0.1`), kết quả Test Accuracy 88,52%, Macro F1 88,33%, demo trực tiếp Streamlit và kết luận. | **4 phút 00 giây** | 4 phút 30 giây | **HOÀN THÀNH** |
| **Tổng cộng** | **Cả 3 thành viên** | **Toàn bộ bài thuyết trình và demo thực nghiệm** | **9 phút 00 giây** | **10 phút 00 giây** | **ĐẠT CHUẨN (7–10 phút)** |

---

## 3. Bảng kiểm tra phương án xử lý tình huống khẩn cấp (Contingency Plans)

1. **Mất kết nối Internet hoặc mạng chập chờn tại phòng hội đồng:**
   - *Hành động*: Thành viên 3 lập tức chuyển sang tab trình duyệt ghim sẵn `http://localhost:8501`.
   - *Thời gian chuyển đổi*: Dưới 3 giây, bài trình bày không bị gián đoạn.
2. **Trình duyệt bị đơ hoặc lỗi tải trang:**
   - *Hành động*: Mở cửa sổ ẩn danh mới hoặc bấm `Ctrl + F5` để làm mới bộ nhớ đệm.
3. **Câu hỏi phản biện hóc búa từ hội đồng:**
   - *Hành động*: Nhóm đã chuẩn bị sẵn tài liệu đối chiếu chi tiết [docs/DEFENSE_QA.md](file:///d:/phan-loai-van-ban-naive-bayes/docs/DEFENSE_QA.md) gồm 12 nhóm câu hỏi cốt lõi về rò rỉ dữ liệu, giả định độc lập Naive Bayes, tại sao chọn TF-IDF và cách tính log-likelihood.

---

## 4. Xác nhận ký duyệt toàn nhóm

Cả 3 thành viên trong nhóm đã hoàn thành toàn bộ các vòng diễn tập thử nghiệm, kiểm tra chéo thiết bị và thống nhất số liệu khoa học. Hồ sơ và sản phẩm hoàn toàn sẵn sàng cho buổi bảo vệ chính thức.

- **Đại diện Thành viên 1**: *Đã ký xác nhận*
- **Đại diện Thành viên 2**: *Đã ký xác nhận*
- **Đại diện Thành viên 3**: *Đã ký xác nhận*
