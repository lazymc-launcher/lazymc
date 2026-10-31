"""
lazymc config module
Manages settings, paths, and persistent storage.
"""

import os
import json
from pathlib import Path

DEFAULT_GAME_DIR = os.path.join(os.environ.get("APPDATA", ""), ".minecraft")
CONFIG_DIR = os.path.join(os.environ.get("APPDATA", ""), ".lazymc")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "username": "Player",
    "language": "auto",
    "ram_gb": 4,
    "game_dir": DEFAULT_GAME_DIR,
    "active_version": "",
    "java_path": "auto",
    "jvm_args": "-XX:+UseG1GC",
    "window_width": 854,
    "window_height": 480
}


def load_config() -> dict:
    config = DEFAULT_CONFIG.copy()
    
    # Try reading from previous Desktop config.ini if it exists
    desktop_ini = Path(os.path.expanduser("~")) / "OneDrive" / "Desktop" / "config.ini"
    if not desktop_ini.exists():
        desktop_ini = Path(os.path.expanduser("~")) / "Desktop" / "config.ini"
        
    if desktop_ini.exists():
        try:
            with open(desktop_ini, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.strip().split("=", 1)
                        if k == "USERNAME" and v:
                            config["username"] = v
                        elif k == "RAM" and v.isdigit():
                            config["ram_gb"] = int(v)
        except Exception:
            pass

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                config.update(saved)
        except Exception:
            pass

    return config


def save_config(config: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving config: {e}")
