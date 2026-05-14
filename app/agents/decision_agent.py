from typing import Dict

from app.policy_engine.financial_rules import (
    calculate_final_approved_amount,
    check_per_claim_limit
)

from app.policy_engine.waiting_period_rules import (
    evaluate_waiting_period
)

from app.policy_engine.exclusion_rules import (
    evaluate_general_exclusions,
    evaluate_dental_claim
)

from app.policy_engine.preauth_rules import (
    evaluate_preauthorization_requirement
)

from app.policy_engine.fraud_rules import (
    evaluate_fraud_risk
)

from app.policy_engine.policy_loader import (
    load_policy,
    get_claim_category_rules
)


def generate_claim_decision(
    claim_input: Dict
):
    policy = load_policy()

    trace = []

    confidence_score = 1.0

    category = claim_input["claim_category"]

    category_rules = get_claim_category_rules(
        category
    )
    print("CATEGORY:", category)
    print("CATEGORY RULES:", category_rules)
    
    claimed_amount = claim_input["claimed_amount"]

    documents = claim_input["documents"]

    member_id = claim_input["member_id"]

    treatment_date = claim_input["treatment_date"]
    
    is_network_hospital = (
        claim_input.get("hospital_name")
        in policy["network_hospitals"]
    )

    # ----------------------------------------
    # PRESCRIPTION EXTRACTION
    # ----------------------------------------

    prescription_doc = next(
        (
            doc for doc in documents
            if doc["actual_type"] == "PRESCRIPTION"
        ),
        None
    )

    diagnosis = ""

    treatment = ""

    if prescription_doc:

        diagnosis = (
            prescription_doc
            ["content"]
            .get("diagnosis", "")
        )

        treatment = (
            prescription_doc
            ["content"]
            .get("treatment", "")
        )
        
        # ----------------------------------------
        # DOCUMENT CONSISTENCY CHECK
        # ----------------------------------------
    from app.agents.consistency_agent import (
            evaluate_document_consistency
        )
    consistency_result = (
        evaluate_document_consistency(
            documents
        )
    )

    if not consistency_result["passed"]:

        trace.append({
            "step": "CONSISTENCY_CHECK",
            "status": "FAILED",
            "details": consistency_result
        })

        return {
            "decision": "REJECTED",
            "approved_amount": 0,
            "confidence_score": confidence_score,
            "reasons": [
                "DOCUMENT_INCONSISTENCY"
            ],
            "trace": trace
        }

    trace.append({
        "step": "CONSISTENCY_CHECK",
        "status": "PASSED"
    })
        
    # ----------------------------------------
    # EXCLUSION CHECK
    # ----------------------------------------

    exclusion_result = evaluate_general_exclusions(
        diagnosis=diagnosis,
        treatment=treatment
    )

    if not exclusion_result["passed"]:

        trace.append({
            "step": "EXCLUSION_CHECK",
            "status": "FAILED",
            "details": exclusion_result
        })

        return {
            "decision": "REJECTED",
            "approved_amount": 0,
            "confidence_score": confidence_score,
            "reasons": ["EXCLUDED_CONDITION"],
            "trace": trace
        }

    trace.append({
        "step": "EXCLUSION_CHECK",
        "status": "PASSED"
    })

    # ----------------------------------------
    # PREAUTH CHECK
    # ----------------------------------------

    if category == "DIAGNOSTIC":

        bill_doc = next(
            (
                doc for doc in documents
                if doc["actual_type"] == "HOSPITAL_BILL"
            ),
            None
        )

        if bill_doc:

            line_items = (
                bill_doc["content"]
                .get("line_items", [])
            )

            preauth_result = (
                evaluate_preauthorization_requirement(
                    claim_amount=claimed_amount,
                    line_items=line_items
                )
            )

            if not preauth_result["passed"]:

                trace.append({
                    "step": "PREAUTH_CHECK",
                    "status": "FAILED",
                    "details": preauth_result
                })

                return {
                    "decision": "REJECTED",
                    "approved_amount": 0,
                    "confidence_score": confidence_score,
                    "reasons": ["PRE_AUTH_MISSING"],
                    "trace": trace
                }

        trace.append({
            "step": "PREAUTH_CHECK",
            "status": "PASSED"
        })

    # ----------------------------------------
    # WAITING PERIOD
    # ----------------------------------------

    waiting_result = evaluate_waiting_period(
        member_id=member_id,
        treatment_date=treatment_date,
        diagnosis=diagnosis
    )

    if not waiting_result["passed"]:

        trace.append({
            "step": "WAITING_PERIOD",
            "status": "FAILED",
            "details": waiting_result
        })

        return {
            "decision": "REJECTED",
            "approved_amount": 0,
            "confidence_score": confidence_score,
            "reasons": ["WAITING_PERIOD"],
            "trace": trace
        }

    trace.append({
        "step": "WAITING_PERIOD",
        "status": "PASSED"
    })

    # ----------------------------------------
    # FRAUD CHECK
    # ----------------------------------------

    fraud_result = evaluate_fraud_risk(
        claims_history=claim_input.get(
            "claims_history",
            []
        ),
        treatment_date=treatment_date,
        claimed_amount=claimed_amount
    )

    if fraud_result["manual_review_required"]:

        confidence_score -= 0.3

        trace.append({
            "step": "FRAUD_CHECK",
            "status": "MANUAL_REVIEW",
            "details": fraud_result
        })

        return {
            "decision": "MANUAL_REVIEW",
            "approved_amount": 0,
            "confidence_score": round(
                confidence_score,
                2
            ),
            "reasons": [
                "SUSPICIOUS_CLAIM_PATTERN"
            ],
            "trace": trace
        }

    trace.append({
        "step": "FRAUD_CHECK",
        "status": "PASSED"
    })

    # ----------------------------------------
    # DENTAL LINE ITEM EVALUATION
    # ----------------------------------------

    if category == "DENTAL":

        bill_doc = next(
            (
                doc for doc in documents
                if doc["actual_type"] == "HOSPITAL_BILL"
            ),
            None
        )

        line_items = (
            bill_doc["content"]
            .get("line_items", [])
        )

        dental_result = evaluate_dental_claim(
            line_items
        )

        approved_amount = dental_result[
            "approved_amount"
        ]

        per_claim_limit = policy["coverage"][
            "per_claim_limit"
        ]

        limit_check = check_per_claim_limit(
            approved_amount,
            category_rules,
            per_claim_limit,
            is_network_hospital=is_network_hospital
        )

        if not limit_check:

            trace.append({
                "step": "PER_CLAIM_LIMIT",
                "status": "FAILED"
            })

            return {
                "decision": "REJECTED",
                "approved_amount": 0,
                "confidence_score": confidence_score,
                "reasons": ["PER_CLAIM_EXCEEDED"],
                "trace": trace
            }

        trace.append({
            "step": "DENTAL_EVALUATION",
            "status": dental_result["decision"]
        })

        return {
            "decision": dental_result["decision"],
            "approved_amount": approved_amount,
            "confidence_score": confidence_score,
            "approved_items": dental_result[
                "approved_items"
            ],
            "rejected_items": dental_result[
                "rejected_items"
            ],
            "trace": trace
        }

    # ----------------------------------------
    # FINANCIAL CALCULATIONS
    # ----------------------------------------

    

    financial_result = (
        calculate_final_approved_amount(
            claimed_amount=claimed_amount,
            category_rules=category_rules,
            is_network_hospital=is_network_hospital
        )
    )

    approved_amount = financial_result[
        "approved_amount"
    ]

    trace.append({
        "step": "FINANCIAL_CALCULATION",
        "status": "PASSED",
        "details": financial_result
    })

    # ----------------------------------------
    # PER CLAIM LIMIT
    # ----------------------------------------

    per_claim_limit = policy["coverage"][
        "per_claim_limit"
    ]

    limit_check = check_per_claim_limit(
        approved_amount,
        category_rules,
        per_claim_limit
    )

    if not limit_check:

        trace.append({
            "step": "PER_CLAIM_LIMIT",
            "status": "FAILED",
            "reason": (
                f"Approved amount "
                f"{approved_amount} "
                f"exceeds limit "
                f"{per_claim_limit}"
            )
        })

        return {
            "decision": "REJECTED",
            "approved_amount": 0,
            "confidence_score": confidence_score,
            "reasons": ["PER_CLAIM_EXCEEDED"],
            "trace": trace
        }

    trace.append({
        "step": "PER_CLAIM_LIMIT",
        "status": "PASSED"
    })

    # ----------------------------------------
    # COMPONENT FAILURE SIMULATION
    # ----------------------------------------

    if claim_input.get(
        "simulate_component_failure"
    ):

        confidence_score -= 0.25

        trace.append({
            "step": "COMPONENT_FAILURE",
            "status": "FAILED",
            "reason": (
                "Simulated component failure"
            )
        })

        recommendation = (
            "Manual review recommended "
            "due to partial pipeline failure."
        )

    else:
        recommendation = None

    # ----------------------------------------
    # FINAL APPROVAL
    # ----------------------------------------

    return {
        "decision": "APPROVED",
        "approved_amount": approved_amount,
        "confidence_score": round(
            confidence_score,
            2
        ),
        "reasons": [],
        "recommendations": (
            [recommendation]
            if recommendation
            else []
        ),
        "trace": trace
    }