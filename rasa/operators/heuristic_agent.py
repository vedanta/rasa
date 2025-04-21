# rasa/operators/heuristic_agent.py

from rasa.core.state import State
from rasa.core.agent import OperatorAgent
import importlib


class HeuristicAgent(OperatorAgent):
    """
    A general-purpose heuristic agent that delegates to domain-specific heuristics
    defined in the persona under 'domain_operators'.
    """

    def run(self, state: State) -> State:
        self.log("Running general heuristic agent")

        domain_operators = state.get("metadata", {}).get("domain_operators", [])

        for op_name in domain_operators:
            try:
                # Try dynamic import from sys.path (e.g., apps/<domain>/operators)
                mod = importlib.import_module(op_name)
                class_name = "".join(word.capitalize() for word in op_name.split("_"))
                cls = getattr(mod, class_name)
                agent = cls(name=op_name)

                self.log(f"Delegating to domain-specific operator: {op_name}")
                state = agent.run(state)
            except Exception as e:
                self.log(f"Failed to run domain operator '{op_name}': {e}")

        return state