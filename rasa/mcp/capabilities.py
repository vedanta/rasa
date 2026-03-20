# rasa/mcp/capabilities.py
from mcp import Capability

capabilities = [
    Capability(
        name="run_persona",
        description="Run a structured cognitive flow using a selected persona and prompt.",
        parameters={
            "type": "object",
            "properties": {
                "persona": {"type": "string"},
                "prompt": {"type": "string"},
                "mode": {"type": "string", "enum": ["text", "json"], "default": "text"}
            },
            "required": ["persona", "prompt"]
        }
    )
]
