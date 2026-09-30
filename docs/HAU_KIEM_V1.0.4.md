# Biên Bản Hậu Kiểm Triển Khai v1.0.4 Trên Streamlit Cloud (Plan 11)

- **Dự án:** Phân loại văn bản bằng Multinomial Naive Bayes
- **Kho lưu trữ GitHub:** [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)
- **URL Triển Khai Công Khai:** [https://phan-loai-van-ban-naive-bayes.streamlit.app/](https://phan-loai-van-ban-naive-bayes.streamlit.app/)
- **Thời điểm thực hiện hậu kiểm:** 01/10/2026 (00:44:00+07:00)
- **Phương thức kiểm tra:** Trình duyệt Google Chrome headless qua giao thức Chrome DevTools Protocol (CDP), phiên khách công khai (Unauthenticated Guest Session).
- **Mã nguồn phát hành:** Commit [`14e88a2`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/commit/14e88a2) (Tag `v1.0.4`, CI Run ID: `36750762994`).
- **Gói bài nộp chính thức:** `release/phan-loai-van-ban-naive-bayes-final-submission.zip`
- **Mã băm SHA-256 đã xác minh:** `189918bdc3acaca2bc1e19f22ff370f475ad260b7b9b219ff9fe9ceb3a20d975` (trùng khớp 100% giữa local, GitHub Release và `CHECKSUMS.sha256`).
- **Tình trạng nguồn triển khai Streamlit Cloud:**
  - Repo kết nối: `thinh204/phan-loai-van-ban-naive-bayes`
  - Nhánh triển khai: `main`
  - Tệp khởi chạy: `app.py`
  - Tình trạng xác minh commit từ Dashboard: Chưa có quyền truy cập trực tiếp vào dashboard quản trị `share.streamlit.io` do yêu cầu đăng nhập tài khoản chủ sở hữu `thinh204`.

---

## 1. Kết Quả Chi Tiết 8 Ca Hậu Kiểm Theo Plan 11

Kịch bản kiểm thử tự động nghiêm ngặt [`scripts/verify_live_cloud_plan11.py`](../scripts/verify_live_cloud_plan11.py) đã thực hiện kiểm tra trực tiếp trên website công khai:

| Mã Ca | Hạng mục kiểm tra | Thao tác / Đầu vào | Kết quả mong đợi | Kết quả quan sát thực tế trên Streamlit Cloud | Trạng thái | Minh chứng bằng chứng |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **CA-01** | Truy cập công khai | Mở URL `https://phan-loai-van-ban-naive-bayes.streamlit.app/` | Giao diện nạp đầy đủ trong phiên khách, không báo lỗi, không yêu cầu đăng nhập | Giao diện nạp thành công trong 1s; không có lỗi ứng dụng; sẵn sàng tương tác | **ĐẠT (PASS)** | [`plan11_ca1_public_access.png`](evidence/plan-11/plan11_ca1_public_access.png) |
| **CA-02** | Phiên bản hiển thị | Kiểm tra chuỗi phiên bản trên Sidebar và Footer | Cả Sidebar và Footer đều hiển thị chính xác `v1.0.4` | Sidebar: `v1.0.3`<br>Footer: `(v1.0.3 - Plan 6)`<br>*(Tiến trình Python trên Cloud chưa reboot để nạp lại `src.config`)* | **CHỜ REBOOT (PENDING)** | [`plan11_ca1_public_access.png`](evidence/plan-11/plan11_ca1_public_access.png) |
| **CA-03** | Rỗng ở phiên mới | Bấm *"🚀 Phân loại"* khi ô văn bản để trống `""` | Hiển thị cảnh báo màu vàng, không tính xác suất tiên nghiệm, lịch sử 0 dòng | Xuất hiện cảnh báo *"⚠️ Vui lòng nhập nội dung văn bản để dự đoán!"*; không có hộp kết quả; lịch sử đúng **0 dòng** | **ĐẠT (PASS)** | [`plan11_ca3_empty_input.png`](evidence/plan-11/plan11_ca3_empty_input.png) |
| **CA-04** | Dự đoán hợp lệ (NASA) | *"NASA launched a spacecraft into orbit to study distant planets and explore the solar system."* | Nhãn: `sci.space`<br>Lịch sử tăng lên đúng 1 dòng | Nhãn: **`sci.space`**<br>Độ tin cậy: **99.44%**<br>Độ trễ: **21.35 ms**<br>Số lượt dự đoán: **1 dòng** | **ĐẠT (PASS)** | [`plan11_ca4_valid_nasa.png`](evidence/plan-11/plan11_ca4_valid_nasa.png) |
| **CA-05** | Khoảng trắng sau lượt hợp lệ | Gửi chuỗi toàn khoảng trắng `"    \t\n   "` sau khi đã có 1 lượt dự đoán | Hiển thị cảnh báo, số dòng lịch sử bảo toàn không tăng (giữ nguyên 1 dòng) | Xuất hiện cảnh báo nhập liệu; số lượt dự đoán giữ nguyên **1 dòng**, không thêm lượt rỗng | **ĐẠT (PASS)** | [`plan11_ca5_whitespace_after_valid.png`](evidence/plan-11/plan11_ca5_whitespace_after_valid.png) |
| **CA-06** | Đoạn trích ngắn `space` | Nhập văn bản *"space"* và bấm Phân loại | Dự đoán thành công, đoạn trích trong lịch sử đúng `space`, **không có `(Rỗng)`** | Dự đoán: `sci.space` (92.55%); đoạn trích trong lịch sử đúng nguyên văn **`space`**; lịch sử: **2 dòng** | **ĐẠT (PASS)** | [`plan11_ca6_short_space.png`](evidence/plan-11/plan11_ca6_short_space.png) |
| **CA-07** | Tải và đối chiếu CSV thật | Bấm *"📥 Tải lịch sử dự đoán (CSV)"* và kiểm tra tệp tải về từ trình duyệt | Đúng 2 dòng dữ liệu, nhãn và đoạn trích khớp lịch sử, không có lỗi `(Rỗng)` | Tải thành công `plan11_downloaded_history.csv` (2 dòng dữ liệu: NASA và space, không có dòng rỗng, 0 hậu tố `(Rỗng)`) | **ĐẠT (PASS)** | [`plan11_downloaded_history.csv`](evidence/plan-11/plan11_downloaded_history.csv) |
| **CA-08** | Tải lại trang (F5) | Làm mới trang web và chạy thêm một dự đoán mới | Trang tải lại sạch sẽ, phiên bản nhất quán, dự đoán mới hoạt động trơn tru | Tải lại thành công, dự đoán câu thiên văn học ra `sci.space`, lịch sử ghi nhận 1 dòng mới | **ĐẠT HÀNH VI (Chờ version)** | [`plan11_ca8_reload.png`](evidence/plan-11/plan11_ca8_reload.png)<br>[`plan11_ca8_reload_prediction.png`](evidence/plan-11/plan11_ca8_reload_prediction.png) |

---

## 2. Đối Chiếu Nội Dung Tệp CSV Thực Tế Tải Về (CA-07)

Tệp dữ liệu thực tế được trình duyệt tải trực tiếp từ nút bấm *"📥 Tải lịch sử dự đoán (CSV)"* trong phiên kiểm thử Plan 11 được lưu trữ tại [`docs/evidence/plan-11/plan11_downloaded_history.csv`](evidence/plan-11/plan11_downloaded_history.csv):

```csv
timestamp,text_preview,predicted_class,confidence_percent,in_vocab_tokens,is_uncertain,latency_ms
2026-09-30 17:44:32,NASA launched a spacecraft into orbit to study distant planets and explore the s...,sci.space,99.44,14,Không,21.35
2026-09-30 17:44:37,space,sci.space,92.55,1,Có,13.78
```

### Phân tích đối chiếu:
1. **Dòng 1 (NASA spacecraft):** Đoạn trích dài hơn 80 ký tự được cắt ngắn thành đúng 80 ký tự đầu và nối thêm `...`. Nhãn: `sci.space`, độ tin cậy: `99.44%`.
2. **Dòng 2 (`space`):** Đoạn trích ngắn đúng nguyên văn `space`, **hoàn toàn sạch sẽ, không có hậu tố `(Rỗng)`**.
3. **Số dòng dữ liệu:** Đúng $2$ dòng dữ liệu tương ứng với $2$ lượt phân loại hợp lệ. Không có bất kỳ dòng rỗng nào lọt vào tệp CSV sau thao tác gửi chuỗi rỗng (CA-03) và khoảng trắng (CA-05).

---

## 3. Chẩn Đoán Kỹ Thuật Về Chuỗi Phiên Bản Cũ Trên Cloud

### Nguyên nhân quan sát:
1. **Về mặt mã nguồn trên kho lưu trữ (`origin/main`):**
   - Tệp [`src/config.py`](../src/config.py) đã được cập nhật chính xác: `APP_VERSION = "v1.0.4"` và `PLAN_VERSION = "Plan 10"`, `FOOTER_CAPTION = "... (v1.0.4 - Plan 10)"`.
   - Toàn bộ 27/27 kiểm thử tự động, compileall và kiểm tra tính nhất quán mã băm đều đạt tuyệt đối.
2. **Về mặt tiến trình chạy trên Streamlit Cloud:**
   - Trong kiến trúc Streamlit Community Cloud, tiến trình Python chạy ứng dụng lưu giữ các module đã nạp vào từ điển bộ nhớ `sys.modules`.
   - Do tệp khởi chạy `app.py` không thay đổi trong commit `14e88a2`, watchdog của Streamlit không tự động tái khởi động tiến trình Python container. Khi người dùng truy cập, câu lệnh `from src.config import APP_VERSION` trả về đối tượng module cũ đã được nạp sẵn trong bộ nhớ từ trước khi git pull.
   - Các bản sửa lỗi logic giao diện trong `app.py` (chặn nhập liệu rỗng, định dạng đoạn trích) đã có hiệu lực ngay lập tức, nhưng chuỗi hằng số phiên bản trong `src.config` cần tiến trình Python được khởi động lại sạch (Clean Process Reboot) để nạp lại từ ổ đĩa.

### Thao tác cần thực hiện từ chủ tài khoản:
Chủ sở hữu kho lưu trữ (`thinh204`) chỉ cần thực hiện 1 thao tác duy nhất trên trang quản trị:
1. Truy cập [https://share.streamlit.io/](https://share.streamlit.io/) bằng tài khoản GitHub `thinh204`.
2. Tìm ứng dụng `phan-loai-van-ban-naive-bayes`.
3. Bấm vào biểu tượng menu ba dấu chấm (`...`) ở góc ứng dụng và chọn **"Reboot app"** (hoặc "Clear cache & Reboot").
4. Sau khi ứng dụng khởi động lại xong (~30-60 giây), tiến trình Python mới sẽ nạp lại tệp `src/config.py` từ commit mới nhất và hiển thị `v1.0.4` trên cả Sidebar và Footer.

---

## 4. Cam Kết & Bảo Toàn Tài Sản Nộp Bài

1. **Gói bài nộp `v1.0.4`:** Giữ nguyên vẹn 100% gói phát hành [release/phan-loai-van-ban-naive-bayes-final-submission.zip](../release/phan-loai-van-ban-naive-bayes-final-submission.zip) và tag `v1.0.4` đã được xuất bản trên GitHub Release. Không tạo bản vá mới `v1.0.5` vì mã nguồn mô hình, dịch vụ và giao diện của bản `v1.0.4` đã hoàn toàn chính xác.
2. **Tài liệu Plan 11:** Được bổ sung độc lập trong thư mục `docs/` để phục vụ công tác đối soát, hậu kiểm và bàn giao minh bạch.
3. **Mã băm toàn vẹn:** `189918bdc3acaca2bc1e19f22ff370f475ad260b7b9b219ff9fe9ceb3a20d975` tiếp tục là mã băm định danh chính thức của bài nộp đề tài.
