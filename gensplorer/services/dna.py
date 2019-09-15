"""Wrestle DNA matches in various ways from various providers."""
import os
import json
from enum import Enum
from dataclasses import dataclass

from gensplorer.services import gedsnip


class DNAProvider(Enum):
    ftdna = 1
    myheritage = 2


@dataclass
class Match:
    xref: str
    matchdata = {}

    def add_matchdata(self, provider, data):
        self.matchdata[provider] = data

    def to_dict(self):
        return {'xref': self.xref, 'matchdata': self.matchdata}


@dataclass
class Profile:
    xref: str
    datafolder: str
    name: str = "unnamed"
    matches = {}

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
    def load(cls, xref, datafolder):
        filename = os.path.join(datafolder, "matches_{}.json".format(xref))
        with open(filename, 'r') as f:
            data = json.load(f)

        match = cls(xref, datafolder)
        match.matches = data

        return match
    
    def delete(self):
        os.unlink(self.filename)

    def to_dict(self):
        return {'xref': self.xref, 'name': self.name, 'matches': matches}


def load_matchfile(path):
    """Get content of a matchfile."""
    with open(path, 'r') as f:
        return json.load(f)


def matchfiles(datafolder):
    """Find all files containing matches."""
    with os.scandir(datafolder) as iterator:
        for entry in iterator:
            if entry.name.startswith("matches_") and entry.is_file():
                yield entry


def profiles(datafolder, gedcomfile):
    """Get list of DNA profiles."""
    files = matchfiles(datafolder)
    gedcom = gedsnip.init_manipulator(gedcomfile)

    for _ in files:
        xref = _.name[len("matches_"):-len(".json")]
        profile = gedcom.gedcom[xref]
        yield {'xref': xref, 'name': profile.name}


def add_profile(datafolder, gedcomfile, xref, name, overwrite=False):
    """Add a new DNA profile."""
    files = matchfiles(datafolder)
    gedcom = gedsnip.init_manipulator(gedcomfile)

    gedprofile = gedcom.gedcom[xref]
    print(gedprofile)

    if not gedcom.gedcom[xref]:
        print("Can't add someone not existing in gedcom")
        return

    profile = Profile(xref, datafolder, name=name)
    profile.save(overwrite=overwrite)


def add_match(datafolder, gedcomfile, xref, matchref, provider, data):
    profile = Profile.load(xref, datafolder)
    match = Match(matchref)
    match.add_matchdata(DNAProvider[provider].name, data)
    profile.matches[matchref] = match
    profile.save(overwrite=True)


def matches(xref, datafolder, gedcomfile):
    """Get matches for a given xref."""
    matches_file = os.path.join(datafolder, "matches_{}.json".format(xref))
    assert os.path.isfile(matches_file)
    for _ in Profile.load(matches_file):
        yield _
