# Cách chạy thực nghiệm

Yêu cầu Python 3.10 trở lên và kết nối mạng ở lần chạy đầu để tải 20 Newsgroups. Dữ liệu tải về được lưu trong `data/cache` và không đưa lên Git.

Trong thư mục gốc của repo:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python src\run_experiment.py
```

Lệnh cuối in số mẫu và hai chỉ số tổng quan. Tệp `results/metrics.json` chứa phiên bản thư viện, tham số, số mẫu, báo cáo theo lớp và ma trận nhầm lẫn. Các tệp `confusion_*.csv` và `errors_*.json` dùng để kiểm tra kết quả và phân tích lỗi. Chạy lại mã sẽ ghi đè các tệp kết quả theo cùng thiết lập.

Hai pipeline đều dùng MNB với `alpha=1`. Khác biệt duy nhất giữa hai lần chạy là `CountVectorizer` và `TfidfVectorizer`. Bộ từ vựng được học từ train thông qua `Pipeline.fit`; trên test, `Pipeline.predict` chỉ biến đổi rồi dự đoán. Không chọn tham số theo điểm test.

Nếu dữ liệu đã có trong cache, có thể chạy lại không cần mạng. Nếu muốn giữ kết quả thử nghiệm riêng, dùng `--output-dir` trỏ đến thư mục khác.
