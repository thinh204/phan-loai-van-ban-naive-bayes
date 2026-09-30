"""Service layer for text preprocessing, TF-IDF transformation, Naive Bayes prediction, and explainability."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

from src.config import (
    CLASS_ICONS,
    CLASS_LABELS_VN,
    CLASS_NAMES_PATH,
    LOW_CONFIDENCE_THRESHOLD,
    MIN_IN_VOCAB_TOKENS,
    MIN_TEXT_LENGTH,
    MIN_WORD_COUNT,
    MODEL_PATH,
    VECTORIZER_PATH,
)


class TextClassifierService:
    """Encapsulates loading models, preprocessing, feature extraction, explainability, and prediction."""

    def __init__(
        self,
        model_path: Path = MODEL_PATH,
        vectorizer_path: Path = VECTORIZER_PATH,
        class_names_path: Path = CLASS_NAMES_PATH,
    ) -> None:
        self.model_path = Path(model_path)
        self.vectorizer_path = Path(vectorizer_path)
        self.class_names_path = Path(class_names_path)

        self.model: MultinomialNB | None = None
        self.vectorizer: TfidfVectorizer | None = None
        self.class_names: list[str] = []
        self._is_loaded: bool = False

    def load_artifacts(self) -> None:
        """Load trained model, TF-IDF vectorizer, and class names from disk."""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        if not self.vectorizer_path.exists():
            raise FileNotFoundError(f"Vectorizer file not found: {self.vectorizer_path}")
        if not self.class_names_path.exists():
            raise FileNotFoundError(f"Class names file not found: {self.class_names_path}")

        self.model = joblib.load(self.model_path)
        self.vectorizer = joblib.load(self.vectorizer_path)
        self.class_names = list(joblib.load(self.class_names_path))
        self._is_loaded = True

    def ensure_loaded(self) -> None:
        """Ensure artifacts are loaded prior to inference."""
        if not self._is_loaded or self.model is None or self.vectorizer is None:
            self.load_artifacts()

    @staticmethod
    def preprocess_text(text: Any) -> str:
        """Sanitize and normalize raw text input."""
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)
        return text.strip()

    def transform_text(self, text: str):
        """Transform text using fitted TF-IDF vectorizer (transform only)."""
        self.ensure_loaded()
        cleaned_text = self.preprocess_text(text)
        return self.vectorizer.transform([cleaned_text])

    def predict(self, text: str) -> str:
        """Return the predicted class name for given text."""
        self.ensure_loaded()
        X_vec = self.transform_text(text)
        pred_idx = self.model.predict(X_vec)[0]
        return self.class_names[pred_idx] if isinstance(pred_idx, (int, np.integer)) else str(pred_idx)

    def predict_proba(self, text: str) -> dict[str, float]:
        """Return a mapping of class names to predicted probabilities."""
        self.ensure_loaded()
        X_vec = self.transform_text(text)
        probs = self.model.predict_proba(X_vec)[0]
        return {name: float(probs[i]) for i, name in enumerate(self.class_names)}

    def get_top_features(self, text: str, top_k: int = 10) -> list[tuple[str, float]]:
        """Extract top TF-IDF tokens from input text that exist in vocabulary."""
        self.ensure_loaded()
        X_vec = self.transform_text(text)
        feature_names = self.vectorizer.get_feature_names_out()
        non_zero_indices = X_vec.nonzero()[1]

        tokens = [(feature_names[i], float(X_vec[0, i])) for i in non_zero_indices]
        tokens.sort(key=lambda x: x[1], reverse=True)
        return tokens[:top_k]

    def explain_prediction(self, text: str, top_k: int = 10) -> list[dict]:
        """
        Compute feature-level attribution and log-odds margin contribution for predicted class.
        Formula: contribution_margin_i = tfidf_i * (log P(w_i | c_pred) - max_{k != c_pred} log P(w_i | c_k))

        Note: This is a mathematical feature attribution under the Naive Bayes model assumptions,
        NOT a causal proof of real-world phenomena.
        """
        self.ensure_loaded()
        cleaned_text = self.preprocess_text(text)
        if not cleaned_text:
            return []

        X_vec = self.transform_text(cleaned_text)
        pred_idx = int(self.model.predict(X_vec)[0])
        feature_names = self.vectorizer.get_feature_names_out()
        non_zero_indices = X_vec.nonzero()[1]

        explanations = []
        for idx in non_zero_indices:
            token = feature_names[idx]
            tfidf_val = float(X_vec[0, idx])
            log_prob_c = float(self.model.feature_log_prob_[pred_idx, idx])

            # Max log_prob across all other competitor classes
            competitor_log_probs = [
                float(self.model.feature_log_prob_[k, idx])
                for k in range(len(self.class_names))
                if k != pred_idx
            ]
            max_other = max(competitor_log_probs) if competitor_log_probs else log_prob_c
            margin_contrib = tfidf_val * (log_prob_c - max_other)

            if margin_contrib > 0.25:
                support_desc = "Rất mạnh"
            elif margin_contrib > 0.05:
                support_desc = "Ủng hộ tích cực"
            elif margin_contrib >= -0.05:
                support_desc = "Trung tính"
            else:
                support_desc = "Hơi thiên lớp khác"

            explanations.append({
                "token": token,
                "tfidf": round(tfidf_val, 4),
                "log_prob_predicted": round(log_prob_c, 3),
                "margin_contribution": round(margin_contrib, 4),
                "support_level": support_desc,
            })

        # Sort primarily by margin contribution to predicted class
        explanations.sort(key=lambda x: x["margin_contribution"], reverse=True)
        return explanations[:top_k]

    def classify(self, text: str, top_k_features: int = 10) -> dict:
        """
        Unified classification method returning prediction, probabilities,
        robust input diagnostics, UX warnings, and feature-level explanations.
        """
        self.ensure_loaded()
        start_time = time.perf_counter()
        cleaned_text = self.preprocess_text(text)

        char_len = len(cleaned_text)
        word_count = len(cleaned_text.split())
        is_empty = (char_len == 0)
        is_too_short = (0 < char_len < MIN_TEXT_LENGTH or 0 < word_count < MIN_WORD_COUNT)

        X_vec = self.transform_text(cleaned_text)
        feature_names = self.vectorizer.get_feature_names_out()
        non_zero_indices = X_vec.nonzero()[1]
        in_vocab_count = len(non_zero_indices)
        has_no_vocab_words = (not is_empty and in_vocab_count == 0)
        has_few_vocab_words = (0 < in_vocab_count <= MIN_IN_VOCAB_TOKENS)

        # Prediction and probabilities
        pred_idx = int(self.model.predict(X_vec)[0])
        pred_class = self.class_names[pred_idx]
        probs_raw = self.model.predict_proba(X_vec)[0]
        prob_dict = {name: float(probs_raw[i]) for i, name in enumerate(self.class_names)}
        confidence = prob_dict[pred_class]
        is_low_confidence = (confidence < LOW_CONFIDENCE_THRESHOLD)

        # Generate UX warnings
        warnings = []
        if is_empty:
            warnings.append({
                "type": "empty",
                "severity": "error",
                "title": "Văn bản rỗng",
                "message": "Văn bản không có ký tự hợp lệ. Kết quả phản ánh xác suất tiên nghiệm (prior probability) của tập huấn luyện.",
            })
        elif has_no_vocab_words:
            warnings.append({
                "type": "no_vocab",
                "severity": "warning",
                "title": "Từ vựng nằm ngoài từ điển (OOV)",
                "message": "Không có từ khóa nào trong văn bản xuất hiện trong bộ từ vựng TF-IDF đã học. Dự đoán hoàn toàn dựa trên phân bố tiên nghiệm giữa các lớp.",
            })
        elif has_few_vocab_words:
            warnings.append({
                "type": "few_vocab",
                "severity": "info",
                "title": "Rất ít từ khóa đặc trưng",
                "message": f"Chỉ tìm thấy {in_vocab_count} từ khóa nằm trong bộ từ vựng TF-IDF ({[feature_names[i] for i in non_zero_indices]}). Tín hiệu ngữ cảnh có thể chưa đủ phong phú.",
            })
        elif is_too_short:
            warnings.append({
                "type": "too_short",
                "severity": "info",
                "title": "Văn bản tương đối ngắn",
                "message": f"Văn bản chỉ có {word_count} từ ({char_len} ký tự). Khuyến khích nhập đoạn văn hoàn chỉnh hơn để tăng độ chính xác.",
            })

        if is_low_confidence and not is_empty:
            warnings.append({
                "type": "low_confidence",
                "severity": "warning",
                "title": f"Độ tin cậy thấp (< {int(LOW_CONFIDENCE_THRESHOLD * 100)}%)",
                "message": f"Mô hình đạt độ tin cậy {confidence * 100:.2f}% (dưới ngưỡng cảnh báo {int(LOW_CONFIDENCE_THRESHOLD * 100)}%). Kết quả mang tính tham khảo và có sự phân vân giữa các lớp cạnh tranh.",
            })

        is_uncertain = (is_empty or has_no_vocab_words or has_few_vocab_words or is_low_confidence)

        # Explainability
        explanations = self.explain_prediction(cleaned_text, top_k=top_k_features)
        top_features = self.get_top_features(cleaned_text, top_k=top_k_features)

        latency_ms = (time.perf_counter() - start_time) * 1000

        explanation_disclaimer = (
            "Lưu ý: Mức đóng góp đặc trưng thể hiện sự chênh lệch log-xác suất có điều kiện P(từ|lớp) "
            "trong mô hình Naive Bayes, không phải bằng chứng nhân quả tuyệt đối. "
            "Độ tin cậy phản ánh xác suất hậu nghiệm dựa trên giả định độc lập có điều kiện của thuật toán."
        )

        return {
            "input_text": cleaned_text,
            "char_length": char_len,
            "word_count": word_count,
            "in_vocab_count": in_vocab_count,
            "is_empty": is_empty,
            "is_too_short": is_too_short,
            "has_known_words": in_vocab_count > 0,
            "has_few_vocab_words": has_few_vocab_words,
            "predicted_class": pred_class,
            "predicted_class_vn": CLASS_LABELS_VN.get(pred_class, pred_class),
            "icon": CLASS_ICONS.get(pred_class, "📌"),
            "confidence": confidence,
            "confidence_percent": confidence * 100,
            "is_low_confidence": is_low_confidence,
            "is_uncertain": is_uncertain,
            "probabilities": prob_dict,
            "top_features": top_features,
            "explanations": explanations,
            "explanation_disclaimer": explanation_disclaimer,
            "warnings": warnings,
            "latency_ms": latency_ms,
        }


# Singleton service instance
_classifier_service: TextClassifierService | None = None


def get_classifier_service() -> TextClassifierService:
    """Return initialized singleton TextClassifierService instance."""
    global _classifier_service
    if _classifier_service is None:
        _classifier_service = TextClassifierService()
        _classifier_service.load_artifacts()
    return _classifier_service
