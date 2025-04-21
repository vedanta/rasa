# tests/test_heuristic_agent.py

import pytest
import sys
from pathlib import Path

# Ensure domain-specific operator is importable
sys.path.append(str(Path("apps/travel_concierge/operators").resolve()))

from rasa.core.agent import OperatorAgent
from rasa.operators.heuristic_agent import HeuristicAgent


# Dummy domain-specific operator to test fallback dispatch
class TravelHeuristicAgent(OperatorAgent):
    def run(self, state):
        state["output"] = "Test destination recommendation"
        return state


def test_heuristic_agent_dispatch(monkeypatch):
    # Patch importlib to return our dummy agent
    import importlib

    def mock_import_module(name):
        if name == "travel_heuristic_agent":
            return sys.modules[__name__]
        return importlib.import_module(name)

    monkeypatch.setattr(importlib, "import_module", mock_import_module)

    agent = HeuristicAgent(name="heuristic_agent")

    state = {
        "context": {
            "preferences": {
                "region": "europe"
            }
        },
        "metadata": {
            "domain_operators": ["travel_heuristic_agent"]
        }
    }

    updated = agent.run(state)
    assert updated["output"] == "Test destination recommendation"