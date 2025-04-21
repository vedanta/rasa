# tests/test_travel_concierge_flow.py
import sys
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO)


# Add app and operator paths for domain agent loading
sys.path.append(str(Path("apps/travel_concierge/operators").resolve()))

from rasa.core.runner import Runner
from rasa.core.persona import Persona


def test_travel_concierge_end_to_end():
    persona_path = "apps/travel_concierge/persona.yaml"
    persona = Persona.from_yaml(persona_path)

    initial_state = {
        "user_input": "I want a cozy weekend escape",
        "preferences": {
            "region": "europe",
            "travel_style": "relaxed",
            "season": "spring"
        },
        "metadata": {
            "tone": "friendly"
        }
    }

    # Inject domain_operators to metadata for heuristic fallback dispatch
    initial_state["metadata"]["domain_operators"] = persona.domain_operators

    runner = Runner(persona)
    final_state = runner.run(initial_state)

    assert "output" in final_state
    assert "Hallstatt" in final_state["output"] or "recommendation" in final_state["output"].lower()
    assert "😊" in final_state["output"]
    print("\\n🧪 Final Output:")
    print(final_state["output"])