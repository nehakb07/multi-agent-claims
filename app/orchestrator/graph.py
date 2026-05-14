from langgraph.graph import (
    StateGraph,
    END
)

from app.orchestrator.state import (
    ClaimPipelineState
)

from app.agents.document_validation_agent import (
    validate_documents
)

from app.agents.consistency_agent import (
    evaluate_document_consistency
)

from app.agents.decision_agent import (
    generate_claim_decision
)


# ----------------------------------------
# DOCUMENT VALIDATION NODE
# ----------------------------------------

def validation_node(
    state: ClaimPipelineState
):
    result = validate_documents(
        state["input_claim"]
    )

    state["validation_result"] = result

    return state


# ----------------------------------------
# CONSISTENCY NODE
# ----------------------------------------

def consistency_node(
    state: ClaimPipelineState
):
    result = evaluate_document_consistency(
        state["input_claim"]["documents"]
    )

    state["consistency_result"] = result

    return state


# ----------------------------------------
# DECISION NODE
# ----------------------------------------

def decision_node(
    state: ClaimPipelineState
):
    result = generate_claim_decision(
        state["input_claim"]
    )

    state["final_decision"] = result

    return state


# ----------------------------------------
# VALIDATION FAILURE NODE
# ----------------------------------------

def validation_failure_node(
    state: ClaimPipelineState
):
    validation_result = state[
        "validation_result"
    ]

    state["final_decision"] = {
        "decision": "REJECTED",
        "approved_amount": 0,
        "confidence_score": 0.95,
        "reasons": [
            validation_result["message"]
        ],
        "trace": [
            validation_result["trace"]
        ]
    }

    return state


# ----------------------------------------
# CONSISTENCY FAILURE NODE
# ----------------------------------------

def consistency_failure_node(
    state: ClaimPipelineState
):
    consistency_result = state[
        "consistency_result"
    ]

    state["final_decision"] = {
        "decision": "REJECTED",
        "approved_amount": 0,
        "confidence_score": 0.90,
        "reasons": [
            (
                "Uploaded documents belong "
                "to different patients."
            )
        ],
        "trace": [
            {
                "step": "CONSISTENCY_CHECK",
                "status": "FAILED",
                "details": consistency_result
            }
        ]
    }

    return state


# ----------------------------------------
# ROUTERS
# ----------------------------------------

def validation_router(
    state: ClaimPipelineState
):
    validation_result = state[
        "validation_result"
    ]

    if validation_result["status"] == "FAILED":
        return "validation_failure_node"

    return "consistency_node"


def consistency_router(
    state: ClaimPipelineState
):
    consistency_result = state[
        "consistency_result"
    ]

    if not consistency_result["passed"]:
        return "consistency_failure_node"

    return "decision_node"


# ----------------------------------------
# GRAPH
# ----------------------------------------

graph = StateGraph(
    ClaimPipelineState
)

graph.add_node(
    "validation_node",
    validation_node
)

graph.add_node(
    "consistency_node",
    consistency_node
)

graph.add_node(
    "decision_node",
    decision_node
)

graph.add_node(
    "validation_failure_node",
    validation_failure_node
)

graph.add_node(
    "consistency_failure_node",
    consistency_failure_node
)

graph.set_entry_point(
    "validation_node"
)

graph.add_conditional_edges(
    "validation_node",
    validation_router
)

graph.add_conditional_edges(
    "consistency_node",
    consistency_router
)

graph.add_edge(
    "decision_node",
    END
)

graph.add_edge(
    "validation_failure_node",
    END
)

graph.add_edge(
    "consistency_failure_node",
    END
)

claim_pipeline = graph.compile()