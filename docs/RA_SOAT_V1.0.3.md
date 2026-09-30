# Biên bản rà soát và bảo toàn trạng thái phát hành v1.0.3

- **Học phần**: Trí tuệ nhân tạo (AI)
- **Đề tài**: Phân loại văn bản đa lớp bằng Multinomial Naive Bayes
- **Repository**: [thinh204/phan-loai-van-ban-naive-bayes](https://github.com/thinh204/phan-loai-van-ban-naive-bayes)
- **Thời điểm rà soát**: 30/09/2026
- **Mục tiêu**: Bảo toàn toàn bộ các thay đổi kỹ thuật của Plan 6 đang có trong working tree, không reset/checkout/xóa tệp, chuẩn bị hoàn tất phát hành phiên bản `v1.0.3`.

---

## 1. Bảng kiểm kê chi tiết các tệp đang thay đổi trong working tree

| STT | Tệp tin | Nhóm chức năng | Trạng thái Git | Mô tả nội dung thay đổi |
| :---: | :--- | :--- | :---: | :--- |
| **1** | `src/config.py` | Cấu hình phiên bản | Đã sửa (Modified) | Đồng bộ `APP_VERSION = "v1.0.3"`, `PLAN_VERSION = "Plan 6"`, `RELEASE_VERSION = "v1.0.3"`. |
| **2** | `scripts/build_package.py` | Tự động hóa đóng gói | Đã sửa (Modified) | Bổ sung thư mục `scripts` vào `ALLOWED_DIRS` (tổng 55 tệp tin đóng gói). |
| **3** | `scripts/verify_clean_package.py` | Kiểm thử môi trường sạch | Đã sửa (Modified) | Tạo `python -m venv` mới cô lập, cài `requirements.txt`, phân tích kết quả pytest động. |
| **4** | `tests/test_release_consistency.py` | Kiểm thử nhất quán CI | Đã sửa (Modified) | Kiểm tra số liệu CV F1 (88,55% và 90,28%) không chứa số liệu cũ, hỗ trợ môi trường giải nén. |
| **5** | `docs/CLEAN_ENV_TEST.md` | Tài liệu nghiệm thu | Đã sửa (Modified) | Biên bản ghi nhận chạy thành công 20 kiểm thử trong môi trường ảo mới độc lập. |
| **6** | `release/MANIFEST.json` | Kiểm kê gói phát hành | Đã sửa (Modified) | Cập nhật danh sách 55 tệp tin và kích thước chi tiết. |
| **7** | `release/CHECKSUMS.sha256` | Mã băm toàn vẹn | Đã sửa (Modified) | Cập nhật mã băm SHA-256 tương ứng của 55 tệp tin và gói ZIP. |
| **8** | `release/phan-loai-van-ban-naive-bayes-final-submission.zip` | Gói nén bài nộp | Đã sửa (Modified) | Gói nén chuẩn 55 tệp (692.511 bytes), không chứa cache, `.venv` hay tệp rác. |
| **9** | `docs/RELEASE_NOTES_v1.0.3.md` | Ghi chú phát hành | Chưa theo dõi (Untracked) | Bản ghi chú chi tiết cho bản phát hành khóa nộp cuối `v1.0.3`. |

---

## 2. Kết quả kiểm tra tính toàn vẹn hiện tại

1. **Kiểm tra cú pháp (`compileall`)**:
   - Lệnh: `python -m compileall -q app.py src tests scripts`
   - Trạng thái: Hợp lệ 100% (Returncode 0).
2. **Kiểm tra bộ kiểm thử tự động (`pytest`)**:
   - Lệnh: `pytest -v`
   - Trạng thái: **21/21 bài kiểm thử ĐẠT (100% PASSED)**.
3. **Kiểm tra đóng gói & môi trường ảo sạch (`verify_clean_package.py`)**:
   - Trạng thái: **PASSED (20 passed trong venv cô lập, suy diễn `sci.space` 99,96%)**.

---

## 3. Kế hoạch hoàn tất các giai đoạn tiếp theo (Plan 7)

- **Giai đoạn 2 & 3**: Chẩn đoán và khôi phục website Streamlit Community Cloud công khai; kiểm tra URL trực tuyến.
- **Giai đoạn 4**: Nghiệm thu các ca sử dụng trực tiếp trên website công khai từ phiên ẩn danh.
- **Giai đoạn 5 & 6**: Hoàn tất commit, tái tạo tài sản ZIP, manifest và checksum đồng bộ 100%.
- **Giai đoạn 7 & 8**: Đẩy lên GitHub, xác nhận CI xanh, tạo tag `v1.0.3`, xuất bản GitHub Release và hậu kiểm.
