#!/usr/bin/env python3
# rasa/mcp/main.py

import sys
import os
import json
import logging
import socket
import asyncio
from aiohttp import web

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [rasa-mcp] %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("rasa-mcp")

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)

# Try to import Runner
try:
    from rasa.core.runner import Runner
    logger.info("✅ Runner imported successfully")
    RUNNER_AVAILABLE = True
except ImportError as e:
    logger.error(f"❌ Error importing Runner: {str(e)}")
    RUNNER_AVAILABLE = False
    
# Function to find an available port
def find_available_port(start_port=8030, max_attempts=100):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find an available port after {max_attempts} attempts")

# Define tools
tools = [
    {
        "name": "count_r",
        "description": "Count the number of 'r' in the given word",
        "inputSchema": {
            "properties": {
                "word": {"title": "Word", "type": "string"}
            },
            "required": ["word"],
            "title": "count_rArguments",
            "type": "object"
        }
    }
]

if RUNNER_AVAILABLE:
    tools.append({
        "name": "run_persona",
        "description": "Run a RASA persona-based cognitive agent",
        "inputSchema": {
            "properties": {
                "persona": {"title": "Persona", "type": "string"},
                "prompt": {"title": "Prompt", "type": "string"},
                "mode": {"title": "Mode", "type": "string", "default": "text"}
            },
            "required": ["persona", "prompt"],
            "title": "runPersonaArguments",
            "type": "object"
        }
    })

# Handle JSON-RPC requests
async def handle_jsonrpc(request):
    try:
        request_data = await request.json()
        method = request_data.get("method")
        params = request_data.get("params", {})
        req_id = request_data.get("id")
        
        logger.info(f"📨 Received request: method={method}, id={req_id}")
        
        if method == "initialize":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "experimental": {},
                        "prompts": {"listChanged": False},
                        "resources": {"subscribe": False, "listChanged": False},
                        "tools": {"listChanged": False}
                    },
                    "serverInfo": {
                        "name": "rasa-agent",
                        "version": "1.0.0"
                    }
                }
            }
        elif method == "tools/list":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": tools
                }
            }
        elif method == "resources/list":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "resources": []
                }
            }
        elif method == "prompts/list":
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "prompts": []
                }
            }
        elif method == "tools/execute":
            tool_name = params.get("name")
            tool_params = params.get("parameters", {})
            
            if tool_name == "count_r":
                word = tool_params.get("word", "")
                count = word.lower().count('r')
                logger.info(f"🔢 Counting 'r' in '{word}': {count}")
                result = {"count": count}
                
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                }
            elif tool_name == "run_persona" and RUNNER_AVAILABLE:
                persona = tool_params.get("persona", "")
                prompt = tool_params.get("prompt", "")
                mode = tool_params.get("mode", "text")
                
                try:
                    # Adjust these based on your actual Runner API
                    logger.info(f"🤖 Running persona '{persona}' with prompt: {prompt}")
                    runner = Runner(persona=persona, prompt=prompt, output_mode=mode)
                    output = runner.run()  # Adjust as needed
                    result = {"response": output}
                except Exception as e:
                    logger.error(f"❌ Error running persona: {str(e)}")
                    result = {"error": str(e)}
                
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": result
                }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Tool '{tool_name}' not found"
                    }
                }
        elif method == "notifications/initialized":
            # This is a notification, no response needed
            logger.info("📣 Received initialized notification")
            return web.Response(status=204)
        else:
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            }
        
        logger.info(f"📤 Sending response for id={req_id}")
        return web.json_response(response)
    except Exception as e:
        logger.error(f"❌ Error handling request: {str(e)}")
        return web.json_response({
            "jsonrpc": "2.0",
            "id": req_id if 'req_id' in locals() else None,
            "error": {
                "code": -32603, 
                "message": f"Internal error: {str(e)}"
            }
        })

# Create web app
async def init_app():
    app = web.Application()
    app.router.add_post("/", handle_jsonrpc)
    return app

# Custom print function to replace web.run_app's print
def silent_print(msg):
    logger.info(msg)

# Main function to run server
async def run_server():
    try:
        # Find an available port
        port = find_available_port(start_port=8050)  # Starting from 8050 to avoid any conflicts
        
        # Initialize the app
        app = await init_app()
        
        # Set up the web runner manually to ensure we respond quickly
        runner = web.AppRunner(app)
        await runner.setup()
        
        # Create site and start it
        site = web.TCPSite(runner, '127.0.0.1', port)
        await site.start()
        
        logger.info(f"🚀 RASA MCP Server running on http://127.0.0.1:{port}")
        
        # Keep the server running
        while True:
            await asyncio.sleep(3600)  # Sleep for an hour (or until interrupted)
            
    except KeyboardInterrupt:
        logger.info("💤 Server shutting down...")
    except Exception as e:
        logger.error(f"❌ Error starting server: {str(e)}")
        sys.exit(1)

# Main entry point
if __name__ == "__main__":
    logger.info("🔌 Starting RASA MCP Server...")
    asyncio.run(run_server())