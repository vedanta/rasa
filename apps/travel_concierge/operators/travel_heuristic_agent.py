# apps/travel_concierge/operators/travel_heuristic_agent.py

from rasa.core.state import State
from rasa.core.agent import OperatorAgent

class TravelHeuristicAgent(OperatorAgent):
    """
    Uses travel heuristics to generate a destination recommendation.
    Relies on preferences like region, season, and travel style.
    """

    def run(self, state: State) -> State:
        self.log("Applying travel heuristics")

        context = state.get("context", {})
        prefs = context.get("preferences", {})

        region = prefs.get("region", "europe")
        style = prefs.get("travel_style", "relaxed")
        season = prefs.get("season", "spring")

        destination = self._select_destination(region, style, season)

        output = f"For a {style} {season} getaway in {region.title()}, consider visiting {destination}."
        return {**state, "output": output}

    def _select_destination(self, region: str, style: str, season: str) -> str:
        # Simple hardcoded heuristic logic
        if region == "europe":
            if style == "relaxed":
                return "Hallstatt, Austria"
            elif style == "adventurous":
                return "Interlaken, Switzerland"
        elif region == "asia":
            if style == "relaxed":
                return "Ubud, Bali"
            elif style == "adventurous":
                return "Pokhara, Nepal"
        elif region == "americas":
            if style == "relaxed":
                return "Santa Fe, New Mexico"
            elif style == "adventurous":
                return "Patagonia, Argentina"
        return "a hidden gem in your chosen region"