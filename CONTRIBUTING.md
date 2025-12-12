# Contributing to RASA

Thank you for your interest in contributing to RASA!

## Getting Started

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   conda create -n rasa python=3.10
   conda activate rasa
   ```
3. Install in development mode:
   ```bash
   make dev
   ```
4. Copy and configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

## Development Workflow

### Running Tests

```bash
make test          # All tests
make test-api      # API tests only
make test-cli      # CLI tests only
pytest tests/test_runner.py -v  # Single file
```

### Code Style

We use `black` for formatting and `ruff` for linting:

```bash
make format        # Auto-format code
make lint          # Check for issues
```

### Pre-commit Hooks

Install pre-commit hooks to auto-check before commits:

```bash
pre-commit install
```

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear, focused commits
3. Add tests for new functionality
4. Ensure all tests pass: `make test`
5. Ensure code is formatted: `make format`
6. Submit a PR with a clear description

### PR Title Convention

Use descriptive titles:
- `feat: add new memory backend for PostgreSQL`
- `fix: resolve session frame state persistence`
- `docs: update persona YAML specification`
- `test: add coverage for travel_concierge flow`

## Adding New Components

### New Persona

1. Create `apps/<persona_name>/persona.yaml`
2. Add custom frames in `apps/<persona_name>/frames/`
3. Add custom operators in `apps/<persona_name>/operators/`
4. Add tests in `tests/test_<persona_name>_flow.py`

### New Frame or Operator

1. Add to `rasa/frames/` or `rasa/operators/`
2. Follow existing patterns (inherit from base classes)
3. Add unit tests

## Reporting Issues

- Check existing issues first
- Include Python version, OS, and steps to reproduce
- For LLM-related issues, include provider and model info

## Questions?

Open a discussion or issue on GitHub.
