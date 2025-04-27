# tests/test_strategic_stock_analyst.py
import sys
from pathlib import Path
import yaml
from rasa.core.runner import Runner
from rasa.core.persona import Persona

def test_strategic_stock_analyst_end_to_end():
    persona_yaml_path = "apps/strategic_stock_analyst/persona.yaml"

    # Step 1: Read and print YAML
    with open(persona_yaml_path, "r") as f:
        raw_yaml = f.read()
        print("\nDEBUG: Raw persona.yaml content:\n", raw_yaml)
        yaml_data = yaml.safe_load(raw_yaml)
        print("DEBUG: Parsed YAML frames:", yaml_data.get("frames"))

    # Step 2: Load Persona object from YAML
    persona = Persona.from_yaml(persona_yaml_path)
    print("DEBUG: Persona object:", persona)
    print("DEBUG: Persona frames attribute:", getattr(persona, 'frames', None))

    # Step 3: Prepare initial state
    user_input = "Should I buy Nvidia today?"
    preferences = {"sector": "technology", "risk_tolerance": "medium"}
    metadata = {"tone": persona.metadata.get("tone", "default")}
    initial_state = {
        "user_input": user_input,
        "preferences": preferences,
        "metadata": metadata
    }
    print("DEBUG: Initial state for Runner:", initial_state)

    # Step 4: Initialize and run the Runner
    try:
        runner = Runner(persona)
        print("DEBUG: Runner initialized successfully.")
    except Exception as e:
        print("ERROR: Runner initialization failed:", e)
        raise

    try:
        final_state = runner.run(initial_state)
        print("DEBUG: Runner execution completed.")
    except Exception as e:
        print("ERROR: Runner execution failed:", e)
        raise

    # Step 5: Inspect and print final state
    print("\nDEBUG: Final state output keys:", list(final_state.keys()))
    print("DEBUG: Full final state:", final_state)

    # Step 6: Assertions
    assert "output" in final_state

    print("\n📈 Stock Analyst Test Output:")
    print(final_state["output"])


if __name__ == "__main__":
    test_strategic_stock_analyst_end_to_end()
