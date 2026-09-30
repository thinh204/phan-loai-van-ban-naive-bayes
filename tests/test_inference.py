"""Unit and end-to-end tests for Text Classification Pipeline."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib


def test_model_and_vectorizer_artifacts():
    vec_path = ROOT / "models" / "tfidf_vectorizer.joblib"
    model_path = ROOT / "models" / "naive_bayes_model.joblib"
    classes_path = ROOT / "models" / "class_names.joblib"

    assert vec_path.exists(), "TF-IDF vectorizer artifact not found"
    assert model_path.exists(), "MultinomialNB model artifact not found"
    assert classes_path.exists(), "Class names artifact not found"

    vec = joblib.load(vec_path)
    model = joblib.load(model_path)
    classes = joblib.load(classes_path)

    assert len(classes) == 4
    assert len(vec.get_feature_names_out()) == 13068


def test_unseen_text_predictions():
    vec = joblib.load(ROOT / "models" / "tfidf_vectorizer.joblib")
    model = joblib.load(ROOT / "models" / "naive_bayes_model.joblib")
    classes = joblib.load(ROOT / "models" / "class_names.joblib")

    samples = [
        ("The 3D renderer supports ray tracing, polygon shading, and OpenGL rasterization.", "comp.graphics"),
        ("The pitcher struck out three batters with curveballs in the bottom of the ninth inning.", "rec.sport.baseball"),
        ("The space shuttle launched a scientific satellite into low Earth orbit to observe solar radiation.", "sci.space"),
        ("The government senate debate focused on presidential election campaigns and constitutional rights.", "talk.politics.misc"),
    ]

    for text, expected_label in samples:
        X_vec = vec.transform([text])
        pred_idx = model.predict(X_vec)[0]
        probs = model.predict_proba(X_vec)[0]
        pred_label = classes[pred_idx]

        assert pred_label == expected_label, f"Expected {expected_label}, got {pred_label} for '{text}'"
        assert probs[pred_idx] > 0.5, f"Confidence too low: {probs[pred_idx]} for '{text}'"
        print(f"[PASS] Predicted '{pred_label}' ({probs[pred_idx]*100:.2f}%) for '{text[:45]}...'")


if __name__ == "__main__":
    print("Testing model artifacts...")
    test_model_and_vectorizer_artifacts()
    print("Testing unseen text classifications...")
    test_unseen_text_predictions()
    print("\nAll pipeline tests passed successfully!")
