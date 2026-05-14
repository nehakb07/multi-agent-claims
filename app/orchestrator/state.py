from typing import TypedDict, Dict, Any


class ClaimPipelineState(TypedDict):
    input_claim: Dict[str, Any]

    validation_result: Dict[str, Any]

    consistency_result: Dict[str, Any]

    final_decision: Dict[str, Any]