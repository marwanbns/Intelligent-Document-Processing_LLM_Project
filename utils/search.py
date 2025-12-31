# utils/search.py
import pytesseract
from pytesseract import Output
import cv2
import difflib

def normalize(text):
    return text.lower().replace(",", " ").replace(";", " ").replace(":", " ").strip()

def find_field_location(field_text: str, image_path: str):
    """
    Locate any token substring of field_text inside OCR of image_path.
    Returns bounding box (x, y, w, h) or None.
    """

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(gray, output_type=Output.DICT)
    tokens = normalize(field_text).split()

    # On normalise les mots de l'OCR
    ocr_words = [normalize(w) for w in data["text"]]

    for token in tokens:
        if len(token) < 2:
            continue
        
        # On essaye de trouver une correspondance parfaite
        for i, word in enumerate(ocr_words):
            # Correspondance à 70%
            if difflib.SequenceMatcher(None, token, word).ratio() > 0.7:
                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]
                return (x, y, w, h)

    return None