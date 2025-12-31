# utils/ocr.py
import os
import pytesseract
from PIL import Image


def run_ocr_on_images(basename, image_folder="temp/images", text_folder="temp/text"):
    os.makedirs(text_folder, exist_ok=True)

    results = {}

    # OCR uniquement sur les pages du document courant
    for img_file in sorted(os.listdir(image_folder)):

        if img_file.endswith(".png") and img_file.startswith(basename):
            img_path = os.path.join(image_folder, img_file)

            # OCR
            text = pytesseract.image_to_string(Image.open(img_path))

            # même nom que l'image
            base_name = os.path.splitext(img_file)[0]
            txt_path = os.path.join(text_folder, f"{base_name}.txt")

            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)

            results[img_path] = text

    return results