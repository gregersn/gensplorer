#!/usr/bin/env python3
"""Command line functions."""

import sys
import argparse

from gensplorer.services import SETTINGS
from gensplorer.services import census
from gensplorer.services import dna

from gensplorer.utils.logger import setup_logger
log = setup_logger("cli")


def argparser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest="command", help="Mode of operation",
        description="Command should be set", required=True)

    census_parser = subparsers.add_parser(
        "census", help="Get markdown of a Norwegian census")
    census_parser.add_argument('url', type=str)

    dna_parser = subparsers.add_parser("dna", help="Handle DNA profiles")
    dna_parser.add_argument(
        '--list-profiles', action="store_true",
        help="Shows current known DNA profiles")
    dna_parser.add_argument('--add-profile', nargs=2,
                            help="Add a new DNA profile",
                            metavar=('xref', 'profilename'))
    dna_parser.add_argument('--list-matches', type=str,
                            help="List matches for given xref")
    dna_parser.add_argument('--add-match', type=str,
                            help="Add a DNA match and DNA data", nargs=3,
                            metavar=('profile_xref', 'match_xref', 'test_provider'))
    return parser


def main():
    arguments = argparser().parse_args()

    if arguments.command == "census":
        print(census.as_markdown(arguments.url))

    if arguments.command == "dna":
        if arguments.list_profiles:
            for profile in dna.profiles(SETTINGS.get("datafolder"),
                                        SETTINGS.get("gedcomfile")):
                print(profile)

        if arguments.list_matches:
            print("List DNA matches for {}".format(arguments.list_matches))
            for match in dna.matches(arguments.list_matches,
                                     SETTINGS.get("datafolder"),
                                     SETTINGS.get("gedcomfile")):
                print("Xref: {xref}, Name: {name}".format(**match))

        if arguments.add_profile:
            print("Add a profile")
            xref, profilename = arguments.add_profile
            log.debug("Parameters: profilename: {}, xref: {}".format(
                profilename, xref))
            dna.add_profile(SETTINGS.get("datafolder"),
                            SETTINGS.get("gedcomfile"),
                            xref,
                            profilename)

        if arguments.add_match:
            print("Add a match")
            xref, matchref, provider = arguments.add_match
            data = [line for line in sys.stdin]
            dna.add_match(SETTINGS.get("datafolder"),
                          SETTINGS.get("gedcomfile"),
                          xref,
                          matchref,
                          provider,
                          data)


if __name__ == "__main__":
    main()
