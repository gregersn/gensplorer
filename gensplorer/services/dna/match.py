from dataclasses import dataclass, field
from typing import Dict
import json

from .provider import DNAProvider
from .utils import match_overlap


class Match:
    pass


@dataclass
class Match:
    xref: str = None
    name: str = "unnamed"
    matchdata: Dict = field(default_factory=lambda: {})

    def add_matchdata(self, provider: DNAProvider, data):
        self.matchdata[provider] = data

    def to_dict(self):
        return {'xref': self.xref, 'name': self.name, 'matchdata': self.matchdata}

    def from_json(self, data):
        for key, value in data.items():
            self.add_matchdata(DNAProvider[key], value)

    def matches(self, other: Match) -> bool:
        return match_overlap(self.matchdata['ftdna'], other.matchdata['ftdna'])


class Matches(object):
    def __init__(self, filename):
        self.data = {}
        with open(filename, 'r') as f:
            self.data = json.load(f)

    @property
    def gedfile(self):
        return self.data['gedfile']

    def get_tester(self, name: str):
        for tester in self.data['testers']:
            if name == tester['name']:
                return tester

    def get_matches(self, tester: str):
        """Get matches for a named tester."""
        matches = {}
        for xref, match in self.data['matches'].items():
            if tester in match['matches']:
                matches[xref] = match
        return matches
