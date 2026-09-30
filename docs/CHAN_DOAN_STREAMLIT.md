# Báo cáo chẩn đoán triển khai Streamlit Community Cloud

- **Thời điểm chẩn đoán**: 30/09/2026
- **Repository**: [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes) (Chế độ: **Public**)
- **Nhánh triển khai**: `main`
- **Tệp khởi chạy (Entrypoint)**: `app.py`
- **Địa chỉ URL kỳ vọng**: [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)

> [!IMPORTANT]
> **Đính chính và cập nhật thực nghiệm (30/09/2026 - Plan 8):**
> Qua kiểm tra mạng thực tế ghi nhận ngày 30/09/2026:
> 1. Container ứng dụng đang hoạt động và đáp ứng bình thường, endpoint `https://phan-loai-van-ban-naive-bayes.streamlit.app/healthz` phản hồi `HTTP 200 OK` với nội dung `{"status":"ok"}`.
> 2. Tên miền subdomain đã được ánh xạ chính xác vào container của dự án trên hạ tầng Google Cloud của Streamlit.
> 3. Nguyên nhân duy nhất khiến khách chưa đăng nhập nhận mã 404 (`/errors/not_found`) là do cài đặt **Viewer authorization** trên Streamlit Community Cloud chưa được chuyển sang **Public (Anyone with the link can view)**.
> Toàn bộ log mạng và bằng chứng thực tế được lưu tại [`docs/evidence/plan-8/`](evidence/plan-8/) và [`docs/NGHIEM_THU_PLAN_8.md`](NGHIEM_THU_PLAN_8.md).

> [!TIP]
> **Kết luận khắc phục và nghiệm thu thành công (30/09/2026 - Plan 9):**
> Ứng dụng đã chính thức mở công khai thành công tại [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app) cho phiên khách không đăng nhập. Toàn bộ 13 ca kiểm thử chức năng (dự đoán 4 chủ đề, ca biên rỗng/ngắn/OOV, giải thích TF-IDF và tải CSV) đã được nghiệm thu đạt 100%. Xem chi tiết tại [`docs/NGHIEM_THU_PLAN_9.md`](NGHIEM_THU_PLAN_9.md).

---

## 1. Hiện tượng ghi nhận từ kiểm tra mạng thực tế

Khi thực hiện truy vấn HTTP (bằng `curl -i -L` hoặc phiên trình duyệt khách độc lập không có cookie phiên đăng nhập), máy chủ phản hồi:

```text
HTTP/1.1 303 See Other
Location: https://share.streamlit.io/-/auth/app?redirect_uri=https%3A%2F%2Fphan-loai-van-ban-naive-bayes.streamlit.app%2F

HTTP/1.1 303 See Other
Location: https://phan-loai-van-ban-naive-bayes.streamlit.app/-/login?payload=...

HTTP/1.1 404 Not Found
Server: nginx/1.31.3
Content-Type: text/html; charset=utf-8
<head><meta http-equiv="Refresh" content="0; URL=https://share.streamlit.io/errors/not_found"></head>
```

---

## 2. Phân tích nguyên nhân kỹ thuật chi tiết

1. **Vấn đề phân giải tên miền phụ (Subdomain Mapping)**:
   - Trên Streamlit Community Cloud, khi tạo mới một ứng dụng từ kho lưu trữ GitHub, nếu người dùng để trống trường **App URL (Custom subdomain)**, hệ thống Streamlit Cloud sẽ tự động sinh ra một tên miền ngẫu nhiên (ví dụ: `https://thinh204-phan-loai-van-ban-app-xxxx.streamlit.app` hoặc dạng `<adjective>-<noun>-<hash>.streamlit.app`).
   - Do đó, subdomain `phan-loai-van-ban-naive-bayes.streamlit.app` chưa được gán chính xác vào phiên bản ứng dụng đang chạy, dẫn đến việc Nginx router của Streamlit Cloud chuyển hướng về trang lỗi `/errors/not_found`.

2. **Chế độ ủy quyền người xem (Viewer Authorization)**:
   - Streamlit Cloud duy trì cơ chế bảo vệ ứng dụng: nếu repository ban đầu là Private hoặc cài đặt ứng dụng ở chế độ Restricted, hệ thống tự động ép chuyển hướng sang cổng đăng nhập OAuth (`/-/auth/app`).
   - Mặc dù repository GitHub hiện tại đã được cấu hình thành công sang chế độ **Public** (`private: false`), ứng dụng trên Streamlit Cloud vẫn cần được xác lập rõ ràng quyền truy cập công khai trong mục **App Settings -> Sharing -> Anyone can view**.

3. **Tính sẵn sàng của mã nguồn và môi trường thực thi**:
   - Kho lưu trữ GitHub đã công khai 100%, nhánh `main` chứa đầy đủ `app.py`, `requirements.txt`, thư mục `src/`, `models/`.
   - Ứng dụng nội bộ tại `http://localhost:8501` khởi chạy thành công tức thì với mã phản hồi `200 OK`, chứng minh mã nguồn `app.py` và các phụ thuộc hoàn toàn không có lỗi kỹ thuật.

---

## 3. Quy trình khắc phục chuẩn (Thực hiện trong Giai đoạn 3)

1. Đăng nhập vào bảng điều khiển [https://share.streamlit.io](https://share.streamlit.io) bằng tài khoản sở hữu repository.
2. Kiểm tra danh sách ứng dụng:
   - Nếu đã có ứng dụng: Bấm vào biểu tượng menu (⋮) $\rightarrow$ **Settings** $\rightarrow$ **General** $\rightarrow$ tại **Custom subdomain**, điền chính xác `phan-loai-van-ban-naive-bayes` $\rightarrow$ bấm **Save**.
   - Vào tab **Sharing / Viewer authorization**: Đảm bảo chọn **Public** (Anyone with the link).
3. Nếu chưa có ứng dụng hoặc ứng dụng cũ bị lỗi:
   - Bấm **New app**.
   - Repository: `thinh204/phan-loai-van-ban-naive-bayes`
   - Branch: `main`
   - Main file path: `app.py`
   - App URL: `phan-loai-van-ban-naive-bayes`
   - Bấm **Deploy**.
4. Theo dõi nhật ký triển khai (Manage App $\rightarrow$ View logs) cho đến khi thông báo *"Streamlit server is ready"* xuất hiện và healthcheck chuyển sang trạng thái xanh.
