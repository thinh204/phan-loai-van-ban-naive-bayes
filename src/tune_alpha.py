"""Module for hyperparameter tuning of alpha in MultinomialNB using Stratified Cross-Validation."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import (
    ALPHA_TUNING_PATH,
    CACHE_DIR,
    CATEGORIES,
    CONFUSION_CSV_PATH,
    DEFAULT_VECTORIZER_PARAMS,
    EVALUATION_SUMMARY_PATH,
    MODELS_DIR,
    RESULTS_DIR,
)
from src.prepare_data import load_dataset_as_dataframe
from src.tfidf_pipeline import build_tfidf_features, split_dataset

CANDIDATE_ALPHAS = [0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 1.5, 2.0]


def run_cross_validation_tuning(
    X_train: pd.Series,
    y_train: pd.Series,
    candidate_alphas: list[float] = CANDIDATE_ALPHAS,
    n_splits: int = 5,
    random_state: int = 42,
) -> tuple[float, list[dict]]:
    """
    Tune alpha strictly on training data using Stratified K-Fold CV.
    Pipeline guarantees TF-IDF is fit strictly within each train fold to avoid data leakage.
    """
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    results = []

    print(f"Bắt đầu {n_splits}-Fold Stratified Cross-Validation trên {len(X_train)} mẫu train...")
    for alpha in candidate_alphas:
        # Pipeline fits TF-IDF on train-fold only, transforms val-fold
        pipeline = Pipeline([
            ("tfidf", build_tfidf_features.__wrapped__ if hasattr(build_tfidf_features, "__wrapped__") else None),
        ])
        from sklearn.feature_extraction.text import TfidfVectorizer
        pipe = Pipeline([
            ("tfidf", TfidfVectorizer(**DEFAULT_VECTORIZER_PARAMS)),
            ("nb", MultinomialNB(alpha=alpha)),
        ])

        scores = cross_validate(
            pipe,
            X_train,
            y_train,
            cv=cv,
            scoring=["accuracy", "f1_macro", "precision_macro", "recall_macro"],
            return_train_score=False,
        )

        acc_mean = float(scores["test_accuracy"].mean())
        acc_std = float(scores["test_accuracy"].std())
        f1_mean = float(scores["test_f1_macro"].mean())
        f1_std = float(scores["test_f1_macro"].std())
        prec_mean = float(scores["test_precision_macro"].mean())
        rec_mean = float(scores["test_recall_macro"].mean())

        entry = {
            "alpha": alpha,
            "cv_accuracy_mean": acc_mean,
            "cv_accuracy_std": acc_std,
            "cv_f1_macro_mean": f1_mean,
            "cv_f1_macro_std": f1_std,
            "cv_precision_macro_mean": prec_mean,
            "cv_recall_macro_mean": rec_mean,
        }
        results.append(entry)
        print(f"  * alpha={alpha:<4} | CV Accuracy: {acc_mean:.4f} (+/- {acc_std:.4f}) | CV Macro-F1: {f1_mean:.4f} (+/- {f1_std:.4f})")

    # Select best alpha based strictly on CV Macro-F1 on training data
    best_entry = max(results, key=lambda x: x["cv_f1_macro_mean"])
    best_alpha = float(best_entry["alpha"])
    print(f"\n=> Alpha tối ưu được chọn từ Cross-Validation: alpha={best_alpha} (CV Macro-F1: {best_entry['cv_f1_macro_mean']:.4f})")

    return best_alpha, results


def train_and_evaluate_final_model(
    best_alpha: float,
    X_train: pd.Series,
    y_train: pd.Series,
    X_test: pd.Series,
    y_test: pd.Series,
    class_names: list[str],
) -> dict:
    """
    Train final model on entire training set with locked best_alpha,
    then evaluate strictly ONCE on the test set.
    """
    print(f"\nHuấn luyện mô hình cuối cùng với alpha={best_alpha} trên toàn bộ tập train...")
    # fit TF-IDF strictly on X_train, transform X_test
    X_train_tfidf, X_test_tfidf, vectorizer = build_tfidf_features(X_train, X_test)

    final_model = MultinomialNB(alpha=best_alpha)
    final_model.fit(X_train_tfidf, y_train)

    print("Đánh giá mô hình cuối cùng trên tập test (đúng một lần duy nhất)...")
    y_pred = final_model.predict(X_test_tfidf)

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

    # Save artifacts
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_model, MODELS_DIR / "naive_bayes_model.joblib")
    joblib.dump(vectorizer, MODELS_DIR / "tfidf_vectorizer.joblib")
    joblib.dump(class_names, MODELS_DIR / "class_names.joblib")

    eval_results = {
        "model": "MultinomialNB",
        "feature_extraction": "TF-IDF (TfidfVectorizer)",
        "selected_alpha": best_alpha,
        "classes": class_names,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "accuracy": acc,
        "precision_macro": prec_macro,
        "precision_weighted": prec_weighted,
        "recall_macro": rec_macro,
        "recall_weighted": rec_weighted,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "classification_report": report,
        "confusion_matrix": conf_matrix,
    }
    return eval_results


def save_tuning_results(cv_results: list[dict], eval_results: dict, class_names: list[str]) -> None:
    """Save all tuning and evaluation files to results/."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Save alpha tuning CV json
    ALPHA_TUNING_PATH.write_text(
        json.dumps(cv_results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 2. Save alpha tuning CV CSV
    cv_csv_path = RESULTS_DIR / "alpha_tuning.csv"
    pd.DataFrame(cv_results).to_csv(cv_csv_path, index=False, encoding="utf-8")

    # 3. Update evaluation_summary.json
    EVALUATION_SUMMARY_PATH.write_text(
        json.dumps(eval_results, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 4. Update confusion matrix CSV
    with CONFUSION_CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["true\\pred", *class_names])
        for label, row in zip(class_names, eval_results["confusion_matrix"]):
            writer.writerow([label, *row])

    print(f"-> Đã lưu bảng so sánh alpha: {ALPHA_TUNING_PATH} và {cv_csv_path}")
    print(f"-> Đã cập nhật kết quả đánh giá mới: {EVALUATION_SUMMARY_PATH}")
    print(f"-> Đã cập nhật ma trận nhầm lẫn: {CONFUSION_CSV_PATH}")


def print_final_report(eval_results: dict, class_names: list[str]) -> None:
    """Print clean summary of final test evaluation."""
    print("=" * 70)
    print(f"KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH SAU TỐI ƯU (Alpha = {eval_results['selected_alpha']})")
    print("=" * 70)
    print(f"1. Test Accuracy:       {eval_results['accuracy']:.4f} ({eval_results['accuracy'] * 100:.2f}%)")
    print(f"2. Test Precision (Macro): {eval_results['precision_macro']:.4f} ({eval_results['precision_macro'] * 100:.2f}%)")
    print(f"   Test Precision (Weighted): {eval_results['precision_weighted']:.4f} ({eval_results['precision_weighted'] * 100:.2f}%)")
    print(f"3. Test Recall (Macro):    {eval_results['recall_macro']:.4f} ({eval_results['recall_macro'] * 100:.2f}%)")
    print(f"   Test Recall (Weighted):    {eval_results['recall_weighted']:.4f} ({eval_results['recall_weighted'] * 100:.2f}%)")
    print(f"4. Test F1-score (Macro):  {eval_results['f1_macro']:.4f} ({eval_results['f1_macro'] * 100:.2f}%)")
    print(f"   Test F1-score (Weighted):  {eval_results['f1_weighted']:.4f} ({eval_results['f1_weighted'] * 100:.2f}%)")
    print("\nChi tiết Classification Report:")
    print(f"{'Class':<22} | {'Precision':<10} | {'Recall':<10} | {'F1-score':<10} | {'Support':<8}")
    print("-" * 70)
    for c in class_names:
        cm = eval_results["classification_report"][c]
        print(f"{c:<22} | {cm['precision']:<10.4f} | {cm['recall']:<10.4f} | {cm['f1-score']:<10.4f} | {int(cm['support']):<8}")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Tune alpha on training data and evaluate once on test.")
    args = parser.parse_args()

    print("Bước 1: Tải dữ liệu bằng Pandas...")
    df_train, df_test, df_all = load_dataset_as_dataframe(CACHE_DIR)
    class_names = list(CATEGORIES)

    print("Bước 2: Phân chia tập dữ liệu Train / Test...")
    X_train, X_test, y_train, y_test = split_dataset(df_all)

    print("\nBước 3: Lựa chọn alpha bằng Stratified 5-Fold Cross-Validation trên tập Train...")
    best_alpha, cv_results = run_cross_validation_tuning(X_train, y_train)

    print("\nBước 4: Khóa alpha tối ưu và huấn luyện trên toàn bộ tập Train...")
    eval_results = train_and_evaluate_final_model(
        best_alpha=best_alpha,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        class_names=class_names,
    )

    print("\nBước 5: Lưu kết quả thực nghiệm mới...")
    save_tuning_results(cv_results, eval_results, class_names)
    print_final_report(eval_results, class_names)


if __name__ == "__main__":
    main()
