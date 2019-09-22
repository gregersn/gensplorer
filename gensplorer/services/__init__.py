import os
from .settings import Settings

DEFAULT_FILE = os.path.join(os.path.expanduser("~/gensplorer.json"))
SETTINGS = Settings(DEFAULT_FILE)


def get(key):
    """Return a value from SETTINGS."""
    return SETTINGS.get(key)


def set(key, value):
    """Set a setting."""
    return SETTINGS.set(key, value)
