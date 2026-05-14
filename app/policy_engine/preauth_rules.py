from typing import List, Dict

from app.policy_engine.policy_loader import (
    load_policy
)


def normalize_text(text: str):
    return text.lower().strip()


def contains_high_value_test(
    line_items: List[Dict],
    high_value_tests: List[str]
):
    detected_tests = []

    for item in line_items:

        description = normalize_text(
            item["description"]
        )

        for test_name in high_value_tests:

            if normalize_text(test_name) in description:

                detected_tests.append({
                    "test_name": test_name,
                    "amount": item["amount"]
                })

    return detected_tests


def evaluate_preauthorization_requirement(
    claim_amount: float,
    line_items: List[Dict]
):
    policy = load_policy()

    diagnostic_rules = (
        policy["opd_categories"]["diagnostic"]
    )

    threshold = diagnostic_rules.get(
        "pre_auth_threshold",
        10000
    )

    high_value_tests = diagnostic_rules.get(
        "high_value_tests_requiring_pre_auth",
        []
    )

    detected_tests = contains_high_value_test(
        line_items,
        high_value_tests
    )

    if not detected_tests:
        return {
            "passed": True,
            "reason": "NO_PREAUTH_REQUIRED"
        }

    requires_preauth = False

    triggering_tests = []

    for detected in detected_tests:

        if detected["amount"] > threshold:

            requires_preauth = True

            triggering_tests.append(detected)

    if requires_preauth:
        return {
            "passed": False,
            "reason": "PRE_AUTH_REQUIRED",
            "triggering_tests": triggering_tests,
            "threshold": threshold
        }

    return {
        "passed": True,
        "reason": "PREAUTH_NOT_REQUIRED"
    }