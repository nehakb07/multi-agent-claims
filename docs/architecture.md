````md
# Plum AI Claims Processing Pipeline - Architecture Document

## 1. System Overview

The Plum AI Claims Processing Pipeline is a multi-agent insurance adjudication system designed to automate health insurance claim review workflows.

The system combines:

- LLM-powered document understanding
- deterministic policy adjudication
- fraud detection
- explainable decision tracing
- workflow orchestration using LangGraph

The architecture is intentionally designed to separate:

| Responsibility | Technology |
|---|---|
| Unstructured medical document understanding | LLM |
| Financial and policy decisions | Deterministic rule engines |

This ensures:
- explainability,
- auditability,
- reproducibility,
- regulatory consistency,
- operational scalability.

---

# 2. Problem Statement

Health insurance claims processing is traditionally manual.

When members submit claims, they upload:
- prescriptions,
- bills,
- lab reports,
- pharmacy invoices,
- diagnostic reports.

Operations teams manually:
- verify documents,
- validate policy coverage,
- calculate payouts,
- detect fraud,
- reject invalid claims.

This process is:
- slow,
- inconsistent,
- difficult to scale.

The goal of this system is to automate the end-to-end adjudication workflow while maintaining explainability and deterministic policy enforcement.

---

# 3. High-Level Architecture


                ┌──────────────────────┐
                │ Raw Medical Documents│
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ LLM Parser Agent     │
                │ (Groq)               │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Structured Claim JSON│
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Validation Agent     │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Consistency Agent    │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Decision Agent       │
                └──────────┬───────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
 ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
 │ Exclusion    │ │ Fraud Engine │ │ Financial    │
 │ Engine       │ │              │ │ Engine       │
 └──────────────┘ └──────────────┘ └──────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
                ┌──────────────────────┐
                │ Final Decision       │
                └──────────┬───────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ Explainable Trace    │
                └──────────────────────┘


---

# 4. Core Architectural Principles

## 4.1 Deterministic Decisioning

Insurance claims require:

* auditability,
* regulatory consistency,
* financial reproducibility.

For this reason:

* LLMs are NOT used for payout decisions,
* all adjudication logic is deterministic.

The LLM is restricted to:

* semantic extraction,
* normalization,
* document understanding.

---

## 4.2 Explainability First

Every claim generates:

* a final decision,
* confidence score,
* approved amount,
* detailed execution trace,
* rejection reasons,
* recommendations.

This allows operations teams to reconstruct:

* what happened,
* which checks passed,
* which checks failed,
* why the final outcome occurred.

---

## 4.3 Fail-Fast Validation

Incorrect document uploads are rejected early before expensive downstream processing occurs.

Examples:

* missing hospital bill,
* unreadable prescription,
* mismatched patient names.

This reduces:

* unnecessary computation,
* fraud risk,
* operational ambiguity.

---

## 4.4 Graceful Degradation

Individual components may fail:

* LLM timeout,
* parser failure,
* malformed input,
* extraction ambiguity.

The system continues processing where possible while:

* lowering confidence,
* adding manual review recommendations,
* preserving partial outputs.

---

# 5. System Components

# 5.1 LLM Parser Agent

## Purpose

Extracts structured medical information from raw medical text.

## Responsibilities

* patient extraction
* diagnosis extraction
* medicine extraction
* billing extraction
* treatment extraction
* semantic normalization

## Technology

* Groq API
* Llama 3.3 70B Versatile

## Why LLM Was Used

Medical documents are:

* inconsistent,
* semi-structured,
* noisy,
* difficult to parse using regex/rules.

LLMs are well suited for semantic understanding.

---

# 5.2 Document Validation Agent

## Purpose

Verifies whether correct documents were uploaded.

## Checks

* missing required documents
* unreadable documents
* category-specific requirements

## Example

Consultation claims require:

* prescription
* hospital bill

If missing:

* processing stops immediately,
* user receives actionable feedback.

---

# 5.3 Consistency Agent

## Purpose

Ensures all documents belong to the same patient.

## Checks

* patient name consistency
* cross-document identity matching

## Importance

Prevents:

* mixed claims,
* accidental uploads,
* fraud attempts.

---

# 5.4 Decision Agent

## Purpose

Central orchestration layer for deterministic adjudication.

## Responsibilities

