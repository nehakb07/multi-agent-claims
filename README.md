# Plum AI Claims Processing Pipeline

Multi-agent health insurance claims adjudication system built for the Plum AI Engineer Assignment.

The system combines:
- LLM-powered medical document understanding,
- deterministic policy adjudication,
- fraud detection,
- explainable traces,
- LangGraph orchestration,
- graceful failure handling.

---

# Problem Statement

Health insurance claims processing is traditionally manual.

Members upload:
- prescriptions,
- hospital bills,
- pharmacy invoices,
- diagnostic reports,

and operations teams manually:
- verify documents,
- extract information,
- validate policy rules,
- calculate payouts,
- detect fraud,
- approve or reject claims.

This project automates the end-to-end adjudication workflow while maintaining:
- explainability,
- auditability,
- deterministic financial decisioning.

---
# Demo 
https://multi-agent-claims.streamlit.app/

# Features

## Multi-Agent Architecture

The system is composed of specialized agents:

- LLM Parser Agent
- Document Validation Agent
- Consistency Agent
- Decision Agent
- Fraud Detection Engine
- Financial Adjudication Engine

---

## LLM-Powered Medical Document Parsing

Uses Groq + Llama 3.3 to:
- extract diagnoses,
- medicines,
- tests,
- patient details,
- billing information,
- normalize messy medical text.

---

## Deterministic Policy Enforcement

All claim decisions are handled through deterministic rule engines:
- exclusions,
- waiting periods,
- copays,
- sub-limits,
- preauthorization rules,
- network discounts.

No payout decisions are made by the LLM.

---

## Explainable Decision Traces

Every claim generates:
- decision,
- approved amount,
- confidence score,
- rejection reasons,
- recommendations,
- full execution trace.

---

## Graceful Failure Handling

The system supports:
- partial failures,
- degraded confidence,
- manual review escalation,
- non-crashing execution.

---

# High-Level Architecture

```text
Raw Medical Documents
        ↓
LLM Parser Agent (Groq)
        ↓
Structured Claim JSON
        ↓
Validation Agent
        ↓
Consistency Agent
        ↓
Decision Agent
    ├── Exclusion Engine
    ├── Waiting Period Engine
    ├── Preauthorization Engine
    ├── Fraud Engine
    ├── Financial Engine
        ↓
Final Decision
        ↓
Explainable Trace





````md
# Plum AI Claims Processing Pipeline

Multi-agent health insurance claims adjudication system built for the Plum AI Engineer Assignment.

The system combines:
- LLM-powered medical document understanding,
- deterministic policy adjudication,
- fraud detection,
- explainable traces,
- LangGraph orchestration,
- graceful failure handling.

---

# Problem Statement

Health insurance claims processing is traditionally manual.

Members upload:
- prescriptions,
- hospital bills,
- pharmacy invoices,
- diagnostic reports,

and operations teams manually:
- verify documents,
- extract information,
- validate policy rules,
- calculate payouts,
- detect fraud,
- approve or reject claims.

This project automates the end-to-end adjudication workflow while maintaining:
- explainability,
- auditability,
- deterministic financial decisioning.

---

# Features

## Multi-Agent Architecture

The system is composed of specialized agents:

- LLM Parser Agent
- Document Validation Agent
- Consistency Agent
- Decision Agent
- Fraud Detection Engine
- Financial Adjudication Engine

---

## LLM-Powered Medical Document Parsing

Uses Groq + Llama 3.3 to:
- extract diagnoses,
- medicines,
- tests,
- patient details,
- billing information,
- normalize messy medical text.

---

## Deterministic Policy Enforcement

All claim decisions are handled through deterministic rule engines:
- exclusions,
- waiting periods,
- copays,
- sub-limits,
- preauthorization rules,
- network discounts.

No payout decisions are made by the LLM.

---

## Explainable Decision Traces

Every claim generates:
- decision,
- approved amount,
- confidence score,
- rejection reasons,
- recommendations,
- full execution trace.

---

## Graceful Failure Handling

The system supports:
- partial failures,
- degraded confidence,
- manual review escalation,
- non-crashing execution.

---

# High-Level Architecture

```text
Raw Medical Documents
        ↓
