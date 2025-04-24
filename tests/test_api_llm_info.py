import pytest
from fastapi.testclient import TestClient
from rasa.api.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_llm_info_no_keys_in_response(client):
    # Call the /llm/info endpoint
    response = client.get("/llm/info")
    assert response.status_code == 200
    data = response.json()

    # Basic structure
    assert "provider" in data
    assert "model" in data
    assert "host" in data
    assert "mode" in data
    assert "config" in data
    assert "api_key_present" in data

    # Never leak sensitive key values
    for k, v in data.items():
        if k == "api_key_present":
            continue
        assert "key" not in k.lower(), f"Sensitive key found in response: {k}"

    assert isinstance(data["api_key_present"], bool)


def test_llm_info_content_values(client):
    # This test is optional, to ensure values reflect your .env or .env-llm setup.
    response = client.get("/llm/info")
    assert response.status_code == 200
    data = response.json()

    # Example: If you have ollama in config, it should be returned
    assert data["provider"] in ("ollama", "openai", "claude")
    assert isinstance(data["model"], str)
    assert isinstance(data["host"], str)
