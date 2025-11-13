from openai import OpenAI
import random
from tqdm import tqdm

from config import *
from scripts.processing import get_all_imgs, convert_png_to_b64

client = OpenAI(
    api_key="EMPTY",
    base_url="http://dev-01.local:8000/v1",
    timeout=3600
)

def generate_message(file_path):
    b64_img_str = convert_png_to_b64(file_path)
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{b64_img_str}",
                    "detail": "high",
                },
                {
                    "type": "text",
                    "text": "OCR:"
                }
            ]
        }
    ]
    return messages

def main(target_folder: Path, sample_count: int = 10, seed: int = None):
    if seed:
        random.seed(seed)
        print("Set random seed: ", seed)
    all_files = get_all_imgs(target_folder)
    samples = random.sample(all_files, sample_count)

    for rel_path in tqdm(samples, desc=f"OCRing {sample_count} random samples\n"):
        print(f"\nSending {rel_path} to vLLM...\n")
        try:
            response = client.chat.completions.create(
                model="PaddlePaddle/PaddleOCR-VL",
                messages=generate_message(rel_path),
                temperature=0.0,
            )
            ocr_vl_result = response.choices[0].message.content

            print(f"\n✅ Done: {rel_path}\n:{ocr_vl_result}\n")

        except Exception as e:
            print(e)

main(
    target_folder=Path(RAW_IMG_DIR.parent) / "resized",
    sample_count=2,
    seed=123,
)
