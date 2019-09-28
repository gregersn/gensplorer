from dataclasses import dataclass, field
from typing import Dict

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
