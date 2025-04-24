# How to Write a Persona

Personas define the identity, behavior, frames, and operators of an agent in RASA.

---

## 🧩 Persona YAML Structure

```yaml
name: "my_demo_persona"
description: "A friendly assistant for travel planning"
state_stack:
  - stateless_frame
frames:
  - stateless_frame
operators: []
prompt_style: default
metadata:
  tone: friendly
  domain: travel
```

**Key fields:**
- `name`: Human-readable name for the persona.
- `description`: What this agent does or who it helps.
- `state_stack`: **REQUIRED**. List of frame names (in order) to execute for this persona.
- `frames`: (Optional, for legacy support or clarity—should match `state_stack`).
- `operators`: List of operators (tools/reasoners) available to this persona.
- `prompt_style`: How prompts are styled (e.g., `default`, `narrative`, etc.).
- `metadata`: Freeform dict for domain, tone, tags, etc.

---

## 🚦 Example: Minimal Stateless Persona

```yaml
name: "llm_stateless_demo"
description: "Demo persona that uses the stateless frame with LLM"
state_stack:
  - stateless_frame
frames:
  - stateless_frame
operators: []
prompt_style: default
```

---

## 🔗 Linking Operators/Frames

To chain multiple reasoning steps, just add more frames:

```yaml
state_stack:
  - stateless_frame
  - short_term_memory_frame
  - recommendation_frame
```

---

## 🛠️ Tips

- The first frame in `state_stack` is always the entry point.
- `operators` can be empty, or you can add operator names to use tools like preference lookups, heuristics, etc.
- For advanced personas, you can add custom fields or extra metadata as your app evolves.

---

## 📁 Placement

- Each persona lives in its own subdirectory under `apps/`, e.g. `apps/demo_app/persona.yaml`.

---

For more usage and CLI examples, see [clients/README.md](clients/README.md).