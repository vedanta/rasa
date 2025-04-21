# Session Frame
# rasa/frames/session_frame.py

from rasa.core.state import State
from rasa.core.agent import FrameAgent

class SessionFrame(FrameAgent):
    """
    Placeholder frame to simulate session context.
    """

    def run(self, state: State) -> State:
        self.log("Simulating session memory (no-op)")
        return state
