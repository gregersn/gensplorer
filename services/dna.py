"""Wrestle DNA matches in various ways from various providers."""
import os
import json

from services import gedsnip


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


def matches(xref, datafolder, gedcomfile):
    """Get matches for a given xref."""
    matches_file = os.path.join(datafolder, "matches_{}.json".format(xref))
    assert os.path.isfile(matches_file)
    for _ in load_matchfile(matches_file):
        yield _
