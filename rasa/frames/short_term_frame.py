# Short-Term Frame
# rasa/frames/short_term_frame.py

from rasa.core.state import State
from rasa.core.agent import FrameAgent

class ShortTermFrame(FrameAgent):
    """
    Placeholder for short-term memory enrichment.
    In the future, this might pull from Redis or summarize recent inputs.
    """

    def run(self, state: State) -> State:
        self.log("Simulating short-term memory enrichment (no-op)")
        return state
