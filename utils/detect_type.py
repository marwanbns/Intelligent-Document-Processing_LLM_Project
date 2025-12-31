# utils/detect_type.py
import os
from huggingface_hub import InferenceClient

MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

def detect_document_type(full_text: str) -> str:
    """
    Robust document classification using keywords + LLM reasoning + examples.
    """

    lower = full_text.lower()
    print("=== FULL OCR TEXT ===")
    print(full_text)
    print("=====================")

    # ID CARD : mots-clés plus spécifiques
    id_keywords = [
        "carte nationale d'identité",
        "national identity card",
        "né(e) le",
        "née le",
        "date de naissance",
        "place of birth",
        "nationalité",
        "mrz",
        "idfr",            # pour les MRZ françaises
        "numéro de carte"
    ]
    if any(k in lower for k in id_keywords):
        return "id_card"

    # INVOICE / FACTURE : mots-clés typiques
    invoice_keywords = [
        "invoice",
        "facture ",
        "facture n", "facture no", "facture numéro",
        "total dû", "total du", "total due",
        "sous-total", "subtotal",
        "tva", "vat",
        "échéance", "echeance",
        "solde dû", "solde do",
        "montant", "prix unitaire", "quantité"
    ]
    if any(k in lower for k in invoice_keywords):
        return "invoice"

    # CERTIFICATE
    certificate_keywords = [
        "certificate", "certificat", "attestation", "diplôme",
        "this certifies that", "is hereby awarded", "has completed"
    ]
    if any(k in lower for k in certificate_keywords):
        return "certificate"

    # Sinon -> LLM
    token = os.getenv("HF_TOKEN_LLM")
    client = InferenceClient(api_key=token)

    prompt = f"""
Your task is to classify the document type STRICTLY as one of:
contract, invoice, id_card, certificate.

Use the following examples:

EXAMPLE 1:
Text: "Invoice Number: 5782, Total Due: 120€, VAT..."
Type: invoice

EXAMPLE 2:
Text: "Carte Nationale d'Identité, Nom, Prénom, Né(e) le..."
Type: id_card

EXAMPLE 3:
Text: "This certificate is awarded to..."
Type: certificate

EXAMPLE 4:
Text: "This Agreement is made between Party A and Party B..."
Type: contract

Now classify THIS TEXT:
{full_text}

Answer ONLY with one word:
contract / invoice / id_card / certificate
"""

    completion = client.chat_completion(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=5,
        temperature=0
    )

    result = completion.choices[0].message.content.strip().lower()

    if result not in ["contract", "invoice", "id_card", "certificate"]:
        return "contract"

    return result