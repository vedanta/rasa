# RASA – Role-Aligned Software Architecture

**Persona-Driven, Memory-Integrated AI Framework for Next-Gen AI Agents**

---

## 🚀 What is RASA?

RASA is a modular Python framework for building advanced, persona-driven, memory-aware AI agents.  
It empowers teams to create agents with unique "personality" and reasoning flows, multi-layered memory, and domain-specific intelligence—operationalized as APIs, command-line tools, or direct Python modules.

- **Persona-based:** Rich agent personas defined in YAML—each with frames (cognitive layers), operators (reasoning steps), and metadata.
- **Memory-integrated:** First-class support for stateless, short-term, session, and long-term memory (e.g. Redis, vector DB).
- **Extensible:** Plug in new personas, frames, operators, tools, or LLMs with minimal code.
- **Multi-interface:** Access RASA via FastAPI server, CLI, or import as a Python library.

---

## 📁 Project Structure

```
rasa/
  core/           # Core logic: runners, memory, agent base classes
  api/            # FastAPI app (main entrypoint)
  frames/         # Built-in cognitive frame classes
  operators/      # Built-in operator modules/tools
  llm/            # LLM adapters and config [see ./rasa/llm/LLM_CONFIG.md]
clients/
  rasa.py         # Unified CLI (local+API mode)
  README.md       # CLI usage and tips
apps/
  <persona>/      # Each persona in its own folder
    persona.yaml
    frames/
    operators/
  README.md       # Persona/app usage guide
  PERSONA.md      # Persona YAML schema/standards
tests/
  ...             # Pytest suite for API, CLI, core, personas
README.md         # (You are here - project onboarding!)
ARCHITECTURE.md   # System architecture and extensibility
CHANGELOG.md      # Version history and changes
```

---

## ⚡ Quick Start for Users & Developers

### 1. **Clone the repo**

```bash
git clone https://github.com/vedanta/rasa
cd rasa
```

### 2. **Set up a Conda Environment (Recommended for All Platforms)**

```bash
conda create -n rasa python=3.10
conda activate rasa
pip install -r requirements.txt
# (Optional, recommended for devs)
pip install -e .
```

### 3. **Run the API Server**

```bash
uvicorn rasa.api.main:app --reload
```

- Runs at http://localhost:8000 by default.
- Explore docs at http://localhost:8000/docs

### 4. **Try the CLI**

```bash
python -m clients.rasa list
python -m clients.rasa run --persona travel_concierge --input "Suggest a scenic European trip"
```

- See full CLI help: `python -m clients.rasa --help`
- To run against the API:  
  `python -m clients.rasa --mode api run --persona travel_concierge --input "Ideas for a weekend in Japan"`

---

## 👤 Adding Personas (Developers)

1. **Create a new folder:**
   ```
   apps/my_persona/
   ```
2. **Write a `persona.yaml`:**
   See `apps/PERSONA.md` for the full schema/spec.
3. **(Optional) Add custom frames/operators** under `frames/` and `operators/` for persona/domain logic.
4. **Test via CLI or API:**
   - `python -m clients.rasa run --persona my_persona --input "Test prompt"`

---

## 🧪 Testing

- **API:**  
  `pytest tests/test_api_master.py -s`
- **CLI:**  
  `pytest tests/test_cli_end_to_end.py -s`
- **All:**  
  `pytest`

All major endpoints and flows are covered with rich debug output.

---

## 🛠️ Advanced Usage

- **Streaming responses:**  
  Use `--stream` in CLI or `/stream` API endpoint.
- **Preferences:**  
  Pass `--preferences key=value` in CLI (repeatable) or in API payload.
- **Get structured JSON:**  
  Use `run-json` in API mode or `/output/json` endpoint.

---

## 🔗 Key Documents & Resources

- [ARCHITECTURE.md](./ARCHITECTURE.md) — Detailed architecture and flow diagrams
- [./clients/README.md](./clients/README.md) — CLI usage and switches
- [./apps/README.md](./apps/README.md) — Persona/app design, best practices
- [./apps/PERSONA.md](./apps/PERSONA.md) — Persona YAML schema and examples
- [./rasa/llm/LLM_CONFIG.md](./rasa/llm/LLM_CONFIG.md) — LLM config and adapters
- [CHANGELOG.md](./CHANGELOG.md) — Version history and recent changes

---

## 🛡️ Troubleshooting

- **ModuleNotFoundError / import issues:**  
  Ensure you have `__init__.py` in `rasa/`, `rasa/core/`, `clients/`.
  Run from the project root.
- **API not responding:**  
  Start with `uvicorn rasa.api.main:app --reload` and check port.
- **Persona not found:**  
  Confirm `apps/<persona>/persona.yaml` exists and is valid YAML.
- **LLM/backend errors:**  
  Check `llm.py`, try `/llm/health` or `/status` endpoints.

---

## 🤝 Contributing

- Fork, clone, and PR your features or fixes!
- Add new personas, frames, or operators following the standard structure.
- Write tests for all new logic—see `tests/`.
- Document YAML fields and code for onboarding.

---

**RASA lets you build and operate real-world, context-aware, persona-aligned AI agents in your domain.  
Get started, explore, and make it your own!**
