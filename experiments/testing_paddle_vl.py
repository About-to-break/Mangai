from ocr.vl import MangaVLAnalyzer
import random
from tqdm import tqdm

from config import *
from scripts.processing import get_all_imgs

paddle_vl_config = {
    "vl_rec_model_dir": MODELS_DIR / "PaddleOCR-VL-For-Manga",
    "use_layout_detection": True,
    "layout_threshold": 0.35,
    "layout_unclip_ratio": 1.5,
    "layout_nms": 0.2,
    "layout_merge_bboxes_mode": "union",
    "use_doc_orientation_classify": False,
    "use_doc_unwarping": False,
    "vl_rec_backend": "native",
    "vl_rec_max_concurrency": 1

}

ocr_vl = MangaVLAnalyzer(config=paddle_vl_config)

"""Проверка PAddleOCR-VL-for-manga + его родного layout detection"""
def main(target_folder: Path, sample_count: int = 10, seed: int = None):
    if seed:
        random.seed(seed)
        print("Set random seed: ", seed)
    all_files = get_all_imgs(target_folder)
    samples = random.sample(all_files, sample_count)

    for rel_path in tqdm(samples, desc=f"OCRing {sample_count} random samples\n"):
        try:
            ocr_vl_result = ocr_vl.predict(rel_path)
            print(f"\n✅ Done: {rel_path}\n:{ocr_vl_result}\n")

        except Exception as e:
            print(e)

main(
    target_folder=Path(RAW_IMG_DIR.parent) / "resized",
    sample_count=2,
    seed=123,
)

# TODO: поменять под использование vLLM




