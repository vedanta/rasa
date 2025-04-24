from typing import Any
from rasa.core.state import State
from rasa.core.agent import FrameAgent
from rasa.llm.llm_client import call_llm  # <--- Add this import

class StatelessFrame(FrameAgent):
    """
    The entry frame that processes raw user input.
    Stateless — does not use memory or session context.
    """

    def run(self, state: State) -> State:
        self.log("Received user input")

        user_input = state.get("user_input", "").strip()
        if not user_input:
            self.log("No input provided.")
            return {**state, "output": "I'm not sure what you're asking for."}

        # Optionally normalize input, tag, etc.

        # NEW: Call the LLM!
        llm_response = call_llm(user_input)

        # Optionally enrich context, or just return output directly
        return {
            **state,
            "context": {
                **state.get("context", {}),
                "intent": "travel_request"
            },
            "output": llm_response  # Add the LLM's response to the output field!
        }
