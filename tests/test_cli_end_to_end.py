import subprocess
import sys
import shlex
import os

PYTHON = sys.executable  # current python
CLI = "-m clients.rasa"

def run_cli(args, env=None):
    cmd = f"{PYTHON} {CLI} {args}"
    print(f"\n\033[96m[CLI DEBUG] Running:\033[0m {cmd}")
    result = subprocess.run(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
        cwd=os.getcwd(),  # ensure running from project root
    )
    print("\033[92m[STDOUT]:\033[0m", result.stdout)
    print("\033[91m[STDERR]:\033[0m", result.stderr)
    return result

def print_test_case(name):
    print(f"\n\033[93m=== RUNNING TEST: {name} ===\033[0m")

def test_list_personas_direct():
    print_test_case("list_personas_direct")
    result = run_cli("list")
    assert "Available personas" in result.stdout

def test_describe_persona_direct():
    print_test_case("describe_persona_direct")
    result = run_cli("describe --persona strategic_stock_analyst")
    out = result.stdout + result.stderr
    assert "Persona:" in out
    assert "Frames:" in out

def test_run_persona_direct():
    print_test_case("run_persona_direct")
    result = run_cli('run --persona strategic_stock_analyst --input "Should I buy Nvidia today?"')
    out = result.stdout + result.stderr
    assert "Nvidia" in out or "NVIDIA" in out

def test_run_with_preferences_direct():
    print_test_case("run_with_preferences_direct")
    result = run_cli('run --persona strategic_stock_analyst --input "Suggest a safe stock" --preferences risk_tolerance=low --preferences sector=utilities')
    out = result.stdout.lower() + result.stderr.lower()
    assert "stock" in out or "johnson" in out or "jnj" in out or "company" in out

def test_run_with_stream_direct():
    print_test_case("run_with_stream_direct")
    result = run_cli('run --persona strategic_stock_analyst --input "Quick tip for tech sector" --stream')
    out = result.stdout.lower() + result.stderr.lower()
    assert "tech" in out

def test_list_personas_api():
    print_test_case("list_personas_api")
    result = run_cli("--mode api list")
    assert "Available personas" in result.stdout

def test_run_persona_api():
    print_test_case("run_persona_api")
    result = run_cli('--mode api run --persona strategic_stock_analyst --input "Should I buy Nvidia today?"')
    out = result.stdout + result.stderr
    assert "Nvidia" in out or "NVIDIA" in out

def test_run_with_preferences_api():
    print_test_case("run_with_preferences_api")
    result = run_cli('--mode api run --persona strategic_stock_analyst --input "Suggest a safe stock" --preferences risk_tolerance=low --preferences sector=utilities')
    out = result.stdout.lower() + result.stderr.lower()
    assert "stock" in out or "johnson" in out or "jnj" in out or "company" in out

def test_run_with_stream_api():
    print_test_case("run_with_stream_api")
    result = run_cli('--mode api run --persona strategic_stock_analyst --input "Quick tip for tech sector" --stream')
    out = result.stdout.lower() + result.stderr.lower()
    assert "tech" in out

def test_run_json_api():
    print_test_case("run_json_api")
    result = run_cli('--mode api run-json --persona strategic_stock_analyst --input "Give me a stock pick"')
    out = result.stdout + result.stderr
    assert "Plain Output:" in out
    assert "Structured JSON:" in out

def test_llm_info_api():
    print_test_case("llm_info_api")
    result = run_cli('--mode api llm-info')
    out = result.stdout + result.stderr
    assert "LLM Info:" in out

def test_llm_health_api():
    print_test_case("llm_health_api")
    result = run_cli('--mode api llm-health')
    out = result.stdout.lower() + result.stderr.lower()
    assert "healthy" in out

def test_status_api():
    print_test_case("status_api")
    result = run_cli('--mode api status')
    out = result.stdout + result.stderr
    assert "RASA API Server Status:" in out

def test_run_persona_missing():
    print_test_case("run_persona_missing")
    result = run_cli('run --persona fake_persona --input "Hello"')
    out = result.stdout + result.stderr
    assert "Error" in out or "Failed" in out or "not found" in out or "FileNotFoundError" in out

def test_run_missing_input():
    print_test_case("run_missing_input")
    result = run_cli('run --persona strategic_stock_analyst')
    out = result.stdout + result.stderr
    assert "Error" in out or "required" in out or "Missing option" in out

def test_invalid_command():
    print_test_case("invalid_command")
    result = run_cli("foobar123")
    out = result.stdout + result.stderr
    assert "No such command" in out or "Error" in out

if __name__ == "__main__":
    # Manual run for debugging (pytest will pick up all functions starting with test_)
    test_list_personas_direct()
    test_describe_persona_direct()
    test_run_persona_direct()
    test_run_with_preferences_direct()
    test_run_with_stream_direct()
    test_list_personas_api()
    test_run_persona_api()
    test_run_with_preferences_api()
    test_run_with_stream_api()
    test_run_json_api()
    test_llm_info_api()
    test_llm_health_api()
    test_status_api()
    test_run_persona_missing()
    test_run_missing_input()
    test_invalid_command()
