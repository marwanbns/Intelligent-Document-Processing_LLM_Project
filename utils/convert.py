# utils/convert.py
from pdf2image import convert_from_path
import os

def convert_pdf_to_images(pdf_path, basename=None):
    os.makedirs("temp/images", exist_ok=True)
    # auto basename si pas fourni
    if basename is None:
        basename = os.path.splitext(os.path.basename(pdf_path))[0]

    images = convert_from_path(pdf_path, dpi=300)

    paths = []
    for i, img in enumerate(images):
        name = f"{basename}_page_{i+1}.png"
        out_path = os.path.join("temp/images", name)
        img.save(out_path, "PNG")
        paths.append(out_path)

    return paths