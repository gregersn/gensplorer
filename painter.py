#!/usr/bin/env python3
import os
import sys
import json
from typing import List, Dict

from gensplorer.services import SETTINGS
from gensplorer.services.dna import DNAProvider


class Matches(object):
    def __init__(self):
        self.data = {}
        filename = os.path.join(SETTINGS.get('datafolder'), "gensplorer.json")
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


def paint(tester, matches, gedfile):
    cwd = os.getcwd()
    os.chdir(SETTINGS.get('datafolder'))
    myheritage_data = DNAProvider.parse_matchfile('myheritage', tester['shared_segments']['myheritage'])
    ftdna_data = DNAProvider.parse_matchfile('ftdna', tester['shared_segments']['ftdna'])

    tester_matches = matches.get_matches(tester['name'])

    myheritage_match_names = [m['myheritage'] for x, m in tester_matches.items() if 'myheritage' in m]
    for match in myheritage_data:
        if match['matchname'] in myheritage_match_names:
            print(match)

    ftdna_match_names = [m['ftdna'] for x, m in tester_matches.items() if 'ftdna' in m]
    for match in ftdna_data:
        if match['matchname'] in ftdna_match_names:
            print(match)

    os.chdir(cwd)


def main():
    matches = Matches()
    tester = matches.get_tester('eric')
    paint(tester, matches, matches.gedfile)



if __name__ == "__main__":
    main()
