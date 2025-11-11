from pathlib import Path


# ───────────────────────────────
# Директории
# ───────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent / "dataset"
PLOTS_DIR = DATASET_DIR / "plots"
STATS_DIR = DATASET_DIR / "stats"
RAW_IMG_DIR = DATASET_DIR / "raw"
DOWNLOADS_DIR = DATASET_DIR / "downloads"

# ───────────────────────────────
# Параметры изображений
# ───────────────────────────────

VALID_IMG_EXT= (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")