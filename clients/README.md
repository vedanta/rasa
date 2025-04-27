# RASA CLI

**Unified Command-Line Interface for Role-Aligned Software Architecture (RASA) Agents**

---

## 🚀 Overview

The **RASA CLI** is your gateway to running, testing, and exploring persona-driven, memory-integrated AI agents directly from your terminal.  
It supports **both direct (local Python)** and **API (HTTP)** operation, making it suitable for local development, production, and automation.

---

## 📦 Features

- List and describe available personas
- Run a persona with custom user input and preferences
- Get structured (JSON) output (API mode)
- Stream output word-by-word (great for chatbots and demos)
- Query LLM backend info and health (API mode)
- Check server status (API mode)
- Powerful preferences via CLI switches
- Works directly on Python or with a running RASA API server

---

## 🛠️ Installation & Setup

- Place the CLI file as `clients/rasa.py` in your repo.
- Make sure your project structure is:

  ```
  project_root/
    rasa/
      core/
      ...
    clients/
      rasa.py
    apps/
      <personas...>
    ...
  ```

- Ensure `rasa/`, `rasa/core/`, and `clients/` all contain `__init__.py`.

---

## 📝 Usage

### Basic Syntax

```bash
python -m clients.rasa [OPTIONS] COMMAND [ARGS]...
```

- By default, runs in **direct** mode (local Python).
- Use `--mode api` to send requests to a RASA API server (`--api-url` to set address, default `http://localhost:8000`).

---

### Commands

| Command      | Description                                                   | Modes        |
|--------------|--------------------------------------------------------------|--------------|
| `list`       | List all available personas                                  | direct, api  |
| `describe`   | Show persona config, frames, operators, and metadata         | direct       |
| `run`        | Run persona with input/preferences; stream supported         | direct, api  |
| `run-json`   | Run persona, get structured JSON output                      | api          |
| `llm-info`   | Show LLM backend/provider info                               | api          |
| `llm-health` | Check LLM backend health                                     | api          |
| `status`     | Show API server status                                       | api          |

---

### Global Options

| Option            | Description                              | Default                |
|-------------------|------------------------------------------|------------------------|
| `--mode`          | Operation mode: `direct` or `api`        | direct                 |
| `--api-url`       | RASA API base URL (API mode only)        | http://localhost:8000  |

---

### Command Arguments & Switches

- `--persona` : Name of the persona (required for most commands)
- `--input` : User input (required for `run` and `run-json`)
- `--preferences` : Key=value preference, repeatable (e.g. `--preferences key=val --preferences foo=bar`)
- `--stream` : Stream output word-by-word (for `run`)

---

## 🎯 Examples

**List personas (direct):**
```bash
python -m clients.rasa list
```

**Describe a persona (direct):**
```bash
python -m clients.rasa describe --persona travel_concierge
```

**Run a persona (direct):**
```bash
python -m clients.rasa run --persona strategic_stock_analyst --input "Should I buy Nvidia today?"
```

**Run with preferences:**
```bash
python -m clients.rasa run --persona strategic_stock_analyst --input "Suggest a safe stock" --preferences risk_tolerance=low --preferences sector=utilities
```

**Run and stream output:**
```bash
python -m clients.rasa run --persona travel_concierge --input "Describe a scenic European trip" --stream
```

**Run in API mode (server must be running):**
```bash
python -m clients.rasa --mode api run --persona travel_concierge --input "Trip for foodies in India"
```

**Get structured output (API mode):**
```bash
python -m clients.rasa --mode api run-json --persona travel_concierge --input "Top travel tips for 2024"
```

**Check LLM info and health (API mode):**
```bash
python -m clients.rasa --mode api llm-info
python -m clients.rasa --mode api llm-health
```

**Show server status (API mode):**
```bash
python -m clients.rasa --mode api status
```

---

## ⚡ Tips & Best Practices

- For all commands, run from the **project root**.
- In **direct mode**, the CLI loads Python classes directly; in **API mode**, it talks to the server.
- **API mode** requires a running RASA API (`uvicorn rasa.api.main:app --reload`).
- Preferences can be passed as many times as needed with `--preferences key=value`.
- Use `--help` or `-h` after any command for quick usage info.

---

## 🧩 Extending the CLI

- Add new commands using `@cli.command` in `rasa.py`.
- Customize output or error handling with `click.secho` for color and clarity.
- All commands are fully type-annotated and easy to expand.

---

## 🛡️ Troubleshooting

- **ModuleNotFoundError:** Ensure you have `__init__.py` files in `rasa/`, `rasa/core/`, `clients/`.
- **"not found" errors:** Check persona folder name and that `persona.yaml` exists.
- **API mode connection errors:** Ensure the server is running and the URL/port is correct.
- **Direct mode import errors:** Run from project root, or ensure Python finds your local packages.

---

## 👋 Get Help

- Run any command with `--help` for usage and options.
- For more info or troubleshooting, see the [RASA documentation](../README.md).

---

**RASA CLI makes persona-powered AI accessible and scriptable for everyone.  
If you have suggestions or find bugs, open an issue or contribute!**
