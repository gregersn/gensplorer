class Group(object):
    def __init__(self, id, ancestor):
        self.id = id
        self.ancestor = ancestor
        self.matches = []
        self.individual = ancestor['individual']
        self.distance = ancestor['distance']
        self.direction = ancestor['direction']
        self.name = " ".join(self.individual.name)
    
    def add_match(self, match):
        if match not in self.matches:
            self.matches.append(match)
