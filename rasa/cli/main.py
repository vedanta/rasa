import click
import os
from pathlib import Path
from rasa.core.runner import Runner
from rasa.core.persona import Persona

def list_personas():
    personas = [d for d in os.listdir("apps") if (Path("apps") / d / "persona.yaml").exists()]
    click.echo("\nAvailable personas:")
    for p in personas:
        click.echo(f" - {p}")

def parse_preferences(prefs_list):
    prefs = {}
    for item in prefs_list or []:
        if "=" in item:
            k, v = item.split("=", 1)
            prefs[k.strip()] = v.strip()
    return prefs

@click.group(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="""
RASA CLI – Run persona-driven, memory-aware agents from the command line.

Examples:
  python -m rasa.cli.main list
  python -m rasa.cli.main describe --persona travel_concierge
  python -m rasa.cli.main run --persona travel_concierge --input "Plan a weekend in Italy" --preferences region=europe --preferences travel_style=relaxed --preferences season=spring

Tips:
- Each '--preferences' flag must be followed by a single key=value pair.
- Use 'describe' to see which preferences a persona expects.
"""
)
def cli():
    """RASA Command Line Interface"""
    pass

@cli.command("list", help="List all available personas in the apps/ directory.")
def list_command():
    """Lists all persona folders with persona.yaml."""
    list_personas()

@cli.command("describe", help="Describe the persona, its configuration, and required preferences.")
@click.option('--persona', required=True, help="Persona name (folder under apps/)")
def describe(persona):
    """
    Print details of the selected persona:
    - Description, operators, domain operators, and metadata
    - Domain operator docstring for preference hints
    - Example usage
    """
    persona_obj = Persona.from_yaml(f"apps/{persona}/persona.yaml")
    click.secho(f"\nPersona: {persona_obj.name}\n", fg="cyan", bold=True)
    click.echo(f"Description: {persona_obj.description}")
    click.echo(f"Prompt Style: {persona_obj.prompt_style}")
    click.echo(f"Operators: {persona_obj.operators}")
    click.echo(f"Domain Operators: {getattr(persona_obj, 'domain_operators', [])}")
    click.echo(f"Metadata: {persona_obj.metadata}")

    # Try to load docstring from the domain operator, if present
    for op in getattr(persona_obj, 'domain_operators', []):
        try:
            import sys
            import importlib
            sys.path.append(f"apps/{persona}/operators")
            op_mod = importlib.import_module(op)
            class_name = "".join([w.capitalize() for w in op.split("_")])
            doc = getattr(op_mod, class_name).__doc__
            if doc:
                click.echo("\nDomain Operator Description:")
                click.echo(doc)
        except Exception as e:
            click.echo(f"\nCould not load domain operator {op}: {e}")

    click.echo("\nExample usage:")
    click.secho(f"python -m rasa.cli.main run --persona {persona} --input \"<your prompt>\" --preferences key=value", fg="yellow")
    click.secho("Repeat --preferences for each key=value needed (e.g., region=europe travel_style=relaxed season=spring)", fg="yellow")

@cli.command(
    "run",
    help="""
Run a persona-driven agent on input and preferences.

Example:
  python -m rasa.cli.main run --persona travel_concierge --input "Plan a weekend in Italy" --preferences region=europe --preferences travel_style=relaxed --preferences season=spring

Tips:
- Each '--preferences' flag must be followed by a single key=value pair.
"""
)
@click.option('--persona', required=True, help="Persona name (folder under apps/). Run 'list' to see available options.")
@click.option('--input', 'user_input', required=True, help="User input prompt/question for the persona.")
@click.option('--preferences', multiple=True, help="Preferences as key=value pairs (repeatable, e.g. --preferences region=europe --preferences season=summer)")
@click.option('--stream', is_flag=True, help="Stream output word-by-word for a live chat-like experience.")
def run(persona, user_input, preferences, stream):
    """
    Run a persona-driven agent on input and preferences.

    See 'describe' for valid keys.
    """
    prefs = parse_preferences(preferences)
    import sys
    sys.path.append(f"apps/{persona}/operators")
    persona_obj = Persona.from_yaml(f"apps/{persona}/persona.yaml")
    runner = Runner(persona_obj)
    state = {
        "user_input": user_input,
        "preferences": prefs,
        "metadata": {
            "tone": persona_obj.metadata.get("tone", "default"),
            "domain_operators": getattr(persona_obj, "domain_operators", [])
        }
    }
    result = runner.run(state)
    output = result.get("output", "")
    if stream:
        for word in output.split():
            click.echo(word, nl=False)
            click.echo(" ", nl=False)
        click.echo()
    else:
        click.secho("\n" + output, fg="green")

if __name__ == "__main__":
    cli()
