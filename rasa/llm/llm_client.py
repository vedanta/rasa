# rasa/llm/llm_client.py
from rasa.llm.llm_adapter import LLMAdapter
from rasa.config import settings

def call_llm(
    prompt: str,
    provider: str = None,
    model: str = None,
    api_key: str = None,
    host: str = None,
    **kwargs
):
    """
    Calls the configured (or specified) LLM and returns the result.
    Parameters can override defaults from settings.
    """
    llm = LLMAdapter(
        provider=provider or settings.get_llm_provider(),
        model=model or settings.get_llm_model(),
        api_key=api_key or settings.get_openai_api_key(),
        host=host or settings.get_llm_host(),
    )
    return llm.generate(prompt, **kwargs)
