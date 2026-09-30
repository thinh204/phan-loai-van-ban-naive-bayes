# Báo cáo: Phân loại văn bản bằng Multinomial Naive Bayes

## 1. Bài toán

Phân loại văn bản là gán một nhãn trong tập lớp đã biết cho một tài liệu mới. Trong đề tài này, đầu vào là nội dung một bài đăng tiếng Anh; đầu ra là một trong bốn chủ đề: đồ họa máy tính (`comp.graphics`), bóng chày (`rec.sport.baseball`), không gian (`sci.space`) hoặc chính trị tổng hợp (`talk.politics.misc`). Nhóm sử dụng bộ dữ liệu 20 Newsgroups qua `fetch_20newsgroups` của scikit-learn [1].

Mục tiêu là giải thích và kiểm chứng **một thuật toán phân loại**, Multinomial Naive Bayes (MNB). Bag of Words và TF-IDF là hai cách biểu diễn đầu vào cho cùng thuật toán đó. Bốn lớp và tập dữ liệu tiếng Anh là phạm vi thực nghiệm; chưa thể suy kết quả trực tiếp cho tiếng Việt.

## 2. Biến văn bản thành đặc trưng

Máy học nhận véc-tơ số. Với Bag of Words, mỗi chiều ứng với một từ trong bộ từ vựng; giá trị là số lần từ xuất hiện trong tài liệu. Ví dụ bộ từ vựng `[bóng, đá, máy]` biến câu “bóng đá bóng” thành `[2, 1, 0]`. Cách này giữ tần suất nhưng không giữ thứ tự từ.

TF-IDF giảm trọng số của từ xuất hiện trong nhiều tài liệu và tăng tương đối trọng số của từ mang tính phân biệt. `TfidfVectorizer` của scikit-learn kết hợp bước đếm từ với biến đổi TF-IDF [2]. MNB được xây dựng cho đặc trưng đếm không âm; scikit-learn ghi nhận véc-tơ TF-IDF cũng có thể dùng được trong thực hành [3]. Vì vậy, thí nghiệm so sánh CountVectorizer với TfidfVectorizer trong khi giữ nguyên thuật toán MNB.

Với cả hai cách, bộ từ vựng và trọng số IDF chỉ được học từ tập huấn luyện. Tập kiểm tra chỉ đi qua phép biến đổi đã học, tránh rò rỉ thông tin.

## 3. Nguyên lý Multinomial Naive Bayes

Theo định lý Bayes, với tài liệu `d` và lớp `c`:

`P(c | d) = P(d | c) P(c) / P(d)`.

Vì `P(d)` như nhau cho mọi lớp khi xét cùng một tài liệu, ta chọn lớp có giá trị `P(d | c) P(c)` lớn nhất. MNB xem tài liệu như các lần xuất hiện của đặc trưng và áp dụng giả định độc lập có điều kiện: khi đã biết lớp, đóng góp của từng đặc trưng được tính riêng. Đây là phép xấp xỉ để mô hình đơn giản và dễ huấn luyện; các từ trong ngôn ngữ thực tế vẫn có quan hệ với nhau.

Với véc-tơ `x = (x₁, ..., x_V)`, điểm dự đoán được tính ở miền log:

`score(c, x) = log P(c) + Σᵢ xᵢ log θ(c,i)`.

Trong đó `V` là kích thước bộ từ vựng; `xᵢ` là số lần xuất hiện hoặc trọng số không âm của đặc trưng `i`; `θ(c,i)` là xác suất đặc trưng đó trong lớp `c`. Miền log giúp tránh nhân nhiều số rất nhỏ. Xác suất tiên nghiệm `P(c)` thường ước lượng từ tỷ lệ tài liệu thuộc lớp `c` trong tập train.

Ước lượng có làm trơn cộng `α`:

`θ(c,i) = [N(c,i) + α] / [N(c) + αV]`, với `N(c) = Σᵢ N(c,i)`.

`N(c,i)` là tổng giá trị đặc trưng `i` ở các tài liệu train thuộc lớp `c`. Khi `α = 1`, đây là làm trơn Laplace. Nó giữ xác suất khác 0 cho từ chưa từng thấy trong một lớp [3]. Trong thực nghiệm, `α = 1` được cố định trước khi xem tập test.

