# 🧠 LLM Configuration & Usage in RASA

## Overview

RASA supports **dynamic, reloadable LLM configuration** for maximum flexibility in both development and production.
All settings for LLMs (Ollama, OpenAI, Claude, etc.) are managed via environment variables, which are loaded from `.env` or `.env-llm` files.

---

## 📦 Where Config Lives

- **Main location:** `rasa/config/.env` and `rasa/config/.env-llm`
- **Settings loader:** `rasa/config/settings.py`
  - Provides `load_env_from_dir()` to dynamically reload config from any directory
  - Exposes getter functions for all config (always up-to-date)

---

## 🛠️ How It Works

1. **Settings are always accessed via dynamic getter functions.**
   This ensures they reflect the latest `.env` loaded—even after a reload.

2. **To load config from a new env file** (e.g., for testing or switching environments):
   ```python
   from rasa.config import settings
   settings.load_env_from_dir("/path/to/env_dir")
   ```
   All subsequent calls to the getters will reflect the new config.

3. **To access config anywhere in your code:**
   ```python
   from rasa.config import settings
   provider = settings.get_llm_provider()
   model = settings.get_llm_model()
   api_key = settings.get_openai_api_key()
   host = settings.get_llm_host()
   ```

---

## ⚡ Example: Using LLM in Your Code

```python
from rasa.llm.llm_adapter import LLMAdapter
from rasa.config import settings

llm = LLMAdapter(
    provider=settings.get_llm_provider(),
    model=settings.get_llm_model(),
    api_key=settings.get_openai_api_key(),
    host=settings.get_llm_host()
)
response = llm.generate("Suggest a spring trip in Europe.")
print(response)
```
Or, use the class’s own config loading:
```python
llm = LLMAdapter.from_config()  # Uses the current values in settings.py
```

---

## 🧪 Testing & Reloading

- Use `settings.load_env_from_dir(tempdir)` in tests to swap between different `.env` files on the fly.
- Use only the dynamic getters (never module-level constants) to always reflect the latest env.

**Tip:** Use pytest’s `monkeypatch.delenv()` to clear variables between tests for full isolation.

---

## 📝 Best Practices

- Only use `settings.get_*()` functions to read config!
- Never rely on cached/static variables from module import.
- Store example config in `.env-llm` and keep real secrets in `.env` (never commit real keys).
- Use `.env-llm` for onboarding, local dev, and as a template for CI/CD.

---

## 💡 Why This Pattern?

- **Hot-reloadable:** Instantly swap environments without restarting your Python process.
- **Testable:** Every test can use its own config, no cross-talk or leaking settings.
- **Clean:** Onboarding and docs always match code behavior.

---

## 🖥️ Sample Program: Print LLM Config and Source

```python
from rasa.config import settings
import os

def detect_config_source():
    this_dir = os.path.dirname(os.path.abspath(settings.__file__))
    env = os.path.join(this_dir, ".env")
    env_llm = os.path.join(this_dir, ".env-llm")
    if os.path.exists(env):
        return env
    elif os.path.exists(env_llm):
        return env_llm
    else:
        return "(No .env or .env-llm found, using defaults)"

print("Active LLM Config:")
print("  PROVIDER:", settings.get_llm_provider())
print("  MODEL:   ", settings.get_llm_model())
print("  HOST:    ", settings.get_llm_host())
print("  OPENAI_KEY (if set):", settings.get_openai_api_key())
print("  CLAUDE_KEY (if set):", settings.get_claude_api_key())
print("Config loaded from:", detect_config_source())
```

---

For any LLM-related development, just:
- Update `rasa/config/.env` or `.env-llm`
- Use the dynamic getters in `rasa.config.settings`
- Import and use `LLMAdapter` with those settings

---

**You now have a fully modern, reloadable, and testable LLM configuration system in RASA!**