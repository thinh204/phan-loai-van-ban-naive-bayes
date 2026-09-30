# Kế hoạch thực hiện đề tài

## Mục tiêu và phạm vi

Nghiên cứu một phương pháp phân loại văn bản: **Multinomial Naive Bayes**. Minh họa cách biến văn bản thành đặc trưng số, cách mô hình tính điểm từng lớp, và cách đánh giá trên dữ liệu chưa thấy khi huấn luyện. Phần trình bày bằng tiếng Việt; dữ liệu thực nghiệm bằng tiếng Anh để dùng bộ dữ liệu chuẩn, có thể tải và chạy lại.

Chọn bốn chủ đề trong 20 Newsgroups: `comp.graphics`, `rec.sport.baseball`, `sci.space`, `talk.politics.misc`. Đây là bài toán phân loại nhiều lớp, đủ khác biệt để giải thích và đủ giao thoa để phân tích lỗi.

## Các giai đoạn và điều kiện hoàn thành

| Giai đoạn | Công việc | Sản phẩm kiểm tra được | Commit |
| --- | --- | --- | --- |
| 1. Đề cương | Chốt bài toán, dữ liệu, vai trò và tiêu chí đánh giá | README, kế hoạch | `docs: lập kế hoạch đề tài và phân công nhóm` |
| 2. Nghiên cứu | Giải thích Bayes, giả định độc lập, làm trơn Laplace, biểu diễn Bag of Words và TF-IDF; ví dụ tính tay | Báo cáo lý thuyết, nguồn tham khảo | `docs: hoàn thành cơ sở lý thuyết Naive Bayes` |
| 3. Thực nghiệm | Viết mã tải dữ liệu, huấn luyện, dự đoán và xuất kết quả | Mã Python, hướng dẫn chạy, tệp phụ thuộc | `feat: xây dựng thực nghiệm phân loại văn bản` |
| 4. Đánh giá | Chạy thực nghiệm và phân tích accuracy, precision, recall, F1, nhầm lẫn giữa lớp và ví dụ sai | Kết quả có số liệu thật | `results: ghi kết quả và phân tích lỗi` |
| 5. Trình bày | Tóm lược lý thuyết và kết quả thành bài trình bày 8–10 slide | Nội dung thuyết trình và ghi chú người nói | `docs: hoàn thiện nội dung thuyết trình` |

## Phân công đề xuất cho 3 thành viên

| Vai trò | Trách nhiệm | Điểm cần tự kiểm tra |
| --- | --- | --- |
| Thành viên 1, điều phối | Chốt phạm vi, rà báo cáo, ghép bài trình bày | Mục tiêu, thuật ngữ và số liệu nhất quán |
| Thành viên 2, lý thuyết | Công thức, ví dụ tính tay, nguồn tài liệu | Có giải thích được giả định độc lập và làm trơn |
| Thành viên 3, thực nghiệm | Mã, cách chạy, bảng kết quả và lỗi dự đoán | Chạy lại được, không rò rỉ dữ liệu test |

Các thành viên có thể đổi vai trò theo thế mạnh. Mỗi người cần đọc toàn bộ bài để trả lời câu hỏi khi thuyết trình.

## Quy ước làm việc

1. Mỗi giai đoạn có một commit nêu rõ việc đã làm và kết quả kiểm tra.
2. Số liệu trong báo cáo và slide phải khớp với tệp kết quả sinh từ mã.
3. Nêu giới hạn: dữ liệu tiếng Anh, bốn chủ đề, và việc loại metadata chỉ là phương pháp giảm rò rỉ theo heuristic.
4. Không đưa dữ liệu gốc hoặc bộ nhớ đệm tải về vào Git; chỉ lưu mã và các kết quả tổng hợp cần kiểm chứng.

## Nguồn khởi đầu

- [20 Newsgroups trong scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html)
- [Hướng dẫn Naive Bayes của scikit-learn](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [Ví dụ phân loại tài liệu của scikit-learn](https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html)
