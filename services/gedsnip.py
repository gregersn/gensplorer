import gedcom


class GedcomManipulator(object):
    def __init__(self, filename):
        self.filename = filename
        self.gedcom = gedcom.parse(self.filename)
        self.names = None

    @property
    def namelist(self):
        if self.names is None:
            self.names = []
            for indi in self.gedcom.individuals:
                self.names.append((indi.id, " ".join(indi.name)))

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