LLM Parser Agent (Groq)
        ↓
Structured Claim JSON
        ↓
Validation Agent
        ↓
Consistency Agent
        ↓
Decision Agent
    ├── Exclusion Engine
    ├── Waiting Period Engine
    ├── Preauthorization Engine
    ├── Fraud Engine
    ├── Financial Engine
        ↓
Final Decision
        ↓
Explainable Trace
````

---

# Tech Stack

| Layer         | Technology |
| ------------- | ---------- |
| Backend API   | FastAPI    |
| Frontend      | Streamlit  |
| LLM           | Groq       |
| Orchestration | LangGraph  |
| Language      | Python     |
| Configuration | JSON       |

---

# Project Structure

```text
multi_agent_claims_pipeline/
│
├── app/
│   ├── agents/
│   ├── orchestrator/
│   ├── policy_engine/
│   ├── llm/
│   ├── tests/
│   ├── streamlit_app.py
│   └── main.py
│
├── data/
│   ├── policy_terms.json
│   ├── test_cases.json
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── COMPONENT_CONTRACTS.md
│   └── EVAL_REPORT.md
│
├── screenshots/
│
├── requirements.txt
├── .env.example
└── README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <repository_url>
cd multi_agent_claims_pipeline
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Running the Streamlit App

```bash
streamlit run app/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

# Running FastAPI

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

# Running Tests

## Main Test Runner

```bash
python -m app.tests.test_cases_runner
```

---

## LangGraph Pipeline Test

```bash
python -m app.tests.test_graph
```

---

## LLM Extraction Test

```bash
python -m app.tests.test_llm_parser
```

---

# Example Flows

## Early Validation Failure

Examples:

* missing documents,
* unreadable uploads,
* wrong document types.

The system stops immediately and returns actionable feedback.

---

## Successful Approval

The system:

* validates documents,
* extracts fields,
* applies policy rules,
* calculates payouts,
* generates explainable traces.

---

## Graceful Degradation

When components fail:

* confidence decreases,
* manual review is recommended,
* processing continues safely.

---

# Example Decision Trace

```text
CONSISTENCY_CHECK - PASSED
EXCLUSION_CHECK - PASSED
WAITING_PERIOD - PASSED
FRAUD_CHECK - PASSED
FINANCIAL_CALCULATION - PASSED
PER_CLAIM_LIMIT - PASSED
```

---

# Screenshots

## LLM Extraction Demo

Add screenshot here.

---

## Early Rejection Flow

Add screenshot here.

---

## Successful Approval Flow

Add screenshot here.

---

## Graceful Degradation Flow

Add screenshot here.

---

# Key Architectural Decisions

## Why LLMs Were Used

LLMs are used for:

* semantic extraction,
* normalization,
* document understanding.

Medical documents are:

* noisy,
* inconsistent,
* semi-structured.

---

## Why Deterministic Adjudication Was Used

Insurance claims require:

* auditability,
* reproducibility,
* financial consistency.

Therefore:

* payouts,
* policy decisions,
* copays,
* exclusions,

are all deterministic.

---

# Future Improvements

Potential future enhancements:

* OCR integration,
* multimodal document parsing,
* ML-based fraud detection,
* historical behavioral modeling,
* asynchronous distributed execution,
* reviewer feedback loops.

---

# Documentation

Detailed documentation is available in:

* `docs/ARCHITECTURE.md`
* `docs/COMPONENT_CONTRACTS.md`
* `docs/EVAL_REPORT.md`

---

# Assignment Coverage

This implementation supports:

* multi-agent orchestration,
* policy-driven adjudication,
* explainable traces,
* document validation,
* LLM extraction,
* graceful degradation,
* fraud scoring.

---

# Author

Neha KB

Built as part of the Plum AI Engineer Assignment.

```
```
