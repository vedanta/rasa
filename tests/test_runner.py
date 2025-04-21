# tests/test_runner.py

import pytest
from rasa.core.runner import Runner
from rasa.core.persona import Persona
from rasa.core.state import State
from rasa.core.agent import FrameAgent, OperatorAgent


# Dummy FrameAgent for test
class DummyFrame(FrameAgent):
    def run(self, state: State) -> State:
        self.log("Running DummyFrame")
        return {**state, "context": {"location": "Test City"}}

# Dummy OperatorAgent for test
class DummyOperator(OperatorAgent):
    def run(self, state: State) -> State:
        self.log("Running DummyOperator")
        output = f"Visit {state['context']['location']} for a fun trip!"
        return {**state, "output": output}


@pytest.fixture
def dummy_persona(monkeypatch):
    # Patch importlib to return dummy agents
    import importlib

    def mock_import(name):
        class DummyModule:
            DummyFrame = DummyFrame
            DummyOperator = DummyOperator
        return DummyModule()

    monkeypatch.setattr(importlib, "import_module", mock_import)

    return Persona(
        name="test_agent",
        description="Test Persona",
        state_stack=["dummy_frame"],
        operators=["dummy_operator"],
        prompt_style="default",
        memory_scope="user",
        metadata={}
    )


def test_runner_executes_flow(dummy_persona):
    runner = Runner(dummy_persona)
    input_state = {"user_input": "Suggest a travel idea"}
    final_state = runner.run(input_state)

    assert "context" in final_state
    assert final_state["context"]["location"] == "Test City"
    assert final_state["output"] == "Visit Test City for a fun trip!"
