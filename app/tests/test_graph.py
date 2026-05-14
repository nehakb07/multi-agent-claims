import json

from app.orchestrator.graph import (
    claim_pipeline
)


TEST_CASE_PATH = "data/test_cases.json"


with open(TEST_CASE_PATH, "r") as file:
    test_cases = json.load(file)


tc004 = test_cases["test_cases"][3]

result = claim_pipeline.invoke({
    "input_claim": tc004["input"]
})

print(result)