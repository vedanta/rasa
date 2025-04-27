from rasa.version import __version__ as rasa_version
from fastapi import FastAPI, HTTPException, APIRouter, Request, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
import os
from pathlib import Path
from rasa.core.runner import Runner
from rasa.core.persona import Persona
import sys
sys.path.append("apps/travel_concierge/operators")

from rasa.api import llm
from rasa.api import status as status_router

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
    # Validate persona and input
    if not req.persona or not req.persona.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or empty 'persona' parameter. Please specify a valid persona name."
        )
    if not req.input or not req.input.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or empty 'input' parameter. Please provide user input text."
        )

    try:
        persona_path = f"apps/{req.persona}/persona.yaml"
        if not Path(persona_path).exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona '{req.persona}' not found. Please check available personas."
            )

        persona = Persona.from_yaml(persona_path)
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/output/json", response_model=OutputJSONResponse, tags=["Core"])
def get_output_json(req: RASARequest):
    # Validate persona and input
    if not req.persona or not req.persona.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or empty 'persona' parameter. Please specify a valid persona name."
        )
    if not req.input or not req.input.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or empty 'input' parameter. Please provide user input text."
        )

    try:
        persona_path = f"apps/{req.persona}/persona.yaml"
        if not Path(persona_path).exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona '{req.persona}' not found. Please check available personas."
            )

        persona = Persona.from_yaml(persona_path)
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stream", tags=["Core"])
async def stream_output(req: RASARequest):
    # Validate persona and input
    if not req.persona or not req.persona.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or empty 'persona' parameter. Please specify a valid persona name."
        )
    if not req.input or not req.input.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing or empty 'input' parameter. Please provide user input text."
        )

    try:
        persona_path = f"apps/{req.persona}/persona.yaml"
        if not Path(persona_path).exists():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Persona '{req.persona}' not found. Please check available personas."
            )

        persona = Persona.from_yaml(persona_path)
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Include routers for LLM and status
app.include_router(llm.router)
app.include_router(status_router.router)