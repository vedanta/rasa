
import os
from dotenv import load_dotenv

def load_env_from_dir(dirpath=None):
    """
    Loads .env or .env-llm from the given directory (or the config dir if not specified).
    Always overrides existing os.environ values for keys in file.
    """
    this_dir = dirpath or os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(this_dir, ".env")
    env_llm_path = os.path.join(this_dir, ".env-llm")
    if os.path.exists(env_path):
        load_dotenv(env_path, override=True)
    elif os.path.exists(env_llm_path):
        load_dotenv(env_llm_path, override=True)
    else:
        print(f"Warning: No .env or .env-llm found in {this_dir}. Using defaults.")

# Load from default config directory on import
load_env_from_dir()

# ========== LLM Settings ==========
def get_llm_mode():
    return os.getenv("LLM_MODE", "local")
def get_llm_provider():
    return os.getenv("LLM_PROVIDER", "ollama")
def get_llm_model():
    return os.getenv("LLM_MODEL", "llama3")
def get_llm_host():
    return os.getenv("LLM_HOST", "http://localhost:11434")

def get_openai_api_key():
    return os.getenv("OPENAI_API_KEY")
def get_openai_model():
    return os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

def get_claude_api_key():
    return os.getenv("CLAUDE_API_KEY")
def get_claude_model():
    return os.getenv("CLAUDE_MODEL", "claude-3-opus")

# ========== Database Settings ==========
def get_default_db_type():
    return os.getenv("DEFAULT_DB_TYPE", "redis")
def get_default_db_url():
    return os.getenv("DEFAULT_DB_URL", "redis://localhost:6379")

def get_default_vector_db_type():
    return os.getenv("DEFAULT_VECTOR_DB_TYPE", "qdrant")
def get_default_vector_db_url():
    return os.getenv("DEFAULT_VECTOR_DB_URL", "qdrant://localhost:6333")

# ========== Any Other Global Settings ==========
def get_api_port():
    return int(os.getenv("API_PORT", 8000))
def get_debug():
    return os.getenv("DEBUG", "false").lower() == "true"