* execute policy engines
* aggregate results
* generate final decision
* compute confidence
* produce explainable trace

---

# 5.5 Exclusion Engine

## Purpose

Rejects excluded conditions and treatments.

## Examples

* cosmetic procedures
* bariatric programs
* weight loss treatments

---

# 5.6 Waiting Period Engine

## Purpose

Enforces treatment waiting periods.

## Example

Diabetes:

* 90-day waiting period.

---

# 5.7 Preauthorization Engine

## Purpose

Ensures mandatory pre-authorization exists for high-risk procedures.

## Example

MRI scans above threshold require:

* prior approval.

---

# 5.8 Fraud Engine

## Purpose

Detects suspicious claims patterns.

## Current Signals

* excessive same-day claims
* unusual claim frequency

## Output

* fraud score
* manual review recommendation

---

# 5.9 Financial Engine

## Purpose

Calculates approved payout amount.

## Handles

* copays
* network discounts
* sub-limits
* per-claim limits

## Why Deterministic

Financial calculations require exact reproducibility.

---

# 6. Policy Configuration Layer

## File

`policy_terms.json`

## Purpose

Centralized configuration-driven insurance rule system.

## Contains

* coverage rules
* copays
* exclusions
* waiting periods
* sub-limits
* member roster
* document requirements

## Architectural Benefit

Separates:

* business configuration
  from:
* business logic

Policy changes can occur without modifying application code.

---

# 7. Workflow Orchestration

## Technology

LangGraph

## Purpose

Coordinates:

* agent execution,
* routing,
* fail-fast behavior,
* graceful recovery.

## Workflow

```text
Validation
    ↓
Consistency
    ↓
Decision Pipeline
    ↓
Final Decision
```

Conditional routing enables:

* early rejection,
* manual review escalation,
* dynamic execution paths.

---

# 8. Frontend Layer

## Streamlit

Provides:

* test case execution
* trace visualization
* LLM extraction demo
* decision review UI

---

# 9. API Layer

## FastAPI

Provides backend endpoints for:

* claim processing
* orchestration
* future integrations

---

# 10. Explainability and Observability

Every decision produces:

* decision type
* approved amount
* confidence score
* reasons
* recommendations
* execution trace

Example:

```text
CONSISTENCY_CHECK - PASSED
EXCLUSION_CHECK - PASSED
WAITING_PERIOD - PASSED
FRAUD_CHECK - PASSED
FINANCIAL_CALCULATION - PASSED
PER_CLAIM_LIMIT - PASSED
```

This enables:

* operational debugging,
* auditability,
* trust,
* reviewer visibility.

---

# 11. Failure Handling Strategy

The system is designed to tolerate:

* parser failures,
* malformed documents,
* partial extraction failures,
* downstream engine errors.

Failure handling strategies include:

* confidence reduction,
* partial approvals,
* manual review escalation,
* trace logging.

---

# 12. Architectural Tradeoffs

## Chosen

### Deterministic adjudication

Used for:

* reliability,
* auditability,
* financial correctness.

### LLM-based extraction

Used for:

* semantic understanding,
* noisy medical text parsing.

---

## Rejected Approaches

### Full LLM decisioning

Rejected because:

* non-deterministic,
* difficult to audit,
* unsuitable for financial approvals.

### OCR-heavy pipelines

Not implemented due to:

* assignment scope,
* absence of image datasets,
* timeline constraints.

The architecture is designed to support OCR in future iterations.

---

# 13. Scalability Considerations

At 10x scale, improvements would include:

## Infrastructure

* asynchronous processing
* distributed workers
* queue-based orchestration

## AI Layer

* batched extraction
* model caching
* fallback LLM providers

## Data Layer

* persistent trace storage
* event-driven processing

## Fraud Detection

* ML-based anomaly detection
* historical behavioral models

---

# 14. Future Improvements

Potential enhancements:

* OCR integration
* multimodal document understanding
* historical fraud learning
* active learning loops
* human-in-the-loop adjudication
* policy versioning
* reviewer feedback integration

---

# 15. Conclusion

The final system demonstrates:

* multi-agent orchestration,
* LLM-powered document understanding,
* deterministic policy enforcement,
* explainable claim adjudication,
* graceful failure handling.

The architecture prioritizes:

* transparency,
* operational reliability,
* modularity,
* extensibility,
* enterprise-readiness.

```
```
