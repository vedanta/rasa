# rasa/api/llm.py
from fastapi import APIRouter
from rasa.llm.llm_adapter import LLMAdapter
from rasa.config import settings
router = APIRouter()
@router.get("/llm/info", tags=["llm"], summary="Get current LLM config (never exposes keys)")
def get_llm_info():
    # llm = LLMAdapter.from_config()
    llm = LLMAdapter(
    provider=settings.get_llm_provider(),
    model=settings.get_llm_model(),
    api_key=settings.get_openai_api_key(),
    host=settings.get_llm_host()
    )
    info = llm.info()
    # Never include actual keys in the output!
    if "api_key" in info:
        del info["api_key"]
    for k in list(info.keys()):
        if "key" in k:
            del info[k]
    return {
        "provider": info.get("provider"),
        "model": info.get("model"),
        "host": info.get("host"),
        "mode": info.get("mode"),
        "config": info.get("config"),
        "api_key_present": info.get("api_key_present", False),
    }
