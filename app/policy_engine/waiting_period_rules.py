from datetime import datetime

from app.policy_engine.policy_loader import (
    load_policy,
    get_member
)


DATE_FORMAT = "%Y-%m-%d"


def calculate_days_between(
    start_date: str,
    end_date: str
):
    start = datetime.strptime(start_date, DATE_FORMAT)

    end = datetime.strptime(end_date, DATE_FORMAT)

    return (end - start).days


def detect_waiting_period_condition(
    diagnosis: str
):
    diagnosis = diagnosis.lower()

    mapping = {
        "diabetes": "diabetes",
        "hypertension": "hypertension",
        "thyroid": "thyroid_disorders",
        "maternity": "maternity",
        "obesity": "obesity_treatment",
        "hernia": "hernia",
        "cataract": "cataract",
        "mental": "mental_health"
    }

    for keyword, condition_key in mapping.items():
        if keyword in diagnosis:
            return condition_key

    return None


def evaluate_waiting_period(
    member_id: str,
    treatment_date: str,
    diagnosis: str
):
    policy = load_policy()

    member = get_member(member_id)

    if not member:
        return {
            "passed": False,
            "reason": "INVALID_MEMBER"
        }

    join_date = member["join_date"]

    days_since_joining = calculate_days_between(
        join_date,
        treatment_date
    )

    condition_key = detect_waiting_period_condition(
        diagnosis
    )

    if not condition_key:
        return {
            "passed": True,
            "reason": "NO_WAITING_PERIOD_APPLICABLE"
        }

    waiting_period_days = (
        policy["waiting_periods"]
        ["specific_conditions"]
        .get(condition_key)
    )

    if not waiting_period_days:
        return {
            "passed": True,
            "reason": "NO_WAITING_RULE_FOUND"
        }

    if days_since_joining < waiting_period_days:

        eligible_after_days = (
            waiting_period_days - days_since_joining
        )

        return {
            "passed": False,
            "reason": "WAITING_PERIOD_ACTIVE",
            "condition": condition_key,
            "days_remaining": eligible_after_days,
            "required_waiting_days": waiting_period_days,
            "days_completed": days_since_joining
        }

    return {
        "passed": True,
        "reason": "WAITING_PERIOD_COMPLETED",
        "condition": condition_key
    }