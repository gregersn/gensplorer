import os
from gedcom.element.individual import IndividualElement
from gedcom.parser import Parser

class GedcomManipulator(object):
    def __init__(self, filename):
        self.filename = filename
        assert os.path.isfile(filename)
        self.gedcom = Parser()
        self.gedcom.parse_file(self.filename)

        self.names = None

    @property
    def namelist(self):
        if self.names is None:
            self.names = []
            root_child_elements = self.gedcom.get_root_child_elements()

            for element in root_child_elements:
                if isinstance(element, IndividualElement):
                    self.names.append((element.get_pointer(),
                                       " ".join(element.get_name())))

        return self.names

    def get_cousins(self, _id, level=2):
        """Find all cousins of given distance."""
        root = self.gedcom[_id]

        assert root is not None

        atlevel = 0
        prevqueue = [root, ]
        while atlevel < level:
            queue = []
            for person in prevqueue:
                for par in person.parents:
                    queue.append(par)

            prevqueue = queue
            atlevel += 1

        queue = set()
        for person in prevqueue:
            famc = person['FAMC']
            if famc is None:
                continue

            def add_siblings(*families):
                for family in families:
                    for child in family.as_individual().children:
                        if child.as_individual().id != person.id:
                            queue.add(child.as_individual())

            if isinstance(famc, list):
                add_siblings(*famc)
            else:
                add_siblings(famc)

        prevqueue = queue

        while atlevel > 0:
            queue = set()
            for person in prevqueue:
                fams = person['FAMS']
                if fams is None:
                    continue

                def add_children(*families):
                    for family in families:
                        for child in family.as_individual().children:
                            queue.add(child.as_individual())
                if isinstance(fams, list):
                    add_children(*fams)
                else:
                    add_children(fams)

            prevqueue = queue
            atlevel -= 1

        return prevqueue

    def get_ydna(self, _id):
        """Find all people that would/should have the same Y-DNA."""

        root = self.gedcom[_id]

        queue = [root, ]
        outelements = set()

        while queue:
            cur = queue.pop(0)

            if cur is None:
                continue

            if cur in outelements:
                continue

            fams = cur['FAMS']

            if cur.father:
                queue.append(cur.father)

            if fams is not None:
                def add_children(*families):
                    for family in families:
                        for child in family.as_individual().children:
                            if child.as_individual().is_male:
                                queue.append(child.as_individual())
                if isinstance(fams, list):
                    add_children(*fams)
                else:
                    add_children(fams)

            outelements.add(cur)

        return outelements

    def get_branch(self, _id,
                   siblings=False,
                   descendants=False,
                   ancestors=True):
        root = self.gedcom[_id]

        queue = [root, ]
        outelements = set()

        while queue:
            # print(len(queue))
            cur = queue.pop(0)

            if cur is None:
                continue

            if cur in outelements:
                continue

            famc = cur['FAMC']
            fams = cur['FAMS']

            if ancestors and famc:
                if famc is not None:
                    outelements.add(famc)

                for par in cur.parents:
                    queue.append(par)

            if siblings and famc:
                if isinstance(famc, list):
                    continue

                fam = famc.as_individual()
                if fam is not None:
                    outelements.add(fam)
                    for child in fam.children:
                        queue.append(child.as_individual())

            if descendants and fams:
                # if cur != root:
                if isinstance(fams, list):
                    for fam in fams:
                        fam = fam.as_individual()
                        if fam is None:
                            continue
                        outelements.add(fams)
                        if fam.husband is not None:
                            outelements.add(fam.husband.as_individual())
                        if fam.wife is not None:
                            outelements.add(fam.wife.as_individual())
                        for child in fam.children:
                            queue.append(child.as_individual())
                elif isinstance(fams, gedcom.Spouse):
                    fam = fams.as_individual()
                    if fam is not None:
                        outelements.add(fams)
                        if fam.husband is not None:
                            outelements.add(fam.husband.as_individual())
                        if fam.wife is not None:
                            outelements.add(fam.wife.as_individual())
                        for child in fam.children:
                            queue.append(child.as_individual())
                elif fams is None:
                    pass
                else:
                    # print(type(fams))
                    pass

            outelements.add(cur)

        output = gedcom.GedcomFile()
        for element in outelements:
            output.add_element(element)
        print(len(outelements))
        return output


MANIPULATOR = None


def init_manipulator(filename=None):
    global MANIPULATOR

    if filename is not None:
        MANIPULATOR = GedcomManipulator(filename)

    return MANIPULATOR
