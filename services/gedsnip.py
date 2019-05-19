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

    def get_branch(self, _id, get_family=False):
        
        root = self.gedcom[_id]

        queue = [root, ]
        outelements = set()

        while len(queue) > 0:
            # print(len(queue))
            cur = queue.pop(0)
            if cur in outelements:
                continue

            if hasattr(cur, 'father'):
                f = cur.father
                if f is not None:
                    queue.append(f)

            if hasattr(cur, 'mother'):
                m = cur.mother
                if m is not None:
                    queue.append(m)

            if get_family:
                fam = cur['FAMC']
                if fam is not None:
                    if type(fam) == list:
                        continue
                    fam = fam.as_individual()
                    queue.append(fam)
                    for child in fam.children:
                        queue.append(child.as_individual())

                if cur != root:
                    fams = cur['FAMS']
                    if type(fams) == list:
                        for fam in fams:
                            fam = fam.as_individual()
                            if fam.husband is not None:
                                queue.append(fam.husband.as_individual())
                            if fam.wife is not None:
                                queue.append(fam.wife.as_individual())
                            for child in fam.children:
                                queue.append(child.as_individual())
                    elif type(fams) == gedcom.Spouse:
                        fam = fams.as_individual()

                        if fam.husband is not None:
                            queue.append(fam.husband.as_individual())

                        if fam.wife is not None:
                            queue.append(fam.wife.as_individual())
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
