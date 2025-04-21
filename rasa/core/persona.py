# rasa/core/persona.py

import yaml
from typing import List, Dict, Optional
from pathlib import Path


class Persona:
    """
    A Persona defines the identity, behavior, and reasoning flow of a RASA agent.
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
        domain_operators: Optional[List[str]] = None
    ):
        self.name = name
        self.description = description
        self.state_stack = state_stack
        self.operators = operators
        self.prompt_style = prompt_style
        self.memory_scope = memory_scope
        self.metadata = metadata or {}
        self.domain_operators = domain_operators or []

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

        return cls.build(data)

    @classmethod
    def build(cls, config: dict) -> "Persona":
        """
        Build a Persona from a dictionary definition.
        """
        return cls(
            name=config.get("name"),
            description=config.get("description", ""),
            state_stack=config.get("state_stack", []),
            operators=config.get("operators", []),
            prompt_style=config.get("prompt_style", "default"),
            memory_scope=config.get("memory_scope", "user"),
            metadata=config.get("metadata", {}),
            domain_operators=config.get("domain_operators", [])
        )

    def __repr__(self) -> str:
        return f"<Persona {self.name} | frames: {len(self.state_stack)} ops: {len(self.operators)}>"