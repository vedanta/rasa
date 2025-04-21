# rasa/core/persona.py

import yaml
from typing import List, Dict, Optional
from pathlib import Path


class Persona:
    """
    A Persona defines the identity, behavior, and reasoning flow of a RASA agent.
    It includes the frame stack, operator agents, tone, memory scope, and metadata.
    """

    def __init__(
        self,
        name: str,
        description: str,
        state_stack: List[str],
        operators: List[str],
        prompt_style: str,
        memory_scope: str,
        metadata: Optional[Dict] = None,
    ):
        self.name = name
        self.description = description
        self.state_stack = state_stack
        self.operators = operators
        self.prompt_style = prompt_style
        self.memory_scope = memory_scope
        self.metadata = metadata or {}

    @classmethod
    def from_yaml(cls, path: str) -> "Persona":
        """
        Load a Persona definition from a YAML file.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Persona YAML not found: {path}")

        with path.open("r") as f:
            data = yaml.safe_load(f)

        return cls(
            name=data.get("name"),
            description=data.get("description", ""),
            state_stack=data.get("state_stack", []),
            operators=data.get("operators", []),
            prompt_style=data.get("prompt_style", "default"),
            memory_scope=data.get("memory_scope", "user"),
            metadata=data.get("metadata", {}),
        )

    def __repr__(self) -> str:
        return f"<Persona {self.name} | frames: {len(self.state_stack)} ops: {len(self.operators)}>"
