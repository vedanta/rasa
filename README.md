# 🧠 RASA – Role-Aligned Software Architecture

*Persona-driven, memory-aware AI agents with clear cognitive structure, modularity, and real-world usability.*

---
# RASA – Role-Aligned Software Architecture

[![Build Status](https://github.com/vedanta/rasa/actions/workflows/ci.yml/badge.svg)](https://github.com/vedanta/rasa/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<!-- Uncomment these once your package is on PyPI! -->
<!--
[![PyPI version](https://badge.fury.io/py/rasa-framework.svg)](https://badge.fury.io/py/rasa-framework)
[![Python Versions](https://img.shields.io/pypi/pyversions/rasa-framework.svg)](https://pypi.org/project/rasa-framework/)
-->

## 🚀 Project Overview

RASA is a Python framework for building **persona-based AI agents** that combine modular cognitive “frames,” memory layers, explicit reasoning operators, and plug-and-play interfaces.  
Inspired by modern LLM agent stacks and production experience, RASA helps you:

- Encode agent identity, behavior, and reasoning flow (personas)
- Compose workflows using frames (stateless, session, short_term, long_term, etc.)
- Integrate operator logic (preference_agent, heuristic_agent, tone_formatter, LLM tools)
- Plug in memory (Redis, VectorDB) and tools as needed
- Deploy as CLI, API, or in any Python environment

---

## 🏗️ Architecture

### 🧩 Key Concepts

- **Frames:**  
  Cognitive state steps (stateless, session, short_term, long_term) executed via LangGraph
- **Operators:**  
  Reasoning/action units (preference_agent, heuristic_agent, tone_formatter, LLM tools)
- **Personas:**  
  Configurations defining agent identity, tone, cognitive flow, and domain tools (`persona.yaml`)
- **Memory:**  
  Session/short-term via Redis, long-term via VectorDB (future-ready)
- **LLM Adapter:**  
  Pluggable interface for OpenAI, Ollama, Claude, etc. (planned)

---

### 🗂️ Directory Structure

```
rasa/
  ├── core/         # BaseAgent, FrameAgent, OperatorAgent, Runner, Persona, State
  ├── frames/       # Stateless, Session, ShortTerm, (LongTerm) frame modules
  ├── operators/    # General operators: preference, heuristic, tone, etc.
  ├── api/          # FastAPI backend (serves personas as an API)
  ├── cli/          # Local CLI for direct persona execution
apps/
  ├── travel_concierge/     # Example persona (travel recommendations)
  ├── economist_advisor/    # Example persona (economics explainer)
client/
  └── api_cli.py    # API-based CLI client (calls FastAPI endpoints)
tests/
  └── ...           # Pytest test suite for core, CLI, API, client
```

---

## 💻 Local Setup

### 1. Clone the repo and install dependencies

```bash
git clone <repo-url>
cd rasa
conda create -n rasa python=3.10 -y
conda activate rasa
pip install -r requirements.txt
```

### 2. Run the CLI

```bash
python -m rasa.cli.main list
python -m rasa.cli.main describe --persona travel_concierge
python -m rasa.cli.main run --persona travel_concierge --input "Plan a weekend in Italy" --preferences region=europe --preferences season=spring
```

### 3. Run the API server

```bash
uvicorn rasa.api.main:app --reload
# Visit http://localhost:8000/docs for interactive Swagger UI
```

### 4. Use the API Client CLI

```bash
python client/api_cli.py list
python client/api_cli.py run --persona travel_concierge --input "..." --preferences region=europe
```

### 5. Run all tests

```bash
pytest tests/ -v
```

---

## 👥 Audience

- **End Users:**  
  Use RASA as a ready-made chatbot, API service, or CLI persona engine.  
  No coding required—just run and configure via persona YAML files.
- **Developers / Researchers:**  
  Build new personas, extend frames/operators, connect memory, or plug in new LLMs/tools.
  All core interfaces are designed for extension and introspection.

---

## 🧑‍💻 **Developer Onboarding**

1. **Explore sample personas in `apps/`**
    - See how `persona.yaml` wires frames, operators, and tone

2. **Run the CLI and API**
    - Try `python -m rasa.cli.main list`
    - Start API with `uvicorn rasa.api.main:app --reload`

3. **Develop & Test**
    - Add new frames/operators with docstrings and `FRAME_META`
    - Add to test suite in `tests/`
    - Regenerate docs and diagrams as your pipeline grows

4. **Contribute**
    - All new frames/operators should document their contract via `FRAME_META` for self-documenting code and tools

---

## 🌟 **Why RASA?**

- Clear, explicit cognitive structure: code and docs are always in sync
- Persona-first: modular, configurable, and human-aligned
- Fully testable and ready for production integration (API, CLI, notebooks, or UI)
- Designed for LLM integration, memory, and team collaboration from day one

---

## 📚 **See Also**

- [CLI README](./rasa/cli/README.md)
- [CHANGELOG](./CHANGELOG.md)
- [API docs (Swagger UI)](http://localhost:8000/docs) – when running locally

---

**Build AI agents that think, remember, and explain—just like your organization.**

*Ready to explore or contribute? Start with the CLI or API, and check out the sample personas!*
