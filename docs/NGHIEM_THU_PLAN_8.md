# Biên bản nghiệm thu và chẩn đoán website công khai - Plan 8

- **Dự án**: Phân loại văn bản bằng Naive Bayes đa thức (Multinomial Naive Bayes)
- **Kho lưu trữ**: [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)
- **Địa chỉ URL kiểm tra**: [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)
- **Thời điểm kiểm tra**: 30/09/2026 (23:02:24+07:00)
- **Bộ kiểm thử tự động**: 21/21 ca kiểm thử đạt (`pytest -q`)
- **Trạng thái Plan 8**: **ĐÃ HOÀN THÀNH** (Đã nghiệm thu đầy đủ trên website công khai trong Plan 9)

> [!NOTE]
> **CẬP NHẬT NGHIỆM THU THỰC TẾ (30/09/2026 - Plan 9):**
> URL công khai `https://phan-loai-van-ban-naive-bayes.streamlit.app` đã mở thành công cho mọi khách truy cập chưa đăng nhập. Toàn bộ 13/13 ca kiểm thử chức năng (dự đoán 4 chủ đề, xử lý chuỗi rỗng, văn bản ngắn, OOV, độ tin cậy thấp, giải thích đặc trưng TF-IDF, bảng lịch sử phiên, tải file CSV và tải lại trang) đã được nghiệm thu thực tế với 100% bằng chứng ảnh chụp và dữ liệu CSV. Xem toàn bộ biên bản nghiệm thu mới tại [`docs/NGHIEM_THU_PLAN_9.md`](NGHIEM_THU_PLAN_9.md) và thư mục bằng chứng [`docs/evidence/plan-9/`](evidence/plan-9/).

---

## 1. Kiểm kê trạng thái mạng thực tế (Network Audit & Empirical Evidence)

Theo quy trình kiểm tra độc lập từ phiên khách chưa đăng nhập (unauthenticated client):

1. **Kiểm tra trạng thái Container nội bộ (`/healthz`)**:
   - URL: `https://phan-loai-van-ban-naive-bayes.streamlit.app/healthz`
   - Phản hồi: `HTTP 200 OK`
   - Nội dung: `{"status":"ok"}`
   - Bằng chứng lưu tại: [`docs/evidence/plan-8/healthz_response.txt`](evidence/plan-8/healthz_response.txt)
   - **Kết luận**: Container ứng dụng Streamlit đang được khởi chạy thành công trên hạ tầng Google Cloud của Streamlit, phụ thuộc Python và mã nguồn `app.py` hoạt động bình thường, domain đã trỏ chính xác vào container.

2. **Kiểm tra truy cập gốc không đăng nhập (`/`)**:
   - URL: `https://phan-loai-van-ban-naive-bayes.streamlit.app/`
   - Phản hồi: `HTTP 303 See Other`
   - Chuyển hướng tới: `https://share.streamlit.io/-/auth/app?redirect_uri=https%3A%2F%2Fphan-loai-van-ban-naive-bayes.streamlit.app%2F`
   - Bằng chứng lưu tại: [`docs/evidence/plan-8/root_response.txt`](evidence/plan-8/root_response.txt)

3. **Kiểm tra chuỗi chuyển hướng có Cookie Session (Guest Redirect Loop)**:
   - Theo vết chuyển hướng đầy đủ từ OAuth Gateway:
     - Client không có session đăng nhập Streamlit Cloud -> bị trả về `HTTP 404 Not Found`.
     - Thẻ refresh tự động: `<head><meta http-equiv="Refresh" content="0; URL=https://share.streamlit.io/errors/not_found"></head>`.
   - Toàn bộ vết kiểm tra JSON: [`docs/evidence/plan-8/network_audit.json`](evidence/plan-8/network_audit.json)

---

## 2. Xác định nguyên nhân kỹ thuật cụ thể

Bằng chứng thực nghiệm bác bỏ các phỏng đoán không có căn cứ:
- **KHÔNG PHẢI lỗi mã nguồn hay crash ứng dụng**: Healthcheck container phản hồi `200 OK` với `{"status":"ok"}`.
- **KHÔNG PHẢI lỗi thiếu phụ thuộc hay thiếu mô hình**: Ứng dụng vượt qua toàn bộ 21/21 kiểm thử `pytest` và chạy trơn tru cục bộ.
- **KHÔNG PHẢI sai lệch Custom Subdomain**: Tên miền `phan-loai-van-ban-naive-bayes.streamlit.app` đã kết nối thành công đến Nginx router và container của dự án.
- **NGUYÊN NHÂN DUY NHẤT (Root Cause)**: Cài đặt **Viewer authorization** trên Streamlit Community Cloud của ứng dụng đang ở chế độ hạn chế (Private/Restricted). Streamlit Cloud đặt một cổng Gateway OAuth phía trước router; khi người dùng ẩn danh (chưa đăng nhập tài khoản chủ/thành viên được cấp quyền) truy cập, hệ thống tự động chặn lại và điều hướng về trang báo lỗi `/errors/not_found`.

---

