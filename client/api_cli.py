import click
import requests

API_URL = "http://localhost:8000"

@click.group(
    help="""
RASA API CLI – Interacts with your FastAPI backend.

Examples:
  python client/api_cli.py list
  python client/api_cli.py describe --persona travel_concierge
  python client/api_cli.py run --persona travel_concierge --input "Plan a weekend in Italy" --preferences region=europe --preferences season=spring
  python client/api_cli.py run-json --persona travel_concierge --input "Plan a weekend in Italy" --preferences region=europe --preferences season=spring
"""
)
def cli():
    pass

@cli.command("list", help="List available personas from the API.")
def list_personas():
    resp = requests.get(f"{API_URL}/persona")
    if resp.status_code == 200:
        personas = resp.json().get("personas", [])
        click.echo("\nAvailable personas:")
        for p in personas:
            click.echo(f" - {p}")
    else:
        click.echo(f"Failed to fetch personas: {resp.text}")

@cli.command("describe", help="Show basic persona info via the API.")
@click.option('--persona', required=True, help="Persona name")
def describe(persona):
    resp = requests.get(f"{API_URL}/persona")
    if resp.status_code == 200:
        personas = resp.json().get("personas", [])
        if persona not in personas:
            click.echo(f"Persona '{persona}' not found.")
            return
        click.echo(f"Persona: {persona}")
        # Optionally, enhance this to call /output/json for more details
    else:
        click.echo(f"Failed to fetch personas: {resp.text}")

def parse_prefs(preferences):
    prefs = {}
    for item in preferences:
        if "=" in item:
            k, v = item.split("=", 1)
            prefs[k.strip()] = v.strip()
    return prefs

@cli.command("run", help="Run a persona via API with input and preferences.")
@click.option('--persona', required=True, help="Persona name")
@click.option('--input', 'user_input', required=True, help="User input prompt")
@click.option('--preferences', multiple=True, help="Preferences as key=value pairs (repeatable)")
@click.option('--stream', is_flag=True, help="Stream output word-by-word from the API.")
def run(persona, user_input, preferences, stream):
    prefs = parse_prefs(preferences)
    payload = {
        "persona": persona,
        "input": user_input,
        "preferences": prefs
    }

    if stream:
        resp = requests.post(f"{API_URL}/stream", json=payload, stream=True)
        if resp.status_code == 200:
            for chunk in resp.iter_content(chunk_size=16):
                click.echo(chunk.decode("utf-8"), nl=False)
            click.echo()
        else:
            click.echo(f"Stream failed: {resp.text}")
    else:
        resp = requests.post(f"{API_URL}/output", json=payload)
        if resp.status_code == 200:
            click.secho(resp.json().get("output", ""), fg="green")
        else:
            click.echo(f"Run failed: {resp.text}")

@cli.command("run-json", help="Run a persona via API and return JSON structured output.")
@click.option('--persona', required=True, help="Persona name")
@click.option('--input', 'user_input', required=True, help="User input prompt")
@click.option('--preferences', multiple=True, help="Preferences as key=value pairs (repeatable)")
def run_json(persona, user_input, preferences):
    prefs = parse_prefs(preferences)
    payload = {
        "persona": persona,
        "input": user_input,
        "preferences": prefs
    }

    resp = requests.post(f"{API_URL}/output/json", json=payload)
    if resp.status_code == 200:
        data = resp.json()
        click.secho("\nPlain Output:", fg="green")
        click.echo(data.get("output", ""))
        click.secho("\nStructured JSON:", fg="yellow")
        click.echo(data.get("output_json", ""))
        click.secho("\nMetadata:", fg="cyan")
        click.echo(data.get("metadata", ""))
    else:
        click.echo(f"Run-JSON failed: {resp.text}")

if __name__ == "__main__":
    cli()
