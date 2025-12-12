# RASA – Role-Aligned Software Architecture

[![CI](https://github.com/vedanta/rasa/actions/workflows/ci.yml/badge.svg)](https://github.com/vedanta/rasa/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Build persona-driven, memory-aware AI agents with declarative YAML configuration.**

RASA is a modular Python framework for creating AI agents with distinct personalities, multi-layered memory, and domain-specific reasoning. Define your agent's behavior in YAML, and access it via API, CLI, or Python.

## Key Features

| Feature | Description |
|---------|-------------|
| **Persona-Driven** | Define agent personality, tone, and behavior in YAML |
| **Memory Layers** | Stateless, short-term, session, and long-term memory support |
| **Cognitive Frames** | Chain reasoning steps with composable frame classes |
| **Multiple LLMs** | Ollama, OpenAI, and Claude adapters included |
| **Flexible Access** | FastAPI server, CLI tool, or direct Python import |

## Quick Start

### Installation

```bash
git clone https://github.com/vedanta/rasa
cd rasa

# Option 1: Using make (recommended)
make install

# Option 2: Manual
conda create -n rasa python=3.10
conda activate rasa
pip install -e .
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your LLM settings (Ollama runs locally by default)
```

### Run the Server

```bash
make serve
# Or: uvicorn rasa.api.main:app --reload
```

API available at http://localhost:8000 | Docs at http://localhost:8000/docs

### Try the CLI

```bash
# List available personas
python -m clients.rasa list

# Run a persona
python -m clients.rasa run --persona travel_concierge --input "Plan a weekend in Tokyo"

# Stream output
python -m clients.rasa run --persona travel_concierge --input "Best cafes in Paris" --stream
```

## Example Persona

Personas are defined in `apps/<name>/persona.yaml`:

```yaml
name: travel_concierge
description: Personalized travel advice and recommendations
frames:
  - stateless_frame
  - session_frame
  - short_term_frame
operators:
  - preference_agent
  - tone_formatter
prompt_style: narrative
metadata:
  tone: friendly
  domain: travel
  traits: ["curious", "helpful"]
```

## API Usage

```bash
# Plain text response
curl -X POST http://localhost:8000/output \
  -H "Content-Type: application/json" \
  -d '{"persona": "travel_concierge", "input": "Suggest a beach destination"}'

# Structured JSON response
curl -X POST http://localhost:8000/output/json \
  -H "Content-Type: application/json" \
  -d '{"persona": "travel_concierge", "input": "Top 3 European cities"}'

# Streaming response
curl -X POST http://localhost:8000/stream \
  -H "Content-Type: application/json" \
  -d '{"persona": "travel_concierge", "input": "Describe Italian cuisine"}'
```

## Python Usage

```python
from rasa.core.persona import Persona
from rasa.core.runner import Runner

persona = Persona.from_yaml("apps/travel_concierge/persona.yaml")
runner = Runner(persona)

result = runner.run({
    "input": "Recommend a hiking trip",
    "preferences": {"difficulty": "moderate"}
})
print(result["output"])
```

## Architecture

```
User Input → API/CLI → Persona Loader → Runner → Frames → Operators → LLM → Output
```

| Component | Purpose |
|-----------|---------|
| **Persona** | YAML config defining agent behavior |
| **Frame** | Cognitive processing step (memory layer) |
| **Operator** | Reasoning/transformation module |
| **Runner** | Orchestrates execution flow |

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed diagrams and extension points.

## Project Structure

```
rasa/
  api/            # FastAPI server
  core/           # Runner, Persona, State, Agent
  frames/         # Built-in frames (stateless, session, short_term, long_term)
  operators/      # Built-in operators (preference, critic, heuristic, tone)
  llm/            # LLM adapters (Ollama, OpenAI, Claude)
  config/         # Settings and env loading
clients/
  rasa.py         # CLI tool
apps/
  <persona>/      # Persona definitions
    persona.yaml
    frames/       # Custom frames
    operators/    # Custom operators
tests/            # Test suite
```

## Development

```bash
make dev          # Install with dev dependencies
make test         # Run all tests
make test-api     # Run API tests
make test-cli     # Run CLI tests
make lint         # Check code style
make format       # Auto-format code
```

## Documentation

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | System design and flow diagrams |
| [PERSONA_DESIGN.md](./PERSONA_DESIGN.md) | Deep dive into persona design |
| [apps/Persona.md](./apps/Persona.md) | Persona YAML specification |
| [clients/README.md](./clients/README.md) | CLI reference |
| [rasa/llm/LLM_CONFIG.md](./rasa/llm/LLM_CONFIG.md) | LLM configuration guide |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guidelines |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run from project root; ensure `__init__.py` files exist |
| API not responding | Check server is running on correct port |
| Persona not found | Verify `apps/<persona>/persona.yaml` exists |
| LLM errors | Check `.env` config; use `/llm/health` endpoint |

## Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

```bash
make dev              # Setup dev environment
pre-commit install    # Enable pre-commit hooks
make test             # Verify tests pass
```

## License

MIT License - see [LICENSE](./LICENSE) for details.
