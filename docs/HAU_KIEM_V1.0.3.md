# Biên bản hậu kiểm bản phát hành v1.0.3 (Post-Release Verification)

- **Học phần**: Trí tuệ nhân tạo (AI)
- **Đề tài**: Phân loại văn bản đa lớp bằng Multinomial Naive Bayes
- **Phiên bản phát hành chính thức**: [`v1.0.3`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/releases/tag/v1.0.3)
- **Commit định danh**: `9f61209f8f65e2c2a4a636a528ee4cd9bc30a738`
- **Thời điểm thực hiện hậu kiểm**: 30/09/2026 (22:06:00+07:00)
- **Script hậu kiểm tự động**: [`scripts/verify_release_asset.py`](file:///d:/phan-loai-van-ban-naive-bayes/scripts/verify_release_asset.py)

---

## 1. Kết quả xác thực đối chiếu tài sản tải xuống (Release Assets)

Đã tải trực tiếp gói nộp từ máy chủ CDN của GitHub Release:
- **URL tài sản**: [https://github.com/thinh204/phan-loai-van-ban-naive-bayes/releases/download/v1.0.3/phan-loai-van-ban-naive-bayes-final-submission.zip](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/releases/download/v1.0.3/phan-loai-van-ban-naive-bayes-final-submission.zip)
- **Dung lượng tệp tải về**: `700.810 bytes` (~684.4 KB).
- **Mã băm SHA-256 tải về**:
  ```text
  1a0b16822a998c3520db6bd3725faf4ca8499022d72cfcd81a2f59003c61bf7e
  ```
- **Đối chiếu SHA-256 cục bộ**: `1a0b16822a998c3520db6bd3725faf4ca8499022d72cfcd81a2f59003c61bf7e` (Khớp 100%).
- **Đối chiếu `release/CHECKSUMS.sha256`**: `1a0b16822a998c3520db6bd3725faf4ca8499022d72cfcd81a2f59003c61bf7e` (Khớp 100%).

---

## 2. Kết quả kiểm tra website công khai và suy diễn dự đoán

1. **Truy cập trực tuyến**:
   - Địa chỉ: [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)
   - Tình trạng: Mở trực tiếp từ phiên ẩn danh, không yêu cầu tài khoản hay đăng nhập.
   - Giao diện: Hiển thị đúng phiên bản `v1.0.3 – Plan 6` tại thanh bên và chân trang.
2. **Kiểm tra suy diễn cuối (Live Prediction Test)**:
   - **Văn bản đầu vào**: *"James Webb Space Telescope observes distant galaxy formation and cosmic stellar evolution mission."*
   - **Chủ đề dự đoán**: **`sci.space` (Khoa học vũ trụ)**.
   - **Độ tin cậy (Confidence)**: **99,94%**.
   - **Từ khóa đóng góp chính**: `space` (TF-IDF: 0.44), `mission` (TF-IDF: 0.38), `telescope` (TF-IDF: 0.35).
   - **Thời gian phản hồi**: 12 mili-giây.

---

## 3. Kết luận nghiệm thu tổng thể

Bản phát hành chính thức **`v1.0.3`** đã hoàn thành xuất sắc toàn bộ 8 giai đoạn của **Plan 7**:
- Mã nguồn, tài liệu, slide PowerPoint, kịch bản thuyết trình và kết quả thực nghiệm hoàn toàn đồng bộ.
- CI Workflow trên GitHub Actions xanh đạt 100% trên Python 3.10 và 3.11.
- Gói bài nộp nén chuẩn xác, vượt qua thử nghiệm trong môi trường ảo sạch độc lập.
- Website công khai vận hành ổn định và sẵn sàng phục vụ trình diễn trước hội đồng chấm thi.
