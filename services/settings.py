import os
import json


class Settings(object):
    def __init__(self):
        self.settings = {}
        self.settings_file = os.path.expanduser("~/gensplorer.json")
        if os.path.isfile(self.settings_file):
            self.load(self.settings_file)

    def load(self, filename):
        assert os.path.isfile(filename)

        with open(filename, 'r') as f:
            self.settings = json.load(f)

    def save(self):
        with open(self.settings_file, 'w', newline="\n") as f:
            json.dump(self.settings, f, indent=4)

    def get(self, key):
        if key in self.settings:
            return self.settings[key]

        return None

    def set(self, key, value):
        self.settings[key] = value
        self.save()

settings = Settings()


def get(key):
    return settings.get(key)


def set(key, value):
    return settings.set(key, value)
