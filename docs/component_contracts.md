````md
# Component Contracts - Plum AI Claims Processing Pipeline

This document defines the contracts for all major components in the claims processing pipeline.

Each contract includes:
- purpose,
- input schema,
- output schema,
- failure modes,
- behavioral expectations.

These contracts are designed so that any individual component can be independently reimplemented without reading internal source code.

---

# 1. LLM Parser Agent

## Component

`document_parser_agent.py`

---

## Purpose

Extract structured insurance-relevant information from raw medical document text.

---

## Input

```json
{
  "raw_document_text": "string"
}
````

---

## Output

### Success

```json
{
  "status": "SUCCESS",
  "parsed_content": {
    "patient_name": "string",
    "doctor_name": "string",
    "diagnosis": "string",
    "treatment": "string",
    "medicines": [],
    "tests_ordered": [],
    "line_items": [],
    "total_amount": 0,
    "confidence_score": 0.0
  }
}
```

---

### Failure

```json
{
  "status": "FAILED",
  "parsed_content": {},
  "raw_response": "string"
}
```

---

## Failure Modes

| Failure            | Behavior                       |
| ------------------ | ------------------------------ |
| LLM timeout        | Return FAILED                  |
| Invalid JSON       | Return FAILED                  |
| Empty extraction   | Reduce confidence              |
| Partial extraction | Continue with available fields |

---

# 2. Document Validation Agent

## Component

`document_validation_agent.py`

---

## Purpose

Validate uploaded documents before downstream processing.

---

## Input

```json
{
  "claim_category": "CONSULTATION",
  "documents": [
    {
      "actual_type": "PRESCRIPTION",
      "quality": "GOOD"
    }
  ]
}
```

---

## Output

### Success

```json
{
  "status": "PASSED",
  "message": "All required documents are present.",
  "missing_documents": [],
  "trace": {
    "step": "DOCUMENT_VALIDATION",
    "status": "PASSED"
  }
}
```

---

### Failure

```json
{
  "status": "FAILED",
  "message": "Specific actionable message",
  "missing_documents": [],
  "trace": {
    "step": "DOCUMENT_VALIDATION",
    "status": "FAILED",
    "reason": "UNREADABLE_DOCUMENT"
  }
}
```

---

## Failure Modes

| Failure             | Behavior         |
| ------------------- | ---------------- |
| Missing document    | Fail immediately |
| Wrong document type | Fail immediately |
| Unreadable document | Fail immediately |

---

# 3. Consistency Agent

## Component

`consistency_agent.py`

---

## Purpose

Verify that uploaded documents belong to the same patient.

---

## Input

```json
## Input

```json
{
  "documents": [
    {
      "actual_type": "PRESCRIPTION",
      "content": {
        "patient_name": "Rajesh Kumar"
      }
    },
    {
      "actual_type": "HOSPITAL_BILL",
      "content": {
        "patient_name": "Rajesh Kumar"
      }
    }
  ]
}
```

---

## Output

### Success

```json
{
  "passed": false,
  "reason": "PATIENT_NAME_MISMATCH",
  "details": [
    {
      "document_type": "PRESCRIPTION",
      "patient_name": "Rajesh Kumar"
    },
    {
      "document_type": "HOSPITAL_BILL",
      "patient_name": "Arjun Mehta"
    }
  ]
}
```

---

### Failure

```json
{
  "passed": false,
  "reason": "PATIENT_NAME_MISMATCH",
  "details": []
}
```

---

## Failure Modes

| Failure               | Behavior                  |
| --------------------- | ------------------------- |
| Name mismatch         | Reject claim              |
| Missing patient names | Escalate to manual review |

---

# 4. Exclusion Engine

## Component

`exclusion_rules.py`

---

## Purpose

Check whether treatment or diagnosis falls under policy exclusions.

---

## Input

```json
{
  "diagnosis": "Morbid Obesity",
  "treatment": "Bariatric Surgery"
}
```

---

## Output

### Success

```json
{
  "passed": true
}
```

---

### Failure

```json
{
  "passed": false,
  "reasons": [
    "Bariatric surgery"
  ]
}
```

---

## Failure Modes

| Failure            | Behavior     |
| ------------------ | ------------ |
| Excluded condition | Reject claim |
| Excluded procedure | Reject claim |

---

# 5. Waiting Period Engine

## Component

`waiting_period_rules.py`

---

## Purpose

Verify whether required waiting period has been completed.

---

## Input

```json
{
  "member_id": "EMP001",
  "treatment_date": "2024-11-01",
  "diagnosis": "Diabetes"
}
```

---

## Output

### Success

```json
{
  "passed": true
}
```

---

### Failure

```json
{
  "passed": false,
  "reason": "WAITING_PERIOD_ACTIVE",
  "days_remaining": 45
}
```

---

## Failure Modes

