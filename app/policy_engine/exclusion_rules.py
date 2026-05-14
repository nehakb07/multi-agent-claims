from typing import List, Dict

from app.policy_engine.policy_loader import (
    load_policy
)


def normalize_text(text: str):
    return text.lower().strip()


def is_excluded_item(
    description: str,
    exclusion_keywords: List[str]
):
    description = normalize_text(description)

    for keyword in exclusion_keywords:
        if normalize_text(keyword) in description:
            return True

    return False


def evaluate_dental_claim(
    line_items: List[Dict]
):
    policy = load_policy()

    dental_rules = policy["opd_categories"]["dental"]

    covered_procedures = [
        normalize_text(item)
        for item in dental_rules["covered_procedures"]
    ]

    excluded_procedures = [
        normalize_text(item)
        for item in dental_rules["excluded_procedures"]
    ]

    approved_items = []

    rejected_items = []

    total_approved_amount = 0

    for item in line_items:

        description = normalize_text(
            item["description"]
        )

        amount = item["amount"]

        if is_excluded_item(
            description,
            excluded_procedures
        ):
            rejected_items.append({
                "description": item["description"],
                "amount": amount,
                "reason": "COSMETIC_PROCEDURE_EXCLUDED"
            })

            continue

        matched = False

        for covered in covered_procedures:

            if covered in description:

                approved_items.append({
                    "description": item["description"],
                    "amount": amount,
                    "reason": "COVERED_PROCEDURE"
                })

                total_approved_amount += amount

                matched = True

                break

        if not matched:
            rejected_items.append({
                "description": item["description"],
                "amount": amount,
                "reason": "PROCEDURE_NOT_COVERED"
            })

    decision = (
        "APPROVED"
        if len(rejected_items) == 0
        else "PARTIAL"
    )

    if total_approved_amount == 0:
        decision = "REJECTED"

    return {
        "decision": decision,
        "approved_amount": total_approved_amount,
        "approved_items": approved_items,
        "rejected_items": rejected_items
    }


def evaluate_general_exclusions(
    diagnosis: str,
    treatment: str = ""
):
    policy = load_policy()

    exclusions = [
        normalize_text(item)
        for item in policy["exclusions"]["conditions"]
    ]

    combined_text = normalize_text(
        diagnosis + " " + treatment
    )

    matched_exclusions = []

    exclusion_keywords = {
        "obesity": "Obesity and weight loss programs",
        "bariatric": "Bariatric surgery",
        "cosmetic": "Cosmetic or aesthetic procedures",
        "infertility": "Infertility and assisted reproduction"
    }

    for keyword, reason in exclusion_keywords.items():

        if keyword in combined_text:

            matched_exclusions.append(reason)

    if matched_exclusions:
        return {
            "passed": False,
            "reasons": matched_exclusions
        }

    return {
        "passed": True,
        "reasons": []
    }