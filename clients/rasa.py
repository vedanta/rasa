import click
import os
import sys
from pathlib import Path
import requests

# ------------------------
# Dynamic Core Imports (for direct mode)
def try_import_runner():
    try:
        from rasa.core.runner import Runner
        from rasa.core.persona import Persona
        return Runner, Persona
    except ImportError as e:
        click.secho(f"Error: Could not import RASA core. {e}", fg="red")
        sys.exit(1)

# ------------------------
# Helpers
def parse_preferences(prefs_list):
    prefs = {}
    for item in prefs_list or []:
        if "=" in item:
            k, v = item.split("=", 1)
            prefs[k.strip()] = v.strip()
    return prefs

# ------------------------
# CLI
@click.group(
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="""
RASA CLI – Unified interface for persona-driven, memory-aware agents.

Supports both direct (local Python) and API (HTTP) operation.

Default mode: direct. Use --mode api to talk to a RASA API server.

Examples:
  python -m clients.rasa list
  python -m clients.rasa describe --persona travel_concierge
  python -m clients.rasa run --persona travel_concierge --input "Suggest a weekend trip"
  python -m clients.rasa --mode api --api-url http://localhost:8000 run --persona travel_concierge --input "Trip for foodies in India"
  python -m clients.rasa --mode api run-json --persona travel_concierge --input "Trip for nature lovers"
"""
)
@click.option('--mode', type=click.Choice(['direct', 'api']), default='direct', show_default=True, help='Run mode: direct (local) or api (HTTP).')
@click.option('--api-url', default='http://localhost:8000', show_default=True, help='Base URL for RASA API server (API mode only).')
@click.pass_context
def cli(ctx, mode, api_url):
    ctx.ensure_object(dict)
    ctx.obj["mode"] = mode
    ctx.obj["api_url"] = api_url

# ------------------------
@cli.command("list", help="List all available personas.")
@click.pass_context
def list_command(ctx):
    """List personas in apps/ (direct) or from API."""
    if ctx.obj["mode"] == "api":
        try:
            resp = requests.get(f"{ctx.obj['api_url']}/persona")
            resp.raise_for_status()
            personas = resp.json().get("personas", [])
            click.secho("\nAvailable personas:", fg="cyan")
            for p in personas:
                click.echo(f" - {p}")
        except Exception as e:
            click.secho(f"Failed to fetch personas from API: {e}", fg="red")
    else:
        apps_path = Path("apps")
        personas = [d.name for d in apps_path.iterdir() if (d / "persona.yaml").exists()]
        click.secho("\nAvailable personas:", fg="cyan")
        for p in personas:
            click.echo(f" - {p}")

# ------------------------
@cli.command("describe", help="Show persona config, frames, operators, and metadata.")
@click.option('--persona', required=True, help="Persona name (folder in apps/ or path to persona YAML).")
@click.pass_context
def describe(ctx, persona):
    persona_path = Path(persona)
    if ctx.obj["mode"] == "api":
        click.secho("Describe is not yet implemented in API mode.", fg="yellow")
        return
    Runner, Persona = try_import_runner()
    if persona_path.exists() and persona_path.suffix == ".yaml":
        persona_obj = Persona.from_yaml(str(persona_path))
    else:
        persona_obj = Persona.from_yaml(f"apps/{persona}/persona.yaml")
    click.secho(f"\nPersona: {persona_obj.name}", fg="cyan", bold=True)
    click.echo(f"Description: {getattr(persona_obj, 'description', 'N/A')}")
    click.echo(f"Prompt Style: {getattr(persona_obj, 'prompt_style', 'N/A')}")
    click.echo(f"Frames: {getattr(persona_obj, 'frames', getattr(persona_obj, 'state_stack', []))}")
    click.echo(f"Operators: {getattr(persona_obj, 'operators', [])}")
    click.echo(f"Domain Operators: {getattr(persona_obj, 'domain_operators', [])}")
    click.echo(f"Metadata: {getattr(persona_obj, 'metadata', {})}")

