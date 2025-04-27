import pytest
from fastapi.testclient import TestClient
from rasa.api.main import app  # Import your FastAPI app directly

client = TestClient(app)

def test_output_success():
    payload = {
        "persona": "strategic_stock_analyst",
        "input": "Should I buy Nvidia today?",
        "preferences": {"sector": "technology", "risk_tolerance": "medium"},
    }
    print(f"\nDEBUG: Sending payload to /output: {payload}")
    response = client.post("/output", json=payload)
    print("DEBUG: Response status code:", response.status_code)
    print("DEBUG: Response JSON:", response.text)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "output" in data
    print("DEBUG: Output:", data["output"])
    assert "NVIDIA" in data["output"] or "Nvidia" in data["output"]

@pytest.mark.parametrize("payload, expected_detail", [
    ({"persona": "", "input": "Should I buy Nvidia today?"}, "Missing or empty 'persona'"),
    ({"persona": "strategic_stock_analyst", "input": ""}, "Missing or empty 'input'"),
    ({}, "field required")
])
def test_output_missing_fields(payload, expected_detail):
    print(f"\nDEBUG: Sending invalid payload to /output: {payload}")
    response = client.post("/output", json=payload)
    print("DEBUG: Response status code:", response.status_code)
    print("DEBUG: Response JSON:", response.text)
    assert response.status_code in (400, 422)  # 422 = Pydantic validation error
    assert expected_detail.lower() in response.text.lower()

def test_output_persona_not_found():
    payload = {
        "persona": "nonexistent_persona",
        "input": "Does this work?"
    }
    print(f"\nDEBUG: Sending payload with invalid persona to /output: {payload}")
    response = client.post("/output", json=payload)
    print("DEBUG: Response status code:", response.status_code)
    print("DEBUG: Response JSON:", response.text)
    assert response.status_code == 404
    assert "not found" in response.text.lower()
