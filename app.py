"""Streamlit Web Application for Text Classification - Defense & Presentation Ready."""

from __future__ import annotations

from datetime import datetime
import json
import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import importlib
import src.config
importlib.reload(src.config)
import src.classifier_service
importlib.reload(src.classifier_service)

from src.classifier_service import get_classifier_service
from src.config import (
    ALPHA_TUNING_PATH,
    APP_VERSION,
    CLASS_ICONS,
    CLASS_LABELS_VN,
    CONFUSION_CSV_PATH,
    EVALUATION_SUMMARY_PATH,
    FOOTER_CAPTION,
    LOW_CONFIDENCE_THRESHOLD,
    SAMPLE_TEXTS,
)


def format_text_preview(text: str | None, max_len: int = 80) -> str:
    """Format text preview for UI history display and CSV export.

    - Strips leading and trailing whitespaces.
    - If text is empty, all-whitespace, or None, returns '(Rỗng)'.
    - If length > max_len, returns first max_len characters with '...'.
    - If length <= max_len, returns the cleaned string unchanged without '(Rỗng)'.
    """
    if text is None:
        return "(Rỗng)"
    clean = text.strip()
    if not clean:
        return "(Rỗng)"
    if len(clean) > max_len:
        return clean[:max_len] + "..."
    return clean




@st.cache_resource
def get_service():
    """Load and cache the classifier service instance (no refitting)."""
    return get_classifier_service()


def load_json_file(file_path: Path) -> dict | list | None:
    """Safely load JSON file with error handling."""
    if not file_path.exists():
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def init_session_state():
    """Initialize session state variables for prediction history."""
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []


