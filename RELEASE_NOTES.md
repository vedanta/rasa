# 🏷️ Release Notes – RASA v0.1.1

**Release Date:** 2025-04-21

## What's New?

- 🚀 **API Layer:**  
  - Production-ready FastAPI backend for persona-driven AI agents
  - Endpoints: `/persona`, `/output`, `/output/json`, `/stream`
- 🖥️ **API Client CLI:**  
  - Decoupled CLI at `client/api_cli.py` for talking to the API (no direct imports)
  - All the features of the local CLI, remotely!
- 📦 **Local CLI Improvements:**  
  - List, describe, run, and stream commands
  - Preference doc auto-discovery from operator docstrings
  - Rich, self-documenting inline help
- 🧪 **Full Test Coverage:**  
  - 13+ robust tests covering API, CLI, API-CLI
  - All green, all platforms!
- 📚 **Docs and Onboarding:**  
  - CLI README, API docstrings, usage examples

---

## Why It Matters

- **You can run, query, and demo RASA from anywhere – code, CLI, or API**
- **Modular for teams, UIs, and future automation**
- **The foundation for LLM, memory, and advanced personas is rock-solid**

---

## Next Up

- FRAME_META system for auto-generated diagrams/docs
- LLM reasoning integration
- Persona and operator introspection APIs

---

_Upgrade, experiment, and build with confidence!_
