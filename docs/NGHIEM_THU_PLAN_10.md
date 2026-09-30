# Biên bản nghiệm thu sửa lỗi nhập liệu rỗng, định dạng đoạn trích và phát hành bản sửa lỗi - Plan 10

- **Dự án**: Phân loại văn bản bằng Naive Bayes đa thức (Multinomial Naive Bayes)
- **Kho lưu trữ**: [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)
- **Địa chỉ URL website công khai**: [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)
- **Thời điểm nghiệm thu**: 01/10/2026 (00:12:00+07:00)
- **Môi trường nghiệm thu**: Phiên khách độc lập chưa đăng nhập (Unauthenticated guest session) – Trình duyệt Google Chrome headless via Chrome DevTools Protocol
- **Tình trạng xác minh Dashboard**: Do bảng điều khiển Streamlit Cloud yêu cầu tài khoản quản trị sở hữu để truy cập, phiên khách chưa xác minh được commit SHA từ dashboard; việc cập nhật deployment được xác minh thông qua hành vi thực tế và quan sát phản hồi trực tiếp trên website.
- **Kết quả kiểm thử tự động**: 27/27 ca kiểm thử `pytest` đạt 100% (bổ sung bộ kiểm thử hành vi giao diện người dùng và định dạng CSV).
- **Trạng thái Plan 10**: **HOÀN THÀNH TOÀN DIỆN (18/18 ca nghiệm thu Cloud ĐẠT 100%)**

---

## 1. Mục tiêu và kết quả khắc phục hai lỗi tồn đọng

| Lỗi phát hiện từ Plan 9 | Nguyên nhân kỹ thuật | Giải pháp khắc phục trong Plan 10 | Trạng thái sau nghiệm thu Cloud |
| :--- | :--- | :--- | :---: |
| **1. Nối hậu tố `(Rỗng)` vào văn bản $\le 80$ ký tự** | Biểu thức toán tử ba ngôi bị đảo logic trong `app.py`: `clean_input[:80] + ("..." if len(clean_input) > 80 else "(Rỗng)")` dẫn tới mọi chuỗi có độ dài $\le 80$ ký tự đều bị gán `"(Rỗng)"`. | Xây dựng hàm `format_text_preview(text, max_len=80)`: Nếu rỗng/None trả về `(Rỗng)`; nếu dài hơn 80 ký tự lấy 80 ký tự đầu + `...`; nếu $\le 80$ ký tự giữ nguyên văn bản gốc, tuyệt đối không thêm `(Rỗng)`. | **ĐÃ KHẮC PHỤC TRIỆT ĐỂ**<br>(Minh chứng: `space`, `zxqvbnm qqqzxvv` và chuỗi 80 ký tự đều không có `(Rỗng)`). |
| **2. Nhập liệu rỗng/khoảng trắng vẫn phân loại và lưu lịch sử** | Nút bấm "🚀 Phân loại" gọi thẳng `service.classify(clean_input)` mà không kiểm tra chuỗi rỗng trước, dẫn tới việc tính toán xác suất tiên nghiệm và ghi thêm 1 dòng vào lịch sử. | Thêm khối chặn rỗng đầu vào: `clean_input = user_text.strip()`; nếu `not clean_input` thì chỉ hiển thị thông báo `st.warning("⚠️ Vui lòng nhập nội dung văn bản để dự đoán!")`, không gọi `service.classify`, không tạo hộp kết quả và không ghi nhận vào lịch sử. | **ĐÃ KHẮC PHỤC TRIỆT ĐỂ**<br>(Minh chứng: Lịch sử giữ nguyên 0 dòng ở phiên mới và không tăng số dòng khi gửi khoảng trắng). |

---

## 2. Bảng kết quả nghiệm thu chi tiết 18 ca kiểm thử trên Cloud

Tất cả các ca kiểm thử dưới đây được tự động thực thi trên website công khai đang hoạt động tại `https://phan-loai-van-ban-naive-bayes.streamlit.app/` và ghi nhận trạng thái thực tế:

