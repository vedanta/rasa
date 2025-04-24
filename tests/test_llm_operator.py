import pytest
from rasa.operators.llm_operator import LLMOperator

def test_llm_operator_returns_text(monkeypatch):
    # Mock call_llm so we don't make real API calls in tests
    from rasa.operators import llm_operator

    def fake_call_llm(prompt, **kwargs):
        return f"FAKE_LLM_RESPONSE: {prompt}"

    monkeypatch.setattr(llm_operator, "call_llm", fake_call_llm)

    input_text = "Hello, world!"
    output = LLMOperator.run(input_text)
    assert output.startswith("FAKE_LLM_RESPONSE")
    assert input_text in output
