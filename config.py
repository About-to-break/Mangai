from pathlib import Path


# ───────────────────────────────
# Директории
# ───────────────────────────────

SCRIPT_DIR = Path(__file__).resolve()
DATASET_DIR = SCRIPT_DIR.parent / "dataset"
PLOTS_DIR = DATASET_DIR / "plots"
STATS_DIR = DATASET_DIR / "stats"
RAW_IMG_DIR = DATASET_DIR / "raw"
DOWNLOADS_DIR = DATASET_DIR / "downloads"
MODELS_DIR = SCRIPT_DIR.parent / "models"

# ───────────────────────────────
# Параметры изображений
# ───────────────────────────────

VALID_IMG_EXT= (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")