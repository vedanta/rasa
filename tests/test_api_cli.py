import subprocess
import sys

def run_api_cli(args):
    cmd = [sys.executable, "client/api_cli.py"] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result

def test_list_command():
    result = run_api_cli(["list"])
    assert result.returncode == 0
    assert "travel_concierge" in result.stdout or "economist_advisor" in result.stdout

def test_describe_command():
    result = run_api_cli(["describe", "--persona", "travel_concierge"])
    assert result.returncode == 0
    assert "travel_concierge" in result.stdout or "thoughtful_travel_concierge" in result.stdout

def test_run_command():
    result = run_api_cli([
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

def test_run_json_command():
    result = run_api_cli([
        "run-json",
        "--persona", "travel_concierge",
        "--input", "Plan a weekend in Italy",
        "--preferences", "region=europe",
        "--preferences", "travel_style=relaxed",
        "--preferences", "season=spring"
    ])
    assert result.returncode == 0
    assert "Plain Output:" in result.stdout
    assert "Structured JSON:" in result.stdout or "output_json" in result.stdout
    assert "Metadata:" in result.stdout

