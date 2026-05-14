import json

from app.llm.groq_client import (
    call_groq
)


def build_extraction_prompt(
    raw_document_text: str
):
    return f"""
Extract structured medical insurance information
from the following document.

Return ONLY valid JSON.

Required JSON structure:

{{
    "patient_name": "",
    "doctor_name": "",
    "diagnosis": "",
    "treatment": "",
    "medicines": [],
    "tests_ordered": [],
    "line_items": [],
    "total_amount": 0,
    "confidence_score": 0
}}

Document:
{raw_document_text}
"""


def parse_document(
    raw_document_text: str
):
    prompt = build_extraction_prompt(
        raw_document_text
    )

    response = call_groq(prompt)

    cleaned_response = (
        response
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    try:
        parsed = json.loads(
            cleaned_response
        )

        return {
            "status": "SUCCESS",
            "parsed_content": parsed
        }

    except Exception:

        return {
            "status": "FAILED",
            "parsed_content": {},
            "raw_response": response
        }