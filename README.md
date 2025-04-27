# RASA – Role-Aligned Software Architecture

**Persona-Driven, Memory-Integrated AI Framework**

---

## 🚀 What is RASA?

RASA is a modular Python framework for building advanced, persona-driven, memory-aware AI agents.  
With RASA, you can create agents with unique behaviors, multi-layered memory, and domain-specific reasoning—either as APIs or directly in your own Python workflows.

- **Persona-based:** Define rich agent "personas" in YAML—each with their own frames (cognitive layers), operators (reasoning tools), and metadata.
- **Memory-integrated:** Support for short-term, session, and long-term memory (vector DB, Redis, etc.).
- **Flexible interfaces:** Use via a FastAPI server, a powerful CLI, or directly as a Python library.
- **Extensible:** Add new personas, frames, and operators in a few lines.

---

## 📁 Project Structure

```
rasa/
  core/           # Core library: runners, base agents, memory, etc.
  api/            # FastAPI application and endpoints
clients/
  rasa.py         # Unified CLI for direct and API usage
apps/
  <persona_name>/
    persona.yaml  # Persona definition
    frames/       # Custom frames for this persona
    operators/    # Custom operators for this persona
tests/
  ...             # Pytest suite (API, CLI, persona, frame/operator tests)
README.md         # (You are here)
```

---

## ⚡ Quick Start

### 1. **Clone & Install**

```bash
git clone https://github.com/your-org/rasa.git
cd rasa
pip install -e .    # Optional, but recommended for dev
pip install -r requirements.txt
```

### 2. **Run the API**

```bash
uvicorn rasa.api.main:app --reload
```

- By default, runs at http://localhost:8000

### 3. **Try the CLI**

- List personas:
  ```bash
  python -m clients.rasa list
  ```

- Run a persona (direct):
  ```bash
  python -m clients.rasa run --persona strategic_stock_analyst --input "Should I buy Nvidia today?"
  ```

- Run via API:
  ```bash
  python -m clients.rasa --mode api run --persona travel_concierge --input "Best city in Europe for food?"
  ```

- Get full CLI help:
  ```bash
  python -m clients.rasa --help
  ```

---

## 👤 Adding Personas

1. **Create a new app folder:**
   ```
   apps/my_persona/
   ```

2. **Write a persona YAML:**
   ```
   apps/my_persona/persona.yaml
   ```
   (See [Persona.md](apps/my_persona/persona.yaml) or sample personas for reference.)

3. **Add custom frames/operators as needed:**
   ```
   apps/my_persona/frames/my_custom_frame.py
   apps/my_persona/operators/my_operator.py
   ```

4. **Test:**
   - Use the CLI:  
     `python -m clients.rasa run --persona my_persona --input "Try me!"`
   - Or call via the API.

---

## 🧪 Testing

- **API tests:**
  ```
  pytest tests/test_api_master.py -s
  ```

- **CLI tests:**
  ```
  pytest tests/test_cli_end_to_end.py -s
  ```

- **Direct Python tests:** (for core/frame/operator logic)
  ```
  pytest
  ```

---

## 🛠️ Advanced Usage

- **Stream responses:**  
  Add `--stream` to CLI run command for word-by-word output.
- **Use preferences:**  
  Pass `--preferences key=value` multiple times.
- **Get JSON output:**  
  Use `run-json` in API mode for structured responses.

---

## 🛡️ Troubleshooting

- **Imports fail / ModuleNotFoundError:**  
  Ensure you run from the project root, and `rasa/`, `clients/` have `__init__.py`.
- **API not responding:**  
  Make sure you started with `uvicorn rasa.api.main:app --reload` and port matches `--api-url`.
- **Persona not found:**  
  Ensure your `apps/<persona>/persona.yaml` exists and is valid YAML.
- **LLM issues:**  
  Check `llm.py` and API health endpoints (`llm-info`, `llm-health`).

---

## 🤝 Contributing

- Open a PR or issue for bugs, ideas, or improvements!
- Add new personas, operators, or frames by following the established folder structure.
- Write tests for new logic or personas.
- Document your persona YAML with field descriptions.

---

## 📚 Reference & Help

- CLI Help:  
  `python -m clients.rasa --help`
- API Docs:  
  http://localhost:8000/docs (when running)
- Persona spec:  
  [Persona.md](apps/sample_persona/persona.yaml) (or see `clients/README_CLI.md`)
- For advanced or team onboarding, see [ARCHITECTURE.md](ARCHITECTURE.md) and code comments.

---

**RASA empowers you to build, test, and operate real-world, context-aware AI agents—fast.  
Get started, explore, and make it your own!**