| Mã ca | Hạng mục kiểm thử | Thao tác / Dữ liệu đầu vào | Kết quả mong đợi | Kết quả quan sát thực tế trên Streamlit Cloud | Trạng thái | File bằng chứng |
| :---: | :--- | :--- | :--- | :--- | :---: | :--- |
| **TC-00** | Tải trang ban đầu | Tải URL website trong phiên mới | Giao diện nạp đầy đủ, lịch sử rỗng | Nạp giao diện thành công; hiện thông báo *"Chưa có lượt dự đoán nào trong phiên hiện tại."* | **ĐẠT** | [`tc00_initial_load.png`](evidence/plan-10/tc00_initial_load.png) |
| **TC-01** | Chuỗi rỗng ở phiên mới | Nhập chuỗi rỗng `""` và bấm Phân loại | Hiện cảnh báo, lịch sử 0 dòng, không có hộp kết quả | Xuất hiện cảnh báo *"Vui lòng nhập nội dung văn bản để dự đoán!"*; không gọi dự đoán; lịch sử vẫn 0 dòng. | **ĐẠT** | [`tc01_empty_input.png`](evidence/plan-10/tc01_empty_input.png) |
| **TC-02** | Toàn khoảng trắng ở phiên mới | Nhập `     \t\n   ` và bấm Phân loại | Hiện cảnh báo, lịch sử 0 dòng, không có hộp kết quả | Xuất hiện cảnh báo *"Vui lòng nhập nội dung văn bản để dự đoán!"*; lịch sử vẫn giữ nguyên 0 dòng. | **ĐẠT** | [`tc02_whitespace_input.png`](evidence/plan-10/tc02_whitespace_input.png) |
| **TC-03** | Dự đoán hợp lệ 1 (Đồ họa) | *"The graphics software renders three dimensional images using polygons, textures and computer animation."* | Nhãn: `comp.graphics`<br>Lịch sử tăng lên 1 dòng | Nhãn: **`comp.graphics`**<br>Độ tin cậy: **99.60%**<br>Độ trễ: **21.76 ms**<br>Lịch sử: 1 dòng. | **ĐẠT** | [`tc03_graphics.png`](evidence/plan-10/tc03_graphics.png) |
| **TC-04** | Khoảng trắng sau lượt hợp lệ | Nhập khoảng trắng `"    "` và bấm Phân loại | Hiện cảnh báo, lịch sử KHÔNG tăng (giữ nguyên 1 dòng) | Xuất hiện cảnh báo nhắc nhở; số lượt dự đoán trong lịch sử giữ nguyên **1 dòng**, không thêm lượt rỗng. | **ĐẠT** | [`tc04_whitespace_after_valid.png`](evidence/plan-10/tc04_whitespace_after_valid.png) |
| **TC-05** | Dự đoán hợp lệ 2 (Bóng chày) | *"The baseball pitcher threw the ball and the batter hit a home run during the game."* | Nhãn: `rec.sport.baseball`<br>Lịch sử tăng lên 2 dòng | Nhãn: **`rec.sport.baseball`**<br>Độ tin cậy: **99.87%**<br>Lịch sử ghi nhận: 2 dòng. | **ĐẠT** | [`tc05_baseball.png`](evidence/plan-10/tc05_baseball.png) |
| **TC-06** | Dự đoán hợp lệ 3 (Vũ trụ) | *"NASA launched a spacecraft into orbit to study distant planets and explore the solar system."* | Nhãn: `sci.space`<br>Lịch sử tăng lên 3 dòng | Nhãn: **`sci.space`**<br>Độ tin cậy: **99.44%**<br>Lịch sử ghi nhận: 3 dòng. | **ĐẠT** | [`tc06_space_nasa.png`](evidence/plan-10/tc06_space_nasa.png) |
| **TC-07** | Dự đoán hợp lệ 4 (Chính trị) | *"The government and parliament debated public policy, elections and political reforms."* | Nhãn: `talk.politics.misc`<br>Lịch sử tăng lên 4 dòng | Nhãn: **`talk.politics.misc`**<br>Độ tin cậy: **87.02%**<br>Lịch sử ghi nhận: 4 dòng. | **ĐẠT** | [`tc07_politics.png`](evidence/plan-10/tc07_politics.png) |
| **TC-08** | Văn bản ngắn (`space`) | Nhập từ *"space"* | Nhãn: `sci.space`<br>Đoạn trích đúng `space` (không có `(Rỗng)`) | Nhãn: **`sci.space`** (92.55%); hiện cảnh báo ngữ cảnh ít từ khóa; đoạn trích trong lịch sử là **`space`**, không có `(Rỗng)`. | **ĐẠT** | [`tc08_short_space.png`](evidence/plan-10/tc08_short_space.png) |
| **TC-09** | Từ vựng ngoài từ điển (OOV) | Nhập *"zxqvbnm qqqzxvv"* | Cảnh báo OOV; đoạn trích không có `(Rỗng)` | Hiện cảnh báo OOV và độ tin cậy thấp (26.66%); đoạn trích là **`zxqvbnm qqqzxvv`**, không có hậu tố `(Rỗng)`. | **ĐẠT** | [`tc09_oov.png`](evidence/plan-10/tc09_oov.png) |
| **TC-10** | Độ tin cậy thấp (Pha trộn) | *"baseball game software render satellite government debate"* | Cảnh báo độ tin cậy thấp | Nhãn: `sci.space` (45.56%); hiện banner cảnh báo màu đỏ về mức độ không chắc chắn. Lịch sử: 7 dòng. | **ĐẠT** | [`tc10_low_conf.png`](evidence/plan-10/tc10_low_conf.png) |
| **TC-11** | Giải thích đặc trưng (Explainability) | *"Hubble space telescope orbit astronaut cosmic galaxy exploration"* | Hiển thị bảng đặc trưng từ khóa | Bảng giải thích hiển thị đầy đủ các từ khóa `orbit`, `astronaut`, `telescope`, `exploration` với mức độ ủng hộ rất mạnh. Lịch sử: 8 dòng. | **ĐẠT** | [`tc11_explanations.png`](evidence/plan-10/tc11_explanations.png) |
| **TC-12** | Biên đúng 80 ký tự | *"The space shuttle orbited the planet Earth and deployed scientific instruments!!"* (80 chars) | Đoạn trích giữ nguyên đúng 80 ký tự (không thêm `...`, không thêm `(Rỗng)`) | Đoạn trích trong lịch sử đúng 80 ký tự, không có dấu ba chấm và không có `(Rỗng)`. Lịch sử: 9 dòng. | **ĐẠT** | [`tc12_boundary_80.png`](evidence/plan-10/tc12_boundary_80.png) |
| **TC-13** | Biên đúng 81 ký tự | Chuỗi 80 ký tự trên nối thêm ký tự `"X"` (81 chars) | Đoạn trích lấy 80 ký tự đầu + `...` | Đoạn trích trong lịch sử lấy đúng 80 ký tự đầu và nối `...`. Lịch sử: 10 dòng. | **ĐẠT** | [`tc13_boundary_81.png`](evidence/plan-10/tc13_boundary_81.png) |
| **TC-14** | Đếm độc lập dữ liệu bảng lịch sử | Đếm số dòng của riêng bảng lịch sử phiên | Đúng 10 dòng dữ liệu | Bộ đếm độc lập xác nhận đúng **10 dòng dữ liệu** (`Tổng số lượt dự đoán: 10`), không đếm nhầm các bảng xác suất/giải thích. | **ĐẠT** | [`tc14_history_table.png`](evidence/plan-10/tc14_history_table.png) |
| **TC-15** | Tải và kiểm tra tệp CSV thật | Bấm *"📥 Tải lịch sử dự đoán (CSV)"* và phân tích file tải về | Đúng 10 dòng dữ liệu, cột chuẩn, không có `(Rỗng)` | Tải tệp thành công (`tc15_downloaded_history.csv`). Tệp có đúng 1 dòng header + 10 dòng dữ liệu; khớp hoàn toàn với lịch sử. | **ĐẠT** | [`tc15_downloaded_history.csv`](evidence/plan-10/tc15_downloaded_history.csv) |
| **TC-16** | Xóa lịch sử phiên | Bấm nút *"🗑️ Xóa lịch sử"* | Lịch sử trở về 0 dòng | Bảng lịch sử được xóa sạch, hiển thị thông báo *"Chưa có lượt dự đoán nào trong phiên hiện tại."* | **ĐẠT** | [`tc16_clear_history.png`](evidence/plan-10/tc16_clear_history.png) |
| **TC-17** | Tải lại trang và tái dự đoán | Tải lại trang (F5) và gửi: *"Astronomers observe deep space stellar explosion with radio telescopes."* | Phiên mới hoạt động bình thường, ghi nhận 1 dòng mới | Dự đoán thành công: `sci.space` (93.89%), phiên mới được khởi tạo sạch sẽ với đúng 1 lượt dự đoán. | **ĐẠT** | [`tc17_reload.png`](evidence/plan-10/tc17_reload.png) |

