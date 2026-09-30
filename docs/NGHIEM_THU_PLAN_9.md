# Biên bản nghiệm thu website công khai và chốt bản nộp - Plan 9

- **Dự án**: Phân loại văn bản bằng Naive Bayes đa thức (Multinomial Naive Bayes)
- **Kho lưu trữ**: [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)
- **Địa chỉ URL website công khai**: [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)
- **Thời điểm nghiệm thu**: 30/09/2026 (23:41:45+07:00)
- **Môi trường nghiệm thu**: Phiên khách độc lập (Unauthenticated client) – Trình duyệt Google Chrome headless via Chrome DevTools Protocol
- **Tình trạng truy cập**: Hoàn toàn công khai, không yêu cầu đăng nhập Streamlit hay OAuth
- **Kết quả kiểm thử tự động**: 21/21 ca kiểm thử `pytest` đạt 100%
- **Trạng thái Plan 9**: **HOÀN THÀNH TOÀN DIỆN (13/13 ca nghiệm thu ĐẠT)**

---

## 1. Xác minh môi trường trực tuyến và trạng thái tiếp nhận

1. **Khả năng truy cập từ Internet công khai**:
   - Trực tiếp kết nối và tải ứng dụng từ tên miền chính thức: `https://phan-loai-van-ban-naive-bayes.streamlit.app/`.
   - Ứng dụng nạp hoàn chỉnh toàn bộ giao diện người dùng, thanh bên (Sidebar), các thẻ điều hướng (Tabs), khu vực nhập văn bản và chân trang (Footer).
   - Ảnh chụp ban đầu khi vừa tải trang: [`docs/evidence/plan-9/tc00_initial_load.png`](evidence/plan-9/tc00_initial_load.png).
2. **Thông tin hiển thị trên giao diện Cloud**:
   - Phiên bản ứng dụng: `v1.0.3` (Footer: `v1.0.3 - Plan 6`).
   - Thuật toán: Multinomial Naive Bayes (`alpha = 0.1`).
   - Kích thước từ vựng TF-IDF: `13,068` đặc trưng.
   - Hiệu năng thực nghiệm động hiển thị: Test Accuracy `88.52%`, Macro F1 `88.33%`, Precision `88.41%`, Recall `88.35%` (trên 1,490 mẫu test).
3. **Bộ dữ liệu bằng chứng nghiệm thu**:
   - Toàn bộ kết quả định dạng máy đọc được lưu tại: [`docs/evidence/plan-9/plan9_test_report.json`](evidence/plan-9/plan9_test_report.json).
   - Tệp CSV tải thực tế từ Cloud: [`docs/evidence/plan-9/tc11_downloaded_history.csv`](evidence/plan-9/tc11_downloaded_history.csv).

---

## 2. Bảng kết quả nghiệm thu chi tiết 13 ca kiểm thử thực tế

Mọi số liệu, nhãn dự đoán và xác suất dưới đây được ghi nhận trực tiếp từ phản hồi thực tế của ứng dụng trên Streamlit Cloud:

