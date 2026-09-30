# Phiên bản phát hành v1.0.1 – Nghiệm thu, triển khai chính thức và đóng gói bài nộp

**Ngày phát hành:** 30/09/2026  
**Repository:** [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)  
**Phiên bản:** `v1.0.1` (Kế thừa và hoàn thiện từ `v1.0.0`)  
**Commit nghiệm thu:** Nhánh `main`

---

## 1. Giới thiệu tổng quan

Phiên bản **v1.0.1** đánh dấu sự hoàn thiện trọn vẹn của đề tài môn Trí tuệ nhân tạo (AI): *Phân loại văn bản đa lớp bằng Multinomial Naive Bayes*. Phiên bản này đóng gói toàn bộ thành quả từ **Plan 1 đến Plan 4**, sẵn sàng 100% cho buổi bảo vệ đề tài trước hội đồng giảng viên và nộp bài chính thức.

---

## 2. Các điểm nổi bật và cải tiến trong v1.0.1

### 1. Đồng bộ mã nguồn và xác minh CI tự động
- Thiết lập quy trình **Continuous Integration (CI)** trên GitHub Actions qua tệp `.github/workflows/ci.yml`.
- Xác minh chạy thành công tự động trên cả hai môi trường **Python 3.10** và **Python 3.11** trên Ubuntu.
- Lưu trữ đầy đủ bằng chứng kiểm thử tại [docs/CI_VERIFICATION.md](CI_VERIFICATION.md).

### 2. Triển khai ứng dụng trực tuyến
- Ứng dụng Streamlit được triển khai chính thức trên nền tảng **Streamlit Community Cloud** tại địa chỉ:  
  👉 **[https://phan-loai-van-ban-naive-bayes.streamlit.app](https://phan-loai-van-ban-naive-bayes.streamlit.app)**
- Hỗ trợ đầy đủ phương án chạy ngoại tuyến độc lập (`streamlit run app.py` trên cổng 8501) cho môi trường không có kết nối mạng.

### 3. Nghiệm thu toàn bộ luồng chức năng (Plan 4)
- Thực hiện nghiệm thu thực tế 11 ca kiểm thử chức năng (TC01 đến TC11) đạt kết quả **100% ĐẠT**:
  - Dự đoán chính xác 4 chủ đề: `comp.graphics`, `rec.sport.baseball`, `sci.space`, `talk.politics.misc`.
  - Xử lý an toàn chuỗi rỗng và khoảng trắng (trả về xác suất tiên nghiệm và cảnh báo an toàn).
  - Cảnh báo văn bản quá ngắn và cảnh báo từ vựng ngoài từ điển (OOV).
  - Cảnh báo độ tin cậy thấp (< 60%) cho các văn bản mơ hồ.
  - Trích xuất top từ khóa giải thích theo mức đóng góp biên log-odds.
  - Xuất toàn bộ bảng lịch sử phân loại trong phiên ra tệp CSV.
- Biên bản nghiệm thu chi tiết được lập tại [docs/NGHIEM_THU.md](NGHIEM_THU.md).

### 4. Đồng bộ hệ thống tài liệu và số liệu thực nghiệm
- Đồng bộ toàn bộ README, báo cáo khoa học, kịch bản thuyết trình và hướng dẫn thực thi:
  - Cập nhật số lượng kiểm thử tự động chính xác là **16 test cases** (`pytest -v`).
  - Đối chiếu số liệu thực nghiệm gốc từ `results/evaluation_summary.json`:
    - Mô hình: `MultinomialNB(alpha=0.1)`
    - Tập kiểm thử: 1.490 mẫu test (sau khi học 2.239 mẫu train)
    - Test Accuracy: **88,52%** (+1,34% so với mô hình cơ sở)
    - Macro F1: **88,33%** (+1,46% so với mô hình cơ sở)
    - Weighted F1: **88,49%**

### 5. Rà soát hoàn thiện Slide thuyết trình PowerPoint
- Cập nhật tệp slide bảo vệ [`presentation/phan-loai-van-ban-naive-bayes-v2.pptx`](../presentation/phan-loai-van-ban-naive-bayes-v2.pptx):
  - Slide 7: Quy trình Stratified 5-Fold Cross-Validation chọn `alpha=0.1` trên tập train.
  - Slide 8: Biểu đồ kết quả trực quan so sánh mô hình cơ sở (`alpha=1.0`) và mô hình tối ưu (`alpha=0.1`).
  - Slide 10: Khẳng định 16 kiểm thử tự động, CI Pipeline xanh, tính năng giải thích và web demo.
  - Toàn bộ speaker notes được rà soát đồng bộ với kịch bản bảo vệ [docs/thuyet-trinh.md](thuyet-trinh.md).

### 6. Đóng gói bài nộp chính thức
- Lập bảng checklist hồ sơ đầy đủ tại [docs/CHECKLIST_NOP_BAI.md](CHECKLIST_NOP_BAI.md).
- Tạo tệp lưu trữ nén sẵn sàng nộp lên LMS: `release/phan-loai-van-ban-naive-bayes-final-submission.zip` (655 KB).

---

## 3. Danh mục tệp bàn giao chính

- **Mã nguồn ứng dụng**: `app.py`, `src/classifier_service.py`, `src/config.py`
- **Mô hình nạp sẵn**: `models/naive_bayes_model.joblib`, `models/tfidf_vectorizer.joblib`
- **Kết quả thực nghiệm**: `results/evaluation_summary.json`, `results/alpha_tuning.json`, `results/error_analysis.json`
- **Slide thuyết trình**: `presentation/phan-loai-van-ban-naive-bayes-v2.pptx`
- **Gói nộp bài**: `release/phan-loai-van-ban-naive-bayes-final-submission.zip`
- **Báo cáo & Hướng dẫn**: `docs/bao-cao.md`, `docs/thuyet-trinh.md`, `docs/DEMO_SCRIPT.md`, `docs/DEFENSE_QA.md`, `docs/NGHIEM_THU.md`, `docs/CI_VERIFICATION.md`

---

## 4. Hướng dẫn cài đặt nhanh

```powershell
# Clone repository
git clone https://github.com/thinh204/phan-loai-van-ban-naive-bayes.git
cd phan-loai-van-ban-naive-bayes

# Cài đặt môi trường
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Chạy kiểm thử tự động (16 passed)
pytest -v

# Khởi chạy giao diện web
streamlit run app.py
```
