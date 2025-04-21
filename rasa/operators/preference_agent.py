# Preference Agent
# rasa/operators/preference_agent.py

from rasa.core.state import State
from rasa.core.agent import OperatorAgent


class PreferenceAgent(OperatorAgent):
    """
    Injects and validates user preferences into the shared context.
    """

    def run(self, state: State) -> State:
        self.log("Applying user preferences")

        prefs = state.get("preferences", {})
        context = state.get("context", {})

        if not prefs:
            self.log("No preferences found in state.")
            return {**state, "context": {**context}}

        validated = self._validate_preferences(prefs)
        context["preferences"] = validated

        return {**state, "context": context}

    def _validate_preferences(self, prefs: dict) -> dict:
        """
        Normalize or sanitize user-provided preferences.
        Can be domain-specific later.
        """
        clean = {}

        for key, value in prefs.items():
            key = key.lower().strip()
            if isinstance(value, str):
                value = value.lower().strip()
            clean[key] = value

        return clean
