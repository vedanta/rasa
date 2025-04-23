# 📦 CHANGELOG

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