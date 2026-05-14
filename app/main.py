from fastapi import FastAPI

from app.orchestrator.graph import (
    claim_pipeline
)

app = FastAPI(
    title="Plum Claims Processing API"
)


@app.get("/")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/claims/process")
def process_claim(
    claim_input: dict
):
    result = claim_pipeline.invoke({
        "input_claim": claim_input
    })

    return result