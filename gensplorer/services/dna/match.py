from dataclasses import dataclass, field
from typing import Dict, Union
import json
import os
from .provider import DNAProvider
from .utils import match_overlap


@dataclass
class Match:
    xref: Union[str, None] = None
    name: str = "unnamed"
    matchdata: Dict = field(default_factory=lambda: {})

    def add_matchdata(self, provider: DNAProvider, data):
        self.matchdata[provider] = data

    def to_dict(self):
        return {'xref': self.xref,
                'name': self.name,
                'matchdata': self.matchdata}

    def from_json(self, data):
        for key, value in data.items():
            self.add_matchdata(DNAProvider[key], value)

    def matches(self, other: "Match") -> bool:
        return match_overlap(self.matchdata['ftdna'], other.matchdata['ftdna'])


class Matches(object):
    def __init__(self, data: Union[str, Dict]) -> None:
        self.workingdir = '.'
        self.data: Dict = {}

        if isinstance(data, str):
            with open(data, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = data

    def save(self, filename):
        print("Saving")
        self.workingdir = os.path.dirname(filename)
        if 'gedfile' in self.data:
            self.data['gedfile'] = os.path.relpath(
                self.data['gedfile'], self.workingdir)

        for tester in self.testers:
            if 'shared_segments' in tester:
                if ('ftdna' in tester['shared_segments']
                        and len(tester['shared_segments']['ftdna']) > 0):
                    tester['shared_segments']['ftdna'] = os.path.relpath(
                        tester['shared_segments']['ftdna'], self.workingdir)

                if ('myheritage' in tester['shared_segments']
                        and len(tester['shared_segments']['myheritage']) > 0):
                    tester['shared_segments']['myheritage'] = os.path.relpath(
                        tester['shared_segments']['myheritage'],
                        self.workingdir)

        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)

    @property
    def gedfile(self):
        if 'gedfile' in self.data:
            return self.data['gedfile']

    @gedfile.setter
    def gedfile(self, filename):
        self.data['gedfile'] = filename

    @property
    def testers(self):
        if 'testers' in self.data:
            return self.data['testers']

        return []

    def get_tester(self, name: str):
        for tester in self.data['testers']:
            if name == tester['name']:
                return tester

    def get_matches(self, tester: str):
        """Get matches for a named tester."""
        matches: Dict = {}
        if 'matches' not in self.data:
            return matches

        for match in self.data['matches']:
            if tester in match['matches']:
                matches[match['xref']] = match
        return matches

    def get_match(self, xref: str):
        """Check if a certain xref has an entry as a matcher."""
        if 'matches' not in self.data:
            return None

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

    def add_match(self, tester: Dict, xref: str, ftdna, myheritage):
        if tester not in self.data['testers']:
            raise Exception

        match = self.get_match(xref)
        if match is None:
            if 'matches' not in self.data:
                self.data['matches'] = []
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
