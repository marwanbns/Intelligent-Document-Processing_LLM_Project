import os
import json
from huggingface_hub import InferenceClient

MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"

def extract_with_text_llm(ocr_text: str, schema: dict) -> str:

    token = os.getenv("HF_TOKEN_LLM")
    client = InferenceClient(api_key=token)

    prompt = f"""
You are an AI system specialized in contract information extraction.

Your task:
- Read the OCR text of a contract.
- Extract structured data that matches STRICTLY the following JSON schema.
- If a field is missing, set it to null or an empty string (according to its type).
- Output ONLY valid JSON. No explanation, no markdown.

JSON SCHEMA:
{json.dumps(schema, indent=2)}

OCR TEXT:
{ocr_text}
"""
    print("\n================ PROMPT SENT TO HF LLM =================\n")
    print(prompt)
    print("\n========================================================\n")
    completion = client.chat_completion(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.1
    )

    return completion.choices[0].message.content