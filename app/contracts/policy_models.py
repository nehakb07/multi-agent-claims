import json
from functools import lru_cache


POLICY_PATH = "data/policy_terms.json"


@lru_cache(maxsize=1)
def load_policy():
    with open(POLICY_PATH, "r") as file:
        return json.load(file)


def get_member(member_id: str):
    policy = load_policy()

    members = policy.get("members", [])

    for member in members:
        if member["member_id"] == member_id:
            return member

    return None


def get_claim_category_rules(category: str):
    policy = load_policy()

    return policy["opd_categories"].get(category.lower())


def get_document_requirements(category: str):
    policy = load_policy()

    return policy["document_requirements"].get(category)