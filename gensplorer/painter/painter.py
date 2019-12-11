#!/usr/bin/env python3

import gedcom
from typing import List, Dict, cast
import colorsys
import svgwrite
from gensplorer.services.dna.chromosomes import chromosomes

from .group import Group

chromosome_list = ['%s' % i
                   for i in list(range(1, 23))] + ['X', 'Y']

chromosome_height = 40 / len(chromosome_list)
chromosome_spacing = 60 / len(chromosome_list)


def bp2percent(chromosome: str, bp: int):
    chromosome_data = cast(Dict[str, Dict], chromosomes)[chromosome]
    chromosome_basepairs = chromosome_data['base_pairs']
    chromosome_length = chromosome_data['length']
    percent = bp / chromosome_basepairs * chromosome_length
    return percent


def lerp(v, a, b):
    if type(a) == tuple:
        return [lerp(v, *t) for t in zip(a, b)]
    return (v * a + (1 - v) * b)


def dircolor(v: float):
    paternal_a = (0.0, 1.0, 1.0)  # Father's father's line,
    paternal_b = (.4, 1.0, 1.0)  # Father's mother's line
    maternal_a = (0.6, 1.0, 1.0)  # Mother's father's line
    maternal_b = (1.0, 1.0, 1.0)  # Mother's mother's line

    if v < 0:
        return colorsys.hsv_to_rgb(*lerp(abs(v), paternal_a, paternal_b))
    elif v > 0:
        return colorsys.hsv_to_rgb(*lerp(v, maternal_a, maternal_b))

    return (.4, .4, .4)




class Painter(object):
    def __init__(self, filename: str, ged, tester_ged):
        self.filename: str = filename
        self.gedcom = ged
        self.tester_ged = tester_ged
        self.dwg = svgwrite.Drawing(filename=self.filename)
        self.draw_outline()
        self.groups = {}

    def draw_outline(self):
        index = 0

        group = self.dwg.g(fill="none", stroke="black")
        for chromosome in chromosome_list:
            data = chromosomes[chromosome]

            chromosome_rect = self.dwg.rect(("{}%".format(0),
                                             "{}%".format((chromosome_height +
                                                           chromosome_spacing) * index)),
                                            ("{}%".format(data['length']),
                                             "{}%".format(chromosome_height)))
            group.add(chromosome_rect)
            index += 1
        self.dwg.add(group)

    def save(self):
        self.dwg.save(pretty=True)

    def create_mark(self, chromosome, start, end, side=0, owner=""):
        color = dircolor(side)
        color_string = "rgb({}%, {}%, {}%)".format(color[0] * 100, color[1] * 100, color[2] * 100)

        index = chromosome_list.index(chromosome)

        start_p = bp2percent(chromosome, start)
        end_p = bp2percent(chromosome, end)

        height = chromosome_height
        offset = 0

        if side != 0:
            height /= 2

        if side > 0:
            offset = height

        desc = "{} {} {} {}".format(chromosome, start, end, side)

        marker_rect = self.dwg.rect(("{}%".format(start_p),
                                     "{}%".format((chromosome_height + chromosome_spacing) * index + offset)),
                                    ("{}%".format(end_p - start_p),
                                     "{}%".format(height)), fill=color_string)
        marker_rect.set_desc(title=owner, desc=desc)
        return marker_rect

    def draw_legend(self):
        groupcount = len(list(self.groups.keys()))
        container = self.dwg.rect((0, 0), ("20%", 20 * groupcount), stroke="black", fill="none")

        group = self.dwg.svg(insert=("80%", "70%"))
        group.add(container)

        matchindex = 0
        group_objs = sorted(self.groups.values(), key=lambda x: x.direction)
        for group_obj in group_objs:
            color = dircolor(group_obj.ancestor['direction'])
            color_string = "rgb({}%, {}%, {}%)".format(color[0] * 100, color[1] * 100, color[2] * 100)

            matchgroup = self.dwg.g()
            matchgroup.add(self.dwg.rect((0, 17 * matchindex), (16, 16), stroke="black", fill=color_string))
            matchgroup.add(self.dwg.text(group_obj.name, insert=(16, 17 * matchindex + 16)))
            group.add(matchgroup)
            matchindex += 1

        self.dwg.add(group)

    def add_match(self, match, xref: str):
        print(xref)
        match_ged = self.gedcom['@' + xref + '@']

        connection = gedcom.individual.connection(self.tester_ged, match_ged)

        if connection is None:
            print("Unknown connection")
            return

        ancestor = gedcom.individual.ancestor(connection)
        ancestor_individual = ancestor['individual']

        if ancestor_individual.id not in self.groups:
            self.groups[ancestor_individual.id] = Group(ancestor_individual.id,
                                                        ancestor)
        self.groups[ancestor_individual.id].add_match({"name": match['matchname'],
                                                       "segments": match['segments']})

    def draw(self):
        print("Drawing")
        matchindex = 0

        for group_id, group in self.groups.items():
            print("* Drawing group {}".format(group.name))
            color = dircolor(group.ancestor['direction'])
            color_string = "rgb({}%, {}%, {}%)".format(color[0] * 100,
                                                       color[1] * 100,
                                                       color[2] * 100)
            svggroup = self.dwg.g(stroke="none",
                                  opacity="0.8",
                                  fill=color_string,
                                  id=group_id)

            for match in group.matches:
                print("** Drawing match: {}".format(match['name']))
                for segment in match['segments']:
                    start = int(segment['start'])
                    end = int(segment['end'])
                    chromosome = segment['chromosome'].strip()
                    svggroup.add(self.create_mark(chromosome, start, end,
                                                  side=group.ancestor['direction'],
                                                  owner=" ".join(match['name'])))
            self.dwg.add(svggroup)
            matchindex += 1