---

## 3. Đối chiếu chi tiết từng dòng trong tệp CSV tải thực tế từ Cloud

Tệp dữ liệu gốc được tải về trực tiếp từ Streamlit Cloud được lưu tại [`docs/evidence/plan-10/tc15_downloaded_history.csv`](evidence/plan-10/tc15_downloaded_history.csv):

```csv
timestamp,text_preview,predicted_class,confidence_percent,in_vocab_tokens,is_uncertain,latency_ms
2026-09-30 17:11:19,"The graphics software renders three dimensional images using polygons, textures ...",comp.graphics,99.6,13,Không,21.76
2026-09-30 17:11:25,The baseball pitcher threw the ball and the batter hit a home run during the gam...,rec.sport.baseball,99.87,12,Không,46.15
2026-09-30 17:11:27,NASA launched a spacecraft into orbit to study distant planets and explore the s...,sci.space,99.44,14,Không,19.22
2026-09-30 17:11:30,"The government and parliament debated public policy, elections and political ref...",talk.politics.misc,87.02,9,Không,21.54
2026-09-30 17:11:32,space,sci.space,92.55,1,Có,29.83
2026-09-30 17:11:35,zxqvbnm qqqzxvv,rec.sport.baseball,26.66,0,Có,18.85
2026-09-30 17:11:38,baseball game software render satellite government debate,sci.space,45.56,7,Có,17.56
2026-09-30 17:11:40,Hubble space telescope orbit astronaut cosmic galaxy exploration,sci.space,99.65,8,Không,22.57
2026-09-30 17:11:43,The space shuttle orbited the planet Earth and deployed scientific instruments!!,sci.space,98.77,10,Không,47.71
2026-09-30 17:11:45,The space shuttle orbited the planet Earth and deployed scientific instruments!!...,sci.space,98.77,10,Không,29.58
```

