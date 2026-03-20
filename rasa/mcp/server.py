# rasa/mcp/server.py
from mcp.fastapi import MCPServer
from rasa.mcp.capabilities import capabilities
from rasa.mcp.handlers import run_persona_handler

mcp_server = MCPServer(
    capabilities=capabilities,
    handler_map={
        "run_persona": run_persona_handler
    }
)

router = mcp_server.router
