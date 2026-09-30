"""Reproducible four-class text classification with Multinomial Naive Bayes."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sklearn
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = (
    "comp.graphics",
    "rec.sport.baseball",
    "sci.space",
    "talk.politics.misc",
)
REMOVE = ("headers", "footers", "quotes")
VECTORIZER_OPTIONS = {"min_df": 2, "max_df": 0.95, "lowercase": True}
ALPHA = 1.0


def run(data_dir: Path, output_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    train = fetch_20newsgroups(
        subset="train", categories=CATEGORIES, remove=REMOVE,
        data_home=str(data_dir), shuffle=True, random_state=42,
    )
    test = fetch_20newsgroups(
        subset="test", categories=CATEGORIES, remove=REMOVE,
        data_home=str(data_dir), shuffle=True, random_state=42,
    )
    if list(train.target_names) != list(test.target_names):
        raise RuntimeError("Train and test have different class orders")

    labels = list(range(len(train.target_names)))
    results = {
        "dataset": "20 Newsgroups, four selected categories",
        "source": "https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html",
        "classes": list(train.target_names),
        "remove": list(REMOVE),
        "n_train": len(train.data),
        "n_test": len(test.data),
        "empty_after_removal": {
            "train": sum(not text.strip() for text in train.data),
            "test": sum(not text.strip() for text in test.data),
        },
        "train_counts": {name: int((train.target == i).sum()) for i, name in enumerate(train.target_names)},
        "test_counts": {name: int((test.target == i).sum()) for i, name in enumerate(test.target_names)},
        "sklearn_version": sklearn.__version__,
        "parameters": {"alpha": ALPHA, "vectorizer": VECTORIZER_OPTIONS},
        "models": {},
    }

    for name, vectorizer in (
        ("count", CountVectorizer(**VECTORIZER_OPTIONS)),
        ("tfidf", TfidfVectorizer(**VECTORIZER_OPTIONS)),
    ):
        # Pipeline.fit learns the vocabulary (and IDF) from train only.
        model = make_pipeline(vectorizer, MultinomialNB(alpha=ALPHA))
        model.fit(train.data, train.target)
        prediction = model.predict(test.data)
        report = classification_report(
            test.target, prediction, labels=labels,
            target_names=train.target_names, output_dict=True, zero_division=0,
        )
        matrix = confusion_matrix(test.target, prediction, labels=labels)
        results["models"][name] = {
            "n_features": len(model[0].get_feature_names_out()),
            "accuracy": float(accuracy_score(test.target, prediction)),
            "macro_f1": float(f1_score(test.target, prediction, average="macro")),
            "classification_report": report,
            "confusion_matrix": matrix.tolist(),
        }

        matrix_path = output_dir / f"confusion_{name}.csv"
        with matrix_path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["true\\pred", *train.target_names])
            for label, row in zip(train.target_names, matrix):
                writer.writerow([label, *row.tolist()])

        # Keep only indices and labels; the raw corpus remains in the local cache.
        errors = []
        for index, (true_label, predicted_label) in enumerate(zip(test.target, prediction)):
            if true_label != predicted_label:
                errors.append({
                    "test_index": index,
                    "true": train.target_names[true_label],
                    "predicted": train.target_names[predicted_label],
                    "characters_after_removal": len(test.data[index].strip()),
                })
            if len(errors) >= 8:
                break
        (output_dir / f"errors_{name}.json").write_text(
            json.dumps(errors, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    (output_dir / "metrics.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Train: {len(train.data)} | Test: {len(test.data)}")
    for name, model_result in results["models"].items():
        print(f"{name}: accuracy={model_result['accuracy']:.4f}, "
              f"macro-F1={model_result['macro_f1']:.4f}")
    print(f"Results saved in {output_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "cache")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    args = parser.parse_args()
    run(args.data_dir, args.output_dir)
