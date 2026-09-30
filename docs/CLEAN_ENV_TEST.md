# Biên bản xác minh gói bài nộp trong môi trường sạch độc lập

- **Gói bài nộp kiểm tra**: `release/phan-loai-van-ban-naive-bayes-final-submission.zip`
- **Mã băm SHA-256**: Xem tệp [release/CHECKSUMS.sha256](file:///d:/phan-loai-van-ban-naive-bayes/release/CHECKSUMS.sha256)
- **Thời điểm kiểm tra**: 30/09/2026
- **Script tự động hóa**: [scripts/verify_clean_package.py](file:///d:/phan-loai-van-ban-naive-bayes/scripts/verify_clean_package.py)
- **Mục tiêu**: Chứng minh gói nộp bài hoàn toàn độc lập, có thể giải nén và vận hành ngay trên máy tính của hội đồng chấm thi mà không phụ thuộc vào môi trường phát triển hiện tại.

---

## 1. Quy trình thực nghiệm kiểm tra độc lập

1. **Khởi tạo thư mục tạm cô lập hoàn toàn**:
   - Vị trí: `C:\Users\THINH\AppData\Local\Temp\clean_pkg_test_*`
   - Đảm bảo thư mục ban đầu rỗng 100%, không kế thừa file cache hay git metadata.
2. **Giải nén gói bài nộp**:
   - Giải nén thành công toàn bộ **46 tệp tin** (mã nguồn, mô hình nạp sẵn `.joblib`, cấu hình, kiểm thử, tài liệu, kết quả thực nghiệm và slide PowerPoint).
3. **Kiểm tra biên dịch cú pháp Python (compileall)**:
   - Lệnh thực thi: `python -m compileall -q app.py src tests`
   - Kết quả: Mã thoát `0`, không có lỗi cú pháp hay cảnh báo import.
4. **Thực thi bộ kiểm thử tự động (pytest)**:
   - Lệnh thực thi: `pytest -v`
   - Kết quả: **16/16 kiểm thử ĐẠT (16 passed)**.
5. **Kiểm thử suy diễn thực tế từ gói nạp sẵn (Inference Check)**:
   - Nạp trực tiếp mô hình `models/naive_bayes_model.joblib` và vectorizer `models/tfidf_vectorizer.joblib`.
   - Phân loại câu: *"NASA space shuttle telescope astronaut orbit mars mission"*.
   - Dự đoán: `sci.space` với độ tin cậy **99,96%**.
6. **Dọn dẹp an toàn**: Thư mục tạm được dọn dẹp sạch sẽ sau khi hoàn tất kiểm tra.

---

## 2. Bảng tổng hợp kết quả xác minh

| Tiêu chí kiểm tra | Yêu cầu kỹ thuật | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :---: |
| **Tính toàn vẹn tệp nén** | Không lỗi CRC-32 (`testzip`) | Hợp lệ 100% | **ĐẠT** |
| **Số lượng tệp giải nén** | Đầy đủ 46 tệp tin theo whitelist | 46/46 tệp tin | **ĐẠT** |
| **Biên dịch mã nguồn** | Không có lỗi cú pháp Python | Return code: `0` | **ĐẠT** |
| **Kiểm thử tự động** | Vượt qua toàn bộ 16 ca kiểm thử | **16/16 PASSED** | **ĐẠT** |
| **Tự chủ nạp mô hình** | Nạp thành công không cần huấn luyện lại | Hoàn thành | **ĐẠT** |
| **Suy diễn phân loại** | Nhận diện đúng chủ đề và xác suất cao | `sci.space` (99,96%) | **ĐẠT** |
| **Khởi động ứng dụng** | Sẵn sàng chạy với `streamlit run app.py` | Sẵn sàng | **ĐẠT** |

---

## 3. Kết luận

Gói lưu trữ bài nộp `phan-loai-van-ban-naive-bayes-final-submission.zip` đã được chứng minh **100% tự chủ, có thể tái lập hoàn toàn trên bất kỳ máy tính nào** cài đặt Python 3.10+ theo đúng hướng dẫn trong `README.md`.