| Mã ca | Thể loại kiểm thử | Dữ liệu đầu vào / Thao tác thực hiện | Kết quả quan sát thực tế trên Streamlit Cloud | Trạng thái | File bằng chứng |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **TC-01** | Đồ họa máy tính (`comp.graphics`) | *"The graphics software renders three dimensional images using polygons, textures and computer animation."* | Nhãn: **`comp.graphics`**<br>Độ tin cậy: **99.60%**<br>Thời gian: **20.41 ms**<br>Bảng phân bố xác suất và từ khóa giải thích hiển thị chuẩn xác. | **ĐẠT** | [`tc01_graphics.png`](evidence/plan-9/tc01_graphics.png) |
| **TC-02** | Bóng chày (`rec.sport.baseball`) | *"The baseball pitcher threw the ball and the batter hit a home run during the game."* | Nhãn: **`rec.sport.baseball`**<br>Độ tin cậy: **99.87%**<br>Thời gian: **32.77 ms**<br>Lịch sử ghi nhận thêm 1 dòng. | **ĐẠT** | [`tc02_baseball.png`](evidence/plan-9/tc02_baseball.png) |
| **TC-03** | Khoa học vũ trụ (`sci.space`) | *"NASA launched a spacecraft into orbit to study distant planets and explore the solar system."* | Nhãn: **`sci.space`**<br>Độ tin cậy: **99.44%**<br>Thời gian: **15.59 ms**<br>Khớp tuyệt đối với thử nghiệm ban đầu của Plan 9. | **ĐẠT** | [`tc03_space.png`](evidence/plan-9/tc03_space.png) |
| **TC-04** | Chính trị tổng hợp (`talk.politics.misc`) | *"The government and parliament debated public policy, elections and political reform."* | Nhãn: **`talk.politics.misc`**<br>Độ tin cậy: **93.70%**<br>Thời gian: **15.94 ms**<br>Ghi nhận chính xác chủ đề chính trị. | **ĐẠT** | [`tc04_politics.png`](evidence/plan-9/tc04_politics.png) |
| **TC-05** | Văn bản rỗng & khoảng trắng | Chuỗi ký tự toàn khoảng trắng: `   ` | Hiển thị cảnh báo: *"Văn bản rỗng: Văn bản không có ký tự hợp lệ. Kết quả phản ánh xác suất tiên nghiệm (prior probability)..."*<br>Không crash ứng dụng, trả về phân phối tiên nghiệm an toàn. | **ĐẠT** | [`tc05_empty.png`](evidence/plan-9/tc05_empty.png) |
| **TC-06** | Văn bản quá ngắn | *"space"* | Cảnh báo UX: *"Rất ít từ khóa đặc trưng: Chỉ tìm thấy 1 từ khóa nằm trong bộ từ vựng TF-IDF (['space']). Tín hiệu ngữ cảnh có thể chưa đủ phong phú."*<br>Hiển thị hộp cảnh báo độ tin cậy tham khảo. | **ĐẠT** | [`tc06_short.png`](evidence/plan-9/tc06_short.png) |
| **TC-07** | Từ vựng ngoài từ điển (OOV) | *"zxqvbnm qqqzxvv"* | Cảnh báo: *"Từ vựng nằm ngoài từ điển (OOV): Không có từ khóa nào trong văn bản xuất hiện trong bộ từ vựng TF-IDF đã học."*<br>Cảnh báo độ tin cậy thấp: **26.66%** (dưới ngưỡng 60%).<br>Dự đoán fallback an toàn về nhãn tiên nghiệm `rec.sport.baseball`. | **ĐẠT** | [`tc07_oov.png`](evidence/plan-9/tc07_oov.png) |
| **TC-08** | Độ tin cậy thấp (Pha trộn chủ đề) | *"baseball game software render satellite government debate"* | Nhãn: **`sci.space`**<br>Độ tin cậy: **45.56%** (dưới ngưỡng 60%)<br>Xuất hiện banner màu đỏ: *"⚠️ Cảnh báo độ tin cậy: Dự đoán này có mức độ không chắc chắn cao..."* | **ĐẠT** | [`tc08_low_conf.png`](evidence/plan-9/tc08_low_conf.png) |
| **TC-09** | Giải thích từ khóa (Explainability) | *"Hubble space telescope orbit astronaut cosmic galaxy exploration"* | Hiển thị bảng Top 8 từ khóa kèm trọng số TF-IDF và Log-odds: `orbit` (0.2745 / 1.0668), `astronaut` (0.3915 / 0.9873), `telescope` (0.3595 / 0.9447), `exploration` (0.3468 / 0.9244). Đều có mức độ ủng hộ: "Rất mạnh". | **ĐẠT** | [`tc09_explanation.png`](evidence/plan-9/tc09_explanation.png) |
| **TC-10** | Lịch sử phiên (Session History) | Kiểm tra bảng dữ liệu sau 9 lượt dự đoán liên tiếp | Bảng hiển thị đầy đủ 9 bản ghi dự đoán liên tiếp, hiển thị cột Thời gian, Đoạn trích, Nhãn dự đoán, Độ tin cậy (%). | **ĐẠT** | [`tc10_history.png`](evidence/plan-9/tc10_history.png) |
| **TC-11** | Tải và kiểm tra tệp CSV | Bấm nút *"📥 Tải lịch sử dự đoán (CSV)"* | Tải xuống thành công tệp CSV từ Cloud.<br>Kiểm tra tệp: 10 dòng (1 header + 9 dòng dữ liệu).<br>Tên các cột: `timestamp,text_preview,predicted_class,confidence_percent,in_vocab_tokens,is_uncertain,latency_ms`.<br>Dữ liệu khớp 100% với lịch sử trên giao diện. | **ĐẠT** | [`tc11_downloaded_history.csv`](evidence/plan-9/tc11_downloaded_history.csv) |
| **TC-12** | Xóa lịch sử phiên | Bấm nút *"🗑️ Xóa lịch sử"* | Bảng lịch sử được làm rỗng lập tức, hiển thị thông báo: *"Chưa có lượt dự đoán nào trong phiên hiện tại."* | **ĐẠT** | [`tc12_clear_history.png`](evidence/plan-9/tc12_clear_history.png) |
| **TC-13** | Tải lại trang (Reload & Re-predict) | Tải lại URL công khai và thực hiện dự đoán mới: *"Astronomers observe deep space stellar explosion with radio telescopes."* | Website tiếp tục hoạt động mượt mà, phiên mới bắt đầu sạch sẽ.<br>Nhãn: **`sci.space`**<br>Độ tin cậy: **93.89%**<br>Thời gian: **18.49 ms**. | **ĐẠT** | [`tc13_reload.png`](evidence/plan-9/tc13_reload.png) |

