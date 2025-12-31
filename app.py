import streamlit as st
import base64
import os
import json
from datetime import datetime

from utils.convert import convert_pdf_to_images
from utils.ocr import run_ocr_on_images
from utils.pipeline import process_document

st.set_page_config(page_title="IDP Multimodal – Contract Analyzer", layout="wide")

st.title("Intelligent Document Processing – Contract Analyzer")

# Creer les fichiers
os.makedirs("temp/images", exist_ok=True)
os.makedirs("temp/text", exist_ok=True)
os.makedirs("output/json", exist_ok=True)

tabs = st.tabs(["📥 Upload PDF", "🖼 PDF → Images", "🔤 OCR", "🧠 Extraction LLM", "📦 Résultats", "🔍 Find Information"])

# TAB 1 : Pour les UPLOAD
with tabs[0]:
    st.header("Upload your contract PDF")
    uploaded = st.file_uploader("Choose a PDF", type=["pdf"])
    if uploaded:
        filename = uploaded.name
        upload_path = os.path.join("input", filename)

        with open(upload_path, "wb") as f:
            f.write(uploaded.read())

        st.session_state["uploaded_pdf"] = upload_path
        st.session_state["pdf_basename"] = os.path.splitext(filename)[0]

        st.success(f"Uploaded: {filename}")


# TAB 2 : Conversion PDF en Image
with tabs[1]:
    st.header("Convert PDF to Images")

    if st.button("Convert"):
        paths = convert_pdf_to_images(
            st.session_state["uploaded_pdf"],
            st.session_state["pdf_basename"]
        )
        st.session_state["image_paths"] = paths
        st.session_state["current_image_index"] = 0
        st.success(f"{len(paths)} pages converted!")

    # Prévisualisation multi-pages
    if "image_paths" in st.session_state:
        paths = st.session_state["image_paths"]
        idx = st.session_state["current_image_index"]

        with open(paths[idx], "rb") as img_file:
            img_bytes = img_file.read()

        img_b64 = base64.b64encode(img_bytes).decode("utf-8")

        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{img_b64}" 
                    style="border: 3px solid black; border-radius: 4px; width: 700px;">
            </div>
            <p style="text-align:center;"><em>Page {idx+1}/{len(paths)}</em></p>
            """,
            unsafe_allow_html=True
        )


        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Previous Image", key="prev_img") and idx > 0:
                st.session_state["current_image_index"] -= 1

        with col2:
            if st.button("Next Image ➡", key="next_img") and idx < len(paths) - 1:
                st.session_state["current_image_index"] += 1

# TAB 3 : OCR
with tabs[2]:
    st.header("Run OCR on images")

    if st.button("Run OCR"):
        texts = run_ocr_on_images(st.session_state["pdf_basename"])
        st.session_state["ocr_texts"] = list(texts.values())
        st.session_state["current_ocr_index"] = 0
        st.success("OCR done!")

    # Affichage multi-pages OCR
    if "ocr_texts" in st.session_state:
        texts = st.session_state["ocr_texts"]
        idx = st.session_state["current_ocr_index"]

        st.text_area(f"OCR Text – Page {idx+1}/{len(texts)}", texts[idx], height=300)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("⬅ Previous OCR", key="prev_ocr") and idx > 0:
                st.session_state["current_ocr_index"] -= 1

        with col2:
            if st.button("Next OCR ➡", key="next_ocr") and idx < len(texts) - 1:
                st.session_state["current_ocr_index"] += 1

# TAB 4 : Extraction
with tabs[3]:
    st.header("Extract structured data")

    mode = st.radio("Choose extraction mode:", [
        "OCR + LLM (FAST, text-only with auto document detection)",
        "OCR + Image + Vision Model (SLOW)"
    ])

    if st.button("Run Extraction"):
        mode_key = "text" if mode.startswith("OCR") else "vision"
        result = process_document(st.session_state["uploaded_pdf"], mode_key)
        st.json(result)
        st.session_state["result_json"] = result


# TAB 5 : Resultas
with tabs[4]:
    st.header("Final JSON Result")

    if "result_json" in st.session_state:
        st.json(st.session_state["result_json"])

        if st.button("Save JSON"):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = f"output/json/contract_{ts}.json"
            with open(path, "w", encoding="utf-8") as f:
                json.dump(st.session_state["result_json"], f, indent=4)

            st.success(f"Saved: {path}")
    else:
        st.info("Run extraction first.")


# TAB 6 : Chercher une information dans le pdf
with tabs[5]:
    st.header("Locate information inside the PDF")

    if "result_json" not in st.session_state:
        st.info("Run extraction first.")
    else:
        result = st.session_state["result_json"]
        st.subheader("Select a field to locate")
        flat = {
            "document_type": result.get("document_type", "")
        }

        def flatten(d, parent=""):
            for k, v in d.items():
                key = f"{parent}.{k}" if parent else k
                if isinstance(v, dict):
                    flatten(v, key)
                elif isinstance(v, list):
                    continue
                else:
                    flat[key] = v

        flatten(result)

        field = st.selectbox("Choose a field", list(flat.keys()))

        if st.button("Locate"):
            value = flat[field]

            if not value:
                st.error("This field is empty.")
            else:
                found = False
                for i, img_path in enumerate(st.session_state["image_paths"]):
                    from utils.search import find_field_location
                    from utils.annotate import draw_bbox

                    bbox = find_field_location(value, img_path)
                    if bbox:
                        highlighted = draw_bbox(img_path, bbox)

                        st.success(f"Found on page {i+1}")
                        st.image(highlighted, width=700)
                        found = True
                        break

                if not found:
                    st.error("Value not found in OCR text.")