import os
import datetime
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd


# ───────────────────────────────
# Константы и пути
# ───────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_FOLDER = SCRIPT_DIR.parent / "dataset" / "downloads"
PLOTS_DIR = SCRIPT_DIR.parent / "dataset" / "plots"
STATS_DIR = SCRIPT_DIR.parent / "dataset" / "stats"

PLOTS_DIR.mkdir(parents=True, exist_ok=True)
STATS_DIR.mkdir(parents=True, exist_ok=True)


# ───────────────────────────────
# Класс статистики
# ───────────────────────────────
class RawDatasetStatistics:
    def __init__(self, folder: Path = DEFAULT_FOLDER):
        self.folder = Path(folder)
        if not self.folder.exists():
            raise FileNotFoundError(f"❌ Dataset folder not found: {self.folder}")
        self.total = self.count_images()

    def count_images(self) -> int:
        """Рекурсивно считает количество изображений в каталоге"""
        valid_ext = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")
        total = sum(
            1 for root, _, files in os.walk(self.folder)
            for f in files if f.lower().endswith(valid_ext)
        )
        return total

    def stat_resolutions(self, target_folder: Path = None, do_plot: bool = False) -> pd.DataFrame:
        """Собирает статистику по всем изображениям (включая подпапки)"""
        target_folder = Path(target_folder or self.folder)
        valid_ext = (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")

        all_files = []
        for root, _, files in os.walk(target_folder):
            for f in files:
                if f.lower().endswith(valid_ext):
                    rel_path = os.path.relpath(os.path.join(root, f), target_folder)
                    all_files.append(rel_path)

        if not all_files:
            raise ValueError(f"❌ No images found in: {target_folder}")

        stats = []
        for rel_path in tqdm(all_files, desc="📸 Scanning images"):
            abs_path = target_folder / rel_path
            try:
                with Image.open(abs_path) as img:
                    w, h = img.size
                    stats.append({
                        "file": rel_path,
                        "width": w,
                        "height": h,
                        "aspect_ratio": round(w / h, 4)
                    })
            except Exception as e:
                print(f"\n⚠️ Error reading {abs_path}: {e}")

        df = pd.DataFrame(stats)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        csv_path = STATS_DIR / f"resolution_stats_{timestamp}.csv"
        df.to_csv(csv_path, index=False)
        print(f"✅ Saved stats to {csv_path}")

        if do_plot:
            print("\n📊 Summary statistics:")
            print(df.describe()[["width", "height", "aspect_ratio"]])

            plot_path = PLOTS_DIR / f"resolution_hist_{timestamp}.png"
            plt.figure(figsize=(8, 5))
            plt.hist(df["width"], bins=40, alpha=0.6, label="Width")
            plt.hist(df["height"], bins=40, alpha=0.6, label="Height")
            plt.xlabel("Pixels")
            plt.ylabel("Count")
            plt.title("Resolution distribution")
            plt.legend()
            plt.tight_layout()
            plt.savefig(plot_path, dpi=200)
            plt.close()

            print(f"✅ Saved plot to {plot_path}")

        return df


# ───────────────────────────────
# Main entry point
# ───────────────────────────────
def main():
    stats = RawDatasetStatistics()
    print(f"🧾 Total raw images for dataset: {stats.total}")

    df = stats.stat_resolutions(do_plot=True, target_folder=stats.folder)
    mean_w, mean_h = df["width"].mean(), df["height"].mean()

    print(f"\n📐 Average resolution: {mean_w:.1f} × {mean_h:.1f}px")
    print(f"🧩 Aspect ratio median: {df['aspect_ratio'].median():.3f}")


if __name__ == "__main__":
    main()
