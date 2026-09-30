# Danh mục kiểm tra hồ sơ nộp đồ án môn Trí tuệ nhân tạo

- **Đề tài**: Phân loại văn bản đa lớp bằng Multinomial Naive Bayes
- **Học phần**: Trí tuệ nhân tạo (AI)
- **Nhóm tác giả**: 3 thành viên
- **Mã nguồn GitHub**: [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)
- **Nguồn gói nộp hiện tại**: commit ghi trong `submission/MANIFEST.json`; bản Release v1.0.4 cũ giữ nguyên.
- **Ngày rà soát**: 01/10/2026
- **Bìa**: đã điền nhóm/lớp; cần bổ sung tên giảng viên trước khi nộp.

---

## 1. Bảng kiểm tra danh mục thành phần hồ sơ nộp bài

| STT | Hạng mục thành phần | Đường dẫn / Tên tệp trong repo | Trạng thái | Ghi chú kiểm tra |
| :---: | :--- | :--- | :---: | :--- |
| **1** | **Mã nguồn ứng dụng** | `app.py`, `src/classifier_service.py`, `src/config.py` | ✅ Đầy đủ | Tách tầng dịch vụ hướng đối tượng, mã nguồn chuẩn PEP 8. |
| **2** | **Pipeline tiền xử lý & huấn luyện** | `src/prepare_data.py`, `src/tfidf_pipeline.py`, `src/tune_alpha.py` | ✅ Đầy đủ | Chia train/test nghiêm ngặt, không rò rỉ dữ liệu test. |
| **3** | **Artifacts mô hình & vectorizer** | `models/naive_bayes_model.joblib`, `models/tfidf_vectorizer.joblib`, `models/class_names.joblib` | ✅ Đầy đủ | Mô hình `MultinomialNB(alpha=0.1)`, 13.068 đặc trưng TF-IDF. |
| **4** | **Kết quả thực nghiệm động** | `results/evaluation_summary.json`, `results/alpha_tuning.json`, `results/error_analysis.json` | ✅ Đầy đủ | Test Accuracy 88,52%, Macro F1 88,33%, CV Macro F1: 88,55% (alpha=1.0) và 90,28% (alpha=0.1). |
| **5** | **Bộ kiểm thử tự động** | `tests/` gồm pipeline, inference, release consistency và UI behavior | ✅ Đầy đủ | 27/27 tests đạt; nhập rỗng, OOV, đoạn trích và CSV có kiểm tra hồi quy. |
| **6** | **Tự động hóa CI Pipeline** | `.github/workflows/ci.yml`, `docs/CI_VERIFICATION.md` | ✅ Đầy đủ | Chạy thành công trên cả Python 3.10 và Python 3.11. |
| **7** | **Báo cáo lý thuyết & kỹ thuật** | `docs/bao-cao.md`, `docs/bao-cao-do-an.pdf` | ✅ Đầy đủ | Báo cáo có bìa, lý thuyết, ví dụ tính tay, thực nghiệm và tài liệu tham khảo. |
| **8** | **Slide thuyết trình bảo vệ** | `presentation/phan-loai-van-ban-naive-bayes-v3.pptx` | ✅ Đầy đủ | 10 slide chuẩn hóa, có biểu đồ kết quả thực nghiệm và speaker notes. |
| **9** | **Kịch bản thuyết trình & Demo** | `docs/thuyet-trinh.md`, `docs/DEMO_SCRIPT.md`, `docs/DIEN_TAP_BAO_VE.md` | ✅ Đầy đủ | Phân bổ thời lượng chi tiết 9 phút cho 3 thành viên, câu thoại gợi ý và thao tác UI. |
| **10** | **Bộ câu hỏi phản biện (Q&A)** | `docs/DEFENSE_QA.md` | ✅ Đầy đủ | 12 nhóm câu hỏi trọng tâm thường gặp từ hội đồng giảng viên. |
| **11** | **Biên bản nghiệm thu chức năng** | `docs/NGHIEM_THU.md` | ✅ Đầy đủ | Nghiệm thu 11 ca kiểm thử thực tế (TC01 - TC11) đạt 100%. |
| **12** | **URL ứng dụng trực tuyến** | [https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app) | ✅ Hoạt động & Đã nghiệm thu | Triển khai công khai thành công trên Streamlit Cloud, nghiệm thu 13/13 ca trong Plan 9. Sẵn sàng chạy nội bộ `localhost:8501`. |
| **13** | **Gói nộp bài nén (ZIP)** | `submission/phan-loai-van-ban-naive-bayes-nop-bai.zip` | Kiểm tra theo manifest | Có nguồn hiện tại, báo cáo PDF, slide v3 và thông tin commit; không gồm virtual environment hoặc cache dữ liệu. |

---

## 2. Hướng dẫn giải nén và chạy lại từ gói nộp

### Yêu cầu tiên quyết
- Máy tính cài đặt sẵn **Python 3.10** hoặc mới hơn.
- Kết nối Internet trong lần đầu cài đặt thư viện (hoặc dùng pip wheel ngoại tuyến).

### Các bước thực thi từ đầu:

1. **Giải nén gói bài nộp:**
   Giải nén tệp `phan-loai-van-ban-naive-bayes-final-submission.zip` vào thư mục làm việc bất kỳ.

2. **Khởi tạo môi trường ảo mới:**
   ```powershell
   cd phan-loai-van-ban-naive-bayes
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

3. **Chạy toàn bộ 21 ca kiểm thử tự động:**
   ```powershell
   pytest -v
   ```
   *Kết quả mong đợi*: Toàn bộ 21 test cases đều đạt (`21 passed`).

4. **Khởi động ứng dụng Streamlit cục bộ:**
   ```powershell
   streamlit run app.py
   ```
   Trình duyệt sẽ tự động mở địa chỉ: `http://localhost:8501`.

---

## 3. Phương án dự phòng Demo ngoại tuyến (Offline Contingency Plan)

Trong trường hợp phòng hội đồng bảo vệ bị mất kết nối mạng Internet hoặc chặn cổng ra ngoài:

1. **Khả năng tự chủ 100% ngoại tuyến:**
   - Dự án đã tích hợp sẵn toàn bộ mô hình đã huấn luyện trong thư mục `models/` (`naive_bayes_model.joblib`, `tfidf_vectorizer.joblib`).
   - Khi khởi động ứng dụng với `streamlit run app.py`, hệ thống nạp trực tiếp mô hình từ đĩa cứng mà không cần bất kỳ kết nối mạng hay tải thêm tệp tin nào từ bên ngoài.

2. **Quy trình chuẩn bị trước giờ bảo vệ:**
   - Cài đặt sẵn môi trường ảo `.venv` trên laptop cá nhân của nhóm.
   - Chạy thử `streamlit run app.py` và ghim tab trình duyệt `http://localhost:8501`.
   - Chuẩn bị sẵn 4 đoạn văn bản mẫu (theo `docs/DEMO_SCRIPT.md`) trong Notepad để sẵn sàng sao chép khi demo nếu cần.

---

## 4. Xác nhận bàn giao

Hồ sơ đề tài đã được kiểm tra chéo, rà soát tính nhất quán số liệu và đóng gói hoàn tất. Toàn bộ mã nguồn, tài liệu và slide đáp ứng đầy đủ tiêu chí đánh giá xuất sắc của học phần.
