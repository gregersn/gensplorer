"""Wrestle DNA matches in various ways from various providers."""
import os
import json
import csv
from io import StringIO
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List

from gensplorer.services import gedsnip


def dict2dict(input, mapping):
    output = {}
    for dest, source in mapping.items():
        output[dest] = input[source].strip()

    return output


ftdna_mappings = {
    "name": "Name",
    "matchname": "Match Name",
    "chromosome": "Chromosome",
    "start": "Start Location",
    "end": "End Location",
    "centimorgans": "Centimorgans",
    "snps": "Matching SNPs"
}

myheritage_mappings = {
    "name": "Name",
    "matchname": "Match Name",
    "chromosome": "Chromosome",
    "start": "Start Location",
    "end": "End Location",
    "startRSID": "Start RSID",
    "endRSID": "End RSID",
    "centimorgans": "Centimorgans",
    "snps": "SNPs"
}


class DNAProvider(str, Enum):
    ftdna: str = "ftdna"
    myheritage: str = "myheritage"

    @staticmethod
    def parse_overlap(data, provider):
        if provider == DNAProvider.ftdna:
            return DNAProvider.parse_overlap_ftdna(data)

        if provider == DNAProvider.myheritage:
            return DNAProvider.parse_overlap_myheritage(data)

    @staticmethod
    def parse_overlap_ftdna(data):

        f = StringIO(data)
        reader = csv.DictReader(f)

        segments = []
        for row in reader:
            segments.append(dict2dict(row, ftdna_mappings))

        return {'segments': segments,
                'name': segments[0]['name'],
                'matchname': segments[0]['matchname']}

    @staticmethod
    def parse_overlap_myheritage(data):

        f = StringIO(data)
        reader = csv.DictReader(f)

        segments = []
        for row in reader:
            segments.append(dict2dict(row, myheritage_mappings))

        return {'segments': segments,
                'name': segments[0]['name'],
                'matchname': segments[0]['matchname']}

    @staticmethod
    def parse_matchfile_ftdna(datafile):
        mappings = {k: ftdna_mappings[k] for k in (
            'chromosome', 'start', 'end', 'centimorgans', 'snps')}
        with open(datafile, 'r', encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            current_name = None
            segments = []
            for row in reader:
                if row['Match Name'] != current_name:
                    if current_name is not None:
                        yield {'segments': segments, 'matchname': current_name}
                    current_name = row['Match Name']
                    segments = []

                segments.append(dict2dict(row, mappings))
        yield {'segments': segments, 'matchname': current_name}

    @staticmethod
    def parse_matchfile_myheritage(datafile):
        mappings = {k: myheritage_mappings[k] for k in (
            'chromosome', 'start', 'end', 'centimorgans', 'snps')}
        with open(datafile, 'r', encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            current_name = None
            segments = []
            for row in reader:
                if row['Match Name'] != current_name:
                    if current_name is not None:
                        yield {'segments': segments, 'matchname': current_name}
                    current_name = row['Match Name']
                    segments = []

                segments.append(dict2dict(row, mappings))
        yield {'segments': segments, 'matchname': current_name}

    @staticmethod
    def parse_matchfile(provider, datafile):
        if provider == DNAProvider.ftdna:
            return DNAProvider.parse_matchfile_ftdna(datafile)

        if provider == DNAProvider.myheritage:
            return DNAProvider.parse_matchfile_myheritage(datafile)


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
        return {'xref': self.xref, 'name': self.name, 'matches': matches}

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
            matchdata = {}
            matchdata[provider] = m['segments']
            match = Match(None, m['matchname'], matchdata)
            self.add_match(match)
        self.save(overwrite=True)

    def find_match(self, xref=None, name=None):
        for m in self.matches:
            if m.xref == xref or m.name == name:
                return m

        return None


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
    # files = matchfiles(datafolder)
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
    profile = Profile.load(xref, datafolder)
    return profile.get_matches()


def import_matches(xref, provider, matchfile, datafolder):
    """Import all matches from a file into a profile."""
    assert os.path.isfile(matchfile)
    assert DNAProvider[provider]
    profile = Profile.load(xref, datafolder, create=True)
    profile.import_matches(DNAProvider[provider], matchfile)
