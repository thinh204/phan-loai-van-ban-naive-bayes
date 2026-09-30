"""Module for training Multinomial Naive Bayes model and evaluating metrics."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.naive_bayes import MultinomialNB

from src.prepare_data import CATEGORIES, DEFAULT_DATA_DIR, load_dataset_as_dataframe
from src.tfidf_pipeline import build_tfidf_features, split_dataset


def train_model(X_train_tfidf, y_train, alpha: float = 1.0) -> MultinomialNB:
    """Train MultinomialNB on TF-IDF features of the training set."""
    model = MultinomialNB(alpha=alpha)
    model.fit(X_train_tfidf, y_train)
    return model


def evaluate_model(model: MultinomialNB, X_test_tfidf, y_test, class_names: list[str]) -> dict:
    """
    Evaluate trained model on test set and return all standard metrics.
    All figures are calculated directly from model predictions.
    """
    y_pred = model.predict(X_test_tfidf)

    acc = float(accuracy_score(y_test, y_pred))
    prec_macro = float(precision_score(y_test, y_pred, average="macro", zero_division=0))
    prec_weighted = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    rec_macro = float(recall_score(y_test, y_pred, average="macro", zero_division=0))
    rec_weighted = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1_macro = float(f1_score(y_test, y_pred, average="macro", zero_division=0))
    f1_weighted = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    report = classification_report(
        y_test,
        y_pred,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )
    conf_matrix = confusion_matrix(y_test, y_pred).tolist()

    metrics = {
        "accuracy": acc,
        "precision_macro": prec_macro,
        "precision_weighted": prec_weighted,
        "recall_macro": rec_macro,
        "recall_weighted": rec_weighted,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "classification_report": report,
        "confusion_matrix": conf_matrix,
        "y_pred": y_pred.tolist(),
    }
    return metrics


def save_evaluation_results(
    metrics: dict,
    class_names: list[str],
    n_train: int,
    n_test: int,
    output_dir: Path,
) -> None:
    """Save metrics and confusion matrix to disk."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save confusion matrix CSV
    cm_path = output_dir / "confusion_tfidf.csv"
    with cm_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["true\\pred", *class_names])
        for label, row in zip(class_names, metrics["confusion_matrix"]):
            writer.writerow([label, *row])

    # Save clean summary json
    summary_path = output_dir / "evaluation_summary.json"
    summary_data = {
        "model": "MultinomialNB",
        "feature_extraction": "TF-IDF (TfidfVectorizer)",
        "classes": class_names,
        "n_train": n_train,
        "n_test": n_test,
        "accuracy": metrics["accuracy"],
        "precision_macro": metrics["precision_macro"],
        "precision_weighted": metrics["precision_weighted"],
        "recall_macro": metrics["recall_macro"],
        "recall_weighted": metrics["recall_weighted"],
        "f1_macro": metrics["f1_macro"],
        "f1_weighted": metrics["f1_weighted"],
        "classification_report": metrics["classification_report"],
        "confusion_matrix": metrics["confusion_matrix"],
    }
    summary_path.write_text(json.dumps(summary_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"-> Đã lưu tệp tổng kết đánh giá: {summary_path}")
    print(f"-> Đã lưu ma trận nhầm lẫn: {cm_path}")


def print_evaluation_report(metrics: dict, class_names: list[str]) -> None:
    """Print readable evaluation metrics to console."""
    print("=" * 65)
    print("KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH MULTINOMIAL NAIVE BAYES (TF-IDF)")
    print("=" * 65)
    print(f"1. Accuracy (Độ chính xác tổng thể):  {metrics['accuracy']:.4f} ({metrics['accuracy'] * 100:.2f}%)")
    print(f"2. Precision (Macro Average):          {metrics['precision_macro']:.4f} ({metrics['precision_macro'] * 100:.2f}%)")
    print(f"   Precision (Weighted Average):       {metrics['precision_weighted']:.4f} ({metrics['precision_weighted'] * 100:.2f}%)")
    print(f"3. Recall (Macro Average):             {metrics['recall_macro']:.4f} ({metrics['recall_macro'] * 100:.2f}%)")
    print(f"   Recall (Weighted Average):          {metrics['recall_weighted']:.4f} ({metrics['recall_weighted'] * 100:.2f}%)")
    print(f"4. F1-score (Macro Average):           {metrics['f1_macro']:.4f} ({metrics['f1_macro'] * 100:.2f}%)")
    print(f"   F1-score (Weighted Average):        {metrics['f1_weighted']:.4f} ({metrics['f1_weighted'] * 100:.2f}%)")
    print("\n5. Chi tiết từng lớp (Classification Report):")
    print(f"{'Class':<22} | {'Precision':<10} | {'Recall':<10} | {'F1-score':<10} | {'Support':<8}")
    print("-" * 65)
    for c in class_names:
        c_metrics = metrics["classification_report"][c]
        print(
            f"{c:<22} | "
            f"{c_metrics['precision']:<10.4f} | "
            f"{c_metrics['recall']:<10.4f} | "
            f"{c_metrics['f1-score']:<10.4f} | "
            f"{int(c_metrics['support']):<8}"
        )
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(description="Train MultinomialNB and evaluate on test set.")
    parser.add_argument("--alpha", type=float, default=1.0, help="Laplace smoothing alpha parameter")
    parser.add_argument("--save-model", action="store_true", default=True, help="Save trained model to models/")
    args = parser.parse_args()

    print("Bước 1: Tải dữ liệu bằng Pandas...")
    df_train, df_test, df_all = load_dataset_as_dataframe(DEFAULT_DATA_DIR)
    class_names = list(CATEGORIES)

    print("Bước 2: Phân chia tập dữ liệu...")
    X_train, X_test, y_train, y_test = split_dataset(df_all)

    print("Bước 3: TF-IDF vectorization (fit chỉ trên train)...")
    X_train_tfidf, X_test_tfidf, vectorizer = build_tfidf_features(X_train, X_test)

    print("Bước 4: Huấn luyện Multinomial Naive Bayes (alpha=1.0)...")
    model = train_model(X_train_tfidf, y_train, alpha=args.alpha)

    print("Bước 5: Dự đoán trên tập test và tính toán metrics thực tế...")
    metrics = evaluate_model(model, X_test_tfidf, y_test, class_names)
    print_evaluation_report(metrics, class_names)

    output_dir = ROOT / "results"
    save_evaluation_results(metrics, class_names, len(X_train), len(X_test), output_dir)

    if args.save_model:
        models_dir = ROOT / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(model, models_dir / "naive_bayes_model.joblib")
        joblib.dump(vectorizer, models_dir / "tfidf_vectorizer.joblib")
        # Also save label names mapping
        joblib.dump(class_names, models_dir / "class_names.joblib")
        print(f"-> Đã lưu model và vectorizer vào: {models_dir}")

    print("\nGiai đoạn 3 hoàn thành thành công!")


if __name__ == "__main__":
    main()
