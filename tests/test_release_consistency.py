"""
Automated consistency and integrity tests for release artifacts, metrics, and documentation.
Fails CI immediately if any documentation differs from JSON ground truth or configuration.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parent.parent


def test_version_configuration_consistency():
    """Verify src/config.py version constants match app.py usage."""
    from src.config import APP_VERSION, PLAN_VERSION, FOOTER_CAPTION
    import app

    assert APP_VERSION.startswith("v1."), f"Invalid APP_VERSION: {APP_VERSION}"
    assert "Plan" in PLAN_VERSION, f"Invalid PLAN_VERSION: {PLAN_VERSION}"
    assert APP_VERSION in FOOTER_CAPTION, "APP_VERSION not present in FOOTER_CAPTION"
    assert PLAN_VERSION in FOOTER_CAPTION, "PLAN_VERSION not present in FOOTER_CAPTION"

    # app.py must import and use these centralized variables
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "APP_VERSION" in app_source, "app.py does not use central APP_VERSION"
    assert "FOOTER_CAPTION" in app_source, "app.py does not use central FOOTER_CAPTION"


def test_ground_truth_metrics_integrity():
    """Verify ground truth metrics in JSON files match locked experimental parameters."""
    eval_file = ROOT / "results" / "evaluation_summary.json"
    alpha_file = ROOT / "results" / "alpha_tuning.json"

    assert eval_file.exists(), "results/evaluation_summary.json missing"
    assert alpha_file.exists(), "results/alpha_tuning.json missing"

    eval_data = json.loads(eval_file.read_text(encoding="utf-8"))
    assert eval_data["model"] == "MultinomialNB"
    assert eval_data["selected_alpha"] == 0.1
    assert eval_data["n_train"] == 2239
    assert eval_data["n_test"] == 1490
    assert round(eval_data["accuracy"] * 100, 2) == 88.52
    assert round(eval_data["f1_macro"] * 100, 2) == 88.33
    assert round(eval_data["f1_weighted"] * 100, 2) == 88.49

    alpha_data = json.loads(alpha_file.read_text(encoding="utf-8"))
    alpha_map = {item["alpha"]: item for item in alpha_data}

    # Best alpha 0.1
    assert 0.1 in alpha_map, "alpha=0.1 missing in alpha_tuning.json"
    assert round(alpha_map[0.1]["cv_f1_macro_mean"] * 100, 2) == 90.28

    # Baseline alpha 1.0
    assert 1.0 in alpha_map, "alpha=1.0 missing in alpha_tuning.json"
    assert round(alpha_map[1.0]["cv_f1_macro_mean"] * 100, 2) == 88.55


def test_no_stale_cv_metrics_in_release_notes():
    """Ensure release notes and active documentation do not cite false/stale CV F1 numbers."""
    for note_name in ["RELEASE_NOTES_v1.0.2.md", "RELEASE_NOTES_v1.0.3.md", "RELEASE_NOTES_v1.0.4.md"]:
        notes_file = ROOT / "docs" / note_name
        if notes_file.exists():
            content = notes_file.read_text(encoding="utf-8")
            assert "89,32%" not in content and "89.32%" not in content, (
                f"Found stale CV F1 89.32% in docs/{note_name}!"
            )
            assert "91,47%" not in content and "91.47%" not in content, (
                f"Found stale CV F1 91.47% in docs/{note_name}!"
            )
            assert "88,55%" in content, f"Missing ground truth 88,55% in docs/{note_name}"
            assert "90,28%" in content, f"Missing ground truth 90,28% in docs/{note_name}"


def test_manifest_and_checksums_sync():
    """Verify that all files documented in MANIFEST.json and CHECKSUMS.sha256 exist."""
    manifest_path = ROOT / "release" / "MANIFEST.json"
    checksums_path = ROOT / "release" / "CHECKSUMS.sha256"

    if not manifest_path.exists():
        pytest.skip("release/MANIFEST.json không có trong môi trường giải nén độc lập.")

    assert checksums_path.exists(), "release/CHECKSUMS.sha256 missing"

    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for file_entry in manifest_data["files"]:
        fpath = ROOT / file_entry["path"]
        assert fpath.exists(), f"File in manifest missing from repo: {file_entry['path']}"


def test_deployment_url_consistency():
    """Verify deployment URL format across documentation and README."""
    expected_url = "https://phan-loai-van-ban-naive-bayes.streamlit.app"
    readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert expected_url in readme_text, f"Deployment URL missing in README.md"
