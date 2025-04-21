# apps/travel_concierge/main.py
import sys
from pathlib import Path
# Add the local travel_concierge operators directory to Python path
sys.path.append(str(Path(__file__).resolve().parent / "operators"))
from rasa.core.runner import Runner
from rasa.core.persona import Persona

if __name__ == "__main__":
    # Load persona
    persona = Persona.from_yaml("apps/travel_concierge/persona.yaml")

    # Sample input
    user_input = "I'm looking for a cozy weekend trip somewhere scenic and quiet."
    preferences = {
        "region": "europe",
        "travel_style": "relaxed",
        "season": "spring"
    }

    # Initialize state
    initial_state = {
        "user_input": user_input,
        "preferences": preferences,
        "metadata": {
            "tone": persona.metadata.get("tone", "default")
        }
    }

    # Run the persona-defined agent flow
    runner = Runner(persona)
    final_state = runner.run(initial_state)

    # Output result
    print("\n✈️  Travel Concierge Recommendation:\n")
    print(final_state.get("output", "[No output generated]"))
