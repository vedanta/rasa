import sys
from pathlib import Path

# Add the local economist_advisor operators directory to Python path
sys.path.append(str(Path(__file__).resolve().parent / "operators"))

from rasa.core.runner import Runner
from rasa.core.persona import Persona

if __name__ == "__main__":
    persona = Persona.from_yaml("apps/economist_advisor/persona.yaml")

    user_input = "Explain the impact of rising interest rates on small businesses."
    preferences = {
        "focus": "small_business",
        "topic": "interest_rates"
    }

    initial_state = {
        "user_input": user_input,
        "preferences": preferences,
        "metadata": {
            "tone": persona.metadata.get("tone", "default"),
            "domain_operators": persona.domain_operators
        }
    }

    runner = Runner(persona)
    final_state = runner.run(initial_state)

    print("\n📊 Economist Advisor Response:\n")
    print(final_state.get("output", "[No output generated]"))