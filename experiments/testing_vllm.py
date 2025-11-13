from openai import OpenAI
from PIL import Image
import io
import base64

client = OpenAI(
    api_key="EMPTY",
    base_url="http://dev-01.local:8000/v1",
    timeout=3600
)

# Task-specific base prompts
TASKS = {
    "ocr": "OCR:",
    "table": "Table Recognition:",
    "formula": "Formula Recognition:",
    "chart": "Chart Recognition:",
}


def image_to_vllm_base64(img_path, max_width=None, max_height=None, convert_to="PNG"):
    """
    Пересобирает изображение в base64, минимизируя размер.
    - img_path: путь к PNG/JPG файлу
    - max_width, max_height: опциональное уменьшение размера
    - convert_to: формат для сохранения ('PNG' или 'JPEG')
    """
    img = Image.open(img_path)

    # Опциональное ресайз
    if max_width or max_height:
        img.thumbnail((max_width or img.width, max_height or img.height))

    # Сохраняем в BytesIO в нужном формате
    buffered = io.BytesIO()
    if convert_to.upper() == "JPEG":
        img.save(buffered, format="JPEG")
    else:
        img.save(buffered, format="PNG", optimize=True)

    # Конвертируем в base64
    img_bytes = buffered.getvalue()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_b64

# Пример использования
b64_data = image_to_vllm_base64("test.png", max_width=1024, convert_to="PNG")

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "input_image",
                "image_url": f"data:image/png;base64,{b64_data}",
                "detail": "high",
            },
            {
                "type": "text",
                "text": TASKS["ocr"]
            }
        ]
    }
]

response = client.chat.completions.create(
    model="PaddlePaddle/PaddleOCR-VL",
    messages=messages,
    temperature=0.1,
)
print(f"Generated text: {response.choices[0].message.content}")