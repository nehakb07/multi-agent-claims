import json
from app.policy_engine.waiting_period_rules import (
    evaluate_waiting_period
)
from app.policy_engine.exclusion_rules import (
    evaluate_dental_claim,
    evaluate_general_exclusions
)
from app.policy_engine.preauth_rules import (
    evaluate_preauthorization_requirement
)
from app.policy_engine.fraud_rules import (
    evaluate_fraud_risk
)
from app.agents.decision_agent import (
    generate_claim_decision
)


TEST_CASE_PATH = "data/test_cases.json"


with open(TEST_CASE_PATH, "r") as file:
    test_cases = json.load(file)


print(test_cases.keys())

print()

for case in test_cases["test_cases"]:
    print(case["case_id"], "->", case["case_name"])
    
print("\n--- WAITING PERIOD TEST ---\n")

tc005 = test_cases["test_cases"][4]

diagnosis = (
    tc005["input"]
    ["documents"][0]
    ["content"]
    ["diagnosis"]
)

result = evaluate_waiting_period(
    member_id=tc005["input"]["member_id"],
    treatment_date=tc005["input"]["treatment_date"],
    diagnosis=diagnosis
)

print(result)

print("\n--- DENTAL EXCLUSION TEST ---\n")

tc006 = test_cases["test_cases"][5]

line_items = (
    tc006["input"]
    ["documents"][0]
    ["content"]
    ["line_items"]
)

result = evaluate_dental_claim(
    line_items
)

print(result)

print("\n--- GENERAL EXCLUSION TEST ---\n")

tc012 = test_cases["test_cases"][11]

content = (
    tc012["input"]
    ["documents"][0]
    ["content"]
)

result = evaluate_general_exclusions(
    diagnosis=content["diagnosis"],
    treatment=content["treatment"]
)

print(result)

print("\n--- PREAUTH TEST ---\n")

tc007 = test_cases["test_cases"][6]

line_items = (
    tc007["input"]
    ["documents"][2]
    ["content"]
    ["line_items"]
)

claim_amount = tc007["input"]["claimed_amount"]

result = evaluate_preauthorization_requirement(
    claim_amount=claim_amount,
    line_items=line_items
)

print(result)

print("\n--- FRAUD TEST ---\n")

tc009 = test_cases["test_cases"][8]

result = evaluate_fraud_risk(
    claims_history=tc009["input"]["claims_history"],
    treatment_date=tc009["input"]["treatment_date"],
    claimed_amount=tc009["input"]["claimed_amount"]
)

print(result)

print("\n--- FULL CLAIM DECISIONS ---\n")

important_cases = [
    "TC004",
    "TC005",
    "TC006",
    "TC007",
    "TC008",
    "TC009",
    "TC010",
    "TC011",
    "TC012"
]

for case in test_cases["test_cases"]:

    if case["case_id"] in important_cases:

        print(f"\n{case['case_id']}")
        print("-" * 50)

        result = generate_claim_decision(
            case["input"]
        )

        print(result)