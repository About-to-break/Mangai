import os
import shutil
from tqdm import tqdm
from typing import List
from pathlib import Path
from PIL import Image
import random
from config import *

# ───────────────────────────────
# Функции обработки данных для датасета
# ───────────────────────────────

def get_all_imgs(source_folder: Path) -> List[Path]:
    """Рекурсивно находит все изображения в папке."""
    valid_ext = tuple(e.lower() for e in VALID_IMG_EXT)
    all_files = [
        Path(root) / f
        for root, _, files in os.walk(source_folder)
        for f in files
        if f.lower().endswith(valid_ext)
    ]
    if not all_files:
        raise ValueError(f"❌ No valid images found in: {source_folder}")
    return all_files


def transfer_images_with_subfolders(source_folder: Path, target_folder: Path = RAW_IMG_DIR):
    """Переносит изображения в общую директорию с новыми именами."""
    target_folder.mkdir(parents=True, exist_ok=True)
    all_files = get_all_imgs(source_folder)

    for c, old_abs_path in enumerate(tqdm(all_files, desc="📂 Transferring images")):
        ext = old_abs_path.suffix.lower()
        new_abs_path = target_folder / f"img_{c:05d}{ext}"
        try:
            shutil.copy2(old_abs_path, new_abs_path)
        except Exception as e:
            print(f"⚠️ Error copying {old_abs_path}: {e}")

    print(f"\n✅ Transferred {len(all_files)} files to {target_folder}\n")


def convert_images_to_png(target_folder: Path, clear_bad: bool = True):
    """Конвертирует изображения в PNG, удаляет битые (если clear_bad=True)."""
    target_folder = Path(target_folder)
    all_files = get_all_imgs(target_folder)

    cleared_counter = 0
    converted_counter = 0

    for old_abs_path in tqdm(all_files, desc="🖼️ Converting images"):
        if old_abs_path.suffix.lower() == ".png":
            continue  # уже PNG

        new_abs_path = old_abs_path.with_suffix(".png")

        try:
            with Image.open(old_abs_path) as img:
                img = img.convert("RGB")
                img.save(new_abs_path, "PNG", optimize=True)
            converted_counter += 1
            old_abs_path.unlink()  # удаляем старый файл
        except Exception as e:
            print(f"\n⚠️ Error converting {old_abs_path}: {e}")
            if clear_bad:
                try:
                    old_abs_path.unlink()
                    cleared_counter += 1
                except Exception:
                    pass

    print(f"\n✅ Converted {converted_counter} images to PNG")
    if cleared_counter:
        print(f"🧹 Cleared {cleared_counter} bad files\n")


def standardise_resolutions(
    source_folder: Path,
    target_folder: Path,
    target_width: int = 1280,
    max_height: int = 1800
):
    """Приводит изображения к общему формату (resize + pad) и сохраняет в отдельную папку."""
    source_folder = Path(source_folder)
    target_folder = Path(target_folder)
    target_folder.mkdir(parents=True, exist_ok=True)

    all_files = get_all_imgs(source_folder)

    for path in tqdm(all_files, desc="📏 Standardising resolutions"):
        try:
            with Image.open(path) as img:
                w, h = img.size
                ratio = target_width / w
                new_h = int(h * ratio)
                img = img.resize((target_width, new_h), Image.LANCZOS)

                # Создаём холст нужного размера
                if new_h < max_height:
                    new_img = Image.new("RGB", (target_width, max_height), (255, 255, 255))
                    new_img.paste(img, (0, (max_height - new_h) // 2))
                else:
                    new_img = img

                # Имя файла сохраняем с тем же именем, что и оригинал
                new_name = path.stem + ".png"
                new_abs_path = target_folder / new_name
                new_img.save(new_abs_path, "PNG")

        except Exception as e:
            print(f"⚠️ Error processing {path}: {e}")

    print(f"\n✅ Normalised {len(all_files)} images saved to {target_folder}")


"""Перемешивает файлы и перемещает в новую директорию"""
def shuffle_png_files(source_folder: Path, target_folder: Path):
    target_folder.mkdir(parents=True, exist_ok=True)

    all_files = [p for p in source_folder.glob("*.png")]
    random.shuffle(all_files)

    for i, img_path in enumerate(tqdm(all_files, desc="\n🥳 Everyday i'm shuffling...\n")):
        new_name = f"page_{i:04d}{img_path.suffix}"
        shutil.copy2(img_path, target_folder / new_name)

    print(f"\n✅ Shuffled {len(all_files)} files and saved to {target_folder}")




class ColorCorrector:
    def __init__(self):
        pass
    # Пока не ясно, понадобится ли

class IcdarConverter:
    def __init__(self):
        pass

# ───────────────────────────────
# Точка входа
# ───────────────────────────────
def main():
    """
    # transfer_images_with_subfolders(DOWNLOADS_DIR, RAW_IMG_DIR)

    # convert_images_to_png(RAW_IMG_DIR)

    standardise_resolutions(
        source_folder=RAW_IMG_DIR,
        target_folder=Path(RAW_IMG_DIR.parent) / "resized",
        target_width=1280,
        max_height=1800
    )
    """

    shuffle_png_files(
        source_folder=Path(RAW_IMG_DIR.parent) / "resized",
        target_folder=Path(RAW_IMG_DIR.parent) / "labels"
    )


if __name__ == "__main__":
    main()
