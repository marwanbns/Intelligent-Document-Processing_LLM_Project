# utils/pipeline.py
import os
import json
from utils.convert import convert_pdf_to_images
from utils.ocr import run_ocr_on_images
from utils.schemas import SCHEMAS
from utils.detect_type import detect_document_type
from utils.extract_text_llm import extract_with_text_llm
from utils.extract_vision import extract_with_vision_llm


def process_document(pdf_path: str, mode: str = "text"):
    """
    mode = 'text'   -> OCR multipage + HF Llama3 (détection + extraction)
    mode = 'vision' -> uniquement page 1 + LLaVA local

    Retourne UN seul JSON.
    """

    # 0) Basename du PDF
    basename = os.path.splitext(os.path.basename(pdf_path))[0]

    # 1) PDF -> Images (uniquement pour ce document)
    image_paths = convert_pdf_to_images(pdf_path, basename)

    # 2) OCR multi-pages (uniquement sur les images de ce document)
    ocr_texts = run_ocr_on_images(basename)
    full_text = ""

    for img, txt in ocr_texts.items():
        page = os.path.basename(img)
        full_text += f"\n--- PAGE {page} ---\n{txt}\n"

    # MODE VISION (LLaVA)
    if mode == "vision":
        first_img = image_paths[0]
        first_text = list(ocr_texts.values())[0]

        raw = extract_with_vision_llm(first_img, first_text, SCHEMAS["contract"])

        try:
            return json.loads(raw)
        except:
            return {"raw_output": raw}

    # MODE TEXTE (LLAMA 3)
    # 3) Détection automatique du document
    print("JSP\n", full_text)
    doc_type = detect_document_type(full_text)

    # 4) Récupération du schéma
    schema = SCHEMAS[doc_type]

    # 5) Extraction via LLM texte
    response = extract_with_text_llm(full_text, schema)

    try:
        parsed = json.loads(response)
        return parsed
    except:
        return {"raw_output": response}