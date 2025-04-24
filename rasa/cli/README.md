# 🖥️ RASA CLI

The command-line interface for [RASA](../), your persona-driven, memory-aware agent framework.

---

## 🚀 Usage Examples

### List all available personas

```bash
python -m rasa.cli.main list
```

### Describe a persona (see preferences, docstring, config)

```bash
python -m rasa.cli.main describe --persona travel_concierge
```

### Run a persona (input and preferences)

```bash
python -m rasa.cli.main run --persona travel_concierge --input "Plan a weekend in Italy" --preferences region=europe --preferences travel_style=relaxed --preferences season=spring
```

### Stream output word by word (for live chat UX)

```bash
python -m rasa.cli.main run --persona travel_concierge --input "Plan a weekend in Italy" --preferences region=europe --stream
```

---

## 🧠 Features

- **Discover**: Lists all personas found under `apps/`.
- **Explain**: Shows persona config and required preferences via docstring.
- **Run**: Executes any persona logic with customizable input and preferences.
- **Stream**: Simulates real-time output (great for CLI chat demos).
- **Help**: Every command supports `-h/--help` for quick guidance.

---

## 📝 Tips & Best Practices

- Each `--preferences` flag must be followed by a single key=value pair.
- Use `describe` to see what each persona expects as input.
- Extend the CLI with new commands using [Click](https://click.palletsprojects.com/).
- Preferences are always strings; validate/convert as needed in your domain agent logic.

---

## 🧩 Extending

To add a new persona:
1. Create a new folder in `apps/` with a `persona.yaml`.
2. Add your domain operators to `apps/<persona>/operators/`.
3. Run `python -m rasa.cli.main list` to see your new persona.

---

## 🤖 Example: Economist Advisor

```bash
python -m rasa.cli.main run --persona economist_advisor --input "Explain inflation for small businesses" --preferences topic=inflation --preferences focus=small_business
```

---

## 📚 See also

- [RASA main README](../README.md)
- [Click documentation](https://click.palletsprojects.com/)

---

Happy reasoning! 🚀