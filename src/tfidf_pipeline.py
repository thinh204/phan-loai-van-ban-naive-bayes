"""Module for train-test splitting and TF-IDF vectorization without data leakage."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import joblib
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
DEFAULT_DATA_DIR = ROOT / "data" / "cache"

DEFAULT_VECTORIZER_PARAMS = {
    "min_df": 2,
    "max_df": 0.95,
    "lowercase": True,
}


def split_dataset(
    df: pd.DataFrame,
    test_size: float | None = None,
    random_state: int = 42,
    stratify: bool = True,
) -> tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """
    Split dataset into train and test sets.
    If df contains a 'split' column and test_size is None, uses predefined benchmark split.
    Otherwise uses train_test_split with fixed random_state and optional stratification.

    Returns:
        (X_train, X_test, y_train, y_test)
    """
    if test_size is None and "split" in df.columns:
        train_mask = df["split"] == "train"
        test_mask = df["split"] == "test"
        X_train = df.loc[train_mask, "text"]
        y_train = df.loc[train_mask, "target"]
        X_test = df.loc[test_mask, "text"]
        y_test = df.loc[test_mask, "target"]
    else:
        actual_test_size = 0.25 if test_size is None else test_size
        stratify_labels = df["target"] if stratify else None
        X_train, X_test, y_train, y_test = train_test_split(
            df["text"],
            df["target"],
            test_size=actual_test_size,
            random_state=random_state,
            stratify=stratify_labels,
        )

    return X_train, X_test, y_train, y_test


def build_tfidf_features(
    X_train: pd.Series | list[str],
    X_test: pd.Series | list[str],
    params: dict | None = None,
) -> tuple[csr_matrix, csr_matrix, TfidfVectorizer]:
    """
    Fit TfidfVectorizer strictly on X_train, then transform X_test.

    DATA LEAKAGE PREVENTION:
    - fit_transform() is strictly executed ONLY on X_train.
    - transform() is executed on X_test.
    - No fitting is performed on X_test or combined dataset.
    """
    vectorizer_params = dict(DEFAULT_VECTORIZER_PARAMS)
    if params:
        vectorizer_params.update(params)

    vectorizer = TfidfVectorizer(**vectorizer_params)

    # STRICT: fit_transform ONLY on X_train
    X_train_tfidf = vectorizer.fit_transform(X_train)

    # STRICT: transform ONLY on X_test
    X_test_tfidf = vectorizer.transform(X_test)

    return X_train_tfidf, X_test_tfidf, vectorizer


def verify_no_data_leakage(
    vectorizer: TfidfVectorizer,
    X_train: pd.Series | list[str],
    X_test: pd.Series | list[str],
) -> bool:
    """
    Check that the vocabulary does not contain terms exclusive to X_test.
    """
    # Fit temporary vectorizer on X_test to find test-only words
    test_only_vec = TfidfVectorizer(min_df=1, lowercase=True)
    test_only_vec.fit(X_test)
    test_vocab = set(test_only_vec.vocabulary_.keys())

    train_only_vec = TfidfVectorizer(min_df=1, lowercase=True)
    train_only_vec.fit(X_train)
    train_vocab = set(train_only_vec.vocabulary_.keys())

    exclusive_test_words = test_vocab - train_vocab
    fitted_vocab = set(vectorizer.vocabulary_.keys())

    # None of the exclusive test words should be in the fitted vectorizer's vocabulary
    leakage = exclusive_test_words.intersection(fitted_vocab)
    assert len(leakage) == 0, f"DATA LEAKAGE DETECTED! Words in fitted vocabulary: {leakage}"
    return True


def main():
    parser = argparse.ArgumentParser(description="Split dataset and build TF-IDF pipeline avoiding data leakage.")
    parser.add_argument("--save-artifacts", action="store_true", help="Save vectorizer to disk")
    args = parser.parse_args()

    from src.prepare_data import load_dataset_as_dataframe

    print("1. Đang tải dữ liệu...")
    df_train, df_test, df_all = load_dataset_as_dataframe(DEFAULT_DATA_DIR)

    print("2. Phân chia tập dữ liệu Train / Test...")
    X_train, X_test, y_train, y_test = split_dataset(df_all)
    print(f"   - Số lượng X_train: {len(X_train)}")
    print(f"   - Số lượng X_test:  {len(X_test)}")

    print("3. Khởi tạo và trích xuất đặc trưng TF-IDF...")
    print("   [QUAN TRỌNG - CHỐNG DATA LEAKAGE]:")
    print("   - fit_transform() CHỈ chạy trên X_train.")
    print("   - transform() CHỈ chạy trên X_test.")
    X_train_tfidf, X_test_tfidf, vectorizer = build_tfidf_features(X_train, X_test)

    print(f"   - Kích thước ma trận TF-IDF X_train: {X_train_tfidf.shape}")
    print(f"   - Kích thước ma trận TF-IDF X_test:  {X_test_tfidf.shape}")
    print(f"   - Số lượng từ vựng (features):        {len(vectorizer.get_feature_names_out())}")

    print("4. Kiểm tra độc lập chống rò rỉ dữ liệu (Data Leakage Verification)...")
    is_safe = verify_no_data_leakage(vectorizer, X_train, X_test)
    if is_safe:
        print("   -> XÁC NHẬN AN TOÀN: Tuyệt đối không có từ vựng riêng của X_test lọt vào bộ từ vựng train!")

    if args.save_artifacts:
        model_dir = ROOT / "models"
        model_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump(vectorizer, model_dir / "tfidf_vectorizer.joblib")
        print(f"   -> Đã lưu vectorizer vào: {model_dir / 'tfidf_vectorizer.joblib'}")

    print("\nGiai đoạn 2 hoàn thành xuất sắc!")


if __name__ == "__main__":
    main()
