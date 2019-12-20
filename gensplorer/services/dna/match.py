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
    def __init__(self, data: str or {}):
        self.data = {}

        if type(data) == str:
            with open(data, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = data

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
        for match in self.data['matches']:
            if tester in match['matches']:
                matches[match['xref']] = match
        return matches

    def get_match(self, xref: str):
        """Check if a certain xref has an entry as a matcher."""
        for match in self.data['matches']:
            if match['xref'] == xref:
                return match

    def add_tester(self, name: str, xref: str,
                   myheritage: str = None,
                   ftdna: str = None):
        if 'testers' not in self.data:
            self.data['testers'] = []

        if self.get_tester(name) is not None:
            raise Exception

        self.data['testers'].append({
            'xref': xref,
            'name': name,
            'shared_segments': {
                'myheritage': myheritage,
                'ftdna': ftdna
            }
        })

    def add_match(self, tester: str, xref: str, ftdna, myheritage):
        if tester not in self.data['testers']:
            raise Exception

        match = self.get_match(xref)
        if match is None:
            self.data['matches'].append({
                'xref': xref,
                'ftdna': ftdna,
                'myheritage': myheritage,
                'matches': [tester['name'], ]
            })
        else:
            if tester not in match['matches']:
                match['matches'].append(tester['name'])

            if 'ftdna' not in match:
                match['ftdna'] = ftdna

            if 'myheritage' not in match:
                match['myheritage'] = myheritage