def main():
    st.set_page_config(
        page_title="Phân Loại Văn Bản - Multinomial Naive Bayes",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    init_session_state()

    # Styling
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.1rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0.1rem;
        }
        .sub-header {
            font-size: 1.0rem;
            color: #4B5563;
            margin-bottom: 1.2rem;
        }
        .result-box {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 5px solid #2563EB;
            padding: 18px;
            border-radius: 8px;
            margin-top: 12px;
            margin-bottom: 16px;
        }
        .uncertainty-box {
            background-color: #FEF2F2;
            border-left: 5px solid #EF4444;
            padding: 14px;
            border-radius: 8px;
            margin-top: 10px;
            margin-bottom: 14px;
        }
        .info-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 14px;
            margin-bottom: 12px;
        }
        .step-badge {
            background-color: #E0E7FF;
            color: #3730A3;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 12px;
            display: inline-block;
            margin-bottom: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Get cached service
    try:
        service = get_service()
    except Exception as exc:
        st.error(f"Lỗi khởi tạo dịch vụ phân loại: {exc}. Vui lòng chạy huấn luyện trước!")
        st.stop()

    # Load dynamic evaluation results
    eval_data = load_json_file(EVALUATION_SUMMARY_PATH)
    alpha_data = load_json_file(ALPHA_TUNING_PATH)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Thông tin hệ thống")
        st.markdown(f"**Phiên bản ứng dụng:** `{APP_VERSION}`")
        st.markdown("**Thuật toán:** Multinomial Naive Bayes")
        st.markdown("**Trích xuất đặc trưng:** TF-IDF (`TfidfVectorizer`)")
        st.markdown("**Siêu tham số tối ưu:** `alpha = 0.1`")
        st.markdown(f"**Kích thước từ vựng:** `{len(service.vectorizer.get_feature_names_out()):,}` đặc trưng")
        st.markdown(f"**Số lớp phân loại:** `{len(service.class_names)}` lớp")


        st.markdown("---")
        st.subheader("📊 Hiệu năng thực nghiệm (Động)")

        if isinstance(eval_data, dict) and "accuracy" in eval_data:
            acc_val = eval_data["accuracy"] * 100
            f1_val = eval_data["f1_macro"] * 100
            prec_val = eval_data.get("precision_macro", 0.0) * 100
            rec_val = eval_data.get("recall_macro", 0.0) * 100
            n_test = eval_data.get("n_test", 1490)

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.metric("Test Accuracy", f"{acc_val:.2f}%")
            with col_s2:
                st.metric("Macro F1", f"{f1_val:.2f}%")

            col_s3, col_s4 = st.columns(2)
            with col_s3:
                st.metric("Precision", f"{prec_val:.2f}%")
            with col_s4:
                st.metric("Recall", f"{rec_val:.2f}%")

            st.caption(f"Tập kiểm thử: {n_test:,} mẫu | Dữ liệu: `results/evaluation_summary.json`")
        else:
            st.warning("⚠️ Chưa nạp được tệp kết quả `results/evaluation_summary.json`.")

        st.markdown("---")
        st.subheader("💡 Văn bản mẫu thử nghiệm")
        st.caption("Chọn bài viết mẫu để điền nhanh:")
        sample_choice = st.selectbox(
            "Chọn bài viết mẫu:",
            ["(Chọn mẫu hoặc tự nhập tay)", *SAMPLE_TEXTS.keys()],
            key="sample_choice_box",
        )

    # Main header
    st.markdown('<div class="main-header">🧠 Hệ Thống Phân Loại Văn Bản - Multinomial Naive Bayes</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">'
        'Mô hình máy học phân loại chủ đề văn bản kết hợp TF-IDF và Multinomial Naive Bayes, '
        'tối ưu hóa bằng Stratified 5-Fold Cross-Validation và tích hợp cơ chế giải thích đặc trưng đóng góp.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Tabs navigation
    tab_pred, tab_intro, tab_eval, tab_limits = st.tabs([
        "🚀 Dự Đoán & Giải Thích",
        "📖 Giới Thiệu Mô Hình",
        "📊 Đánh Giá Thực Nghiệm",
        "⚠️ Giới Hạn & Lưu Ý",
    ])

    # ==========================================
    # TAB 1: DỰ ĐOÁN & PHÂN TÍCH
    # ==========================================
    with tab_pred:
        default_text = ""
        if sample_choice and sample_choice != "(Chọn mẫu hoặc tự nhập tay)":
            default_text = SAMPLE_TEXTS[sample_choice]

        user_text = st.text_area(
            label="Nội dung văn bản (tiếng Anh):",
            value=default_text,
            height=150,
            placeholder="Nhập hoặc dán nội dung văn bản tiếng Anh cần phân loại vào đây...",
            key="input_text_area",
        )

        col_b1, col_b2 = st.columns([1, 4])
        with col_b1:
            classify_clicked = st.button("🚀 Phân loại", type="primary", use_container_width=True)

        if classify_clicked:
            clean_input = user_text.strip()
            if not clean_input:
                st.warning("⚠️ **Vui lòng nhập nội dung văn bản để dự đoán!**")
            else:
                with st.spinner("Đang trích xuất TF-IDF và tính toán xác suất Naive Bayes..."):
                    result = service.classify(clean_input)

                # Display any UX warnings first
                if result["warnings"]:
                    for warn in result["warnings"]:
                        if warn["severity"] == "error":
                            st.error(f"**{warn['title']}**: {warn['message']}")
                        elif warn["severity"] == "warning":
                            st.warning(f"**{warn['title']}**: {warn['message']}")
                        else:
                            st.info(f"**{warn['title']}**: {warn['message']}")

                # Banner for uncertainty
                if result["is_uncertain"] and not result["is_empty"]:
                    st.markdown(
                        f"""
                        <div class="uncertainty-box">
                            <b>⚠️ Cảnh báo độ tin cậy:</b> Dự đoán này có mức độ không chắc chắn cao do tín hiệu văn bản yếu,
                            thiếu từ vựng trong từ điển TF-IDF hoặc độ tin cậy thấp ({result['confidence_percent']:.1f}%).
                            Kết quả cần được người dùng kiểm tra kỹ.
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                pred_class = result["predicted_class"]
                vn_name = result["predicted_class_vn"]
                icon = result["icon"]
                max_prob = result["confidence_percent"]
                prob_dict = result["probabilities"]
                explanations = result["explanations"]
                latency = result["latency_ms"]

                # Save to session history
                history_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text_preview": format_text_preview(clean_input, 80),
                    "predicted_class": pred_class,
                    "confidence_percent": round(max_prob, 2),
                    "in_vocab_tokens": result["in_vocab_count"],
                    "is_uncertain": "Có" if result["is_uncertain"] else "Không",
                    "latency_ms": round(latency, 2),
                }
                st.session_state.prediction_history.append(history_entry)

                # Result box
                st.markdown(
                    f"""
                    <div class="result-box">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h3 style="margin:0; color:#1E40AF;">{icon} Chủ đề dự đoán: <b>{pred_class}</b></h3>
                            <span style="font-size:0.9rem; color:#4B5563; background:#FFFFFF; padding:4px 8px; border-radius:4px; border:1px solid #CBD5E1;">
                                ⏱️ Thời gian xử lý: <b>{latency:.2f} ms</b>
                            </span>
                        </div>
                        <p style="font-size:1.15rem; margin-top:8px; margin-bottom:5px;"><b>Tên tiếng Việt:</b> {vn_name}</p>
                        <p style="font-size:1.05rem; color:#1E3A8A; margin-bottom:0;">
                            <b>Độ tin cậy (Xác suất hậu nghiệm):</b> <span style="font-size:1.25rem; font-weight:700;">{max_prob:.2f}%</span>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                col_l, col_r = st.columns([3, 2])

                with col_l:
                    st.subheader("📈 Phân bố xác suất 4 lớp")
                    prob_df = pd.DataFrame({
                        "Chủ đề": [f"{CLASS_ICONS.get(c, '')} {c}" for c in service.class_names],
                        "Tên tiếng Việt": [CLASS_LABELS_VN.get(c, c) for c in service.class_names],
                        "Xác suất": [prob_dict[c] for c in service.class_names],
                        "Tỷ lệ (%)": [f"{prob_dict[c] * 100:.2f}%" for c in service.class_names],
                    }).sort_values(by="Xác suất", ascending=False)

                    st.dataframe(prob_df[["Chủ đề", "Tên tiếng Việt", "Tỷ lệ (%)"]], hide_index=True, use_container_width=True)
                    st.bar_chart(data=prob_df.set_index("Chủ đề")["Xác suất"], height=220)

                with col_r:
                    st.subheader("🔍 Giải thích đặc trưng (Explainability)")
                    if explanations:
                        st.caption("Các từ khóa trong văn bản ủng hộ mạnh nhất cho lớp dự đoán:")
                        exp_df = pd.DataFrame(explanations)[["token", "tfidf", "margin_contribution", "support_level"]]
                        exp_df.columns = ["Từ khóa", "TF-IDF", "Mức đóng góp", "Mức độ ủng hộ"]
                        st.dataframe(exp_df, hide_index=True, use_container_width=True)
                    else:
                        st.info("Không có từ khóa nào trong văn bản nằm trong bộ từ vựng TF-IDF đã học.")

                    st.caption(
                        "ℹ️ *Lưu ý về tính giải thích:* Mức đóng góp thể hiện chênh lệch log-xác suất có điều kiện "
                        "của từ khóa đối với lớp dự đoán so với các lớp còn lại. "
                        "Đây là phân tích đặc trưng của mô hình, không phải bằng chứng nhân quả tuyệt đối."
                    )

        # Session history section
        st.markdown("---")
        st.subheader("📜 Lịch sử các lần dự đoán trong phiên")
        history = st.session_state.prediction_history

        if not history:
            st.caption("Chưa có lượt dự đoán nào trong phiên hiện tại.")
        else:
            hist_df = pd.DataFrame(history)
            col_h1, col_h2 = st.columns([4, 1])
            with col_h1:
                st.caption(f"Tổng số lượt dự đoán: **{len(history)}**")
            with col_h2:
                if st.button("🗑️ Xóa lịch sử", use_container_width=True):
                    st.session_state.prediction_history = []
                    st.rerun()

            display_cols = ["timestamp", "text_preview", "predicted_class", "confidence_percent", "in_vocab_tokens", "is_uncertain", "latency_ms"]
            rename_cols = {
                "timestamp": "Thời gian",
                "text_preview": "Đoạn trích",
                "predicted_class": "Nhãn dự đoán",
                "confidence_percent": "Độ tin cậy (%)",
                "in_vocab_tokens": "Số từ vựng",
                "is_uncertain": "Không chắc chắn",
                "latency_ms": "Độ trễ (ms)",
            }
            st.dataframe(hist_df[display_cols].rename(columns=rename_cols), hide_index=True, use_container_width=True)

            csv_export = hist_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="📥 Tải lịch sử dự đoán (CSV)",
                data=csv_export,
                file_name="lich_su_du_doan_naive_bayes.csv",
                mime="text/csv",
                type="primary",
            )

    # ==========================================
    # TAB 2: GIỚI THIỆU MÔ HÌNH
    # ==========================================
    with tab_intro:
        st.subheader("📖 Tổng Quan Về Phương Pháp & Kiến Trúc Pipeline")

        st.markdown(
            """
            Hệ thống giải quyết bài toán **Phân loại văn bản nhiều lớp (Multi-class Text Classification)** 
            sử dụng thuật toán **Multinomial Naive Bayes (MNB)** kết hợp với trích xuất đặc trưng **TF-IDF**.
            """
        )

        st.markdown("### 🔄 Quy trình xử lý đầu-cuối (End-to-End Pipeline)")
        st.info("Văn bản thô  ➔  Tiền xử lý (loại bỏ metadata)  ➔  TF-IDF Vectorizer (13.068 từ vựng)  ➔  Multinomial Naive Bayes (alpha=0.1)  ➔  Dự đoán & Xác suất")

        col_m1, col_m2 = st.columns(2)

        with col_m1:
            st.markdown("#### 1. Biểu diễn đặc trưng TF-IDF")
            st.markdown(
                """
                - **Term Frequency (TF):** Đo lường tần suất xuất hiện của từ trong văn bản.
                - **Inverse Document Frequency (IDF):** Giảm trọng số của các từ xuất hiện phổ biến trong toàn bộ tập tài liệu, làm nổi bật các từ mang tính phân biệt chủ đề cao.
                - **Chống rò rỉ dữ liệu (Anti-Data Leakage):** `TfidfVectorizer` chỉ được `fit_transform` trên **tập train** (2.239 mẫu) để học bộ từ vựng và trọng số IDF. Tập test hoặc văn bản mới chỉ thực hiện phép chiếu `transform`.
                """
            )

        with col_m2:
            st.markdown("#### 2. Thuật toán Multinomial Naive Bayes")
            st.markdown(
                """
                - **Định lý Bayes:** Tính xác suất hậu nghiệm $P(c | d) = \\frac{P(d | c) P(c)}{P(d)}$.
                - **Giả định độc lập có điều kiện:** Giả định các từ độc lập khi đã biết lớp: $P(d | c) = \\prod_{i=1}^V P(w_i | c)^{x_i}$.
                - **Tính toán ở miền Log:** Giúp tránh hiện tượng tràn số dưới (underflow):
                  $$\\text{score}(c, x) = \\log P(c) + \\sum_{i=1}^V x_i \\log \\theta_{c, i}$$
                - **Làm trơn Laplace/Lidstone:** Tránh xác suất bằng 0 với từ chưa từng gặp:
                  $$\\theta_{c, i} = \\frac{N(c, i) + \\alpha}{N(c) + \\alpha V}$$
                """
            )

        st.markdown("---")
        st.markdown("### 🛡️ Chiến lược lựa chọn siêu tham số Alpha")
        st.markdown(
            """
            - **Nguyên tắc:** Tuyệt đối không dùng tập test để chọn tham số.
            - **Phương pháp:** Sử dụng **Stratified 5-Fold Cross-Validation** trên tập train (2.239 mẫu).
            - **Kết quả:** `alpha = 0.1` đạt điểm **CV Macro F1 = 90.28%** (cao nhất trong các giá trị khảo sát `[0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0]`).
            - Sau khi khóa `alpha = 0.1`, mô hình được huấn luyện trên toàn bộ tập train và đánh giá đúng 1 lần trên tập test.
            """
        )

    # ==========================================
    # TAB 3: ĐÁNH GIÁ THỰC NGHIỆM
    # ==========================================
    with tab_eval:
        st.subheader("📊 Kết Quả Thực Nghiệm & Tối Ưu Hóa (Dữ liệu thực)")

        if isinstance(eval_data, dict) and "accuracy" in eval_data:
            st.markdown("#### 1. Các chỉ số đo lường trên tập kiểm thử độc lập (1.490 mẫu)")

            col_e1, col_e2, col_e3, col_e4 = st.columns(4)
            col_e1.metric("Accuracy", f"{eval_data['accuracy'] * 100:.2f}%")
            col_e2.metric("Macro Precision", f"{eval_data.get('precision_macro', 0.0) * 100:.2f}%")
            col_e3.metric("Macro Recall", f"{eval_data.get('recall_macro', 0.0) * 100:.2f}%")
            col_e4.metric("Macro F1-Score", f"{eval_data['f1_macro'] * 100:.2f}%")

            st.markdown("#### 2. Chi tiết từng lớp (Classification Report)")
            rep = eval_data.get("classification_report", {})
            rep_list = []
            for c in service.class_names:
                if c in rep:
                    rep_list.append({
                        "Chủ đề": c,
                        "Tên tiếng Việt": CLASS_LABELS_VN.get(c, c),
                        "Precision": f"{rep[c]['precision'] * 100:.2f}%",
                        "Recall": f"{rep[c]['recall'] * 100:.2f}%",
                        "F1-Score": f"{rep[c]['f1-score'] * 100:.2f}%",
                        "Số mẫu test": int(rep[c]["support"]),
                    })
            st.dataframe(pd.DataFrame(rep_list), hide_index=True, use_container_width=True)

            st.markdown("#### 3. Ma trận nhầm lẫn (Confusion Matrix trên 1.490 mẫu test)")
            cm_matrix = eval_data.get("confusion_matrix", [])
            if cm_matrix:
                cm_df = pd.DataFrame(cm_matrix, index=[f"Thực: {c}" for c in service.class_names], columns=[f"Dự đoán: {c}" for c in service.class_names])
                st.dataframe(cm_df, use_container_width=True)

            # Hyperparameter tuning table
            if isinstance(alpha_data, list) and len(alpha_data) > 0:
                st.markdown("---")
                st.markdown("#### 4. Bảng kết quả Stratified 5-Fold Cross-Validation trên tập Train")
                alpha_rows = []
                for item in alpha_data:
                    is_best = (item["alpha"] == eval_data.get("selected_alpha", 0.1))
                    alpha_rows.append({
                        "Giá trị Alpha": f"{item['alpha']}" + (" (Được chọn)" if is_best else ""),
                        "CV Accuracy TB": f"{item['cv_accuracy_mean'] * 100:.2f}% (+/- {item['cv_accuracy_std'] * 100:.2f}%)",
                        "CV Macro F1 TB": f"{item['cv_f1_macro_mean'] * 100:.2f}% (+/- {item['cv_f1_macro_std'] * 100:.2f}%)",
                        "CV Precision TB": f"{item.get('cv_precision_macro_mean', 0.0) * 100:.2f}%",
                        "CV Recall TB": f"{item.get('cv_recall_macro_mean', 0.0) * 100:.2f}%",
                    })
                st.dataframe(pd.DataFrame(alpha_rows), hide_index=True, use_container_width=True)
        else:
            st.warning("⚠️ Chưa nạp được tệp kết quả thực nghiệm `results/evaluation_summary.json`.")

    # ==========================================
    # TAB 4: GIỚI HẠN & LƯU Ý
    # ==========================================
    with tab_limits:
        st.subheader("⚠️ Giới Hạn Của Mô Hình & Khuyến Nghị Thực Tiễn")

        st.markdown(
            """
            Khi đánh giá và ứng dụng mô hình trong thực tế, cần nhận thức rõ các giới hạn mang tính phương pháp luận:
            """
        )

        col_lim1, col_lim2 = st.columns(2)

        with col_lim1:
            st.markdown("#### 1. Phụ thuộc tập dữ liệu huấn luyện")
            st.markdown(
                """
                - Mô hình được huấn luyện trên bộ dữ liệu **20 Newsgroups tiếng Anh**.
                - Bộ từ vựng đã học gồm **13.068 đặc trưng**. Nếu áp dụng cho văn bản tiếng Việt hoặc các chủ đề hoàn toàn mới (y học, tài chính), mô hình sẽ không có từ khóa nhận diện phù hợp.
                """
            )

            st.markdown("#### 2. Vấn đề từ vựng ngoài từ điển (OOV)")
            st.markdown(
                """
                - Với các câu chỉ chứa các từ chưa từng xuất hiện trong tập train, véc-tơ TF-IDF sẽ hoàn toàn bằng 0.
                - Khi đó, mô hình sẽ dự đoán dựa trên xác suất tiên nghiệm (prior probability) và trả về độ tin cậy thấp. Ứng dụng đã tích hợp cảnh báo cho trường hợp này.
                """
            )

        with col_lim2:
            st.markdown("#### 3. Giả định độc lập Naive Bayes")
            st.markdown(
                """
                - MNB giả định sự xuất hiện của các từ là độc lập khi biết lớp. Trong ngôn ngữ thực tế, các cụm từ (n-gram, ngữ cảnh) có mối liên hệ chặt chẽ.
                - Do đó, độ tin cậy của Naive Bayes là **xác suất hậu nghiệm trong khuôn khổ giả định của thuật toán**, không phải là bằng chứng bảo đảm tuyệt đối về chân lý thực tế.
                """
            )

            st.markdown("#### 4. Văn bản quá ngắn hoặc rỗng")
            st.markdown(
                """
                - Phân tích lỗi thực nghiệm chỉ ra: các bài viết có ít hơn hoặc bằng 2 từ vựng TF-IDF có tỷ lệ lỗi lên tới **53.33%** (so với 9.72% ở văn bản đầy đủ).
                - Khuyến nghị: Người dùng nên cung cấp văn bản hoàn chỉnh có ít nhất 1-2 câu để mô hình có đủ tín hiệu phân loại.
                """
            )

    # Footer
    st.markdown("---")
    st.caption(FOOTER_CAPTION)



if __name__ == "__main__":
    main()
