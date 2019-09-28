import os
import json
from dataclasses import dataclass, field
from typing import List

from .match import Match
from .provider import DNAProvider


@dataclass
class Profile:
    xref: str
    datafolder: str
    name: str = "unnamed"
    # matches: Dict = field(default_factory=lambda: {})
    matches: List = field(default_factory=lambda: [])

    @property
    def filename(self):
        return os.path.join(
            self.datafolder, "matches_{}.json".format(self.xref))

    def save(self, overwrite=False):
        if os.path.isfile(self.filename) and not overwrite:
            print("Profile already exists")
            return

        with open(self.filename, "w", newline="\n") as f:
            json.dump(self.matches, f, indent=4, default=lambda x: x.to_dict())

    @classmethod
    def load(cls, xref, datafolder='.', create=False):
        filename = os.path.join(datafolder, "matches_{}.json".format(xref))
        if not os.path.isfile(filename):
            print("Profile does not exist, creating")
            data = []
        else:
            with open(filename, 'r') as f:
                data = json.load(f)

        profile = cls(xref, datafolder)
        profile.from_json(data)

        return profile

    def from_json(self, data):
        for matchdata in data:
            match = Match(xref=matchdata['xref'], name=matchdata['name'])
            match.from_json(matchdata['matchdata'])
            self.add_match(match)

    def delete(self):
        if os.path.isfile(self.filename):
            os.unlink(self.filename)

    def to_dict(self):
        return {'xref': self.xref, 'name': self.name, 'matches': self.matches}

    def add_match(self, match: Match):
        for m in self.matches:
            if match.name == m.name and match.xref == m.xref:
                print("Match, {}, already exists?".format(m.name))
                return

        self.matches.append(match)

    def add_matchdata(self, matchxref: str, provider, data):
        match = self.find_match(matchxref)
        match.add_matchdata(provider, data)

    @property
    def matchcount(self):
        return len(self.matches)

    def get_matches(self):
        for data in self.matches:
            if data.xref is not None:
                yield {'xref': data.xref, 'name': data.name}

    def import_matches(self, provider, datafile):
        for m in DNAProvider.parse_matchfile(provider, datafile):
            chromosomes = {}
            for segment in m['segments']:
                if segment['chromosome'] not in chromosomes:
                    chromosomes[segment['chromosome']] = []
                chromosomes[segment['chromosome']].append(segment)
            matchdata = {}
            matchdata[provider] = chromosomes
            match = Match(None, m['matchname'], matchdata)
            self.add_match(match)
        self.save(overwrite=True)

    def find_match(self, xref=None, name=None):
        for m in self.matches:
            if (xref is not None and m.xref == xref) or (name is not None and m.name == name):
                return m

        return None
