# Hướng dẫn triển khai lên Streamlit Community Cloud

Tài liệu này hướng dẫn chi tiết các bước triển khai ứng dụng phân loại văn bản Naive Bayes lên nền tảng đám mây miễn phí **Streamlit Community Cloud** để phục vụ demo trực tuyến.

---

## 1. Chuẩn hóa repository phục vụ triển khai

Repository đã được chuẩn hóa 100% để tương thích với môi trường Streamlit Cloud:
- **Tệp yêu cầu phụ thuộc:** `requirements.txt` đầy đủ, tương thích Linux/Cloud (scikit-learn, pandas, streamlit, joblib, numpy, scipy).
- **Điểm khởi chạy (Entry Point):** `app.py` tại thư mục gốc của repository.
- **Đường dẫn tương đối (Relative Paths):** Mọi đường dẫn truy xuất mô hình và kết quả (`models/`, `results/`) đều sử dụng `Path(__file__).resolve().parent`, hoàn toàn độc lập với hệ điều hành và không chứa đường dẫn tuyệt đối cục bộ.
- **Tệp cấu hình giao diện:** `.streamlit/config.toml` đã được thiết lập theme hiện đại (màu chủ đạo xanh `#2563EB`, chế độ `headless = true`).
- **Mô hình nạp sẵn:** Các tệp `.joblib` đã được lưu sẵn trong thư mục `models/` được commit trên Git, giúp ứng dụng trên Cloud khởi động ngay lập tức mà không phải huấn luyện lại.

---

## 2. Các bước triển khai trực tuyến trên Streamlit Cloud

1. **Truy cập nền tảng:**
   Mở trình duyệt và truy cập [https://share.streamlit.io/](https://share.streamlit.io/). Đăng nhập bằng tài khoản GitHub sở hữu repository.

2. **Tạo ứng dụng mới (New App):**
   Nhấn vào nút **"Create app"** (hoặc **"New app"**).

3. **Cấu hình thông tin ứng dụng:**
   - **Repository:** Chọn `thinh204/phan-loai-van-ban-naive-bayes`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Đã đăng ký tên miền: `https://phan-loai-van-ban-naive-bayes.streamlit.app`

4. **Triển khai (Deploy):**
   Nhấn nút **"Deploy!"**. Quá trình dựng môi trường và cài đặt `requirements.txt` sẽ diễn ra trong khoảng 1–2 phút.

5. **Xác nhận hoạt động và URL chính thức:**
   - **URL triển khai chính thức**: [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)
   - **Kết quả kiểm tra thực tế (30/09/2026)**:
     - Máy chủ phản hồi: `nginx/1.31.3` (Hạ tầng Google Cloud/Streamlit).
     - Giao thức: HTTPS / HTTP/2.
     - *Lưu ý*: Với repository ở chế độ Private trên GitHub, Streamlit Cloud tự động yêu cầu xác thực tài khoản GitHub (OAuth redirect tới `share.streamlit.io/-/auth/app`) để bảo mật quyền truy cập. Khi repository chuyển sang Public, ứng dụng có thể mở công khai cho tất cả người dùng không cần đăng nhập.

---


## 3. Khởi chạy thử nghiệm cục bộ (Local Testing)

Nếu máy tính không có kết nối mạng hoặc cần demo trực tiếp trên máy chấm điểm:

```powershell
# Kích hoạt môi trường ảo
.\.venv\Scripts\Activate.ps1

# Chạy ứng dụng Streamlit
streamlit run app.py
```

Truy cập địa chỉ cục bộ: `http://localhost:8501`.
