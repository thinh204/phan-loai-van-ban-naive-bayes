# Biên bản nghiệm thu toàn bộ luồng chức năng (Plan 4)

- **Dự án**: Hệ thống phân loại văn bản đa lớp Multinomial Naive Bayes
- **Repository**: `thinh204/phan-loai-van-ban-naive-bayes`
- **Mô hình nghiệm thu**: `MultinomialNB(alpha=0.1)` kết hợp `TfidfVectorizer` (13.068 đặc trưng)
- **Thời gian nghiệm thu**: 30/09/2026
- **Môi trường thực thi**: Python 3.10.11 / Streamlit 1.40.0 / Scikit-learn 1.7.2

---

## 1. Bảng tổng hợp kết quả nghiệm thu chức năng

| Mã TC | Hạng mục kiểm thử | Dữ liệu đầu vào thực tế | Dự đoán / Phản hồi | Độ tin cậy | Cảnh báo UX / Chẩn đoán | Kết quả |
| :---: | :--- | :--- | :--- | :---: | :--- | :---: |
| **TC01** | Dự đoán lớp `comp.graphics` | `3D polygon mesh rendering rasterization shader graphics card opengl directx...` | `comp.graphics` (Đồ họa máy tính) | 99,92% | Không phát sinh cảnh báo | **ĐẠT** |
| **TC02** | Dự đoán lớp `rec.sport.baseball` | `The pitcher threw a curveball for a strikeout in the ninth inning of the baseball championship game...` | `rec.sport.baseball` (Thể thao - Bóng chày) | 99,93% | Không phát sinh cảnh báo | **ĐẠT** |
| **TC03** | Dự đoán lớp `sci.space` | `NASA space shuttle telescope astronaut orbit mars mission satellite planetary astronomy lunar launch` | `sci.space` (Khoa học vũ trụ) | 100,00% | Không phát sinh cảnh báo | **ĐẠT** |
| **TC04** | Dự đoán lớp `talk.politics.misc` | `The president signed the federal bill passed by Congress regarding political elections...` | `talk.politics.misc` (Chính trị tổng hợp) | 97,48% | Không phát sinh cảnh báo | **ĐẠT** |
| **TC05** | Xử lý văn bản rỗng | Chuỗi rỗng `""` | `rec.sport.baseball` | 26,66% | Cảnh báo lỗi `empty`: Văn bản rỗng, trả về xác suất tiên nghiệm | **ĐẠT** |
| **TC06** | Xử lý ký tự trắng/ngắt dòng | Chuỗi `"   \t\n   "` | `rec.sport.baseball` | 26,66% | Cảnh báo lỗi `empty`: Loại bỏ whitespace và báo rỗng an toàn | **ĐẠT** |
| **TC07** | Cảnh báo văn bản ngắn / ít từ | `"space launch"` (2 từ, < 15 ký tự) | `sci.space` | 97,91% | Cảnh báo thông tin `few_vocab`: Rất ít từ khóa đặc trưng | **ĐẠT** |
| **TC08** | Cảnh báo từ ngoài từ điển (OOV) | `"xyzzyflurble qwertyquux zzzopblargh unkunkunk"` | `rec.sport.baseball` | 26,66% | Cảnh báo `no_vocab` + `low_confidence`: Không có từ khóa trong từ điển | **ĐẠT** |
| **TC09** | Cảnh báo độ tin cậy thấp (< 60%) | `"the project report was updated with common information on new development"` | `sci.space` | 56,53% | Cảnh báo `low_confidence`: Độ tin cậy 56,53% < 60% ngưỡng cảnh báo | **ĐẠT** |
| **TC10** | Trích xuất từ khóa giải thích | `"Hubble telescope captured deep space galaxy images of planetary nebula"` | `sci.space` | 97,49% | Trích xuất top từ: `hubble` (0,410), `telescope` (0,357), `planetary` (0,344) | **ĐẠT** |
| **TC11** | Xuất báo cáo lịch sử định dạng CSV | Bảng lịch sử phiên gồm 10 dự đoán | Tệp CSV mã hóa UTF-8, 6 cột chuẩn | 100% | Tải tệp thành công, dung lượng 1.410 bytes | **ĐẠT** |

