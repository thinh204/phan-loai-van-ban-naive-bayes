"""Streamlit Web Application for Text Classification using Multinomial Naive Bayes & TF-IDF."""

from __future__ import annotations

from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / "models"
RESULTS_DIR = ROOT / "results"

CLASS_LABELS_VN = {
    "comp.graphics": "Đồ họa máy tính (Computer Graphics)",
    "rec.sport.baseball": "Thể thao - Bóng chày (Baseball)",
    "sci.space": "Khoa học vũ trụ (Space Science)",
    "talk.politics.misc": "Chính trị tổng hợp (Politics)",
}

CLASS_ICONS = {
    "comp.graphics": "🖥️",
    "rec.sport.baseball": "⚾",
    "sci.space": "🚀",
    "talk.politics.misc": "🏛️",
}

SAMPLE_TEXTS = {
    "Đồ họa máy tính (3D Rendering)": (
        "I am looking for a 3D graphics rendering library with ray tracing and OpenGL shader support. "
        "The polygon mesh needs to render at 60 fps with texture mapping and antialiasing."
    ),
    "Bóng chày (Baseball game)": (
        "The pitcher threw a 95 mph fastball right down the strike zone for the strikeout. "
        "The batter swung and missed, leaving runners on first and third base in the bottom of the ninth inning."
    ),
    "Khoa học không gian (Space mission)": (
        "NASA and ESA have announced a new deep space robotic mission to explore the icy moons of Jupiter. "
        "The satellite orbit will utilize gravitational assists to study atmospheric solar radiation and planetary magnetic fields."
    ),
    "Chính trị (Government policy)": (
        "The Senate committee held an intensive debate regarding federal tax reform, individual liberty, and civil rights legislation. "
        "Both parties presented opposing viewpoints on government regulation and constitutional amendments."
    ),
}


@st.cache_resource
def load_classification_pipeline():
    """Load pre-trained TF-IDF vectorizer, MultinomialNB model, and class names."""
    vec_path = MODELS_DIR / "tfidf_vectorizer.joblib"
    model_path = MODELS_DIR / "naive_bayes_model.joblib"
    classes_path = MODELS_DIR / "class_names.joblib"

    if not vec_path.exists() or not model_path.exists() or not classes_path.exists():
        st.error("Chưa tìm thấy mô hình hoặc vectorizer đã huấn luyện trong thư mục 'models/'. "
                 "Vui lòng chạy 'python src/train_evaluate.py' trước!")
        st.stop()

    vectorizer = joblib.load(vec_path)
    model = joblib.load(model_path)
    class_names = joblib.load(classes_path)
    return vectorizer, model, class_names


def classify_text(text: str, vectorizer, model, class_names: list[str]):
    """Transform text using fitted TF-IDF vectorizer and predict with MultinomialNB."""
    # Data leakage safe: strictly transform only
    X_vec = vectorizer.transform([text])
    pred_idx = model.predict(X_vec)[0]
    pred_class = class_names[pred_idx] if isinstance(pred_idx, (int, np.integer)) else pred_idx

    # Probabilities
    probs = model.predict_proba(X_vec)[0]
    prob_dict = {class_names[i]: float(probs[i]) for i in range(len(class_names))}

    # Significant TF-IDF tokens in input
    feature_names = vectorizer.get_feature_names_out()
    non_zero_indices = X_vec.nonzero()[1]
    tokens_tfidf = [(feature_names[i], X_vec[0, i]) for i in non_zero_indices]
    tokens_tfidf.sort(key=lambda x: x[1], reverse=True)

    return pred_class, prob_dict, tokens_tfidf


