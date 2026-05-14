import json

import streamlit as st

from app.orchestrator.graph import (
    claim_pipeline
)

from app.agents.document_parser_agent import (
    parse_document
)


TEST_CASE_PATH = "data/test_cases.json"


# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(
    page_title="Plum Claims Pipeline",
    layout="wide"
)

st.title(
    "Plum AI Claims Processing Pipeline"
)

st.markdown(
    """
    Multi-agent insurance claims processing system with:

    - deterministic policy engines
    - fraud scoring
    - explainable traces
    - LangGraph orchestration
    - Groq-powered document extraction
    """
)


# ----------------------------------------
# LLM EXTRACTION SECTION
# ----------------------------------------

st.header(
    "LLM Medical Document Extraction"
)

raw_document = st.text_area(
    "Paste Raw Medical Document Text",
    height=250
)

if st.button(
    "Parse Using Groq LLM"
):

    if raw_document.strip():

        with st.spinner(
            "Extracting structured fields..."
        ):

            parsed_result = parse_document(
                raw_document
            )

        st.subheader(
            "Extracted Structured JSON"
        )

        st.json(parsed_result)

    else:

        st.warning(
            "Please enter document text."
        )


st.divider()


# ----------------------------------------
# LOAD TEST CASES
# ----------------------------------------

with open(TEST_CASE_PATH, "r") as file:
    test_cases_data = json.load(file)

test_cases = test_cases_data["test_cases"]

test_case_mapping = {
    f"{case['case_id']} - {case['case_name']}": case
    for case in test_cases
}


# ----------------------------------------
# SIDEBAR
# ----------------------------------------

st.sidebar.header(
    "Claim Input"
)

selected_case_name = st.sidebar.selectbox(
    "Select Test Case",
    list(test_case_mapping.keys())
)

selected_case = test_case_mapping[
    selected_case_name
]

run_button = st.sidebar.button(
    "Run Claim Pipeline"
)


# ----------------------------------------
# DISPLAY INPUT
# ----------------------------------------

st.subheader(
    "Input Claim"
)

st.json(
    selected_case["input"]
)


# ----------------------------------------
# RUN PIPELINE
# ----------------------------------------

if run_button:

    with st.spinner(
        "Processing claim through multi-agent pipeline..."
    ):

        result = claim_pipeline.invoke({
            "input_claim": selected_case["input"]
        })

    final_decision = result.get(
        "final_decision",
        {}
    )

    decision = final_decision.get(
        "decision",
        "UNKNOWN"
    )

    approved_amount = final_decision.get(
        "approved_amount",
        0
    )

    confidence_score = final_decision.get(
        "confidence_score",
        0
    )

    reasons = final_decision.get(
        "reasons",
        []
    )

    recommendations = final_decision.get(
        "recommendations",
        []
    )

    trace = final_decision.get(
        "trace",
        []
    )

    # ----------------------------------------
    # FINAL DECISION
    # ----------------------------------------

    st.subheader(
        "Final Decision"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Decision",
            decision
        )

    with col2:
        st.metric(
            "Approved Amount",
            f"₹{approved_amount}"
        )

    with col3:
        st.metric(
            "Confidence Score",
            confidence_score
        )

    # ----------------------------------------
    # REASONS
    # ----------------------------------------

    if reasons:

        st.subheader(
            "Reasons"
        )

        for reason in reasons:
            st.warning(reason)

    # ----------------------------------------
    # RECOMMENDATIONS
    # ----------------------------------------

    if recommendations:

        st.subheader(
            "Recommendations"
        )

        for rec in recommendations:
            st.info(rec)

    # ----------------------------------------
    # TRACE
    # ----------------------------------------

    st.subheader(
        "Decision Trace"
    )

    for step in trace:

        with st.expander(
            f"{step['step']} - {step['status']}"
        ):
            st.json(step)

    # ----------------------------------------
    # FULL RESPONSE
    # ----------------------------------------

    st.subheader(
        "Full Pipeline Output"
    )

    st.json(result)