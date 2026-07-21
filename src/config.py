"""Configuration manager for ClipMind."""

import json
import os
import platform

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".clipmind")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "provider": "deepseek",
    "api_key": "",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com/v1",
    "language": "es",
    "hotkey": "ctrl+c+m",
    "auto_start": True,
    "theme": "dark",
    "auto_copy": False
}


def ensure_config_dir():
    """Create config directory if it doesn't exist."""
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load_config():
    """Load configuration from file or return defaults."""
    ensure_config_dir()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                merged = DEFAULT_CONFIG.copy()
                merged.update(config)
                return merged
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file."""
    ensure_config_dir()
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def get_platform():
    """Return the current platform name."""
    return platform.system()
