from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class DecisionBreakdown(BaseModel):
    approved_items: Optional[List[Dict[str, Any]]] = []

    rejected_items: Optional[List[Dict[str, Any]]] = []


class ClaimDecisionResponse(BaseModel):
    decision: Optional[str]

    approved_amount: Optional[float]

    confidence_score: float

    reasons: List[str]

    recommendations: List[str]

    breakdown: Optional[DecisionBreakdown] = None

    trace: List[Dict[str, Any]]