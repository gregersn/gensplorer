import os
import json
from typing import Dict

from gensplorer.services.gedsnip import GedcomManipulator


class Tester(object):
    def __init__(self, data: Dict = {}, project=None):
        self.data = data
        self.project = project

    @property
    def matches(self):
        if self.project is None:
            return []

        return self.project.find_matches(self.name)

    @property
    def xref(self):
        return self.data['xref']

    @property
    def name(self):
        return self.data['name']

    def get_match(self, xref: str):
        for m in self.matches:
            if m['xref'] == xref:
                return m

    def get_ancestors(self, xref: str) -> str:
        return self.project.find_common(self.xref, xref)


class Project(object):
    def __init__(self, filename: str = None):
        self.filename = filename
        self.data = self.load_project(filename)

        folder = os.path.dirname(os.path.abspath(self.filename))

        self.gedcom = GedcomManipulator(os.path.join(folder, self.gedfile))

    def load_project(self, filename: str):
        if filename is None:
            return {}
        with open(filename, 'r') as f:
            return json.load(f)

    def save_project(self, filename: str):
        pass

    @property
    def testers(self):
        return self.data.get('testers', [])

    @property
    def gedfile(self):
        return self.data.get('gedfile', None)

    @property
    def matches(self):
        return self.data.get('matches', [])

    def __getitem__(self, testername: str):
        for t in self.testers:
            if t['name'] == testername:
                return Tester(t, self)

        return None

    def find_matches(self, username):
        return [m for m in self.matches if username in m['matches']]

    def find_common(self, xref_a: str, xref_b: str) -> str:
        return self.gedcom.find_common(xref_a, xref_b)
