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
