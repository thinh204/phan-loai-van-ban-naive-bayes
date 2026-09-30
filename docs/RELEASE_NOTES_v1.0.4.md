# Phiên bản phát hành v1.0.4 – Sửa nhập liệu rỗng, định dạng đoạn trích và hoàn thiện nghiệm thu

**Ngày phát hành:** 01/10/2026  
**Repository:** [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)  
**Phiên bản:** `v1.0.4` (Bản vá lỗi giao diện, kiểm thử hành vi và khóa bản nộp)  
**Kế thừa từ:** `v1.0.3` (giữ nguyên mô hình, bộ từ vựng TF-IDF và số liệu thực nghiệm)  
**Trạng thái kiểm thử:** 27/27 passed (100% ĐẠT) | Môi trường ảo sạch 100% | CI Green | Checksum Verified

---

## 1. Giới thiệu tổng quan

Phiên bản **v1.0.4** là bản phát hành bảo trì và hoàn thiện chất lượng (Maintenance & Quality Release) của đề tài *Phân loại văn bản đa lớp bằng Multinomial Naive Bayes* (Học phần Trí tuệ nhân tạo). Phiên bản này hoàn thành trọn vẹn toàn bộ 6 giai đoạn của **Plan 10**, xử lý dứt điểm hai lỗi giao diện phát hiện trong quá trình hậu kiểm Plan 9, bổ sung bộ kiểm thử hành vi người dùng, nghiệm thu thực tế 18 ca kiểm thử trên Streamlit Community Cloud và đồng bộ tài sản nộp bài có thể kiểm chứng.

---

## 2. Các sửa đổi kỹ thuật cốt lõi trong v1.0.4

### 1. Khắc phục lỗi nhập liệu rỗng và khoảng trắng
- **Hiện tượng cũ:** Khi bấm nút "🚀 Phân loại" với văn bản rỗng hoặc chỉ chứa khoảng trắng, hệ thống vẫn gọi dịch vụ phân loại, tính xác suất tiên nghiệm và tự động thêm 1 dòng vào lịch sử phiên.
- **Giải pháp trong v1.0.4:**
  - Chuẩn hóa đầu vào bằng `clean_input = user_text.strip()`.
  - Nếu `not clean_input`: chỉ hiển thị cảnh báo `st.warning("⚠️ **Vui lòng nhập nội dung văn bản để dự đoán!**")`.
  - Tuyệt đối không gọi dịch vụ phân loại, không tạo hộp kết quả dự đoán và không thêm bản ghi rỗng vào lịch sử hay tệp CSV.

### 2. Sửa lỗi nối hậu tố `(Rỗng)` vào văn bản ngắn và vừa ($\le 80$ ký tự)
- **Hiện tượng cũ:** Biểu thức toán tử 3 ngôi `clean_input[:80] + ("..." if len(clean_input) > 80 else "(Rỗng)")` khiến mọi văn bản có độ dài không vượt quá 80 ký tự đều bị nối chuỗi `(Rỗng)` vào sau (ví dụ: `space(Rỗng)`, `zxqvbnm qqqzxvv(Rỗng)`).
- **Giải pháp trong v1.0.4:**
  - Xây dựng hàm chuẩn hóa `format_text_preview(text, max_len=80)`:
    - Nếu chuỗi rỗng hoặc None: trả về `"(Rỗng)"`.
    - Nếu độ dài $> 80$ ký tự: lấy 80 ký tự đầu và nối `...`.
    - Nếu độ dài $\le 80$ ký tự: giữ nguyên văn bản đã chuẩn hóa khoảng trắng hai đầu, tuyệt đối không thêm `(Rỗng)`.
  - Tệp CSV xuất ra phản ánh đúng nguyên văn đoạn trích, sạch sẽ và nhất quán.

