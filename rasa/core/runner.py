# rasa/core/runner.py

from typing import Dict, Any
from rasa.core.state import State
from rasa.core.persona import Persona
from rasa.core.agent import FrameAgent, OperatorAgent
import importlib

from langgraph.graph import StateGraph


class Runner:
    """
    Executes a RASA persona-defined flow using LangGraph.
    """

    def __init__(self, persona: Persona):
        self.persona = persona
        self.frames = self._load_agents(persona.state_stack, FrameAgent)
        self.operators = self._load_agents(persona.operators, OperatorAgent)
        self.graph = self._build_graph()

    def _load_agents(self, agent_names: list, base_cls: type) -> Dict[str, Any]:
        agents = {}
        for name in agent_names:
            # Infer the import path from naming convention
            if name.endswith("_frame"):
                module_path = f"rasa.frames.{name}"
                class_name = "".join([word.capitalize() for word in name.split("_")])
            else:
                module_path = f"rasa.operators.{name}"
                class_name = "".join([word.capitalize() for word in name.split("_")])

            module = importlib.import_module(module_path)
            cls = getattr(module, class_name)
            if not issubclass(cls, base_cls):
                raise TypeError(f"{class_name} is not a subclass of {base_cls.__name__}")
            agents[name] = cls(name=name)

        return agents

    def _build_graph(self):
        sg = StateGraph(State)

        # Add frames in sequence
        last_node = None
        for frame_name in self.persona.state_stack:
            agent = self.frames[frame_name]
            sg.add_node(frame_name, agent.run)
            if last_node:
                sg.add_edge(last_node, frame_name)
            last_node = frame_name

        # Add operators in sequence
        for operator_name in self.persona.operators:
            agent = self.operators[operator_name]
            sg.add_node(operator_name, agent.run)
            sg.add_edge(last_node, operator_name)
            last_node = operator_name

        sg.set_entry_point(self.persona.state_stack[0])
        sg.set_finish_point(last_node)

        return sg.compile()

    def run(self, state: State) -> State:
        """
        Executes the full cognitive flow and returns the final state.
        """
        return self.graph.invoke(state)

