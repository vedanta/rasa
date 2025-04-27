# rasa/operators/critic_agent.py
from rasa.core.agent import OperatorAgent  # <-- Import the base class

class CriticAgent(OperatorAgent):          # <-- Inherit from OperatorAgent
    def run(self, state):
        state["critic_agent"] = "critic_agent: Not implemented"
        return state
