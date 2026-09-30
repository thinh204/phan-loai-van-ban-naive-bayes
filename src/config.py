"""Central configuration file for paths, categories, labels, and parameters."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
DATA_DIR = ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"
DEFAULT_DATA_DIR = CACHE_DIR
MODELS_DIR = ROOT / "models"
RESULTS_DIR = ROOT / "results"
DOCS_DIR = ROOT / "docs"

# Central version and release metadata (Nguồn duy nhất cho thông tin phiên bản)
APP_NAME = "Phân loại văn bản bằng Naive Bayes đa thức"
APP_VERSION = "v1.0.3"
PLAN_VERSION = "Plan 6"
RELEASE_VERSION = "v1.0.3"
FOOTER_CAPTION = f"Khoa Công nghệ Thông tin • Đề tài: Phân loại văn bản bằng Multinomial Naive Bayes ({APP_VERSION} - {PLAN_VERSION})"

# Artifact file paths
MODEL_PATH = MODELS_DIR / "naive_bayes_model.joblib"
VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.joblib"
CLASS_NAMES_PATH = MODELS_DIR / "class_names.joblib"

# Results file paths
EVALUATION_SUMMARY_PATH = RESULTS_DIR / "evaluation_summary.json"
METRICS_PATH = RESULTS_DIR / "metrics.json"
CONFUSION_CSV_PATH = RESULTS_DIR / "confusion_tfidf.csv"
ALPHA_TUNING_PATH = RESULTS_DIR / "alpha_tuning.json"
ERROR_ANALYSIS_PATH = RESULTS_DIR / "error_analysis.json"


# Dataset classes and metadata
CATEGORIES = (
    "comp.graphics",
    "rec.sport.baseball",
    "sci.space",
    "talk.politics.misc",
)
REMOVE_METADATA = ("headers", "footers", "quotes")

CLASS_LABELS_VN = {
    "comp.graphics": "Đồ họa máy tính (Computer Graphics)",
    "rec.sport.baseball": "Thể thao - Bóng chày (Baseball)",
    "sci.space": "Khoa học vũ trụ (Space Science)",
    "talk.politics.misc": "Chính trị tổng hợp (Politics)",
}

CLASS_ICONS = {
    "comp.graphics": "🖥️",
    "rec.sport.baseball": "⚾",
    "sci.space": "🚀",
    "talk.politics.misc": "🏛️",
}

DEFAULT_VECTORIZER_PARAMS = {
    "min_df": 2,
    "max_df": 0.95,
    "lowercase": True,
}

# UX WARNING THRESHOLDS (Ngưỡng cảnh báo giao diện phục vụ trải nghiệm người dùng, KHÔNG phải metric tối ưu)
MIN_TEXT_LENGTH = 10               # Số ký tự tối thiểu để coi là văn bản có ý nghĩa
MIN_WORD_COUNT = 3                 # Số từ tối thiểu trong văn bản
MIN_IN_VOCAB_TOKENS = 2            # Ngưỡng số lượng từ khóa TF-IDF để coi là đủ tín hiệu
LOW_CONFIDENCE_THRESHOLD = 0.60    # Ngưỡng cảnh báo độ tin cậy thấp (< 60%)

SAMPLE_TEXTS = {
    "Đồ họa máy tính (3D Rendering)": (
        "I am looking for a 3D graphics rendering library with ray tracing and OpenGL shader support. "
        "The polygon mesh needs to render at 60 fps with texture mapping and antialiasing."
    ),
    "Bóng chày (Baseball game)": (
        "The pitcher threw a 95 mph fastball right down the strike zone for the strikeout. "
        "The batter swung and missed, leaving runners on first and third base in the bottom of the ninth inning."
    ),
    "Khoa học không gian (Space mission)": (
        "NASA and ESA have announced a new deep space robotic mission to explore the icy moons of Jupiter. "
        "The satellite orbit will utilize gravitational assists to study atmospheric solar radiation and planetary magnetic fields."
    ),
    "Chính trị (Government policy)": (
        "The Senate committee held an intensive debate regarding federal tax reform, individual liberty, and civil rights legislation. "
        "Both parties presented opposing viewpoints on government regulation and constitutional amendments."
    ),
}
