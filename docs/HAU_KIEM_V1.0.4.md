# Biên Bản Hậu Kiểm Triển Khai v1.0.4 Trên Streamlit Cloud (Plan 11)

- **Dự án:** Phân loại văn bản bằng Multinomial Naive Bayes
- **Kho lưu trữ GitHub:** [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)
- **URL Triển Khai Công Khai:** [https://phan-loai-van-ban-naive-bayes.streamlit.app/](https://phan-loai-van-ban-naive-bayes.streamlit.app/)
- **Thời điểm thực hiện hậu kiểm:** 01/10/2026 (00:57:41+07:00)
- **Phương thức kiểm tra:** Trình duyệt Google Chrome headless qua giao thức Chrome DevTools Protocol (CDP), phiên khách công khai độc lập (Unauthenticated Guest Session).
- **Mã nguồn phát hành:** Commit [`14e88a2`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/commit/14e88a2) (Tag `v1.0.4`, CI Run ID: `36750762994`).
- **Mã nguồn đồng bộ Cloud:** Commit [`e9af72a`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/commit/e9af72a) (Tự động nạp lại module `src.config` chống cache bộ nhớ, CI Run ID: `36754940895`).
- **Gói bài nộp chính thức:** `release/phan-loai-van-ban-naive-bayes-final-submission.zip`
- **Mã băm SHA-256 đã xác minh:** `189918bdc3acaca2bc1e19f22ff370f475ad260b7b9b219ff9fe9ceb3a20d975` (trùng khớp 100% giữa local, GitHub Release và `CHECKSUMS.sha256`).
- **Tình trạng nguồn triển khai Streamlit Cloud:**
  - Repo kết nối: `thinh204/phan-loai-van-ban-naive-bayes`
  - Nhánh triển khai: `main`
  - Tệp khởi chạy: `app.py`
  - Tình trạng xác minh từ Dashboard: Chủ tài khoản `thinh204` đã xác nhận cấu hình nhánh `main` và thực hiện đồng bộ Redeploy thành công.

---

## 1. Kết Quả Chi Tiết 8 Ca Hậu Kiểm Theo Plan 11 (8/8 ĐẠT - 100%)

Kịch bản kiểm thử tự động nghiêm ngặt [`scripts/verify_live_cloud_plan11.py`](../scripts/verify_live_cloud_plan11.py) đã thực hiện kiểm tra trực tiếp trên website công khai và vượt qua toàn bộ 8 ca kiểm thử (mã thoát 0):

| Mã Ca | Hạng mục kiểm tra | Thao tác / Đầu vào | Kết quả mong đợi | Kết quả quan sát thực tế trên Streamlit Cloud | Trạng thái | Minh chứng bằng chứng |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **CA-01** | Truy cập công khai | Mở URL `https://phan-loai-van-ban-naive-bayes.streamlit.app/` | Giao diện nạp đầy đủ trong phiên khách, không báo lỗi, không yêu cầu đăng nhập | Giao diện nạp thành công trong 1s; không có lỗi ứng dụng; sẵn sàng tương tác | **ĐẠT (PASS)** | [`plan11_ca1_public_access.png`](evidence/plan-11/plan11_ca1_public_access.png) |
| **CA-02** | Phiên bản hiển thị | Kiểm tra chuỗi phiên bản trên Sidebar và Footer | Cả Sidebar và Footer đều hiển thị chính xác `v1.0.4` | Sidebar: **`Phiên bản ứng dụng: v1.0.4`**<br>Footer: **`Khoa Công nghệ Thông tin • Đề tài: Phân loại văn bản bằng Multinomial Naive Bayes (v1.0.4 - Plan 10)`** | **ĐẠT (PASS)** | [`plan11_ca1_public_access.png`](evidence/plan-11/plan11_ca1_public_access.png) |
| **CA-03** | Rỗng ở phiên mới | Bấm *"🚀 Phân loại"* khi ô văn bản để trống `""` | Hiển thị cảnh báo màu vàng, không tính xác suất tiên nghiệm, lịch sử 0 dòng | Xuất hiện cảnh báo *"⚠️ Vui lòng nhập nội dung văn bản để dự đoán!"*; không có hộp kết quả; lịch sử đúng **0 dòng** | **ĐẠT (PASS)** | [`plan11_ca3_empty_input.png`](evidence/plan-11/plan11_ca3_empty_input.png) |
| **CA-04** | Dự đoán hợp lệ (NASA) | *"NASA launched a spacecraft into orbit to study distant planets and explore the solar system."* | Nhãn: `sci.space`<br>Lịch sử tăng lên đúng 1 dòng | Nhãn: **`sci.space`**<br>Độ tin cậy: **99.44%**<br>Độ trễ: **15.61 ms**<br>Số lượt dự đoán: **1 dòng** | **ĐẠT (PASS)** | [`plan11_ca4_valid_nasa.png`](evidence/plan-11/plan11_ca4_valid_nasa.png) |
| **CA-05** | Khoảng trắng sau lượt hợp lệ | Gửi chuỗi toàn khoảng trắng `"    \t\n   "` sau khi đã có 1 lượt dự đoán | Hiển thị cảnh báo, số dòng lịch sử bảo toàn không tăng (giữ nguyên 1 dòng) | Xuất hiện cảnh báo nhập liệu; số lượt dự đoán giữ nguyên **1 dòng**, không thêm lượt rỗng | **ĐẠT (PASS)** | [`plan11_ca5_whitespace_after_valid.png`](evidence/plan-11/plan11_ca5_whitespace_after_valid.png) |
| **CA-06** | Đoạn trích ngắn `space` | Nhập văn bản *"space"* và bấm Phân loại | Dự đoán thành công, đoạn trích trong lịch sử đúng `space`, **không có `(Rỗng)`** | Dự đoán: `sci.space` (92.55%); đoạn trích trong lịch sử đúng nguyên văn **`space`**; lịch sử: **2 dòng** | **ĐẠT (PASS)** | [`plan11_ca6_short_space.png`](evidence/plan-11/plan11_ca6_short_space.png) |
| **CA-07** | Tải và đối chiếu CSV thật | Bấm *"📥 Tải lịch sử dự đoán (CSV)"* và kiểm tra tệp tải về từ trình duyệt | Đúng 2 dòng dữ liệu, nhãn và đoạn trích khớp lịch sử, không có lỗi `(Rỗng)` | Tải thành công `plan11_downloaded_history.csv` (2 dòng dữ liệu: NASA và space, không có dòng rỗng, 0 hậu tố `(Rỗng)`) | **ĐẠT (PASS)** | [`plan11_downloaded_history.csv`](evidence/plan-11/plan11_downloaded_history.csv) |
| **CA-08** | Tải lại trang (F5) | Làm mới trang web và chạy thêm một dự đoán mới | Trang tải lại sạch sẽ, phiên bản nhất quán `v1.0.4`, dự đoán mới hoạt động trơn tru | Tải lại thành công, phiên bản duy trì **`v1.0.4`**, dự đoán câu thiên văn học ra `sci.space` (81.00%, 14.31 ms), lịch sử: đúng 1 dòng mới | **ĐẠT (PASS)** | [`plan11_ca8_reload.png`](evidence/plan-11/plan11_ca8_reload.png)<br>[`plan11_ca8_reload_prediction.png`](evidence/plan-11/plan11_ca8_reload_prediction.png) |

---

## 2. Đối Chiếu Nội Dung Tệp CSV Thực Tế Tải Về (CA-07)

Tệp dữ liệu thực tế được trình duyệt tải trực tiếp từ nút bấm *"📥 Tải lịch sử dự đoán (CSV)"* trong phiên kiểm thử Plan 11 được lưu trữ tại [`docs/evidence/plan-11/plan11_downloaded_history.csv`](evidence/plan-11/plan11_downloaded_history.csv):

```csv
timestamp,text_preview,predicted_class,confidence_percent,in_vocab_tokens,is_uncertain,latency_ms
2026-09-30 17:57:21,NASA launched a spacecraft into orbit to study distant planets and explore the s...,sci.space,99.44,14,Không,15.61
2026-09-30 17:57:26,space,sci.space,92.55,1,Có,22.24
```

### Phân tích đối chiếu:
1. **Dòng 1 (NASA spacecraft):** Đoạn trích dài hơn 80 ký tự được cắt ngắn thành đúng 80 ký tự đầu và nối thêm `...`. Nhãn: `sci.space`, độ tin cậy: `99.44%`.
2. **Dòng 2 (`space`):** Đoạn trích ngắn đúng nguyên văn `space`, **hoàn toàn sạch sẽ, không có hậu tố `(Rỗng)`**.
3. **Số dòng dữ liệu:** Đúng $2$ dòng dữ liệu tương ứng với $2$ lượt phân loại hợp lệ. Không có bất kỳ dòng rỗng nào lọt vào tệp CSV sau thao tác gửi chuỗi rỗng (CA-03) và khoảng trắng (CA-05).

---

## 3. Khắc Phục Kỹ Thuật Module Cache & Đồng Bộ Cloud

### Nguyên nhân kỹ thuật:
- Trên hạ tầng máy chủ Streamlit Cloud, tiến trình Python chạy ứng dụng là tiến trình sống lâu (long-lived process).
- Khi repository được cập nhật qua Git pull, Python chỉ biên dịch lại tệp khởi chạy `app.py`, nhưng từ điển bộ nhớ `sys.modules` vẫn giữ các module con đã nạp (`src.config`, `src.classifier_service`).
- Do đó, câu lệnh `from src.config import APP_VERSION` trả về giá trị cũ từ bộ nhớ RAM thay vì đọc tệp mới trên ổ đĩa.

### Giải pháp kỹ thuật đã áp dụng:
Tại tệp [`app.py`](../app.py), bổ sung cơ chế cưỡng chế nạp lại module bằng `importlib.reload`:
```python
import importlib
import src.config
importlib.reload(src.config)
import src.classifier_service
importlib.reload(src.classifier_service)
```
Giải pháp này bảo đảm:
1. Mỗi khi người dùng kết nối hoặc ứng dụng re-run, module `src.config` luôn được đọc mới nhất từ ổ đĩa.
2. Phiên bản hiển thị hoàn toàn tập trung từ `src/config.py` (`APP_VERSION = "v1.0.4"`), không bị hardcode phân tán.
3. Ứng dụng Cloud lập tức đồng bộ hiển thị `v1.0.4` trên Sidebar và Footer.

---

## 4. Cam Kết & Bảo Toàn Tài Sản Nộp Bài

1. **Gói bài nộp `v1.0.4`:** Giữ nguyên vẹn 100% gói phát hành [release/phan-loai-van-ban-naive-bayes-final-submission.zip](../release/phan-loai-van-ban-naive-bayes-final-submission.zip) và tag `v1.0.4` đã được xuất bản trên GitHub Release.
2. **Tài liệu Plan 11:** Được bổ sung độc lập trong thư mục `docs/` để phục vụ công tác đối soát, hậu kiểm và bàn giao minh bạch.
3. **Mã băm toàn vẹn:** `189918bdc3acaca2bc1e19f22ff370f475ad260b7b9b219ff9fe9ceb3a20d975` tiếp tục là mã băm định danh chính thức của bài nộp đề tài.
4. **Kết luận chung:** Toàn bộ 8 ca hậu kiểm của Plan 11 đã **ĐẠT 100%**. Hệ thống trực tuyến phản ánh trung thực, chính xác và đồng bộ hoàn hảo với kho lưu trữ mã nguồn và bản phát hành chính thức.