### Bảng phân tích đối chiếu từng dòng CSV:
1. **Dòng 1 (`comp.graphics`)**: Chuỗi dài $\ge 80$ ký tự được rút gọn 80 ký tự + `...`.
2. **Dòng 2 (`rec.sport.baseball`)**: Chuỗi dài $\ge 80$ ký tự được rút gọn 80 ký tự + `...`.
3. **Dòng 3 (`sci.space`)**: Chuỗi dài $\ge 80$ ký tự được rút gọn 80 ký tự + `...`.
4. **Dòng 4 (`talk.politics.misc`)**: Chuỗi dài $\ge 80$ ký tự được rút gọn 80 ký tự + `...`.
5. **Dòng 5 (`space`)**: Chuỗi ngắn 5 ký tự hiển thị đúng nguyên văn `space`, **hoàn toàn không có hậu tố `(Rỗng)`**.
6. **Dòng 6 (`zxqvbnm qqqzxvv`)**: Chuỗi OOV 15 ký tự hiển thị đúng nguyên văn `zxqvbnm qqqzxvv`, **hoàn toàn không có hậu tố `(Rỗng)`**.
7. **Dòng 7 (`baseball game...`)**: Chuỗi 57 ký tự hiển thị đúng nguyên văn không có hậu tố lạ.
8. **Dòng 8 (`Hubble space...`)**: Chuỗi 63 ký tự hiển thị đúng nguyên văn.
9. **Dòng 9 (Biên 80 ký tự)**: Đúng 80 ký tự, không có dấu ba chấm và không có `(Rỗng)`.
10. **Dòng 10 (Biên 81 ký tự)**: Đúng 80 ký tự đầu kết hợp `...`.
- **Tổng số dòng dữ liệu**: Đúng 10 dòng (khớp 100% với 10 lượt phân loại hợp lệ; 2 lượt rỗng và khoảng trắng bị chặn hoàn toàn, không lọt vào CSV).

