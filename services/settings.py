"""App settings."""
import os
import json


class Settings(object):
    """Settings container."""
    def __init__(self):
        self.settings = {}
        self.settings_file = os.path.expanduser("~/gensplorer.json")
        if os.path.isfile(self.settings_file):
            self.load(self.settings_file)

    def load(self, filename):
        """Load from JSON file."""
        assert os.path.isfile(filename)

        with open(filename, 'r') as settings_file:
            self.settings = json.load(settings_file)

    def save(self):
        """Save to JSON file."""
        with open(self.settings_file, 'w', newline="\n") as settings_file:
            json.dump(self.settings, settings_file, indent=4)

    def get(self, key, parent=None):
        """Get a settings value."""
        hierarchy = key.split(".")

        if len(hierarchy) == 1:
            if parent:
                return parent[hierarchy[0]]

            return self.settings[hierarchy[0]]
        
        if hierarchy[0] in self.settings:
            return self.get(".".join(hierarchy[1:]),
                            parent=self.settings[hierarchy[0]])

        return None

    def set(self, key, value, parent=None):
        """Set (and overwrite) a setting."""
        hierarchy = key.split(".")

        if len(hierarchy) == 1:
            if parent:
                parent[hierarchy[0]] = value
            else:
                self.settings[hierarchy[0]] = value
            
            return

        if len(hierarchy) > 1:
            root = hierarchy[0]
            
            if parent is None:
                if root not in self.settings:
                    self.settings[root] = {}
                target = self.settings[root]
            else:
                if len(hierarchy) > 1:
                    if root not in parent:
                        parent[root] = {}
            return self.set(".".join(hierarchy[1:]), value, parent=target)


SETTINGS = Settings()


def get(key):
    """Return a value from SETTINGS."""
    return SETTINGS.get(key)


def set(key, value):
    """Set a setting."""
    return SETTINGS.set(key, value)
