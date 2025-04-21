# tests/test_persona_build.py

from rasa.core.persona import Persona

def test_persona_build_from_dict():
    config = {
        "name": "test_builder_persona",
        "description": "Built programmatically for testing",
        "state_stack": ["stateless_frame"],
        "operators": ["preference_agent", "heuristic_agent"],
        "domain_operators": ["mock_heuristic_agent"],
        "prompt_style": "neutral",
        "memory_scope": "user",
        "metadata": {
            "tone": "neutral",
            "domain": "test"
        }
    }

    persona = Persona.build(config)

    assert persona.name == "test_builder_persona"
    assert persona.prompt_style == "neutral"
    assert persona.domain_operators == ["mock_heuristic_agent"]
    assert persona.metadata["tone"] == "neutral"

    print("\n🧪 Persona.build() Test Passed:")
    print(f"Name: {persona.name}")
    print(f"Operators: {persona.operators}")
    print(f"Domain Operators: {persona.domain_operators}")