## 4. Ví dụ tính tay

Giả sử có bốn câu huấn luyện, tách theo dấu cách:

| Lớp | Câu huấn luyện |
| --- | --- |
| Thể thao | “bóng đá thắng” |
| Thể thao | “bóng đá đội” |
| Công nghệ | “máy tính nhanh” |
| Công nghệ | “máy tính mới” |

Bộ từ vựng có 8 từ: `bóng, đá, thắng, đội, máy, tính, nhanh, mới`. Mỗi lớp có 2 trong 4 câu nên `P(Thể thao) = P(Công nghệ) = 1/2`. Mỗi lớp có 6 lượt từ. Với `α = 1`, mẫu số cho mỗi xác suất từ là `6 + 8 = 14`.

Xét câu cần phân loại **“bóng đá mới”**:

| Từ | `P(từ | Thể thao)` | `P(từ | Công nghệ)` |
| --- | ---: | ---: |
| bóng | 3/14 | 1/14 |
| đá | 3/14 | 1/14 |
| mới | 1/14 | 2/14 |

Điểm chưa chuẩn hóa của Thể thao là `(1/2) × (3/14) × (3/14) × (1/14) = 9/5488`. Điểm của Công nghệ là `(1/2) × (1/14) × (1/14) × (2/14) = 2/5488`. Vì `9 > 2`, mô hình dự đoán **Thể thao**. Ví dụ này minh họa cơ chế, không phải số liệu thực nghiệm trên 20 Newsgroups.

## 5. Thiết kế thực nghiệm

- Dùng bốn lớp đã nêu và đúng hai tập `train`/`test` do bộ dữ liệu cung cấp [1].
- Gọi `remove=('headers', 'footers', 'quotes')` ở cả train và test. Metadata có thể tiết lộ lớp; bộ lọc này giảm rủi ro nhưng không loại bỏ hoàn toàn [4].
- Huấn luyện hai pipeline: `CountVectorizer + MultinomialNB` và `TfidfVectorizer + MultinomialNB`, cùng `α = 1`.
- Đánh giá accuracy toàn bộ, precision/recall/F1 theo lớp, macro F1 và ma trận nhầm lẫn. Macro F1 cho mỗi lớp trọng số như nhau, hữu ích khi số mẫu từng lớp khác nhau [5].
- Lưu số mẫu, phiên bản thư viện, tham số, kết quả và một số trường hợp sai được rút từ dự đoán trên test. Không dùng test để chọn tham số.

## 6. Kết quả thực nghiệm

Kết quả sẽ được điền sau khi chạy mã và kiểm tra tệp đầu ra. Mọi số liệu phải dẫn về một lần chạy có thể tái lập.

## 7. Ưu điểm, giới hạn và hướng mở rộng

MNB học nhanh, cần ít tham số và có thể giải thích ảnh hưởng của từ thông qua xác suất đặc trưng theo lớp. Giả định độc lập có điều kiện không mô tả quan hệ ngữ nghĩa hoặc thứ tự dài giữa các từ. Bag of Words bỏ thứ tự; TF-IDF vẫn dựa trên thống kê từ vựng. Tài liệu ngắn, từ hiếm và chủ đề giao nhau có thể gây nhầm lẫn. Ngoài ra, điểm số từ bộ dữ liệu tiếng Anh không đo chất lượng phân loại văn bản tiếng Việt.

Nếu mở rộng, nhóm có thể dùng một tập dữ liệu tiếng Việt có nhãn rõ nguồn, thử đặc trưng n-gram hoặc so sánh với một mô hình khác. Các thử nghiệm mở rộng phải dùng một tập validation riêng thay vì điều chỉnh theo test.

## Tài liệu tham khảo

[1] scikit-learn, [fetch_20newsgroups](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html).

[2] scikit-learn, [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html).

[3] scikit-learn, [Naive Bayes, mục Multinomial Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html).

[4] scikit-learn, [Classification of text documents using sparse features](https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html).

[5] scikit-learn, [classification_report](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html).
