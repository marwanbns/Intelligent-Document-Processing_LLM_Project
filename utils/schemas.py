# utils/schemas.py
CONTRACT_SCHEMA = {
    "document_type": "contract",
    "contract_title": "",
    "parties": {
        "party_1": {"name": "", "address": ""},
        "party_2": {"name": "", "address": ""}
    },
    "dates": {
        "signature_party_1": "",
        "signature_party_2": "",
        "start_date": "",
        "end_date": ""
    },
    "contract_summary": "",
    "key_clauses": []
}

ID_CARD_SCHEMA = {
    "document_type": "id_card",
    "full_name": "",
    "birth_name": "",
    "gender": "",
    "date_of_birth": "",
    "place_of_birth": "",
    "nationality": "",
    "document_number": "",
    "expiration_date": "",
    "issue_date": "",
    "issuing_authority": "",
    "address": ""
}

INVOICE_SCHEMA = {
    "document_type": "invoice",
    "invoice_number": "",
    "invoice_date": "",
    "due_date": "",
    "seller": {
        "name": "",
        "address": "",
        "vat_number": ""
    },
    "buyer": {
        "name": "",
        "address": "",
        "vat_number": ""
    },
    "items": [
        {"description": "", "quantity": "", "unit_price": "", "total_price": ""}
    ],
    "totals": {
        "subtotal": "",
        "tax": "",
        "total_due": ""
    }
}

CERTIFICATE_SCHEMA = {
    "document_type": "certificate",
    "certificate_title": "",
    "recipient": {
        "full_name": "",
        "birth_date": ""
    },
    "issuing_organization": "",
    "issue_date": "",
    "program_or_degree": "",
    "result_or_level": "",
    "validity_period": "",
    "signatures": []
}

SCHEMAS = {
    "contract": CONTRACT_SCHEMA,
    "id_card": ID_CARD_SCHEMA,
    "invoice": INVOICE_SCHEMA,
    "certificate": CERTIFICATE_SCHEMA
}