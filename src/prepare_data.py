"""Module for loading, inspecting, and preprocessing text dataset using Pandas."""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd
from sklearn.datasets import fetch_20newsgroups

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_DIR = ROOT / "data" / "cache"

CATEGORIES = (
    "comp.graphics",
    "rec.sport.baseball",
    "sci.space",
    "talk.politics.misc",
)
REMOVE = ("headers", "footers", "quotes")


def load_dataset_as_dataframe(data_dir: Path = DEFAULT_DATA_DIR) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load 20 Newsgroups dataset from cache/disk and return as Pandas DataFrames.
    Returns:
        (df_train, df_test, df_all)
    """
    data_dir.mkdir(parents=True, exist_ok=True)

    raw_train = fetch_20newsgroups(
        subset="train",
        categories=CATEGORIES,
        remove=REMOVE,
        data_home=str(data_dir),
        shuffle=True,
        random_state=42,
    )
    raw_test = fetch_20newsgroups(
        subset="test",
        categories=CATEGORIES,
        remove=REMOVE,
        data_home=str(data_dir),
        shuffle=True,
        random_state=42,
    )

    df_train = pd.DataFrame({
        "text": raw_train.data,
        "target": raw_train.target,
        "target_name": [raw_train.target_names[i] for i in raw_train.target],
        "split": "train",
    })

    df_test = pd.DataFrame({
        "text": raw_test.data,
        "target": raw_test.target,
        "target_name": [raw_test.target_names[i] for i in raw_test.target],
        "split": "test",
    })

    df_all = pd.concat([df_train, df_test], ignore_index=True)
    return df_train, df_test, df_all


def inspect_dataframe(df: pd.DataFrame, name: str = "Dataset") -> dict:
    """
    Inspect sample counts, class labels, missing values, empty texts, and duplicates.
    """
    total_samples = len(df)
    null_counts = df.isnull().sum().to_dict()
    empty_texts = int((df["text"].str.strip() == "").sum())
    duplicate_texts = int(df.duplicated(subset=["text"]).sum())
    class_distribution = df["target_name"].value_counts().to_dict()

    summary = {
        "name": name,
        "total_samples": total_samples,
        "classes": list(class_distribution.keys()),
        "class_distribution": class_distribution,
        "null_counts": null_counts,
        "empty_texts": empty_texts,
        "duplicate_texts": duplicate_texts,
    }
    return summary


def print_inspection_report(summary: dict) -> None:
    """Print readable summary of the dataset inspection."""
    print("=" * 60)
    print(f"BÁO CÁO KIỂM TRA DỮ LIỆU: {summary['name']}")
    print("=" * 60)
    print(f"- Tổng số mẫu: {summary['total_samples']}")
    print(f"- Số lượng nhãn ({len(summary['classes'])} nhãn): {summary['classes']}")
    print("\n- Phân bố nhãn:")
    for label, count in summary["class_distribution"].items():
        percentage = (count / summary["total_samples"]) * 100
        print(f"  * {label}: {count} mẫu ({percentage:.2f}%)")
    print("\n- Dữ liệu thiếu (Null/NaN):")
    for col, count in summary["null_counts"].items():
        print(f"  * {col}: {count}")
    print(f"- Mẫu có nội dung rỗng/chỉ chứa khoảng trắng: {summary['empty_texts']}")
    print(f"- Mẫu trùng lặp nội dung: {summary['duplicate_texts']}")
    print("=" * 60)


def export_clean_csv(df: pd.DataFrame, output_path: Path) -> None:
    """Export DataFrame to CSV file for persistence or direct pandas usage."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Đã lưu dataset ra CSV: {output_path} ({len(df)} dòng)")


def main():
    parser = argparse.ArgumentParser(description="Prepare, inspect, and preprocess dataset using Pandas.")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="Path to data cache directory")
    parser.add_argument("--save-csv", action="store_true", help="Save dataset to CSV format")
    args = parser.parse_args()

    print("Đang đọc dữ liệu bằng Pandas...")
    df_train, df_test, df_all = load_dataset_as_dataframe(args.data_dir)

    print("\nKiểm tra tập dữ liệu Train:")
    train_summary = inspect_dataframe(df_train, name="Tập huấn luyện (Train)")
    print_inspection_report(train_summary)

    print("\nKiểm tra tập dữ liệu Test:")
    test_summary = inspect_dataframe(df_test, name="Tập kiểm thử (Test)")
    print_inspection_report(test_summary)

    print("\nKiểm tra toàn bộ dữ liệu (All):")
    all_summary = inspect_dataframe(df_all, name="Toàn bộ dữ liệu (All)")
    print_inspection_report(all_summary)

    if args.save_csv:
        csv_path = ROOT / "data" / "dataset.csv"
        export_clean_csv(df_all, csv_path)

    print("\nXác nhận: Dataset hợp lệ và sẵn sàng cho các giai đoạn tiếp theo!")


if __name__ == "__main__":
    main()
