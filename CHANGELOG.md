# 📦 CHANGELOG

## v0.1.2 – Public Release + Framework Introduction (2025-04-29)

### 🌐 Public Launch

- Published official Medium article: “RASA – A Cognitive Framework for Agentic Memory in AI Systems”
- Released audio companion overview via NotebookLM
- Launched GitHub repo publicly with core implementation and docs

### 🧠 Conceptual Foundation

- Formalized the RASA architecture: Frames, Operators, Persona
- Refined messaging and language across README and public materials
- Defined RASA as a cognitive framework for building modular, memory-aware, role-aligned agents

### 🧭 Repository Enhancements

- Added detailed `README.md` aligned with article
- Linked Medium + audio narrative from GitHub and documentation
- Added changelog history and tagged `v0.1.2` as initial public release

---

### 🧭 Next Up

- Expand persona execution flows
- Add deeper LLM operator integration and role-driven reasoning
- Introduce memory persistence with Redis and ChromaDB



## v0.1.1 – API, Client CLI, and Robust Test Coverage (2025-04-21)

### ✨ Highlights

- Introduced `rasa/api/main.py` – FastAPI backend with endpoints: `/persona`, `/output`, `/output/json`, `/stream`
- Implemented top-level API client CLI (`client/api_cli.py`) for remote/API usage
- Added streaming and structured JSON output support to API and CLI
- Extended local CLI (`rasa/cli/main.py`) with:
    - List, describe, run commands
    - Richer inline help, preference docs, and streaming
- Added extensive pytest coverage for API, CLI, and API-CLI (13+ tests, all passing)
- CLI and API endpoints now fully documented
- New `README.md` for CLI usage and extension
- Improved developer onboarding and DX

---

### 🛠 Improvements

- Persona config (`describe`) now auto-loads domain operator docstrings
- Easier persona creation and extension patterns

---

### 🧭 Ready for Next

- FRAME_META, introspection, and self-documenting flows
- LLM operator integration
- UI and notebook demos


## v0.1.0 – Persona-Driven Cognitive Framework MVP (2025-04-20)

### ✨ Highlights

- Introduced `rasa/` as a reusable, modular framework for persona-based AI agents.
- Created a declarative `Persona` system with YAML + programmatic `.build()` support.
- Defined cognitive `Frames` and reasoning `Operators` as composable agents.
- Integrated `LangGraph` for step-by-step cognition flow control.

---

### 🧠 Core Framework

- `State`: Shared state structure with support for `user_input`, `context`, `preferences`, `output`, `metadata`, etc.
- `Runner`: Executes a persona-defined flow using LangGraph (with dynamic frame/operator loading).
- `BaseAgent`, `FrameAgent`, `OperatorAgent`: Core abstractions with clean `run(state: State) -> State` contract.

---

### 🎭 Persona System

- `Persona.from_yaml(path)` and `Persona.build(dict)` support
- Declarative fields:
  - `state_stack` (frames)
  - `operators` (generic)
  - `domain_operators` (app-specific fallback logic)
  - `metadata` (tone, domain)
- Persona trace and tone-based reasoning

---

### ⚙️ Operators

- `preference_agent.py`: Normalizes and injects user preferences
- `tone_formatter.py`: Adjusts output style (friendly, poetic, analytical)
- `heuristic_agent.py`: Delegates to `domain_operators` dynamically

---

### 🧩 Domain-Specific Operators

- `travel_heuristic_agent.py`: Suggests destinations based on region, style, season
- `economy_heuristic_agent.py`: Explains impacts of interest rates on small businesses

---

### 👥 Example Apps

- `apps/travel_concierge`: Narrative travel assistant
- `apps/economist_advisor`: Analytical policy explainer

---

### 🧪 Test Coverage

- `test_runner.py`: Graph runner with dummy frames/operators
- `test_travel_concierge_flow.py`: Full persona execution + formatting
- `test_economist_advisor_flow.py`: Domain-specific operator dispatch
- `test_heuristic_agent.py`: Fallback logic for operator routing
- `test_persona_build.py`: Programmatic persona construction

---

### 📁 Structure

```
rasa/
├── core/            # State, Agent, Persona, Runner
├── frames/          # Stateless, Session, Short-Term
├── operators/       # General operators
├── memory/          # (Placeholder)
apps/
├── travel_concierge/
├── economist_advisor/
tests/
```

---

### 🧭 Next Steps (v0.2.0 Preview)

- LangGraph visualization (Mermaid)
- Memory integration (Redis, Chroma)
- CLI runner for personas
- LLM toolchain via LangChain
- Multi-tone personas and CoT prompting
- Dev docs and API reference