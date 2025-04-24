import subprocess
import sys

def run_cli(args):
    # Runs: python -m rasa.cli.main <args>
    cmd = [sys.executable, "-m", "rasa.cli.main"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def test_list_command():
    result = run_cli(["list"])
    assert result.returncode == 0
    assert "travel_concierge" in result.stdout or "economist_advisor" in result.stdout

def test_describe_command():
    result = run_cli(["describe", "--persona", "travel_concierge"])
    assert result.returncode == 0
    assert "thoughtful_travel_concierge" in result.stdout or "travel_concierge" in result.stdout
    assert "region" in result.stdout or "relaxed" in result.stdout

def test_run_command():
    result = run_cli([
        "run",
        "--persona", "travel_concierge",
        "--input", "Plan a weekend in Italy",
        "--preferences", "region=europe",
        "--preferences", "travel_style=relaxed",
        "--preferences", "season=spring"
    ])
    assert result.returncode == 0
    assert (
        "Hallstatt" in result.stdout
        or "Europe" in result.stdout
        or "getaway" in result.stdout
        or "recommendation" in result.stdout.lower()
    )

def test_run_stream_command():
    result = run_cli([
        "run",
        "--persona", "travel_concierge",
        "--input", "Plan a weekend in Italy",
        "--preferences", "region=europe",
        "--stream"
    ])
    assert result.returncode == 0
    # Just check it returns something plausible
    assert "Europe" in result.stdout or "Italy" in result.stdout