---

## 2. Chi tiết phân tích các ca kiểm thử điển hình

### 2.1. Kiểm thử phân loại 4 chủ đề chính (TC01 - TC04)
- **Độ chính xác**: 4/4 văn bản đại diện cho từng chủ đề đều được mô hình nhận diện chính xác tuyệt đối với độ tin cậy rất cao từ 97,48% đến 100,00%.
- **Thời gian đáp ứng**: Thời gian suy diễn (latency) dao động từ 12,99ms đến 17,67ms, hoàn toàn đáp ứng tiêu chuẩn phản hồi thời gian thực trên giao diện web.

### 2.2. Kiểm thử an toàn đầu vào và trường hợp biên (TC05 - TC08)
- Khi người dùng bấm phân loại mà không nhập nội dung (hoặc chỉ gõ phím cách/Enter), hệ thống không bị crash (`IndexError` hay `ValueError`) mà kích hoạt cảnh báo `empty`, giải thích rõ cho người dùng rằng kết quả chỉ là xác suất tiên nghiệm của tập huấn luyện.
- Với trường hợp từ vựng hoàn toàn mới (OOV), vector TF-IDF toàn bộ là số 0; hệ thống bắt chính xác trạng thái `no_vocab` và hiển thị cảnh báo từ vựng ngoài từ điển cùng cảnh báo độ tin cậy thấp.

### 2.3. Kiểm thử cơ chế cảnh báo độ tin cậy thấp (TC09)
- Với văn bản mơ hồ chứa nhiều từ thông dụng không thuộc lĩnh vực đặc thù (`"the project report was updated with common information..."`), xác suất cao nhất chỉ đạt **56,53%** (dưới ngưỡng 60%).
- Hệ thống tự động kích hoạt khung cảnh báo màu vàng: `Độ tin cậy thấp (< 60%)`, thông báo rõ cho người dùng kết quả có sự phân vân giữa các lớp.

### 2.4. Kiểm thử tính giải thích được (Explainability - TC10)
- Đối với câu `"Hubble telescope captured deep space galaxy images of planetary nebula"`, hệ thống trích xuất danh sách đặc trưng đóng góp theo công thức biên log-odds:
  - `hubble`: TF-IDF = 0,410 | Mức đóng góp: Rất mạnh
  - `telescope`: TF-IDF = 0,357 | Mức đóng góp: Rất mạnh
  - `planetary`: TF-IDF = 0,344 | Mức đóng góp: Rất mạnh
- Kèm disclaimer khoa học nêu rõ: Đây là mức đóng góp theo giả định độc lập có điều kiện của Naive Bayes, không phải bằng chứng nhân quả thực tế.

### 2.5. Kiểm thử trích xuất dữ liệu lịch sử CSV (TC11)
- Lịch sử phân loại trong phiên được lưu vết đầy đủ với 6 trường thông tin: `Thời điểm`, `Văn bản xem trước`, `Nhãn dự đoán (Anh)`, `Nhãn dự đoán (Việt)`, `Độ tin cậy (%)`, `Cảnh báo`.
- Dữ liệu xuất ra file CSV hợp lệ, hỗ trợ tiếng Việt có dấu qua mã hóa UTF-8.

---

## 3. Kết luận nghiệm thu

Hệ thống đã vượt qua toàn bộ **11/11 ca kiểm thử nghiệm thu chức năng**, kết hợp với **16/16 ca kiểm thử tự động pytest**, đảm bảo ứng dụng vận hành an toàn, chính xác và minh bạch trước khi đưa vào báo cáo và trình chiếu bảo vệ đề tài.
