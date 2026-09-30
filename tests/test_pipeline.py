"""Comprehensive automated tests for Text Classification Pipeline with pytest."""

from __future__ import annotations

import math
import sys
from pathlib import Path
import pytest
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.classifier_service import TextClassifierService, get_classifier_service
from src.config import CATEGORIES, CLASS_NAMES_PATH, MODEL_PATH, VECTORIZER_PATH


@pytest.fixture(scope="module")
def service() -> TextClassifierService:
    """Fixture providing initialized TextClassifierService instance."""
    srv = TextClassifierService(
        model_path=MODEL_PATH,
        vectorizer_path=VECTORIZER_PATH,
        class_names_path=CLASS_NAMES_PATH,
    )
    srv.load_artifacts()
    return srv


# 1. Load model thành công
def test_load_model_success(service: TextClassifierService):
    """Verify that MultinomialNB model is successfully loaded."""
    assert service.model is not None
    assert isinstance(service.model, MultinomialNB)
    assert hasattr(service.model, "classes_")


# 2. Load TF-IDF thành công
def test_load_tfidf_success(service: TextClassifierService):
    """Verify that TfidfVectorizer is successfully loaded with vocabulary."""
    assert service.vectorizer is not None
    assert isinstance(service.vectorizer, TfidfVectorizer)
    features = service.vectorizer.get_feature_names_out()
    assert len(features) > 0
    assert len(features) == 13068


# 3. Prediction trả về nhãn hợp lệ
def test_prediction_returns_valid_label(service: TextClassifierService):
    """Verify that prediction output is one of the valid dataset categories."""
    sample = "The OpenGL graphics engine renders 3D shaded polygon meshes."
    label = service.predict(sample)
    assert isinstance(label, str)
    assert label in CATEGORIES
    assert label == "comp.graphics"


# 4. Văn bản rỗng được xử lý an toàn
@pytest.mark.parametrize("empty_input", ["", "   ", "\n\t  \n", None])
def test_empty_text_handled_safely(service: TextClassifierService, empty_input):
    """Verify that empty, whitespace, and None text inputs do not cause exceptions."""
    result = service.classify(empty_input)
    assert isinstance(result, dict)
    assert result["is_empty"] is True
    assert result["predicted_class"] in CATEGORIES
    assert 0.0 <= result["confidence"] <= 1.0
    assert len(result["top_features"]) == 0


# 5. Văn bản chỉ chứa từ ngoài vocabulary không làm ứng dụng crash
def test_out_of_vocabulary_text_does_not_crash(service: TextClassifierService):
    """Verify that unseen out-of-vocabulary words do not crash the pipeline."""
    oov_text = "xyzabc12345 nonexistingsupercalifragilistic randomgibberishword"
    result = service.classify(oov_text)
    assert isinstance(result, dict)
    assert result["has_known_words"] is False
    assert result["predicted_class"] in CATEGORIES
    assert 0.0 <= result["confidence"] <= 1.0
    # Probabilities should still be valid
    for prob in result["probabilities"].values():
        assert not math.isnan(prob)
        assert prob >= 0.0


# 6. predict_proba trả về xác suất hợp lệ
def test_predict_proba_returns_valid_probabilities(service: TextClassifierService):
    """Verify that predict_proba returns probabilities in range [0, 1] for all classes."""
    text = "Astronauts aboard the International Space Station conducted scientific experiments."
    prob_dict = service.predict_proba(text)

    assert isinstance(prob_dict, dict)
    assert len(prob_dict) == 4
    for class_name, prob in prob_dict.items():
        assert class_name in CATEGORIES
        assert 0.0 <= prob <= 1.0
        assert not math.isnan(prob)


# 7. Tổng xác suất xấp xỉ 1
def test_predict_proba_sums_to_one(service: TextClassifierService):
    """Verify that the sum of class probabilities equals approximately 1.0."""
    texts = [
        "The pitcher threw a curveball for a strikeout in the ninth inning.",
        "Quantum satellites transmit encrypted optical communications from orbit.",
        "The parliamentary committee drafted constitutional amendments on civil rights.",
        "Ray tracing computes lighting reflections across polygon meshes.",
    ]
    for text in texts:
        prob_dict = service.predict_proba(text)
        prob_sum = sum(prob_dict.values())
        assert pytest.approx(prob_sum, rel=1e-5) == 1.0


# 8. Model nhận diện đúng số lượng 4 lớp của dataset hiện tại
def test_model_recognizes_exact_four_classes(service: TextClassifierService):
    """Verify that the model recognizes exactly the 4 required classes."""
    assert len(service.class_names) == 4
    assert tuple(sorted(service.class_names)) == tuple(sorted(CATEGORIES))
    assert tuple(sorted(service.model.classes_)) == (0, 1, 2, 3)


# 9. Pipeline có thể dự đoán một văn bản mới
def test_pipeline_predicts_new_text(service: TextClassifierService):
    """Verify that the pipeline can accurately classify unseen new texts across all domains."""
    unseen_cases = [
        ("The pitcher struck out three batters with fastballs in the ninth inning.", "rec.sport.baseball"),
        ("The Hubble telescope observed distant galaxies and planetary nebulae in outer space.", "sci.space"),
        ("The 3D graphics card accelerates ray tracing shaders and texture rendering.", "comp.graphics"),
        ("The senate legislation on federal taxes sparked debates between political parties.", "talk.politics.misc"),
    ]
    for text, expected_label in unseen_cases:
        res = service.classify(text)
        assert res["predicted_class"] == expected_label
        assert res["confidence"] > 0.50
        assert len(res["top_features"]) > 0
        assert res["latency_ms"] >= 0.0
