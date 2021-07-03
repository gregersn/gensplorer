#!/usr/bin/env python3

import os
from gedcom.element.individual import IndividualElement
from gedcom.element.family import FamilyElement
from gedcom.element.element import Element
from gedcom.parser import Parser


class Tree():
    pass


class TreePart(object):
    def __init__(self, xref: str, element: Element, tree: Tree = None):
        self.xref = xref
        self.element = element
        self.tree = tree

    def __str__(self):
        return f"{self.xref}: {self.element}"


class Individual(TreePart):
    def get_parents(self):
        parent_families = self.element.get_parents()
        parents = []
        for ref in parent_families:
            family = self.tree.families.get(ref, None)
            if family is not None:
                parents += family.element.get_husband()
                parents += family.element.get_wife()
        return parents


class Family(TreePart):
    pass


class Tree(object):
    def __init__(self, filename: str):
        self.filename = filename
        self.gedcom: Parser = Parser()
        self.gedcom.parse_file(self.filename)

        self.families = {}
        self.individuals = {}
        self.other = {}

    def build_tree(self):
        root_child_elements = self.gedcom.get_root_child_elements()
        for element in root_child_elements:
            xref = element.get_pointer()
            if isinstance(element, FamilyElement):
                if xref in self.families:
                    raise AttributeError("Family alread in system")
                self.families[xref] = Family(xref, element, self)

            elif isinstance(element, IndividualElement):
                if xref in self.individuals:
                    raise AttributeError("Family alread in system")
                self.individuals[xref] = Individual(xref, element, self)
            else:
                pass
        
        for xref, individual in self.individuals.items():
            # print(individual)
            pass


def main():
    tree = Tree("./tests/test.ged")
    tree.build_tree()

if __name__ == "__main__":
    main()
