import json
from pathlib import Path
import logging

CONFIG_FILE = Path(__file__).parent / "config.json"

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        raise FileNotFoundError(f"Config file not found: {CONFIG_FILE}")

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

# load
config = load_config()

# Helper functions to get and set config values
def get(key_path, default=None):
    keys = key_path.split(".")
    value = config
    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return default
    return value

def set(key_path, value):
    try:
        keys = key_path.split(".")
        d = config

        for key in keys[:-1]:
            if key not in d or not isinstance(d[key], dict):
                logging.error(f"Config update failed: '{key}' in '{key_path}' does not exist.")
                return False
            d = d[key]

        if keys[-1] not in d:
            logging.error(f"Config update failed: '{keys[-1]}' in '{key_path}' does not exist.")
            return False

        # Update
        d[keys[-1]] = value
        save_config(config)
        logging.info(f"Config updated: {key_path} set to {value}")
        return True

    except Exception as e:
        logging.error(f"Failed to set config value: {e}")
        return False