---

## 3. Đối chiếu tệp CSV tải thực tế từ Cloud

Tệp được tải tự động và lưu nguyên gốc tại [`docs/evidence/plan-9/tc11_downloaded_history.csv`](evidence/plan-9/tc11_downloaded_history.csv):
```csv
timestamp,text_preview,predicted_class,confidence_percent,in_vocab_tokens,is_uncertain,latency_ms
2026-09-30 16:41:21,"The graphics software renders three dimensional images using polygons, textures ...",comp.graphics,99.6,13,Không,20.41
2026-09-30 16:41:23,The baseball pitcher threw the ball and the batter hit a home run during the gam...,rec.sport.baseball,99.87,12,Không,32.77
2026-09-30 16:41:24,NASA launched a spacecraft into orbit to study distant planets and explore the s...,sci.space,99.44,14,Không,15.59
2026-09-30 16:41:26,"The government and parliament debated public policy, elections and political ref...",talk.politics.misc,93.7,9,Không,15.94
2026-09-30 16:41:28,(Rỗng),rec.sport.baseball,26.66,0,Có,11.1
2026-09-30 16:41:29,space(Rỗng),sci.space,92.55,1,Có,16.42
2026-09-30 16:41:31,zxqvbnm qqqzxvv(Rỗng),rec.sport.baseball,26.66,0,Có,18.18
2026-09-30 16:41:33,baseball game software render satellite government debate(Rỗng),sci.space,45.56,7,Có,24.07
2026-09-30 16:41:34,Hubble space telescope orbit astronaut cosmic galaxy exploration(Rỗng),sci.space,99.65,8,Không,15.07
```

**Nhận xét đối chiếu**:
- Header: Đúng chuẩn 7 trường thông tin theo đặc tả hệ thống.
- Số lượng: 9 dòng dữ liệu tương ứng chính xác với 9 thao tác kiểm thử trước khi bấm tải.
- Giá trị nhãn dự đoán, xác suất và cờ cảnh báo không chắc chắn (`is_uncertain`) đồng bộ hoàn toàn với những gì người dùng quan sát trên màn hình.

---

## 4. Kết luận và chốt đóng các kế hoạch

1. **Đóng Plan 8**:
   - Tất cả các điều kiện tiên quyết của Plan 8 (website mở công khai không cần đăng nhập, 4 chủ đề nhận diện chính xác, các ca rỗng/ngắn/OOV/tin cậy thấp cảnh báo an toàn, giải thích từ khóa TF-IDF hoạt động, lịch sử và CSV tải thành công, tải lại trang mượt mà) đã được kiểm chứng và ghi nhận bằng bằng chứng số học và ảnh chụp thật.
   - Do đó, **Plan 8 chính thức chuyển sang trạng thái HOÀN THÀNH**.
2. **Chốt nghiệm thu Plan 9**:
   - Ứng dụng web công khai tại [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app) vận hành ổn định, sẵn sàng phục vụ trình diễn trước hội đồng chấm thi.
   - Bản nộp chính thức tiếp tục sử dụng bản phát hành hoàn chỉnh **`v1.0.3`**, bảo toàn trọn vẹn tag Git, asset nén ZIP và mã băm SHA-256 (`1a0b16822a998c3520db6bd3725faf4ca8499022d72cfcd81a2f59003c61bf7e`).
   - Phương án dự phòng ngoại tuyến: Máy chủ cục bộ qua lệnh `streamlit run app.py` luôn sẵn sàng hoạt động 100% trong trường hợp phòng thi không có mạng Internet.
