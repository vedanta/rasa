# Long-Term Frame
from rasa.core.state import State
from rasa.core.agent import FrameAgent

class LongTermFrame(FrameAgent):
    """
    Placeholder for long-term memory logic.
    """
    def run(self, state: State) -> State:
        self.log("Simulating long-term memory (no-op)")
        return state
