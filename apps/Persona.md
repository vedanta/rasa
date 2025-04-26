# Persona YAML Specification

This document explains the **persona.yaml** file format for RASA agents.  
Use this guide to create new personas, understand all options, and ensure your personas are robust and future-proof.

---

## 🧩 Field Reference

| Field             | Type         | Required | Description                                                                 |
|-------------------|--------------|----------|-----------------------------------------------------------------------------|
| `name`            | str          | **Yes**  | Unique name for the persona.                                                |
| `alias`           | str          | No       | Short unique identifier (for CLI/API, e.g. `aa`).                           |
| `description`     | str          | **Yes**  | Short, human-friendly description.                                          |
| `frames`          | list[str]    | **Yes**  | Ordered list of frame names to execute (from core or domain frames).        |
| `operators`       | list[str]    | No       | General-purpose operator/tool names (for core logic).                       |
| `domain_frames`   | list[str]    | No       | App-specific frame names (modules in `apps/<persona>/frames/`).             |
| `domain_operators`| list[str]    | No       | App-specific operator/tool names (in `apps/<persona>/operators/`).          |
| `prompt_style`    | str          | No       | LLM output prompt style (e.g., `default`, `scientific`).                    |
| `metadata`        | dict         | No       | Arbitrary metadata (tone, domain, traits, sources, etc.).                   |

---

## ✨ Example: Minimal Persona

```yaml
name: "llm_stateless_demo"
description: "Demo persona using only the stateless frame and LLM"
frames:
  - stateless_frame
operators: []
prompt_style: default
```

---

## 🌟 Example: Full Persona (All Features)

```yaml
name: "analytical_astronomer"
alias: "aa"
description: "An analytical and inquisitive astronomer for cosmic insights"
frames:
  - stateless_frame
  - analytical_frame
domain_frames:
  - exoplanet_analysis_frame
operators:
  - explanation_operator
domain_operators:
  - planet_info_operator
prompt_style: scientific
metadata:
  tone: analytical
  domain: astronomy
  preferred_sources: ["NASA", "ESA", "arXiv"]
  persona_traits: ["curious", "data-driven", "patient"]
```

---

## 📝 Field-by-Field Guidance

### **name** (Required)
- A unique string identifier for your persona.
- Used for referencing in code, CLI, and UI.

### **alias** (Optional, but recommended for frequently-used personas)
- Short, unique string (e.g. `"aa"` for Analytical Astronomer).
- Enables quick CLI and API access.

### **description** (Required)
- A brief, friendly description.
- Appears in `describe` CLI output and helps onboarding.

### **frames** (Required)
- Ordered list of frames (reasoning steps) to execute.
- Each entry must match a Python file/class in `rasa/frames/` or your app’s domain frames.
- First frame is always the entry point.

### **operators** (Optional)
- List of general-purpose operators/tools.
- Each must match a Python file/class in `rasa/operators/`.

### **domain_frames** (Optional)
- List of persona-specific frame names (files in `apps/<persona>/frames/`).
- Lets you add custom logic only for this persona.

### **domain_operators** (Optional)
- List of persona-specific operator names (files in `apps/<persona>/operators/`).

### **prompt_style** (Optional)
- String indicating prompt/response style for the LLM.
- Examples: `default`, `scientific`, `narrative`, `casual`.

### **metadata** (Optional)
- Dictionary for any extra info.
- Use for: tone, domain, traits, preferred_sources, etc.
- Example:
    ```yaml
    metadata:
      tone: analytical
      domain: astronomy
      preferred_sources: ["NASA", "ESA", "arXiv"]
      persona_traits: ["curious", "data-driven", "patient"]
    ```

---

## 🛠️ Dev Tips

- All field names are case-sensitive.
- Comments in YAML start with `#` and are ignored.
- For most use-cases, `name`, `description`, and `frames` are required—add others as needed.
- Keep each persona in its own directory under `apps/`:
    ```
    apps/
      astronomer/
        persona.yaml
        frames/
        operators/
    ```
- If you add new fields, update this document and the loader/parser logic.

---

## 🔗 How to Reference Frames and Operators

- **Core frames/operators**: just use the name (e.g., `stateless_frame`)
- **Domain frames/operators**: add to `domain_frames` or `domain_operators` and put the Python files in `apps/<persona>/frames/` or `/operators/`

---

## 🚦 Example: Chaining Frames

```yaml
frames:
  - stateless_frame
  - short_term_memory_frame
  - recommendation_frame
```

---

## 🟩 Best Practices

- Use `alias` for all personas that might be used often or referenced in automation.
- Use `metadata` for anything you might want to filter or display in the UI.
- Standardize on `frames` for your reasoning flow.
- Prefer `domain_frames` and `domain_operators` for app/persona-specific logic.

---

## 📝 Update this document as your framework grows!

---