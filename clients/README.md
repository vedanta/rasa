# RASA CLI

Unified command-line interface for running, inspecting, and debugging persona-driven AI agents.  
Supports both direct (in-process Python) and API (HTTP) operation.

---

## 🏃‍♂️ Usage

**From project root:**  
```bash
PYTHONPATH=. python -m clients.main --mode [direct|api] <command> [options]
```

- `--mode direct`: Run everything locally using Python (default).
- `--mode api`: Send all commands via HTTP to your RASA API server (e.g., http://localhost:8000).

---

## 💻 Available Commands

| Command      | Description                                         | Modes         |
|--------------|-----------------------------------------------------|---------------|
| `list`       | List available personas in `apps/`                  | direct, api   |
| `describe`   | Show persona config and metadata                    | direct        |
| `run`        | Run a persona with input and preferences            | direct, api   |
| `run-json`   | Run persona, get JSON-structured output             | api only      |
| `llm-info`   | Show LLM provider/model config (API only)           | api only      |
| `llm-health` | Check LLM server health (API only)                  | api only      |
| `status`     | Show API server status (API only)                   | api only      |

---

## 🔎 Examples

**List personas:**  
```bash
PYTHONPATH=. python -m clients.main --mode direct list
```

**Describe a persona:**  
```bash
PYTHONPATH=. python -m clients.main --mode direct describe --persona demo_app
```

**Run a persona:**  
```bash
PYTHONPATH=. python -m clients.main --mode direct run --persona demo_app --input "Suggest a weekend trip"
```

**Run with preferences:**  
```bash
PYTHONPATH=. python -m clients.main --mode direct run --persona demo_app --input "Trip for foodies in India" --preferences region=italy --preferences travel_style=foodie
```

**Run with streaming output:**  
```bash
PYTHONPATH=. python -m clients.main --mode api run --persona demo_app --input "Where to travel in spring?" --stream
```

**Run and get JSON output (API only):**  
```bash
PYTHONPATH=. python -m clients.main --mode api run-json --persona demo_app --input "Trip for nature lovers"
```

**LLM info and status (API):**
```bash
PYTHONPATH=. python -m clients.main --mode api llm-info
PYTHONPATH=. python -m clients.main --mode api llm-health
PYTHONPATH=. python -m clients.main --mode api status
```

---

## 📝 Tips

- Always put global options like `--mode` *before* the command.
- Preferences can be repeated: `--preferences key=value --preferences another=val`
- Persona name can be just the folder (e.g., `demo_app`) or a full path to a persona YAML.

---

For more, see [Persona.md](../Persona.md) at the repo root.