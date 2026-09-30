"""Service layer for text preprocessing, TF-IDF transformation, and Naive Bayes prediction."""

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
    MODEL_PATH,
    VECTORIZER_PATH,
)


class TextClassifierService:
    """Encapsulates loading models, preprocessing, feature extraction, and prediction."""

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

    def classify(self, text: str, top_k_features: int = 10) -> dict:
        """
        Unified classification method returning full prediction result and diagnostics.
        Gracefully handles empty strings, OOV text, and measures inference latency.
        """
        self.ensure_loaded()
        start_time = time.perf_counter()
        cleaned_text = self.preprocess_text(text)

        is_empty = len(cleaned_text) == 0
        X_vec = self.transform_text(cleaned_text)

        # Prediction and probabilities
        pred_idx = self.model.predict(X_vec)[0]
        pred_class = self.class_names[pred_idx] if isinstance(pred_idx, (int, np.integer)) else str(pred_idx)
        probs_raw = self.model.predict_proba(X_vec)[0]
        prob_dict = {name: float(probs_raw[i]) for i, name in enumerate(self.class_names)}
        confidence = prob_dict[pred_class]

        top_features = self.get_top_features(cleaned_text, top_k=top_k_features)
        has_known_words = len(top_features) > 0

        latency_ms = (time.perf_counter() - start_time) * 1000

        return {
            "input_text": cleaned_text,
            "is_empty": is_empty,
            "has_known_words": has_known_words,
            "predicted_class": pred_class,
            "predicted_class_vn": CLASS_LABELS_VN.get(pred_class, pred_class),
            "icon": CLASS_ICONS.get(pred_class, "📌"),
            "confidence": confidence,
            "confidence_percent": confidence * 100,
            "probabilities": prob_dict,
            "top_features": top_features,
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
