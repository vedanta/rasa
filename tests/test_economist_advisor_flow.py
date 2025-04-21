# tests/test_economist_advisor_flow.py

import logging
import sys
from pathlib import Path

# Enable operator discovery from the economist app
sys.path.append(str(Path("apps/economist_advisor/operators").resolve()))

from rasa.core.runner import Runner
from rasa.core.persona import Persona

logging.basicConfig(level=logging.INFO)

def test_economist_advisor_end_to_end():
    persona = Persona.from_yaml("apps/economist_advisor/persona.yaml")

    initial_state = {
        "user_input": "Explain the impact of rising interest rates on small businesses.",
        "preferences": {
            "focus": "small_business",
            "topic": "interest_rates"
        },
        "metadata": {
            "tone": persona.metadata.get("tone", "default"),
            "domain_operators": persona.domain_operators
        }
    }

    runner = Runner(persona)
    final_state = runner.run(initial_state)

    assert "output" in final_state
    assert "interest rates" in final_state["output"].lower()
    assert "small business" in final_state["output"].lower() or "firms" in final_state["output"].lower()

    print("\n📊 Economist Advisor Test Output:")
    print(final_state["output"])