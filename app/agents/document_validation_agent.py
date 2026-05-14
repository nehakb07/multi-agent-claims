from app.policy_engine.policy_loader import (
    get_document_requirements
)


def validate_documents(claim):
    category = claim["claim_category"]

    document_rules = get_document_requirements(
        category
    )

    required_documents = document_rules.get(
        "required",
        []
    )

    uploaded_documents = [
        doc["actual_type"]
        for doc in claim["documents"]
    ]

    missing_documents = [
        doc
        for doc in required_documents
        if doc not in uploaded_documents
    ]

    unreadable_documents = [
        doc["file_name"]
        for doc in claim["documents"]
        if doc.get("quality") == "UNREADABLE"
    ]

    if unreadable_documents:

        return {
            "status": "FAILED",
            "message": (
                f"The following documents are unreadable: "
                f"{', '.join(unreadable_documents)}. "
                f"Please re-upload clear copies."
            ),
            "missing_documents": [],
            "trace": {
                "step": "DOCUMENT_VALIDATION",
                "status": "FAILED",
                "reason": "UNREADABLE_DOCUMENT"
            }
        }

    if missing_documents:

        return {
            "status": "FAILED",
            "message": (
                f"You uploaded {uploaded_documents}, "
                f"but {category} claims require "
                f"{missing_documents}."
            ),
            "missing_documents": missing_documents,
            "trace": {
                "step": "DOCUMENT_VALIDATION",
                "status": "FAILED",
                "reason": "MISSING_REQUIRED_DOCUMENTS"
            }
        }

    return {
        "status": "PASSED",
        "message": (
            "All required documents are present."
        ),
        "missing_documents": [],
        "trace": {
            "step": "DOCUMENT_VALIDATION",
            "status": "PASSED"
        }
    }