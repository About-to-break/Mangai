from ocr.manga import MangaAnalyzer

import random
from tqdm import tqdm

from config import *
from scripts.processing import get_all_imgs

ocr_unit = MangaAnalyzer()

def main(target_folder: Path, sample_count: int = 10, seed: int = None):
    if seed:
        random.seed(seed)
        print("Set random seed: ", seed)
    all_files = get_all_imgs(target_folder)
    samples = random.sample(all_files, sample_count)

    for rel_path in tqdm(samples, desc=f"OCRing {sample_count} random samples\n"):
        try:
            ocr_result = ocr_unit.predict(rel_path)

            print(f"\n✅ Done: {rel_path}\n:{ocr_result}\n")

        except Exception as e:
            print(e)

main(
    target_folder=Path(RAW_IMG_DIR.parent) / "resized",
    sample_count=2,
    seed=123,
)