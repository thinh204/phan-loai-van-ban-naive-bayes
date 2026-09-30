"""
Behavioral and regression tests for Streamlit UI interactions, empty input guarding,
text preview formatting, and CSV history exports (Plan 10).
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.classifier_service import format_text_preview


# =============================================================================
# Unit tests for format_text_preview
# =============================================================================

def test_format_text_preview_rules():
    """Verify that format_text_preview conforms strictly to Plan 10 requirements."""
    # 1. Empty, whitespace, None
    assert format_text_preview("") == "(Rỗng)"
    assert format_text_preview("   ") == "(Rỗng)"
    assert format_text_preview(" \n \t ") == "(Rỗng)"
    assert format_text_preview(None) == "(Rỗng)"

    # 2. Short text (e.g. 'space') - MUST NOT have '(Rỗng)' suffix
    assert format_text_preview("space") == "space"
    assert format_text_preview("   space   ") == "space"

    # 3. OOV text - MUST NOT have '(Rỗng)' suffix
    assert format_text_preview("zxqvbnm qqqzxvv") == "zxqvbnm qqqzxvv"

    # 4. Exact 80 characters - MUST NOT have '...' and MUST NOT have '(Rỗng)'
    text_80 = "A" * 80
    assert len(text_80) == 80
    assert format_text_preview(text_80) == text_80
    assert not format_text_preview(text_80).endswith("...")
    assert not format_text_preview(text_80).endswith("(Rỗng)")

    # 5. Exact 81 characters - MUST take 80 chars + '...'
    text_81 = ("B" * 80) + "C"
    assert len(text_81) == 81
    assert format_text_preview(text_81) == ("B" * 80) + "..."

    # 6. Much longer text
    text_long = "NASA launched a spacecraft into orbit to study distant planets and explore the solar system."
    clean_long = text_long.strip()
    assert format_text_preview(text_long) == clean_long[:80] + "..."


# =============================================================================
# Behavioral tests with Streamlit AppTest
# =============================================================================

def test_empty_and_whitespace_input_on_new_session():
    """Empty or whitespace input in a new session must show warning and produce 0 history entries."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()

    # 1. Empty string submission
    at.text_area[0].input("").run()
    at.button[0].click().run()

    # Must display warning
    assert len(at.warning) > 0
    assert any("Vui lòng nhập nội dung văn bản để dự đoán" in w.value for w in at.warning)

    # History must remain strictly empty (0 rows)
    history = at.session_state["prediction_history"]
    assert len(history) == 0

    # 2. Whitespace-only submission
    at.text_area[0].input("     \n\t   ").run()
    at.button[0].click().run()

    assert any("Vui lòng nhập nội dung văn bản để dự đoán" in w.value for w in at.warning)
    assert len(at.session_state["prediction_history"]) == 0


def test_valid_input_followed_by_whitespace_preserves_history():
    """A valid prediction followed by a whitespace submission must preserve existing history row count."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()

    # Step 1: Valid classification
    valid_text = "NASA launched a spacecraft into orbit to study distant planets and explore the solar system."
    at.text_area[0].input(valid_text).run()
    at.button[0].click().run()

    assert len(at.session_state["prediction_history"]) == 1
    assert at.session_state["prediction_history"][0]["predicted_class"] == "sci.space"

    # Step 2: Whitespace submission
    at.text_area[0].input("    \t\n   ").run()
    at.button[0].click().run()

    # Warning must appear
    assert any("Vui lòng nhập nội dung văn bản để dự đoán" in w.value for w in at.warning)
    # History must NOT increase; still exactly 1 entry
    assert len(at.session_state["prediction_history"]) == 1
    assert at.session_state["prediction_history"][0]["predicted_class"] == "sci.space"


def test_short_text_and_oov_previews_and_warnings():
    """Verify short text and OOV trigger appropriate warnings/info and have clean previews without (Rỗng)."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()

    # 1. Input 'space'
    at.text_area[0].input("space").run()
    at.button[0].click().run()

    history = at.session_state["prediction_history"]
    assert len(history) == 1
    assert history[0]["text_preview"] == "space"
    assert not history[0]["text_preview"].endswith("(Rỗng)")
    alerts_space = [w.value for w in at.warning] + [i.value for i in at.info]
    # Alert for few vocab words / short context
    assert any("từ khóa" in a.lower() or "ngắn" in a.lower() for a in alerts_space)

    # 2. Input OOV text 'zxqvbnm qqqzxvv'
    at.text_area[0].input("zxqvbnm qqqzxvv").run()
    at.button[0].click().run()

    assert len(history) == 2
    assert history[1]["text_preview"] == "zxqvbnm qqqzxvv"
    assert not history[1]["text_preview"].endswith("(Rỗng)")
    alerts_oov = [w.value for w in at.warning] + [i.value for i in at.info]
    # OOV warning should be present
    assert any("từ điển" in a.lower() or "oov" in a.lower() for a in alerts_oov)



def test_boundary_80_and_81_characters_previews():
    """Verify preview for boundary inputs of 80 and 81 characters."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()

    # 80 characters
    text_80 = "The space shuttle orbited the planet Earth and deployed scientific instruments!!"
    assert len(text_80) == 80
    at.text_area[0].input(text_80).run()
    at.button[0].click().run()

    hist80 = at.session_state["prediction_history"][-1]
    assert hist80["text_preview"] == text_80
    assert not hist80["text_preview"].endswith("...")
    assert not hist80["text_preview"].endswith("(Rỗng)")

    # 81 characters
    text_81 = text_80 + "X"
    assert len(text_81) == 81
    at.text_area[0].input(text_81).run()
    at.button[0].click().run()

    hist81 = at.session_state["prediction_history"][-1]
    assert hist81["text_preview"] == text_80 + "..."


def test_csv_export_content_and_columns():
    """Verify that CSV generated from session history strictly matches recorded entries."""
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()

    test_inputs = [
        "The graphics software renders three dimensional images using polygons and textures.",
        "",  # Must be ignored
        "space",
        "   ",  # Must be ignored
        "zxqvbnm qqqzxvv",
    ]

    for inp in test_inputs:
        at.text_area[0].input(inp).run()
        at.button[0].click().run()

    history = at.session_state["prediction_history"]
    # Only 3 valid submissions should be in history
    assert len(history) == 3

    # Export to DataFrame and CSV
    df = pd.DataFrame(history)
    csv_bytes = df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")

    # Read back CSV
    read_df = pd.read_csv(io.BytesIO(csv_bytes), encoding="utf-8-sig")
    assert len(read_df) == 3
    assert list(read_df.columns) == [
        "timestamp",
        "text_preview",
        "predicted_class",
        "confidence_percent",
        "in_vocab_tokens",
        "is_uncertain",
        "latency_ms",
    ]

    # Previews must match exactly
    assert read_df["text_preview"].iloc[0].startswith("The graphics software")
    assert read_df["text_preview"].iloc[1] == "space"
    assert read_df["text_preview"].iloc[2] == "zxqvbnm qqqzxvv"

    # None of them should contain "(Rỗng)"
    for preview in read_df["text_preview"]:
        assert "(Rỗng)" not in str(preview)
