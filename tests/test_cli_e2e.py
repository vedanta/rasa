import subprocess
import sys

def run_cli(args):
    """Helper to run CLI command and return (stdout, stderr, exit_code)."""
    cmd = [sys.executable, '-m', 'clients.main'] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode

def test_cli_list_personas():
    out, err, code = run_cli(['--mode', 'direct', 'list'])
    print("LIST OUTPUT:\n", out)
    assert "Available personas" in out
    assert code == 0

def test_cli_describe_persona():
    out, err, code = run_cli(['--mode', 'direct', 'describe', '--persona', 'demo_app'])
    print("DESCRIBE OUTPUT:\n", out)
    assert "Persona: " in out
    assert "stateless_frame" in out
    assert code == 0

def test_cli_run_persona():
    out, err, code = run_cli(['--mode', 'direct', 'run', '--persona', 'demo_app', '--input', 'Hello'])
    print("RUN OUTPUT:\n", out)
    assert out.strip() != ""
    assert code == 0

# You can add more tests for run-json, API mode, etc.
