from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class DocumentContent(BaseModel):
    doctor_name: Optional[str] = None
    doctor_registration: Optional[str] = None
    patient_name: Optional[str] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None
    medicines: Optional[List[str]] = []
    tests_ordered: Optional[List[str]] = []
    hospital_name: Optional[str] = None
    total: Optional[float] = None
    line_items: Optional[List[Dict[str, Any]]] = []


class ClaimDocument(BaseModel):
    file_id: str
    file_name: Optional[str] = None

    actual_type: str

    quality: Optional[str] = "GOOD"

    patient_name_on_doc: Optional[str] = None

    content: Optional[DocumentContent] = None


class ClaimInput(BaseModel):
    member_id: str
    policy_id: str

    claim_category: str

    treatment_date: str

    claimed_amount: float

    hospital_name: Optional[str] = None

    ytd_claims_amount: Optional[float] = 0

    claims_history: Optional[List[Dict[str, Any]]] = []

    simulate_component_failure: Optional[bool] = False

    documents: List[ClaimDocument]


class TraceStep(BaseModel):
    step: str
    status: str

    reason: Optional[str] = None

    metadata: Optional[Dict[str, Any]] = {}


class CanonicalClaim(BaseModel):
    claim_id: Optional[str] = None

    input_claim: ClaimInput

    extracted_entities: Optional[Dict[str, Any]] = {}

    validation_status: Optional[str] = "PENDING"

    fraud_score: Optional[float] = 0.0

    confidence_score: Optional[float] = 1.0

    decision: Optional[str] = None

    approved_amount: Optional[float] = None

    reasons: Optional[List[str]] = []

    recommendations: Optional[List[str]] = []

    trace: Optional[List[TraceStep]] = []