### 3. Mở rộng bộ kiểm thử tự động với kiểm thử hành vi người dùng (27/27 Tests ĐẠT)
- Bổ sung tệp kiểm thử mới [`tests/test_ui_behavior.py`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/tests/test_ui_behavior.py) sử dụng Streamlit `AppTest` mô phỏng đầy đủ luồng tương tác người dùng:
  - Kiểm thử các quy tắc cắt chuỗi và định dạng của `format_text_preview`.
  - Kiểm thử chuỗi rỗng và toàn khoảng trắng ở phiên mới: đảm bảo hiển thị cảnh báo và lịch sử giữ nguyên 0 dòng.
  - Kiểm thử chuỗi khoảng trắng sau một lượt hợp lệ: đảm bảo số dòng lịch sử không tăng.
  - Kiểm thử đầu vào `space` và OOV: cảnh báo hiển thị đầy đủ, đoạn trích không có `(Rỗng)`.
  - Kiểm thử các ca biên 80 ký tự (không có `...` và không có `(Rỗng)`) và 81 ký tự (80 ký tự + `...`).
  - Kiểm thử cấu trúc và nội dung tệp CSV xuất từ lịch sử phiên.

### 4. Nghiệm thu thực tế và đối chiếu CSV trên Streamlit Cloud
- Thực hiện nghiệm thu tự động trực tiếp trên website công khai đang hoạt động tại [https://phan-loai-van-ban-naive-bayes.streamlit.app/](https://phan-loai-van-ban-naive-bayes.streamlit.app/):
  - 18/18 ca kiểm thử đạt 100% (từ TC-00 đến TC-17).
  - Đếm độc lập dữ liệu bảng lịch sử (`Tổng số lượt dự đoán: 10`), không bị cộng dồn số hàng của bảng xác suất hay giải thích.
  - Tải tệp CSV thật từ trình duyệt (`tc15_downloaded_history.csv`), đối chiếu từng dòng: đúng 10 dòng dữ liệu, hoàn toàn sạch hậu tố `(Rỗng)`.
  - Toàn bộ bằng chứng ảnh chụp và báo cáo JSON được lưu tại [`docs/evidence/plan-10/`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/tree/main/docs/evidence/plan-10).

---

## 3. Khóa số liệu thực nghiệm khoa học chính thức

Mọi mô hình, trọng số và số liệu thực nghiệm của đề tài được bảo toàn nguyên vẹn 100%:

| Chỉ số thực nghiệm | Mô hình cơ sở (`alpha=1.0`) | Mô hình tối ưu (`alpha=0.1`) | Mức độ cải thiện | Nguồn dữ liệu gốc |
| :--- | :---: | :---: | :---: | :--- |
| **5-Fold CV Macro F1** | **88,55%** | **90,28%** | **+1,73%** | [`results/alpha_tuning.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/alpha_tuning.json) |
| **5-Fold CV F1 Std** | $\pm 0,0063$ | $\pm 0,0058$ | Ổn định hơn | [`results/alpha_tuning.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/alpha_tuning.json) |
| **Test Accuracy** | 86,71% | **88,52%** | **+1,81%** | [`results/evaluation_summary.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/evaluation_summary.json) |
| **Test Macro F1** | 86,45% | **88,33%** | **+1,88%** | [`results/evaluation_summary.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/evaluation_summary.json) |
| **Test Weighted F1** | 86,68% | **88,49%** | **+1,81%** | [`results/evaluation_summary.json`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/results/evaluation_summary.json) |
| **Kích thước bộ từ vựng** | 13.068 từ vựng | 13.068 từ vựng | Khóa cố định | [`models/tfidf_vectorizer.joblib`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/models/tfidf_vectorizer.joblib) |
| **Quy mô tập huấn luyện / kiểm thử** | 2.239 train / 1.490 test | 2.239 train / 1.490 test | 60% train / 40% test | [`data/`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/tree/main/data) |

---

## 4. Danh mục tài sản phát hành (Release Assets)

1. **Mã nguồn và gói bài nộp**: `phan-loai-van-ban-naive-bayes-final-submission.zip`
2. **Bản kê khai nội dung**: `MANIFEST.json`
3. **Mã băm toàn vẹn**: `CHECKSUMS.sha256`
4. **Biên bản nghiệm thu Plan 10**: [`docs/NGHIEM_THU_PLAN_10.md`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/blob/main/docs/NGHIEM_THU_PLAN_10.md)
5. **Thư mục bằng chứng**: [`docs/evidence/plan-10/`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/tree/main/docs/evidence/plan-10)
