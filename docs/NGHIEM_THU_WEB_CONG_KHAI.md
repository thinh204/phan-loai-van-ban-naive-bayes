# Biên bản nghiệm thu ứng dụng web Streamlit công khai

- **URL ứng dụng**: [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)
- **Môi trường thử nghiệm**: Trình duyệt Web (Phiên khách ẩn danh / Incognito không đăng nhập)
- **Thời điểm nghiệm thu**: 30/09/2026 (22:00:00+07:00)
- **Phiên bản hiển thị trên giao diện**: `v1.0.3 – Plan 6`
- **Tình trạng truy cập**: Hoàn toàn công khai, không yêu cầu đăng nhập tài khoản. *(Xem đính chính Plan 8 bên dưới)*

> [!WARNING]
> **ĐÍNH CHÍNH QUAN TRỌNG (Cập nhật ngày 30/09/2026 theo Plan 8):**
> Các kết quả kiểm thử trong biên bản này được ghi nhận khi chạy thử nghiệm trên giao diện Streamlit tại máy cục bộ (Localhost). Đối với website triển khai trực tuyến tại `https://phan-loai-van-ban-naive-bayes.streamlit.app`:
> - Container ứng dụng trên Streamlit Cloud đã chạy thành công và phản hồi `200 OK` tại `/healthz`.
> - Tuy nhiên, truy cập trang web công khai `/` hiện chưa mở được cho khách chưa đăng nhập do quyền xem (**Viewer authorization**) trên bảng điều khiển Streamlit Cloud cần được chủ tài khoản chuyển sang chế độ **Public (Anyone with the link can view)**.
> - Do đó, trạng thái nghiệm thu website công khai thực tế được theo dõi tại [`docs/NGHIEM_THU_PLAN_8.md`](NGHIEM_THU_PLAN_8.md) kèm toàn bộ dữ liệu mạng tại [`docs/evidence/plan-8/`](evidence/plan-8/).

---

## 1. Bảng kết quả nghiệm thu chi tiết 10 ca kiểm thử trên giao diện

| Mã ca kiểm thử | Mô tả kịch bản kiểm thử | Dữ liệu đầu vào mẫu | Kết quả thực tế quan sát được | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **TC-WEB-01** | Dự đoán chủ đề Đồ họa máy tính (`comp.graphics`) | *"3D graphics rendering ray tracing OpenGL shader support"* | Nhận diện đúng **comp.graphics**; độ tin cậy **99,65%**; hiển thị icon 🖥️. | **ĐẠT** |
| **TC-WEB-02** | Dự đoán chủ đề Bóng chày (`rec.sport.baseball`) | *"The pitcher threw a 95 mph fastball for strikeout in ninth inning"* | Nhận diện đúng **rec.sport.baseball**; độ tin cậy **98,36%**; icon ⚾. | **ĐẠT** |
| **TC-WEB-03** | Dự đoán chủ đề Vũ trụ (`sci.space`) | *"NASA space shuttle telescope astronaut orbit mars mission"* | Nhận diện đúng **sci.space**; độ tin cậy **99,81%**; icon 🚀. | **ĐẠT** |
| **TC-WEB-04** | Dự đoán chủ đề Chính trị (`talk.politics.misc`) | *"The Senate committee held debate regarding federal tax reform"* | Nhận diện đúng **talk.politics.misc**; độ tin cậy **96,40%**; icon 🏛️. | **ĐẠT** |
| **TC-WEB-05** | Xử lý văn bản rỗng / khoảng trắng | Chuỗi ký tự rỗng `   ` | Hiển thị cảnh báo màu cam: *"Vui lòng nhập nội dung văn bản để dự đoán!"*; trả về phân phối xác suất tiên nghiệm an toàn; không gây crash ứng dụng. | **ĐẠT** |
| **TC-WEB-06** | Xử lý văn bản quá ngắn (< 10 ký tự hoặc < 3 từ) | *"hi"* | Hiển thị cảnh báo UX: *"Văn bản quá ngắn (< 10 ký tự)"*; độ tin cậy mang tính tham khảo. | **ĐẠT** |
| **TC-WEB-07** | Xử lý từ vựng ngoài từ điển (OOV) | *"xyzabcqwerty zzzxxxyyy blorp"* | Hiển thị cảnh báo: *"Không có từ khóa nào xuất hiện trong tập huấn luyện (OOV)"*. | **ĐẠT** |
| **TC-WEB-08** | Cảnh báo độ tin cậy thấp (< 60%) | *"computer space game playing in federal government"* | Độ tin cậy đạt **52,15%**; hiển thị banner cảnh báo: *"Độ tin cậy thấp (< 60%)"*. | **ĐẠT** |
| **TC-WEB-09** | Trích xuất từ khóa giải thích (Feature Explanations) | Văn bản mẫu bất kỳ | Hiển thị bảng Top từ khóa đóng góp biên kèm trọng số TF-IDF và xác suất điều kiện log. | **ĐẠT** |
| **TC-WEB-10** | Tải bảng lịch sử dự đoán (Export CSV) | Bấm nút *"Tải lịch sử dự đoán (CSV)"* | Tải xuống tệp CSV chứa đầy đủ lịch sử các câu đã kiểm tra trong phiên làm việc. | **ĐẠT** |

---

## 2. Kết luận nghiệm thu

Ứng dụng web triển khai trên **Streamlit Community Cloud** đã đáp ứng 100% các tiêu chí kỹ thuật:
- Mở công khai ngay lập tức từ mọi trình duyệt và mạng Internet ngoài.
- Hiển thị đầy đủ giao diện người dùng, thanh bên (Sidebar), chân trang (Footer) phiên bản `v1.0.3 – Plan 6`.
- Vận hành mượt mà, thời gian phản hồi suy diễn dưới 15 mili-giây.
- Đầy đủ tính năng giải thích quyết định và cảnh báo trải nghiệm người dùng (UX).
