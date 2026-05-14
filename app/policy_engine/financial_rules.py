from typing import Dict


def apply_network_discount(
    amount: float,
    network_discount_percent: float
):
    discount_multiplier = 1 - (
        network_discount_percent / 100
    )

    return round(
        amount * discount_multiplier,
        2
    )


def apply_copay(
    amount: float,
    copay_percent: float
):
    copay_multiplier = 1 - (
        copay_percent / 100
    )

    return round(
        amount * copay_multiplier,
        2
    )


def check_per_claim_limit(
    claimed_amount: float,
    category_rules: Dict,
    default_limit: float,
    is_network_hospital: bool = False
):
    """
    Network hospitals use the broader
    policy-level limit after discounts.

    Non-network hospitals use
    category-specific sub-limits.
    """

    if is_network_hospital:

        category_limit = float(default_limit)

    else:

        category_limit = float(
            category_rules.get(
                "sub_limit",
                default_limit
            )
        )

    claimed_amount = float(claimed_amount)

    return claimed_amount <= category_limit


def calculate_final_approved_amount(
    claimed_amount: float,
    category_rules: Dict,
    is_network_hospital: bool = False
):
    amount = claimed_amount

    breakdown = []

    # ----------------------------------------
    # NETWORK DISCOUNT
    # ----------------------------------------

    if is_network_hospital:

        network_discount = category_rules.get(
            "network_discount_percent",
            0
        )

        discounted_amount = apply_network_discount(
            amount,
            network_discount
        )

        breakdown.append({
            "step": "NETWORK_DISCOUNT",
            "original_amount": amount,
            "discount_percent": network_discount,
            "amount_after_discount": discounted_amount
        })

        amount = discounted_amount

    # ----------------------------------------
    # COPAY
    # ----------------------------------------

    copay_percent = category_rules.get(
        "copay_percent",
        0
    )

    final_amount = apply_copay(
        amount,
        copay_percent
    )

    breakdown.append({
        "step": "COPAY",
        "amount_before_copay": amount,
        "copay_percent": copay_percent,
        "final_amount": final_amount
    })

    return {
        "approved_amount": round(
            final_amount,
            2
        ),
        "breakdown": breakdown
    }