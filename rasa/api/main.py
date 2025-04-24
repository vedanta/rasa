from rasa.version import __version__ as rasa_version
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
import os
from pathlib import Path
from rasa.core.runner import Runner
from rasa.core.persona import Persona
import sys
sys.path.append("apps/travel_concierge/operators")

app = FastAPI(
    title="RASA API",
    description="Role-Aligned Software Architecture API – Multi-persona, memory-aware AI",
    version=rasa_version
)

class PersonaListResponse(BaseModel):
    personas: List[str] = Field(..., description="List of available personas")

class RASARequest(BaseModel):
    persona: str = Field(..., description="Persona name (e.g. 'travel_concierge')")
    input: str = Field(..., description="User input prompt")
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, description="User preferences (domain-specific)")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata/context")

class OutputResponse(BaseModel):
    output: str = Field(..., description="Plain output text from persona")

class OutputJSONResponse(BaseModel):
    output: str = Field(..., description="Plain output text")
    output_json: Optional[Any] = Field(None, description="Structured output, if persona supports")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="State metadata after reasoning")

@app.get("/persona", response_model=PersonaListResponse, tags=["Personas"])
def get_personas():
    """List all available personas based on persona.yaml in apps/."""
    personas = [d for d in os.listdir("apps") if (Path("apps") / d / "persona.yaml").exists()]
    return {"personas": personas}

@app.post("/output", response_model=OutputResponse, tags=["Core"])
def get_output(req: RASARequest):
    """Run the full persona cognitive flow and return plain output."""
    try:
        persona = Persona.from_yaml(f"apps/{req.persona}/persona.yaml")
        runner = Runner(persona)
        state = {
            "user_input": req.input,
            "preferences": req.preferences or {},
            "metadata": {
                **req.metadata,
                "tone": persona.metadata.get("tone", "default"),
                "domain_operators": getattr(persona, "domain_operators", [])
            }
        }
        result = runner.run(state)
        return {"output": result.get("output", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/output/json", response_model=OutputJSONResponse, tags=["Core"])
def get_output_json(req: RASARequest):
    """Return output and any structured JSON output with metadata."""
    try:
        persona = Persona.from_yaml(f"apps/{req.persona}/persona.yaml")
        runner = Runner(persona)
        state = {
            "user_input": req.input,
            "preferences": req.preferences or {},
            "metadata": {
                **req.metadata,
                "tone": persona.metadata.get("tone", "default"),
                "domain_operators": getattr(persona, "domain_operators", [])
            }
        }
        result = runner.run(state)
        return {
            "output": result.get("output", ""),
            "output_json": result.get("output_json", []),
            "metadata": result.get("metadata", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream", tags=["Core"])
async def stream_output(req: RASARequest):
    """
    Stream output tokens for real-time consumption (useful for chat UIs or CLI).
    This version streams by words, simulating LLM token output.
    """
    try:
        persona = Persona.from_yaml(f"apps/{req.persona}/persona.yaml")
        runner = Runner(persona)
        state = {
            "user_input": req.input,
            "preferences": req.preferences or {},
            "metadata": {
                **req.metadata,
                "tone": persona.metadata.get("tone", "default"),
                "domain_operators": getattr(persona, "domain_operators", [])
            }
        }
        result = runner.run(state)
        output = result.get("output", "")
        async def word_stream():
            for word in output.split():
                yield word + " "
        return StreamingResponse(word_stream(), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
