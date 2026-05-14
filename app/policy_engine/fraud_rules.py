from typing import List, Dict

from app.policy_engine.policy_loader import (
    load_policy
)


def evaluate_same_day_claims(
    claims_history: List[Dict],
    treatment_date: str
):
    same_day_claims = [
        claim
        for claim in claims_history
        if claim["date"] == treatment_date
    ]

    return same_day_claims


def calculate_fraud_score(
    same_day_claim_count: int,
    monthly_claim_count: int,
    claimed_amount: float,
    high_value_threshold: float
):
    fraud_score = 0.0

    if same_day_claim_count > 2:
        fraud_score += 0.5

    if monthly_claim_count > 6:
        fraud_score += 0.2

    if claimed_amount > high_value_threshold:
        fraud_score += 0.2

    return min(fraud_score, 1.0)


def evaluate_fraud_risk(
    claims_history: List[Dict],
    treatment_date: str,
    claimed_amount: float
):
    policy = load_policy()

    fraud_thresholds = policy["fraud_thresholds"]

    same_day_limit = fraud_thresholds[
        "same_day_claims_limit"
    ]

    monthly_limit = fraud_thresholds[
        "monthly_claims_limit"
    ]

    high_value_threshold = fraud_thresholds[
        "high_value_claim_threshold"
    ]

    manual_review_threshold = fraud_thresholds[
        "fraud_score_manual_review_threshold"
    ]

    same_day_claims = evaluate_same_day_claims(
        claims_history,
        treatment_date
    )

    same_day_count = len(same_day_claims)

    monthly_claim_count = len(claims_history)

    fraud_score = calculate_fraud_score(
        same_day_claim_count=same_day_count,
        monthly_claim_count=monthly_claim_count,
        claimed_amount=claimed_amount,
        high_value_threshold=high_value_threshold
    )

    signals = []

    if same_day_count > same_day_limit:

        signals.append({
            "signal": "EXCESSIVE_SAME_DAY_CLAIMS",
            "count": same_day_count,
            "threshold": same_day_limit
        })

    if monthly_claim_count > monthly_limit:

        signals.append({
            "signal": "EXCESSIVE_MONTHLY_CLAIMS",
            "count": monthly_claim_count,
            "threshold": monthly_limit
        })

    if claimed_amount > high_value_threshold:

        signals.append({
            "signal": "HIGH_VALUE_CLAIM",
            "amount": claimed_amount,
            "threshold": high_value_threshold
        })

    requires_manual_review = (
        fraud_score >= manual_review_threshold
        or same_day_count > same_day_limit
    )

    return {
        "fraud_score": fraud_score,
        "signals": signals,
        "manual_review_required": requires_manual_review
    }