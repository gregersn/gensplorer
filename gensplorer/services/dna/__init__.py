"""Wrestle DNA matches in various ways from various providers."""
import os
import json

from gensplorer.services import gedsnip
from .profile import Profile
from .match import Match
from .provider import DNAProvider


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
