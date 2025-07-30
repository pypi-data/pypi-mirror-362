import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".sqlite_toolkit"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_DB_PATH = str(CONFIG_DIR / "app.db")


def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def save_db_path(db_path: str):
    ensure_config_dir()
    config = {"db_path": db_path}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)


def load_db_path() -> str:
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return config.get("db_path", DEFAULT_DB_PATH)
    return DEFAULT_DB_PATH
