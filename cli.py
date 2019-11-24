#!/usr/bin/env python3
"""Command line functions."""

import sys
import argparse

from gensplorer.services import SETTINGS
from gensplorer.services import census
from gensplorer.services import dna

from gensplorer.utils.logger import setup_logger
log = setup_logger("cli")


def dnaparser(parser):
    dna_parser = parser.add_parser("dna", help="Handle DNA profiles")
    sub_parsers = dna_parser.add_subparsers(dest="dna")

    sub_parsers.add_parser("profiles", help="List existing DNA profiles")

    matches_parser = sub_parsers.add_parser(
        "matches", help="List matches for given DNA profile")
    matches_parser.add_argument(
        'xref', type=str, help="Xref to list matches for")

    profile_parser = sub_parsers.add_parser(
        "addprofile", help="Create a new DNA profile")
    profile_group = profile_parser.add_mutually_exclusive_group(required=True)
    profile_group.add_argument(
        "--interactive", action="store_true")
    profile_group.add_argument(
        '--profile', metavar=('xref', 'profilename'), nargs=2)

    match_parser = sub_parsers.add_parser(
        "addmatch", help="Add a match to a profile")
    match_group = match_parser.add_mutually_exclusive_group(required=True)
    match_group.add_argument("--interactive", action="store_true")

    match_group.add_argument(
        "--match", metavar=('profile_xref', 'match_xref', 'test_provider'), nargs=3)
    match_group.add_argument(
        "--import", dest="importfile", metavar=('profile_xref', 'test_provider', 'matchfile'), nargs=3)


def argparser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        dest="command", help="Mode of operation",
        description="Command should be set", required=True)

    census_parser = subparsers.add_parser(
        "census", help="Get markdown of a Norwegian census")
    census_parser.add_argument('url', type=str)

    dnaparser(subparsers)
    return parser


def main():
    arguments = argparser().parse_args()

    if arguments.command == "census":
        print(census.as_markdown(arguments.url))

    if arguments.command == "dna":
        if arguments.dna == "profiles":
            for profile in dna.profiles(SETTINGS.get("datafolder"),
                                        SETTINGS.get("gedcomfile")):
                print(profile)

        if arguments.dna == "matches":
            print("List DNA matches for {}".format(arguments.xref))
            for match in dna.matches(arguments.xref,
                                     SETTINGS.get("datafolder"),
                                     SETTINGS.get("gedcomfile")):
                print("Xref: {xref}, Name: {name}".format(**match))

        if arguments.dna == "addprofile":
            print("Add a profile")
            if(arguments.interactive):
                profilename = input("Name: ")
                xref = input("Xref: ")
            else:
                xref, profilename = arguments.add_profile
            log.debug("Parameters: profilename: {}, xref: {}".format(
                profilename, xref))
            dna.add_profile(SETTINGS.get("datafolder"),
                            SETTINGS.get("gedcomfile"),
                            xref,
                            profilename)

        if arguments.dna == "addmatch":
            if arguments.interactive:
                xref = input("Profile xref: ")
                matchref = input("Match name or xref: ")
                provider = input("Match provider (ftdna or myheritage): ")
            elif arguments.importfile:
                xref, provider, filename = arguments.importfile
                dna.import_matches(xref, provider, filename,
                                   SETTINGS.get("datafolder"))
                return
            else:
                print("Add a match")
                xref, matchref, provider = arguments.add_match

            print("Add match data, end with ^D: ")
            data = [line for line in sys.stdin]
            dna.add_match(SETTINGS.get("datafolder"),
                          SETTINGS.get("gedcomfile"),
                          xref,
                          matchref,
                          provider,
                          data)


if __name__ == "__main__":
    main()
