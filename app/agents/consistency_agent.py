from typing import Dict, List


def normalize_name(name: str):
    if not name:
        return ""

    return (
        name.lower()
        .strip()
        .replace(".", "")
    )


def extract_patient_names(
    documents: List[Dict]
):
    patient_names = []

    for doc in documents:

        patient_name = (
            doc.get(
                "patient_name_on_doc"
            )
            or
            doc.get("content", {}).get(
                "patient_name"
            )
        )

        if patient_name:

            patient_names.append({
                "document_type": doc[
                    "actual_type"
                ],
                "patient_name": patient_name
            })

    return patient_names


def evaluate_document_consistency(
    documents: List[Dict]
):
    patient_entries = extract_patient_names(
        documents
    )

    normalized_names = [
        normalize_name(
            item["patient_name"]
        )
        for item in patient_entries
    ]

    unique_names = list(
        set(normalized_names)
    )

    if len(unique_names) > 1:

        return {
            "passed": False,
            "reason": (
                "PATIENT_NAME_MISMATCH"
            ),
            "details": patient_entries
        }

    return {
        "passed": True,
        "reason": "CONSISTENT_DOCUMENTS"
    }