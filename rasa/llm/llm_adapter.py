import os
from typing import Optional, Dict, Any
import requests


# Assumes all LLM config loaded via rasa/config/settings.py
try:
    from rasa.config import settings
except ImportError:
    settings = None  # For isolated test/debugging

class LLMAdapter:
    """
    Unified interface for LLMs in RASA.
    Supports: Ollama (local), OpenAI, Claude (Anthropic)
    """

    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        host: Optional[str] = None,
        **kwargs
    ):
        # Load from settings or env if not provided directly
        self.provider = provider or (getattr(settings, "LLM_PROVIDER", None) if settings else os.getenv("LLM_PROVIDER", "ollama"))
        self.model = model or (getattr(settings, "LLM_MODEL", None) if settings else os.getenv("LLM_MODEL", "llama3"))
        self.host = host or (getattr(settings, "LLM_HOST", None) if settings else os.getenv("LLM_HOST", "http://localhost:11434"))
        self.api_key = api_key or self._get_api_key(self.provider)
        self.mode = getattr(settings, "LLM_MODE", os.getenv("LLM_MODE", "local"))
        self.config = kwargs

    @staticmethod
    def _get_api_key(provider):
        if provider == "openai":
            return getattr(settings, "OPENAI_API_KEY", None) if settings else os.getenv("OPENAI_API_KEY")
        if provider == "claude":
            return getattr(settings, "CLAUDE_API_KEY", None) if settings else os.getenv("CLAUDE_API_KEY")
        return None  # Ollama/local does not require API key

    @classmethod
    def from_config(cls, **overrides):
        """
        Instantiate adapter from config (settings/env), with optional overrides.
        """
        return cls(**overrides)

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Calls the configured LLM and returns generated text.
        Supports ollama (local), openai (cloud), claude (cloud).
        """
        provider = (self.provider or "").lower()
        if provider == "ollama":
            return self._ollama_generate(prompt, **kwargs)
        elif provider == "openai":
            return self._openai_generate(prompt, **kwargs)
        elif provider == "claude":
            return self._claude_generate(prompt, **kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def _ollama_generate(self, prompt: str, **kwargs) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "options": kwargs.get("options", {}),
            "stream": False
        }
        url = f"{self.host.rstrip('/')}/api/generate"
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "")

    def _openai_generate(self, prompt: str, **kwargs) -> str:
        import openai
        openai.api_key = self.api_key
        model = self.model
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 512)
        )
        return response.choices[0].message.content.strip()

    def _claude_generate(self, prompt: str, **kwargs) -> str:
        # Requires: pip install anthropic
        import anthropic
        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 512),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7)
        )
        return response.content[0].text.strip()

    def info(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "host": self.host,
            "mode": self.mode,
            "api_key_present": bool(self.api_key),
            "config": self.config
        }