---

## 4. Bảo toàn số liệu mô hình và tham số thực nghiệm

Toàn bộ thông số huấn luyện và số liệu thực nghiệm được bảo tồn nguyên vẹn theo đúng cam kết:
- **Tập dữ liệu**: 4 nhóm tin 20 Newsgroups (2.239 mẫu train, 1.490 mẫu test).
- **Bộ từ vựng TF-IDF**: `13.068` đặc trưng (học độc quyền trên train set, không rò rỉ dữ liệu).
- **Mô hình**: Multinomial Naive Bayes (`alpha = 0.1`).
- **Chỉ số kiểm chứng chéo (5-Fold CV)**:
  - Baseline (`alpha = 1.0`): Macro F1 = **88.55%**
  - Tối ưu (`alpha = 0.1`): Macro F1 = **90.28%**
- **Hiệu năng trên tập kiểm thử độc lập (Test Set)**:
  - Accuracy: **88.52%**
  - Macro F1: **88.33%**
  - Weighted F1: **88.49%**
  - Precision: **88.41%**
  - Recall: **88.35%**

---

## 5. Kết luận nghiệm thu Plan 10 & Chú thích hậu kiểm

1. **Khắc phục triệt để hành vi:** Hai lỗi phát hiện từ Plan 9 (nhập liệu rỗng và hậu tố `(Rỗng)` trong đoạn trích) đã được sửa triệt để cả ở mã nguồn cục bộ và hệ thống triển khai thực tế trên Streamlit Cloud (18/18 ca kiểm thử đạt 100%).
2. **Kiểm thử tự động:** 27/27 kiểm thử tự động đạt 100%, bao gồm kiểm thử hồi quy hành vi người dùng (`tests/test_ui_behavior.py`) và xuất CSV.
3. **Bằng chứng nghiệm thu:** Toàn bộ bằng chứng ảnh chụp, file JSON báo cáo và file CSV tải thực tế đã được lưu trữ có thể kiểm chứng tại thư mục [`docs/evidence/plan-10/`](evidence/plan-10/).
4. **Phát hành chính thức v1.0.4:** Bản phát hành chính thức [`v1.0.4`](https://github.com/thinh204/phan-loai-van-ban-naive-bayes/releases/tag/v1.0.4) đã được xuất bản thành công trên GitHub Release (Release ID: `400276283`) với 3 tài sản đính kèm (`phan-loai-van-ban-naive-bayes-final-submission.zip`, `MANIFEST.json`, `CHECKSUMS.sha256`). Mã băm SHA-256 tải về khớp tuyệt đối: `189918bdc3acaca2bc1e19f22ff370f475ad260b7b9b219ff9fe9ceb3a20d975`.

> [!NOTE]
> **Đính chính và chú thích về ảnh `tc18_post_release_v1_0_4.png`:**
> - Ảnh chụp `tc18_post_release_v1_0_4.png` ghi nhận việc kiểm thử hành vi sau sửa lỗi (đầu vào rỗng hiển thị cảnh báo và không sinh dòng lịch sử mới, đầu vào hợp lệ suy diễn ra `sci.space` 93,80% trong 14,77 ms và sinh đúng 1 dòng lịch sử).
> - Tuy nhiên, do tiến trình container Python trên Streamlit Cloud lúc đó chưa được khởi động lại (Reboot) nên `sys.modules['src.config']` trong bộ nhớ vẫn giữ giá trị chuỗi phiên bản cũ `v1.0.3` thay vì nạp lại từ tệp `src/config.py` mới của commit phát hành `14e88a2`. Do đó, ảnh `tc18_post_release_v1_0_4.png` là bằng chứng về **hành vi đã sửa**, không phải bằng chứng về **chuỗi phiên bản hiển thị v1.0.4**.
> - Việc xác minh nghiêm ngặt phiên bản hiển thị `v1.0.4` trên Sidebar và Footer được bàn giao sang **Plan 11** tại [`docs/HAU_KIEM_V1.0.4.md`](HAU_KIEM_V1.0.4.md) cùng thư mục bằng chứng độc lập [`docs/evidence/plan-11/`](evidence/plan-11/).