def main():
    st.set_page_config(
        page_title="Phân loại văn bản - Multinomial Naive Bayes",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom styling
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.05rem;
            color: #4B5563;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #F8FAFC;
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #E2E8F0;
            text-align: center;
        }
        .result-box {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 5px solid #2563EB;
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Load artifacts
    vectorizer, model, class_names = load_classification_pipeline()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Thông tin mô hình")
        st.markdown("**Thuật toán:** Multinomial Naive Bayes (`MultinomialNB`)")
        st.markdown("**Đặc trưng:** TF-IDF (`TfidfVectorizer`)")
        st.markdown("**Làm trơn (Smoothing):** Laplace (`alpha = 1.0`)")
        st.markdown(f"**Số lượng từ vựng:** `{len(vectorizer.get_feature_names_out()):,}` đặc trưng")
        st.markdown("**Dữ liệu kiểm thử:** 20 Newsgroups (4 lớp)")

        st.markdown("---")
        st.subheader("📊 Hiệu năng thực nghiệm")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.metric("Accuracy", "87.18%")
        with col_s2:
            st.metric("Macro F1", "86.87%")

        st.markdown("---")
        st.subheader("💡 Văn bản mẫu thử nghiệm")
        st.caption("Chọn một văn bản mẫu để tự động điền vào ô nhập:")
        selected_sample = st.selectbox(
            "Chọn bài viết mẫu:",
            ["(Chọn mẫu hoặc tự nhập tay)", *SAMPLE_TEXTS.keys()],
        )

    # Main content
    st.markdown('<div class="main-header">🧠 Hệ Thống Phân Loại Văn Bản Tự Động</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">'
        'Mô hình <b>Multinomial Naive Bayes</b> kết hợp <b>TF-IDF</b> huấn luyện trên tập dữ liệu chuẩn 20 Newsgroups. '
        'Hệ thống chuyển đổi văn bản qua TF-IDF (fit từ tập train) và tính toán xác suất tiên nghiệm - hậu nghiệm.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Pre-fill sample if chosen
    initial_text = ""
    if selected_sample and selected_sample != "(Chọn mẫu hoặc tự nhập tay)":
        initial_text = SAMPLE_TEXTS[selected_sample]

    st.markdown("### 📝 Nhập văn bản cần phân loại")
    user_text = st.text_area(
        label="Nội dung văn bản (tiếng Anh):",
        value=initial_text,
        height=180,
        placeholder="Nhập hoặc dán nội dung đoạn văn bản vào đây (ví dụ: bài viết về đồ họa, vũ trụ, thể thao, chính trị)...",
        key="input_text_area",
    )

    col_btn, col_clear = st.columns([1, 5])
    with col_btn:
        classify_clicked = st.button("🚀 Phân loại", type="primary", use_container_width=True)

    if classify_clicked:
        clean_input = user_text.strip()
        if not clean_input:
            st.warning("⚠️ Vui lòng nhập nội dung văn bản trước khi nhấn nút Phân loại!")
        else:
            with st.spinner("Đang tính toán ma trận TF-IDF và dự đoán xác suất Naive Bayes..."):
                pred_class, prob_dict, tokens_tfidf = classify_text(clean_input, vectorizer, model, class_names)

            vn_name = CLASS_LABELS_VN.get(pred_class, pred_class)
            icon = CLASS_ICONS.get(pred_class, "📌")
            max_prob = prob_dict[pred_class] * 100

            st.markdown(
                f"""
                <div class="result-box">
                    <h3 style="margin-top:0; color:#1E40AF;">{icon} Kết Quả Dự Đoán: <b>{pred_class}</b></h3>
                    <p style="font-size:1.15rem; margin-bottom:5px;"><b>Chủ đề:</b> {vn_name}</p>
                    <p style="font-size:1.05rem; color:#1E3A8A; margin-bottom:0;">
                        <b>Độ tin cậy (Xác suất dự đoán):</b> <span style="font-size:1.25rem; font-weight:700;">{max_prob:.2f}%</span>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Details: Probabilities and TF-IDF terms
            col_left, col_right = st.columns([3, 2])

            with col_left:
                st.subheader("📈 Phân bố xác suất các lớp")
                prob_df = pd.DataFrame({
                    "Chủ đề": [f"{CLASS_ICONS.get(c, '')} {c}" for c in class_names],
                    "Tên tiếng Việt": [CLASS_LABELS_VN.get(c, c) for c in class_names],
                    "Xác suất": [prob_dict[c] for c in class_names],
                    "Tỷ lệ (%)": [f"{prob_dict[c] * 100:.2f}%" for c in class_names],
                }).sort_values(by="Xác suất", ascending=False)

                st.dataframe(
                    prob_df[["Chủ đề", "Tên tiếng Việt", "Tỷ lệ (%)"]],
                    hide_index=True,
                    use_container_width=True,
                )
                st.bar_chart(
                    data=prob_df.set_index("Chủ đề")["Xác suất"],
                    height=260,
                )

            with col_right:
                st.subheader("🔍 Từ khóa quan trọng (TF-IDF)")
                if tokens_tfidf:
                    st.caption("Các từ trong văn bản có trọng số TF-IDF cao nhất:")
                    token_df = pd.DataFrame(tokens_tfidf[:10], columns=["Từ khóa", "Trọng số TF-IDF"])
                    token_df["Trọng số TF-IDF"] = token_df["Trọng số TF-IDF"].apply(lambda v: f"{v:.4f}")
                    st.dataframe(token_df, hide_index=True, use_container_width=True)
                else:
                    st.info("Không có từ khóa nào trong văn bản nằm trong bộ từ vựng đã học.")

    # Footer
    st.markdown("---")
    st.caption("Khoa Công nghệ Thông tin • Môn Trí tuệ Nhân tạo • Đề tài: Phân loại văn bản bằng Multinomial Naive Bayes")


if __name__ == "__main__":
    main()