| Failure               | Behavior     |
| --------------------- | ------------ |
| Waiting period active | Reject claim |

---

# 6. Preauthorization Engine

## Component

`preauth_rules.py`

---

## Purpose

Determine whether mandatory preauthorization is required.

---

## Input

```json
{
  "claim_amount": 15000,
  "line_items": []
}
```

---

## Output

### Success

```json
{
  "passed": true
}
```

---

### Failure

```json
{
  "passed": false,
  "reason": "PRE_AUTH_REQUIRED",
  "triggering_tests": []
}
```

---

## Failure Modes

| Failure                  | Behavior     |
| ------------------------ | ------------ |
| Missing preauthorization | Reject claim |

---

# 7. Fraud Engine

## Component

`fraud_rules.py`

---

## Purpose

Detect suspicious claims behavior.

---

## Input

```json
{
  "claims_history": [],
  "claimed_amount": 50000,
  "treatment_date": "2024-11-01"
}
```

---

## Output

```json
{
  "fraud_score": 0.5,
  "signals": [],
  "manual_review_required": true
}
```

---

## Failure Modes

| Failure             | Behavior                         |
| ------------------- | -------------------------------- |
| Suspicious activity | Escalate to manual review        |
| Missing history     | Continue with reduced confidence |

---

# 8. Financial Engine

## Component

`financial_rules.py`

---

## Purpose

Calculate approved payout amount.

---

## Input

```json
{
  "claimed_amount": 10000,
  "category_rules": {},
  "is_network_hospital": false
}
```

---

## Output

```json
{
  "approved_amount": 9000,
  "breakdown": []
}
```

---

## Failure Modes

| Failure                | Behavior           |
| ---------------------- | ------------------ |
| Invalid amount         | Reject calculation |
| Missing category rules | Use default limits |

---

# 9. Decision Agent

## Component

`decision_agent.py`

---

## Purpose

Aggregate outputs from all policy engines and produce final claim decision.

---

## Input

```json
{
  "member_id": "EMP001",
  "claim_category": "CONSULTATION",
  "documents": []
}
```

---

## Output

```json
{
  "decision": "APPROVED",
  "approved_amount": 5000,
  "confidence_score": 1.0,
  "reasons": [],
  "recommendations": [],
  "trace": []
}
```

---

## Possible Decisions

| Decision      | Meaning                   |
| ------------- | ------------------------- |
| APPROVED      | Claim fully approved      |
| PARTIAL       | Partial payout approved   |
| REJECTED      | Claim denied              |
| MANUAL_REVIEW | Human escalation required |

---

## Failure Modes

| Failure                   | Behavior                          |
| ------------------------- | --------------------------------- |
| Downstream engine failure | Continue with degraded confidence |
| Invalid policy state      | Escalate to manual review         |

---

# 10. LangGraph Orchestrator

## Component

`graph.py`

---

## Purpose

Coordinate execution order and routing between agents.

---

## Input

```json
{
  "input_claim": {}
}
```

---

## Output

```json
{
  "validation_result": {},
  "consistency_result": {},
  "final_decision": {}
}
```

---

## Routing Behavior

| Condition          | Route                      |
| ------------------ | -------------------------- |
| Validation failed  | Immediate rejection        |
| Consistency failed | Immediate rejection        |
| All checks passed  | Continue to decision agent |

---

# 11. Policy Loader

## Component

`policy_loader.py`

---

## Purpose

Load centralized insurance policy configuration.

---

## Input

```json
{
  "policy_id": "PLUM_GHI_2024"
}
```

---

## Output

```json
{
  "copay_percent": 10,
  "sub_limit": 5000
}
```

---

## Failure Modes

| Failure        | Behavior                           |
| -------------- | ---------------------------------- |
| Missing policy | Reject claim                       |
| Missing rule   | Use fallback/default configuration |

---

# 12. Streamlit Frontend

## Component

`streamlit_app.py`

---

## Purpose

Provide UI for:

* claim submission,
* trace review,
* LLM extraction demo.

---

## Input

* test case selection
* raw medical text

---

## Output

* structured extraction
* final claim decision
* explainable trace

---

# 13. FastAPI Service

## Component

`main.py`

---

## Purpose

Expose backend APIs for claim processing.

---

## Example Endpoint

```http
POST /process_claim
```

---

## Request

```json
{
  "claim": {}
}
```

---

## Response

```json
{
  "decision": "APPROVED"
}
```

---

# 14. Global Failure Handling Principles

All components must:

* fail gracefully,
* avoid system crashes,
* preserve partial outputs,
* expose failure traces,
* adjust confidence appropriately.

---

# 15. Traceability Requirements

Every component must produce:

* step name,
* status,
* reason for failure (if any),
* metadata relevant to the decision.

This ensures:

* auditability,
* operational debugging,
* explainability,
* regulatory trace reconstruction.
