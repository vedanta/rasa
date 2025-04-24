import os
import shutil
import tempfile

def test_env_loading_priority():
    # Setup: Create a temp config dir with .env-llm and .env
    tempdir = tempfile.mkdtemp()
    env_llm_path = os.path.join(tempdir, ".env-llm")
    env_path = os.path.join(tempdir, ".env")
    with open(env_llm_path, "w") as f:
        f.write("LLM_PROVIDER=ollama\nLLM_MODEL=orca-mini\n")
    with open(env_path, "w") as f:
        f.write("LLM_PROVIDER=openai\nLLM_MODEL=gpt-3.5-turbo\nOPENAI_API_KEY=fakekey\n")

    from rasa.config import settings
    settings.load_env_from_dir(tempdir)

    assert settings.get_llm_provider() == "openai"
    assert settings.get_llm_model() == "gpt-3.5-turbo"
    assert settings.get_openai_api_key() == "fakekey"

    # Remove .env and reload (should now fallback to .env-llm)
    os.remove(env_path)
    settings.load_env_from_dir(tempdir)
    assert settings.get_llm_provider() == "ollama"
    assert settings.get_llm_model() == "orca-mini"

    shutil.rmtree(tempdir)

def test_default_values(monkeypatch):
    # Clear related env vars before running this test!
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("LLM_MODEL", raising=False)
    monkeypatch.delenv("DEFAULT_DB_TYPE", raising=False)
    monkeypatch.delenv("DEFAULT_VECTOR_DB_TYPE", raising=False)

    from rasa.config import settings
    settings.load_env_from_dir("/nonexistent")
    assert settings.get_llm_provider() == "ollama"
    assert settings.get_llm_model() == "llama3"
    assert settings.get_default_db_type() == "redis"
    assert settings.get_default_vector_db_type() == "qdrant"
