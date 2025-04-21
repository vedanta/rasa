# rasa/operators/tone_formatter.py (updated)

import re
from rasa.core.state import State
from rasa.core.agent import OperatorAgent


class ToneFormatter(OperatorAgent):
    """
    Adjusts the tone of the output using rule-based text transformations.
    """

    def run(self, state: State) -> State:
        self.log("Formatting output tone")

        output = state.get("output", "")
        tone = state.get("metadata", {}).get("tone", "default")

        if not output:
            return {**state, "output": "No response to format."}

        formatted = self._apply_tone(output, tone)
        return {**state, "output": formatted}

    def _apply_tone(self, text: str, tone: str) -> str:
        if tone == "friendly":
            return self._make_friendly(text)
        elif tone == "poetic":
            return self._make_poetic(text)
        elif tone == "concise":
            return self._make_concise(text)
        else:
            return text

    def _make_friendly(self, text: str) -> str:
        softened = text.replace("You should", "You might want to") \
                       .replace("must", "could") \
                       .replace("!", ".")
        return softened.strip() + " 😊 Let me know if you need more ideas."

    def _make_poetic(self, text: str) -> str:
        poeticized = text
        poeticized = poeticized.replace("visit", "wander through")
        poeticized = poeticized.replace("peaceful", "serene")
        poeticized = poeticized.replace("city", "landscape")
        poeticized += "\n\nLet your soul drift with the wind of new places."
        return poeticized

    def _make_concise(self, text: str) -> str:
        return text.strip().split(".")[0].strip() + "."
