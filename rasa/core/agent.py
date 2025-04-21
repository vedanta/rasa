# rasa/core/agent.py
# BaseAgent, FrameAgent, OperatorAgent

from abc import ABC, abstractmethod
from typing import Any, Dict
from rasa.core.state import State
import logging

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Abstract base class for all agents — both frames and operators.
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, state: State) -> State:
        """
        Each agent receives a State object and must return a new updated State.
        """
        pass

    def log(self, message: str, extra: Dict[str, Any] = {}) -> None:
        """
        Standardized logging format for agents.
        """
        logger.info(f"[{self.name}] {message}", extra=extra)


class FrameAgent(BaseAgent):
    """
    Represents a frame (cognitive state) in the agent's reasoning flow.
    Example: stateless_frame, session_frame, short_term_frame.
    """
    pass


class OperatorAgent(BaseAgent):
    """
    Represents an operator (reasoning tool) applied during cognition.
    Example: preference_agent, heuristic_agent, tone_formatter.
    """
    pass
