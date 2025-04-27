import pytest
from fastapi.testclient import TestClient
from rasa.api.main import app

client = TestClient(app)

# ANSI color codes for terminal
def debug(msg):
    print(f"\033[96mDEBUG:\033[0m {msg}")

def green(msg):
    print(f"\033[92m{msg}\033[0m")

def yellow(msg):
    print(f"\033[93m{msg}\033[0m")

def red(msg):
    print(f"\033[91m{msg}\033[0m")

def cyan(msg):
    print(f"\033[96m{msg}\033[0m")

# ---------- /output ----------
def test_output_success():
    payload = {
        "persona": "strategic_stock_analyst",
        "input": "Should I buy Nvidia today?",
        "preferences": {"sector": "technology", "risk_tolerance": "medium"},
    }
    cyan(f"\n[TEST] /output: Sending valid payload: {payload}")
    response = client.post("/output", json=payload)
    debug(f"/output status: {response.status_code}")
    debug(f"/output response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "output" in data
    green("PASS: /output returns output.")
    debug(f"Output: {data['output'][:120]}...")

@pytest.mark.parametrize("payload, expected_detail", [
    ({"persona": "", "input": "Should I buy Nvidia today?"}, "Missing or empty 'persona'"),
    ({"persona": "strategic_stock_analyst", "input": ""}, "Missing or empty 'input'"),
    ({}, "field required")
])
def test_output_missing_fields(payload, expected_detail):
    yellow(f"\n[TEST] /output: Sending invalid payload: {payload}")
    response = client.post("/output", json=payload)
    debug(f"/output status: {response.status_code}")
    debug(f"/output response: {response.text}")
    assert response.status_code in (400, 422)
    assert expected_detail.lower() in response.text.lower()
    green("PASS: /output handles missing/invalid fields.")

def test_output_persona_not_found():
    payload = {
        "persona": "nonexistent_persona",
        "input": "Does this work?"
    }
    yellow(f"\n[TEST] /output: Invalid persona: {payload}")
    response = client.post("/output", json=payload)
    debug(f"/output status: {response.status_code}")
    debug(f"/output response: {response.text}")
    assert response.status_code == 404
    assert "not found" in response.text.lower()
    green("PASS: /output handles non-existent persona.")

# ---------- /output/json ----------
def test_output_json_success():
    payload = {
        "persona": "strategic_stock_analyst",
        "input": "Should I buy Nvidia today?",
        "preferences": {"sector": "technology", "risk_tolerance": "medium"},
    }
    cyan(f"\n[TEST] /output/json: Sending valid payload: {payload}")
    response = client.post("/output/json", json=payload)
    debug(f"/output/json status: {response.status_code}")
    debug(f"/output/json response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "output" in data
    assert "metadata" in data
    green("PASS: /output/json returns output and metadata.")

# ---------- /stream ----------
def test_stream_success():
    payload = {
        "persona": "strategic_stock_analyst",
        "input": "Should I buy Nvidia today?",
        "preferences": {"sector": "technology", "risk_tolerance": "medium"},
    }
    cyan(f"\n[TEST] /stream: Sending valid payload: {payload}")
    response = client.post("/stream", json=payload)
    debug(f"/stream status: {response.status_code}")
    output = b"".join(response.iter_bytes()).decode()
    debug(f"/stream output (first 120 chars): {output[:120]}...")
    assert response.status_code == 200
    assert "nvidia" in output.lower()
    green("PASS: /stream returns streamed output.")

# ---------- /persona ----------
def test_persona_list():
    cyan("\n[TEST] /persona: Listing personas")
    response = client.get("/persona")
    debug(f"/persona status: {response.status_code}")
    debug(f"/persona response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "personas" in data
    assert "strategic_stock_analyst" in data["personas"]
    green("PASS: /persona lists available personas.")

# ---------- /llm/info, /llm/health, /status ----------
@pytest.mark.parametrize("endpoint", ["/llm/info", "/llm/health", "/status"])
def test_system_endpoints(endpoint):
    cyan(f"\n[TEST] {endpoint}: System endpoint")
    response = client.get(endpoint)
    debug(f"{endpoint} status: {response.status_code}")
    debug(f"{endpoint} response: {response.text}")
    assert response.status_code == 200
    green(f"PASS: {endpoint} returns 200.")

