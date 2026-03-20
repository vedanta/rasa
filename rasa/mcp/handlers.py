# rasa/mcp/handlers.py

# Replace this with your actual RASA runner when ready
def run_persona_handler(params: dict) -> dict:
    persona = params["persona"]
    prompt = params["prompt"]
    mode = params.get("mode", "text")

    # Temporary stub
    response = f"[{persona}] says: Responding to '{prompt}' in {mode} mode."

    return {"response": response}
