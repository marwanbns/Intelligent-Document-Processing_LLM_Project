# utils/extract_vision.py
import base64
import json
from io import BytesIO
import requests
from PIL import Image

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llava"

def encode_image(pil_img):
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def extract_with_vision_llm(image_path, ocr_text, schema):
    image = Image.open(image_path)
    image_b64 = encode_image(image)

    prompt = f"""
Extract structured information from this scanned contract.
Use BOTH the OCR text and the visual content of the image.

JSON schema:
{json.dumps(schema, indent=2)}

OCR TEXT:
{ocr_text}

Return only JSON.
"""

    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "images": [image_b64],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    data = response.json()
    return data["message"]["content"]