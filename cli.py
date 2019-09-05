#!/usr/bin/env python3
"""Command line functions."""

import argparse

from services.settings import SETTINGS
from services import census
from services import dna


def argparser():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="command")

    census_parser = subparsers.add_parser("census")
    census_parser.add_argument('url', type=str)

    dna_parser = subparsers.add_parser("dna")
    dna_parser.add_argument('--list-profiles', action="store_true")
    dna_parser.add_argument('--list-matches', type=str)

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

        # print(arguments)


if __name__ == "__main__":
    main()
