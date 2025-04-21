# 🧠 RASA Example Apps

This directory contains example applications built using the **RASA (Role-Aligned Software Architecture)** framework.  
Each app showcases how to define a `Persona`, wire it with cognitive `Frames` and reasoning `Operators`, and run it via LangGraph.

---

## 📂 Current Apps

- `travel_concierge/` – A warm, narrative agent that gives cozy trip recommendations
- `economist_advisor/` – An analytical assistant explaining economic tradeoffs and policy impacts

---

## 🚀 Running an App

```bash
PYTHONPATH=. python apps/<app_name>/main.py
```

Example:

```bash
PYTHONPATH=. python apps/travel_concierge/main.py
```

---

## 🧑‍🎓 How to Build a New Persona

Each app contains a `persona.yaml` file that defines:

```yaml
name: pragmatic_economist
description: A measured, analytical assistant for economic analysis.

state_stack:
  - stateless_frame
  - session_frame

operators:
  - preference_agent
  - heuristic_agent
  - tone_formatter

domain_operators:
  - economy_heuristic_agent

prompt_style: analytical
memory_scope: user

metadata:
  domain: economy
  tone: analytical
```

### 📌 Required Fields

| Field | Description |
|-------|-------------|
| `state_stack` | Ordered list of Frames (cognitive states) |
| `operators` | Core Operators used across domains |
| `domain_operators` | Optional per-domain tools (e.g., `travel_heuristic_agent`) |
| `metadata` | Contextual cues like `tone`, `domain` |

---

## ⚙️ Adding a Domain Operator

1. Create a file under your app’s `operators/` directory  
   Example: `apps/economist_advisor/operators/economy_heuristic_agent.py`

2. Define a class that inherits from `OperatorAgent`:

```python
from rasa.core.state import State
from rasa.core.agent import OperatorAgent

class EconomyHeuristicAgent(OperatorAgent):
    def run(self, state: State) -> State:
        # Perform domain logic
        return {**state, "output": "Your explanation here"}
```

3. Add it to `domain_operators` in your `persona.yaml`.

4. RASA will dispatch to it via the shared `heuristic_agent`.

---

## 🧪 Testing New Apps

Add a test under `tests/`:

```bash
tests/test_<app_name>_flow.py
```

Use the full Runner like this:

```python
from rasa.core.runner import Runner
from rasa.core.persona import Persona

persona = Persona.from_yaml("apps/economist_advisor/persona.yaml")
runner = Runner(persona)
final_state = runner.run(state)
```

---

## 🧠 Tip

You can also define personas directly in Python using:

```python
Persona.build({...})
```

---

Ready to add your own?  
Clone any app directory, modify `persona.yaml`, and start exploring the power of modular cognition.