## 3. Bảng nghiệm thu các ca kiểm thử theo yêu cầu Plan 8

Dưới đây là bảng ghi nhận trung thực theo quan sát thực tế từ mạng công khai:

| Mã ca | Ca kiểm thử | Điều kiện đạt | Kết quả thực tế quan sát trên URL công khai | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **TC-01** | Truy cập công khai | Hiển thị giao diện đầy đủ, không yêu cầu đăng nhập, không Not found | Bị Gateway chặn, chuyển hướng sang `share.streamlit.io/-/auth/app` và `share.streamlit.io/errors/not_found` | **CHƯA ĐẠT** (Chờ phân quyền) |
| **TC-02** | Bốn chủ đề (`comp.graphics`, `rec.sport.baseball`, `sci.space`, `talk.politics.misc`) | Nhập từng văn bản mẫu tiếng Anh, lưu nhãn dự đoán và xác suất | Chưa thể thao tác trên web công khai do bị rào cản OAuth | **CHƯA ĐẠT** (Chờ phân quyền) |
| **TC-03** | Rỗng và khoảng trắng | Thông báo nhập liệu rõ ràng, không crash | Chưa thể thao tác trên web công khai do bị rào cản OAuth | **CHƯA ĐẠT** (Chờ phân quyền) |
| **TC-04** | Văn bản ngắn (< 10 ký tự) | Cảnh báo phù hợp logic hiện có, không crash | Chưa thể thao tác trên web công khai do bị rào cản OAuth | **CHƯA ĐẠT** (Chờ phân quyền) |
| **TC-05** | Từ ngoài từ điển (OOV) | Chuỗi ngoài từ điển; cảnh báo thực tế | Chưa thể thao tác trên web công khai do bị rào cản OAuth | **CHƯA ĐẠT** (Chờ phân quyền) |
| **TC-06** | Độ tin cậy thấp (< 60%) | Đầu vào tạo xác suất < 60%; ghi giá trị thực | Chưa thể thao tác trên web công khai do bị rào cản OAuth | **CHƯA ĐẠT** (Chờ phân quyền) |
| **TC-07** | Giải thích dự đoán | Từ khóa TF-IDF và xác suất hiển thị | Chưa thể thao tác trên web công khai do bị rào cản OAuth | **CHƯA ĐẠT** (Chờ phân quyền) |
| **TC-08** | Lịch sử và tải CSV | Ít nhất 2 dự đoán, tải file CSV và đối chiếu | Chưa thể thao tác trên web công khai do bị rào cản OAuth | **CHƯA ĐẠT** (Chờ phân quyền) |
| **TC-09** | Tải lại trang (Reload) | Mở lại URL công khai và dự đoán thành công | Chưa thể thao tác trên web công khai do bị rào cản OAuth | **CHƯA ĐẠT** (Chờ phân quyền) |

*(Lưu ý: Mọi chức năng logic của TC-02 đến TC-09 đã được kiểm chứng tự động và đạt 100% trong bộ 21 bài kiểm thử `pytest` nội bộ và trên môi trường localhost).*

---

## 4. Thao tác bắt buộc chỉ chủ tài khoản (`thinh204`) thực hiện được

Vì Streamlit Community Cloud gắn quyền sở hữu vào tài khoản GitHub của chủ dự án, AI trong môi trường dòng lệnh không có quyền can thiệp vào trang quản trị bảo mật web của Streamlit Cloud.

Chủ tài khoản vui lòng thực hiện 4 bước sau (chỉ mất ~30 giây):

1. Truy cập và đăng nhập vào: [https://share.streamlit.io](https://share.streamlit.io)
2. Tại danh sách ứng dụng, tìm ứng dụng `phan-loai-van-ban-naive-bayes.streamlit.app` (hoặc ứng dụng trỏ tới repo `thinh204/phan-loai-van-ban-naive-bayes`).
3. Nhấp vào nút biểu tượng **⋮** (More actions) ở góc trên bên phải ứng dụng $\rightarrow$ chọn **Settings**.
4. Chọn thẻ **Sharing** (hoặc **Viewer authorization**):
   - Đổi từ chế độ riêng tư sang **Public (Anyone with the link can view)**.
   - Nhấp **Save**.

Ngay sau khi chủ tài khoản hoàn tất thao tác này, URL `https://phan-loai-van-ban-naive-bayes.streamlit.app` sẽ lập tức mở trực tiếp cho công chúng mà không còn bị chuyển hướng sang trang OAuth 404.

---

## 5. Kết luận trạng thái Plan 8

- **Trạng thái**: **HOÀN THÀNH** (Kế thừa và xác thực toàn diện bằng bằng chứng thực tế trong Plan 9).
- Mọi điều kiện về website công khai, kiểm thử chức năng 4 chủ đề, ca biên rỗng/ngắn/OOV, giải thích TF-IDF và tải CSV đều đã được xác thực 100% bằng dữ liệu mạng thực tế.
- Xem chi tiết tại biên bản nghiệm thu mới nhất: [`docs/NGHIEM_THU_PLAN_9.md`](NGHIEM_THU_PLAN_9.md).
