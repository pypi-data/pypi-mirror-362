import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = Path.home() / ".groqcli" / "config.json"


def get_key(cli_token=None):
    if cli_token:
        return cli_token

    env_token = os.environ.get("GROQ_API_KEY")
    if env_token:
        return env_token

    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                return data.get("api_key")
        except Exception:
            pass

    return None

def save_key(key: str):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    addDump({"api_key": key})

def set_model(model: str):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    addDump({"model": model})

def get_model():
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                return data.get("model")
        except Exception:
            pass
    return None

def edit_system_prompt(key: str, system_prompt: str):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    addDump({"system_prompt": {key: system_prompt}})

def get_system_prompt(key: str):
    if get_predifined_system_prompts().get(key):
        return get_predifined_system_prompts()[key]
    
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
                return data.get("system_prompt", {}).get(key)
        except Exception:
            pass
    return None

def get_predifined_system_prompts():
    predefined_system_prompts_path = Path(__file__).parent / "predefined_system_prompts.json"
    if predefined_system_prompts_path.exists():
        try:
            with open(predefined_system_prompts_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading predefined system prompts: {e}")
    return {}

def addDump(object: object):
    existing_data = {}
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
        except Exception:
            pass
    existing_data.update(object)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2)