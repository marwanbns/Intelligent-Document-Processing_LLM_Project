# Intelligent-Document-Processing_LLM_Project
Projet d’**Intelligent Document Processing (IDP)** utilisant l’OCR et des modèles de LLM multimodaux pour extraire automatiquement des informations structurées à partir de documents PDF scannés (factures, cartes d’identité, certificats, contrats).

Le projet met en œuvre un pipeline complet combinant OCR, détection automatique du type de document, raisonnement sémantique via LLM, et visualisation interactive.

- 📄 **Traitement de documents PDF** : conversion des pages en images.
- 🔤 **OCR** : extraction du texte avec Tesseract.
- 🧠 **IA Générative** : extraction d’informations structurées via Meta-Llama (Hugging Face API).
- 👁️ **Multimodal (optionnel)** : raisonnement image + texte avec LLaVA via Ollama.
- 📦 **Sortie structurée** : génération de fichiers JSON suivant des schémas définis.
- 🖥 **Interface Streamlit** : upload, preview, OCR, extraction et localisation des informations.

## Installation 

> [!WARNING]
> Necessite d'avoir l'OCR Tesseract installer.

```bash
git clone https://github.com/marwanbns/Intelligent-Document-Processing_LLM_Project.git
cd Intelligent-Document-Processing_LLM_Project
pip install -r requirements.txt
```

## Configuration
Définir la clé API Hugging Face dans une variable d’environnement :
```bash
export HF_TOKEN_LLM="hf_xxxxxxxx"
```

## Arborescence
```bash
C:.
│   app.py
│   requirements.txt
│
├───input
├───output
│   └───json
├───temp
│   ├───images
│   ├───logs
│   └───text
└───utils
        annotate.py
        convert.py
        detect_type.py
        extract_text_llm.py
        extract_vision.py
        ocr.py
        pipeline.py
        schemas.py
        search.py
```

## Utilisation
Ouvrir une invite de commande (cmd)
```bash
streamlit run app.py
```

## Fonctionnement
1. Upload d’un document PDF

2. Transformation PDF en images et visualisation des pages

3. Extraction OCR page par page

4. Requête API vers le LLM avec extraction structurée (JSON)

5. Localisation visuelle des informations extraites

## Auteur
Projet développé par Marwan bns et Lucas M