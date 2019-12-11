#!/usr/bin/env python3
import os

import gedcom

from gensplorer.services import SETTINGS
from gensplorer.services.dna import DNAProvider

from gensplorer.services.dna.match import Matches

from gensplorer.painter import Painter


def paint(tester, matches, gedfile):
    cwd = os.getcwd()
    os.chdir(SETTINGS.get('datafolder'))

    # Load up the gedcom file to be able to find relationships
    ged = gedcom.parse(gedfile)

    # Get the Gedcom data for the person we are making a dnapainting for
    tester_ged = ged['@' + tester['xref'] + '@']

    myheritage_data = DNAProvider.parse_matchfile('myheritage',
                                                  tester['shared_segments']['myheritage'])
    ftdna_data = DNAProvider.parse_matchfile('ftdna',
                                             tester['shared_segments']['ftdna'])

    # Find all matches for the current tester
    tester_matches = matches.get_matches(tester['name'])

    painting = Painter(tester['name'] + ".svg", ged, tester_ged)

    # Find the name of all matchers on MyHeritage
    myheritage_match_names = {m['myheritage']: m['xref']
                              for x, m in tester_matches.items()
                              if 'myheritage' in m}

    # Add all MyHeritage matchers
    for match in myheritage_data:
        if match['matchname'] in myheritage_match_names.keys():
            painting.add_match(match, myheritage_match_names[match['matchname']])

    # Find the name of all matchers on FTDNA
    ftdna_match_names = {m['ftdna']: m['xref']
                         for x, m in tester_matches.items()
                         if 'ftdna' in m}

    # Add all FTDNA matchers
    for match in ftdna_data:
        if match['matchname'] in ftdna_match_names.keys():
            painting.add_match(match, ftdna_match_names[match['matchname']])
    
    painting.draw()
    painting.draw_legend()

    painting.save()
    os.chdir(cwd)


def main():
    matches = Matches(os.path.join(SETTINGS.get('datafolder'),
                                   "gensplorer.json"))
    tester = matches.get_tester('eric')
    paint(tester, matches, matches.gedfile)


if __name__ == "__main__":
    main()
