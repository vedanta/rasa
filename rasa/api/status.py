from fastapi import APIRouter
from rasa.config import settings

router = APIRouter()

@router.get("/status", tags=["system"], summary="Get RASA API server status")
def get_status():
    return {
        "status": "ok",
        "llm_provider": settings.get_llm_provider(),
        "llm_model": settings.get_llm_model(),
        "llm_mode": settings.get_llm_mode(),
        "db_type": settings.get_default_db_type(),
        "vector_db_type": settings.get_default_vector_db_type(),
        # Optionally: add build/version info
        "version": "0.1.2",  # Or import from a version.py
    }
