from rasa.core.state import State
from rasa.core.agent import OperatorAgent

class EconomyHeuristicAgent(OperatorAgent):
    """
    Applies economic reasoning to explain impacts of market policies or conditions.
    """

    def run(self, state: State) -> State:
        self.log("Applying economic heuristics")

        topic = state.get("preferences", {}).get("topic", "")
        focus = state.get("preferences", {}).get("focus", "")

        if topic == "interest_rates" and focus == "small_business":
            explanation = (
                "Rising interest rates increase borrowing costs, which reduces access to capital for small businesses. "
                "This can lead to slowed investment, reduced hiring, and higher default risk for debt-heavy firms."
            )
        else:
            explanation = "Economic impacts vary. Please specify a clearer focus or topic for analysis."

        return {**state, "output": explanation}