"""Module for in-depth error analysis on test set predictions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import (
    CACHE_DIR,
    CATEGORIES,
    ERROR_ANALYSIS_PATH,
    MODELS_DIR,
    RESULTS_DIR,
)
from src.prepare_data import load_dataset_as_dataframe
from src.tfidf_pipeline import split_dataset

LOW_CONFIDENCE_THRESHOLD = 0.60


def run_error_analysis(
    low_confidence_threshold: float = LOW_CONFIDENCE_THRESHOLD,
) -> dict:
    """
    Perform deep analysis of errors on test set predictions.
    All figures are calculated strictly from real predictions.
    """
    print("1. Đang tải dữ liệu và nạp mô hình...")
    df_train, df_test, df_all = load_dataset_as_dataframe(CACHE_DIR)
    X_train, X_test, y_train, y_test = split_dataset(df_all)

    model = joblib.load(MODELS_DIR / "naive_bayes_model.joblib")
    vectorizer = joblib.load(MODELS_DIR / "tfidf_vectorizer.joblib")
    class_names = list(CATEGORIES)

    print("2. Chuyển đổi TF-IDF và dự đoán trên tập test...")
    X_test_tfidf = vectorizer.transform(X_test)
    y_pred = model.predict(X_test_tfidf)
    y_proba = model.predict_proba(X_test_tfidf)
    confidences = np.max(y_proba, axis=1)

    n_test = len(y_test)
    y_test_arr = np.array(y_test)
    is_correct = (y_pred == y_test_arr)

    n_correct = int(np.sum(is_correct))
    n_wrong = int(n_test - n_correct)
    acc = float(n_correct / n_test)

    # Confusion matrix and confused pairs
    cm = confusion_matrix(y_test_arr, y_pred, labels=list(range(len(class_names))))
    confused_pairs = []
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            if i != j and cm[i, j] > 0:
                confused_pairs.append({
                    "true_class": class_names[i],
                    "predicted_class": class_names[j],
                    "count": int(cm[i, j]),
                    "rate_of_true_class": float(cm[i, j] / np.sum(cm[i, :])),
                })
    confused_pairs.sort(key=lambda x: x["count"], reverse=True)

    # In-vocabulary token counts per sample
    vocab_set = set(vectorizer.vocabulary_.keys())
    token_counts = []
    for text in X_test:
        tokens = text.lower().split()
        in_vocab = sum(1 for t in tokens if t in vocab_set)
        token_counts.append(in_vocab)
    token_counts = np.array(token_counts)

    few_tokens_mask = (token_counts <= 2)
    n_few_tokens = int(np.sum(few_tokens_mask))
    err_rate_few_tokens = float(np.mean(~is_correct[few_tokens_mask])) if n_few_tokens > 0 else 0.0
    err_rate_normal = float(np.mean(~is_correct[~few_tokens_mask]))

    # Confidence analysis
    low_conf_mask = (confidences < low_confidence_threshold)
    n_low_conf = int(np.sum(low_conf_mask))
    err_rate_low_conf = float(np.mean(~is_correct[low_conf_mask])) if n_low_conf > 0 else 0.0
    err_rate_high_conf = float(np.mean(~is_correct[~low_conf_mask])) if (n_test - n_low_conf) > 0 else 0.0

    # Representative error cases
    error_indices = np.where(~is_correct)[0]
    representative_errors = []

    for idx in error_indices:
        text = X_test.iloc[idx]
        true_idx = y_test_arr[idx]
        pred_idx = y_pred[idx]
        conf = float(confidences[idx])
        in_v = int(token_counts[idx])

        representative_errors.append({
            "test_index": int(idx),
            "true_class": class_names[true_idx],
            "predicted_class": class_names[pred_idx],
            "confidence": conf,
            "char_length": len(text),
            "in_vocab_tokens": in_v,
            "snippet": text.strip()[:180].replace("\n", " "),
        })
        if len(representative_errors) >= 10:
            break

    analysis_data = {
        "dataset": "20 Newsgroups (4 categories)",
        "model": "MultinomialNB (Tuned alpha=0.1)",
        "n_test": n_test,
        "n_correct": n_correct,
        "n_wrong": n_wrong,
        "accuracy": acc,
        "confusion_matrix": cm.tolist(),
        "top_confused_pairs": confused_pairs[:6],
        "vocabulary_analysis": {
            "total_vocab_size": len(vocab_set),
            "samples_with_few_or_no_tokens": n_few_tokens,
            "error_rate_few_tokens": err_rate_few_tokens,
            "error_rate_normal_tokens": err_rate_normal,
        },
        "confidence_analysis": {
            "threshold": low_confidence_threshold,
            "samples_below_threshold": n_low_conf,
            "error_rate_below_threshold": err_rate_low_conf,
            "error_rate_above_threshold": err_rate_high_conf,
        },
        "representative_errors": representative_errors,
    }

    return analysis_data


def save_and_print_error_analysis(analysis: dict) -> None:
    """Save results to error_analysis.json and print human-readable summary."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    ERROR_ANALYSIS_PATH.write_text(
        json.dumps(analysis, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n-> Đã lưu kết quả phân tích lỗi vào: {ERROR_ANALYSIS_PATH}")

    print("\n" + "=" * 70)
    print("BÁO CÁO PHÂN TÍCH LỖI THỰC TẾ TRÊN TẬP TEST")
    print("=" * 70)
    print(f"- Tổng số mẫu test:              {analysis['n_test']}")
    print(f"- Số dự đoán ĐÚNG:              {analysis['n_correct']} ({analysis['accuracy'] * 100:.2f}%)")
    print(f"- Số dự đoán SAI:               {analysis['n_wrong']} ({(1 - analysis['accuracy']) * 100:.2f}%)")

    print("\n1. Các cặp lớp thường bị nhầm lẫn nhiều nhất:")
    for pair in analysis["top_confused_pairs"]:
        print(f"  * Thật: {pair['true_class']:<20} -> Nhầm sang: {pair['predicted_class']:<20} | {pair['count']:>2} lần ({pair['rate_of_true_class'] * 100:.1f}%)")

    print(f"\n2. Phân tích văn bản ngắn / ít từ vựng (<= 2 từ trong TF-IDF vocabulary):")
    va = analysis["vocabulary_analysis"]
    print(f"  * Số mẫu ít hoặc không có từ vựng: {va['samples_with_few_or_no_tokens']} mẫu")
    print(f"  * Tỷ lệ lỗi ở nhóm ít từ vựng:    {va['error_rate_few_tokens'] * 100:.2f}% (so với {va['error_rate_normal_tokens'] * 100:.2f}% ở nhóm bình thường)")

    print(f"\n3. Phân tích độ tin cậy thấp (Confidence < {analysis['confidence_analysis']['threshold'] * 100:.0f}%):")
    ca = analysis["confidence_analysis"]
    print(f"  * Số mẫu có độ tin cậy thấp:       {ca['samples_below_threshold']} mẫu")
    print(f"  * Tỷ lệ lỗi ở nhóm tin cậy thấp:   {ca['error_rate_below_threshold'] * 100:.2f}% (so với {ca['error_rate_above_threshold'] * 100:.2f}% ở nhóm tin cậy cao)")

    print("\n4. Một số ví dụ dự đoán sai tiêu biểu:")
    for i, err in enumerate(analysis["representative_errors"][:5], start=1):
        print(f"  [{i}] Mẫu #{err['test_index']} | Thật: '{err['true_class']}' -> Dự đoán: '{err['predicted_class']}' (Tin cậy: {err['confidence'] * 100:.1f}%, Từ vựng: {err['in_vocab_tokens']})")
        print(f"      Đoạn trích: \"{err['snippet']}...\"\n")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Run error analysis on test set.")
    parser.add_argument("--threshold", type=float, default=LOW_CONFIDENCE_THRESHOLD, help="Low confidence threshold")
    args = parser.parse_args()

    analysis = run_error_analysis(low_confidence_threshold=args.threshold)
    save_and_print_error_analysis(analysis)


if __name__ == "__main__":
    main()
