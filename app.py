"""Streamlit Web Application for Text Classification using Multinomial Naive Bayes & TF-IDF."""

from __future__ import annotations

import sys
from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.classifier_service import get_classifier_service
from src.config import CLASS_ICONS, CLASS_LABELS_VN, SAMPLE_TEXTS


@st.cache_resource
def get_service():
    """Load and cache the classifier service instance."""
    return get_classifier_service()


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

    # Get cached service
    try:
        service = get_service()
    except Exception as exc:
        st.error(f"Lỗi nạp mô hình: {exc}. Vui lòng chạy huấn luyện mô hình trước!")
        st.stop()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Thông tin mô hình")
        st.markdown("**Thuật toán:** Multinomial Naive Bayes (`MultinomialNB`)")
        st.markdown("**Đặc trưng:** TF-IDF (`TfidfVectorizer`)")
        st.markdown("**Làm trơn (Smoothing):** Laplace (`alpha = 1.0`)")
        st.markdown(f"**Số lượng từ vựng:** `{len(service.vectorizer.get_feature_names_out()):,}` đặc trưng")
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
                result = service.classify(clean_input)

            pred_class = result["predicted_class"]
            vn_name = result["predicted_class_vn"]
            icon = result["icon"]
            max_prob = result["confidence_percent"]
            prob_dict = result["probabilities"]
            tokens_tfidf = result["top_features"]

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
                    "Chủ đề": [f"{CLASS_ICONS.get(c, '')} {c}" for c in service.class_names],
                    "Tên tiếng Việt": [CLASS_LABELS_VN.get(c, c) for c in service.class_names],
                    "Xác suất": [prob_dict[c] for c in service.class_names],
                    "Tỷ lệ (%)": [f"{prob_dict[c] * 100:.2f}%" for c in service.class_names],
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
                    token_df = pd.DataFrame(tokens_tfidf, columns=["Từ khóa", "Trọng số TF-IDF"])
                    token_df["Trọng số TF-IDF"] = token_df["Trọng số TF-IDF"].apply(lambda v: f"{v:.4f}")
                    st.dataframe(token_df, hide_index=True, use_container_width=True)
                else:
                    st.info("Không có từ khóa nào trong văn bản nằm trong bộ từ vựng đã học.")

    # Footer
    st.markdown("---")
    st.caption("Khoa Công nghệ Thông tin • Môn Trí tuệ Nhân tạo • Đề tài: Phân loại văn bản bằng Multinomial Naive Bayes")


if __name__ == "__main__":
    main()