# ------------------------
@cli.command("run", help="Run a persona on user input and preferences.")
@click.option('--persona', required=True, help="Persona name (folder or path to YAML).")
@click.option('--input', 'user_input', required=True, help="User input prompt/question.")
@click.option('--preferences', multiple=True, help="Preferences as key=value (repeatable).")
@click.option('--stream', is_flag=True, help="Stream output word-by-word.")
@click.pass_context
def run(ctx, persona, user_input, preferences, stream):
    prefs = parse_preferences(preferences)
    persona_path = Path(persona)
    if ctx.obj["mode"] == "api":
        payload = {
            "persona": str(persona_path.stem if persona_path.suffix == ".yaml" else persona),
            "input": user_input,
            "preferences": prefs
        }
        try:
            if stream:
                resp = requests.post(f"{ctx.obj['api_url']}/stream", json=payload, stream=True)
                resp.raise_for_status()
                for chunk in resp.iter_content(chunk_size=32):
                    click.echo(chunk.decode("utf-8"), nl=False)
                click.echo()
            else:
                resp = requests.post(f"{ctx.obj['api_url']}/output", json=payload)
                resp.raise_for_status()
                click.secho(resp.json().get("output", ""), fg="green")
        except Exception as e:
            click.secho(f"API run failed: {e}", fg="red")
    else:
        Runner, Persona = try_import_runner()
        if persona_path.exists() and persona_path.suffix == ".yaml":
            persona_obj = Persona.from_yaml(str(persona_path))
        else:
            persona_obj = Persona.from_yaml(f"apps/{persona}/persona.yaml")
        runner = Runner(persona_obj)
        state = {
            "user_input": user_input,
            "preferences": prefs,
            "metadata": {
                "tone": getattr(persona_obj, "metadata", {}).get("tone", "default"),
                "domain_operators": getattr(persona_obj, "domain_operators", [])
            }
        }
        try:
            result = runner.run(state)
            output = result.get("output", "")
            if stream:
                for word in output.split():
                    click.echo(word, nl=False)
                    click.echo(" ", nl=False)
                click.echo()
            else:
                click.secho("\n" + output, fg="green")
        except Exception as e:
            click.secho(f"Error: {e}", fg="red")

# ------------------------
@cli.command("run-json", help="(API only) Run persona, get JSON-structured output.")
@click.option('--persona', required=True, help="Persona name.")
@click.option('--input', 'user_input', required=True, help="User input prompt.")
@click.option('--preferences', multiple=True, help="Preferences as key=value (repeatable).")
@click.pass_context
def run_json(ctx, persona, user_input, preferences):
    if ctx.obj["mode"] != "api":
        click.secho("run-json is only available in API mode.", fg="yellow")
        return
    prefs = parse_preferences(preferences)
    payload = {
        "persona": persona,
        "input": user_input,
        "preferences": prefs
    }
    try:
        resp = requests.post(f"{ctx.obj['api_url']}/output/json", json=payload)
        resp.raise_for_status()
        data = resp.json()
        click.secho("\nPlain Output:", fg="green")
        click.echo(data.get("output", ""))
        click.secho("\nStructured JSON:", fg="yellow")
        click.echo(data.get("output_json", ""))
        click.secho("\nMetadata:", fg="cyan")
        click.echo(data.get("metadata", ""))
    except Exception as e:
        click.secho(f"API run-json failed: {e}", fg="red")

# ------------------------
@cli.command("llm-info", help="Show LLM provider/model config (API only).")
@click.pass_context
def llm_info(ctx):
    if ctx.obj["mode"] != "api":
        click.secho("llm-info is only available in API mode.", fg="yellow")
        return
    try:
        resp = requests.get(f"{ctx.obj['api_url']}/llm/info")
        resp.raise_for_status()
        data = resp.json()
        click.secho("\nLLM Info:", fg="cyan")
        for k, v in data.items():
            click.echo(f"{k}: {v}")
    except Exception as e:
        click.secho(f"Failed to fetch LLM info: {e}", fg="red")

# ------------------------
@cli.command("llm-health", help="Check LLM server health (API only).")
@click.pass_context
def llm_health(ctx):
    if ctx.obj["mode"] != "api":
        click.secho("llm-health is only available in API mode.", fg="yellow")
        return
    try:
        resp = requests.get(f"{ctx.obj['api_url']}/llm/health")
        resp.raise_for_status()
        data = resp.json()
        healthy = data.get("healthy", False)
        msg = "LLM is healthy!" if healthy else "LLM is NOT healthy!"
        click.secho(msg, fg="green" if healthy else "red")
        if "error" in data:
            click.secho("Error: " + data["error"], fg="red")
    except Exception as e:
        click.secho(f"Failed to fetch LLM health: {e}", fg="red")

# ------------------------
@cli.command("status", help="Show API server status (API only).")
@click.pass_context
def status(ctx):
    if ctx.obj["mode"] != "api":
        click.secho("status is only available in API mode.", fg="yellow")
        return
    try:
        resp = requests.get(f"{ctx.obj['api_url']}/status")
        resp.raise_for_status()
        data = resp.json()
        click.secho("\nRASA API Server Status:", fg="cyan")
        for k, v in data.items():
            click.echo(f"{k}: {v}")
    except Exception as e:
        click.secho(f"Failed to fetch API status: {e}", fg="red")

# ------------------------
if __name__ == "__main__":
    cli()
