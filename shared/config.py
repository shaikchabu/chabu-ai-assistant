import json
import os

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config.json")
_cache = None


def load_config():
    global _cache
    if _cache is not None:
        return _cache
    defaults = {
        "app_name": "Chabu AI",
        "tagline": "Your Voice · Your Control",
        "version": "1.0.0",
        "wake_word": "harry potter",
        "team": "Chabu Labs",
        "demo_commands": [],
    }
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            _cache = {**defaults, **json.load(f)}
    except (OSError, json.JSONDecodeError):
        _cache = defaults
    return _cache
