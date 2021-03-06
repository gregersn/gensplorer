"""App settings."""
import os
import json


class Settings(object):
    """Settings container."""

    def __init__(self, filename):
        self.settings = {}
        self.settings_file = filename
        if os.path.isfile(self.settings_file):
            self.load(self.settings_file)
        else:
            print("No settings files, creating default")
            self.save()

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

        value = None

        if len(hierarchy) == 1:
            if parent is None:
                value = self.settings.get(hierarchy[0])
            else:
                value = parent.get(hierarchy[0])
            return value
        else:
            if parent is None:
                value = self.get(".".join(hierarchy[1:]),
                                 parent=self.settings[hierarchy[0]])
            else:
                value = self.get(".".join(hierarchy[1:]),
                                 parent=parent[hierarchy[0]])
            return value

    def set(self, key, value, parent=None):
        """Set (and overwrite) a setting."""
        hierarchy = key.split(".")

        if len(hierarchy) == 1:
            if parent is None:
                self.settings[hierarchy[0]] = value
            else:
                parent[hierarchy[0]] = value
            return

        if len(hierarchy) > 1:
            root = hierarchy[0]

            if parent is None:
                if root not in self.settings:
                    self.settings[root] = {}
                target = self.settings[root]
            else:
                if root not in parent:
                    parent[root] = {}
                target = parent[root]
            return self.set(".".join(hierarchy[1:]), value, parent=target)

    def __str__(self):
        return json.dumps(self.settings, indent=4)
