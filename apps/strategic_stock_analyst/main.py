import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Add the local operators directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent / "operators"))
from rasa.core.runner import Runner
from rasa.core.persona import Persona

env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print("Warning: .env file not found. Using defaults or hardcoded values.")

persona_path = os.getenv("PERSONA_PATH", str(Path(__file__).parent / "persona.yaml"))
persona = Persona.from_yaml(persona_path)

user_input = os.getenv("USER_INPUT", "Please provide your input in .env.")
preferences = {k.replace("PREFERENCE_", "").lower(): v for k, v in os.environ.items() if k.startswith("PREFERENCE_")}
metadata = {k.replace("METADATA_", "").lower(): v for k, v in os.environ.items() if k.startswith("METADATA_")}

initial_state = {
    "user_input": user_input,
    "preferences": preferences,
    "metadata": metadata
}

runner = Runner(persona)
final_state = runner.run(initial_state)

print("\n📈 Stock Analyst Recommendation:\n")
print(final_state.get("output", "[No output generated]"))
