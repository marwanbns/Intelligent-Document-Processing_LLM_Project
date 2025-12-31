import base64
import json
from io import BytesIO
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llava"

def encode_image(pil_img):
    buffer = BytesIO()
    pil_img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def query_llava_ollama(image, ocr_text, schema):
    image_b64 = encode_image(image)

    prompt = f"""
You are an Intelligent Document Processing system.
Extract structured information from the scanned contract image.

Use BOTH:
- the OCR text
- the visual elements in the image

Return ONLY valid JSON following this schema:

{json.dumps(schema, indent=2)}

OCR TEXT:
{ocr_text}

Answer ONLY with JSON.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "images": [image_b64],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)

    try:
        data = response.json()
        return data["message"]["content"]
    except Exception as e:
        return {"error": response.text, "exception": str(e)}