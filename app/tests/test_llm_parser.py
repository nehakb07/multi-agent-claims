from app.agents.document_parser_agent import (
    parse_document
)


sample_document = """
Dr. Arun Sharma
Diagnosis: Viral Fever

Medicines:
- Paracetamol 650mg
- Vitamin C

Patient Name: Rajesh Kumar

Consultation Fee: 1000
CBC Test: 300
Total: 1300
"""


result = parse_document(
    sample_document
)

print(result)