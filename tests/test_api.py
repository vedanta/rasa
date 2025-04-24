import pytest
from fastapi.testclient import TestClient
from rasa.api.main import app

client = TestClient(app)

def test_get_personas():
    response = client.get("/persona")
    assert response.status_code == 200
    data = response.json()
    assert "personas" in data
    assert isinstance(data["personas"], list)
    assert "travel_concierge" in data["personas"] or "economist_advisor" in data["personas"]

def test_output_travel_concierge():
    req = {
        "persona": "travel_concierge",
        "input": "Plan a romantic spring trip in Europe",
        "preferences": {"region": "europe", "travel_style": "romantic", "season": "spring"}
    }
    response = client.post("/output", json=req)
    assert response.status_code == 200
    data = response.json()
    assert "output" in data
    assert "Europe" in data["output"] or "romantic" in data["output"]

def test_output_json_travel_concierge():
    req = {
        "persona": "travel_concierge",
        "input": "Plan a relaxing summer getaway",
        "preferences": {"region": "europe", "travel_style": "relaxed", "season": "summer"}
    }
    response = client.post("/output/json", json=req)
    assert response.status_code == 200
    data = response.json()
    assert "output" in data
    assert "output_json" in data
    assert isinstance(data["metadata"], dict)

def test_stream_travel_concierge():
    req = {
        "persona": "travel_concierge",
        "input": "Suggest a fun weekend city break",
        "preferences": {"region": "europe"}
    }
    with client.stream("POST", "/stream", json=req) as response:
        assert response.status_code == 200
        output = ""
        for chunk in response.iter_text():
            output += chunk
        assert (
            "weekend" in output
            or "city" in output
            or "break" in output
            or "Hallstatt" in output
            or "Europe" in output
            or "getaway" in output
        )
