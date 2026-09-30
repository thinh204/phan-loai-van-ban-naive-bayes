"""Streamlit Web Application for Text Classification with Session History & Analytics."""

from __future__ import annotations

from datetime import datetime
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
    """Load and cache the classifier service instance (no refitting)."""
    return get_classifier_service()


def init_session_state():
    """Initialize session state variables for prediction history and inputs."""
    if "prediction_history" not in st.session_state:
        st.session_state.prediction_history = []
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""


def main():
    st.set_page_config(
        page_title="Phân loại văn bản - Multinomial Naive Bayes",
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
            font-size: 2.2rem;
            font-weight: 700;
            color: #1E3A8A;
            margin-bottom: 0.2rem;
        }
        .sub-header {
            font-size: 1.02rem;
            color: #4B5563;
            margin-bottom: 1.5rem;
        }
        .result-box {
            background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
            border-left: 5px solid #2563EB;
            padding: 20px;
            border-radius: 8px;
            margin-top: 15px;
            margin-bottom: 20px;
        }
        .history-card {
            background-color: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
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
        st.header("⚙️ Cấu hình & Thông tin")
        st.markdown("**Thuật toán:** Multinomial Naive Bayes (`MultinomialNB`)")
        st.markdown("**Đặc trưng:** TF-IDF (`TfidfVectorizer`)")
        st.markdown("**Làm trơn (Laplace):** `alpha = 1.0`")
        st.markdown(f"**Số lượng từ vựng:** `{len(service.vectorizer.get_feature_names_out()):,}` đặc trưng")
        st.markdown(f"**Số lớp bài toán:** `{len(service.class_names)}` lớp")

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
        sample_choice = st.selectbox(
            "Chọn bài viết mẫu:",
            ["(Chọn mẫu hoặc tự nhập tay)", *SAMPLE_TEXTS.keys()],
            key="sample_choice_box",
        )

    # Header
    st.markdown('<div class="main-header">🧠 Hệ Thống Phân Loại Văn Bản Tự Động</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">'
        'Mô hình <b>Multinomial Naive Bayes</b> kết hợp <b>TF-IDF</b> huấn luyện trên bộ dữ liệu 20 Newsgroups. '
        'Ứng dụng hỗ trợ phân loại tức thì, phân tích độ tin cậy, trực quan hóa từ khóa và lưu vết lịch sử phiên làm việc.'
        '</div>',
        unsafe_allow_html=True,
    )

    # Tabs for main features
    tab_classify, tab_history = st.tabs(["🚀 Phân Loại Văn Bản", "📜 Lịch Sử Dự Đoán & Xuất Dữ Liệu"])

    with tab_classify:
        # Pre-fill sample if selected
        default_text = ""
        if sample_choice and sample_choice != "(Chọn mẫu hoặc tự nhập tay)":
            default_text = SAMPLE_TEXTS[sample_choice]

        user_text = st.text_area(
            label="Nội dung văn bản (tiếng Anh):",
            value=default_text,
            height=160,
            placeholder="Nhập hoặc dán nội dung đoạn văn bản vào đây (ví dụ: tin tức công nghệ, đồ họa, vũ trụ, thể thao, chính trị)...",
            key="input_text_area",
        )

        col_act1, col_act2 = st.columns([1, 4])
        with col_act1:
            classify_clicked = st.button("🚀 Phân loại", type="primary", use_container_width=True)

        if classify_clicked:
            clean_input = user_text.strip()
            if not clean_input:
                st.warning("⚠️ Vui lòng nhập nội dung văn bản trước khi nhấn nút Phân loại!")
            else:
                with st.spinner("Đang trích xuất đặc trưng TF-IDF và tính xác suất Naive Bayes..."):
                    result = service.classify(clean_input)

                pred_class = result["predicted_class"]
                vn_name = result["predicted_class_vn"]
                icon = result["icon"]
                max_prob = result["confidence_percent"]
                prob_dict = result["probabilities"]
                tokens_tfidf = result["top_features"]
                latency = result["latency_ms"]

                # Save to session history
                history_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "text_preview": clean_input[:100] + ("..." if len(clean_input) > 100 else ""),
                    "full_text": clean_input,
                    "predicted_class": pred_class,
                    "class_vn": vn_name,
                    "confidence_percent": round(max_prob, 2),
                    "latency_ms": round(latency, 2),
                }
                st.session_state.prediction_history.append(history_entry)

                # Display result banner
                st.markdown(
                    f"""
                    <div class="result-box">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <h3 style="margin:0; color:#1E40AF;">{icon} Kết Quả Dự Đoán: <b>{pred_class}</b></h3>
                            <span style="font-size:0.9rem; color:#4B5563; background:#FFFFFF; padding:4px 8px; border-radius:4px; border:1px solid #CBD5E1;">
                                ⏱️ Thời gian xử lý: <b>{latency:.2f} ms</b>
                            </span>
                        </div>
                        <p style="font-size:1.15rem; margin-top:8px; margin-bottom:5px;"><b>Chủ đề:</b> {vn_name}</p>
                        <p style="font-size:1.05rem; color:#1E3A8A; margin-bottom:0;">
                            <b>Độ tin cậy:</b> <span style="font-size:1.25rem; font-weight:700;">{max_prob:.2f}%</span>
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                # Probabilities & Features
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
                        height=240,
                    )

                with col_right:
                    st.subheader("🔍 Từ khóa quan trọng (TF-IDF)")
                    if tokens_tfidf:
                        st.caption("Các từ trong văn bản có trọng số TF-IDF nổi bật:")
                        token_df = pd.DataFrame(tokens_tfidf, columns=["Từ khóa", "Trọng số TF-IDF"])
                        token_df["Trọng số TF-IDF"] = token_df["Trọng số TF-IDF"].apply(lambda v: f"{v:.4f}")
                        st.dataframe(token_df, hide_index=True, use_container_width=True)
                    else:
                        st.info("Không có từ khóa nào trong văn bản nằm trong bộ từ vựng đã học (OOV).")

    with tab_history:
        st.subheader("📜 Lịch sử các lần dự đoán trong phiên")
        history = st.session_state.prediction_history

        if not history:
            st.info("Chưa có lượt dự đoán nào trong phiên hiện tại. Hãy thực hiện phân loại ở tab bên cạnh!")
        else:
            hist_df = pd.DataFrame(history)

            col_h1, col_h2 = st.columns([4, 1])
            with col_h1:
                st.caption(f"Tổng số lượt dự đoán: **{len(history)}**")
            with col_h2:
                if st.button("🗑️ Xóa lịch sử", use_container_width=True):
                    st.session_state.prediction_history = []
                    st.rerun()

            display_cols = ["timestamp", "text_preview", "predicted_class", "confidence_percent", "latency_ms"]
            rename_cols = {
                "timestamp": "Thời gian",
                "text_preview": "Đoạn trích văn bản",
                "predicted_class": "Nhãn dự đoán",
                "confidence_percent": "Độ tin cậy (%)",
                "latency_ms": "Độ trễ (ms)",
            }
            st.dataframe(
                hist_df[display_cols].rename(columns=rename_cols),
                hide_index=True,
                use_container_width=True,
            )

            # CSV Download
            csv_export = hist_df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
            st.download_button(
                label="📥 Tải lịch sử dự đoán (CSV)",
                data=csv_export,
                file_name="lich_su_du_doan_naive_bayes.csv",
                mime="text/csv",
                type="primary",
            )

    # Footer
    st.markdown("---")
    st.caption("Khoa Công nghệ Thông tin • Môn Trí tuệ Nhân tạo • Đề tài: Phân loại văn bản bằng Multinomial Naive Bayes")


if __name__ == "__main__":
    main()
