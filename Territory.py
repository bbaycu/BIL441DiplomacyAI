from Order import Order


class Territory:
    moveorders = None
    supportorders = None
    soldierShape = [[True, True, True, True, True, True, True, True, True, True],
                    [True, True, False, False, False, False, False, False, True, True],
                    [True, False, True, True, False, False, True, True, False, True],
                    [True, False, False, False, True, True, False, False, False, True],
                    [True, False, True, True, False, False, True, True, False, True],
                    [True, True, False, False, False, False, False, False, True, True],
                    [True, True, True, True, True, True, True, True, True, True]]

    def __init__(self, name, owner, hasSC, isSea, center):
        self.name = name
        self.owner = owner
        self.hasSC = hasSC
        self.isSea = isSea
        self.center = center
        self.adj = []
        if (owner is not None) and hasSC:
            self.hasUnit = True
        else:
            self.hasUnit = False
        self.nextOwner = None

    def __str__(self):
        return self.name

    def getPossibleMoves(self):
        moves = []
        for adj in self.adj:
            moves.append(Order("mov",self, adj))
        return moves

    def getPossibleSupports(self):
        supports = []
        countries = [None]
        for adj1 in self.adj:
            for adj2 in adj1.adj:
                if (adj2.owner != self.owner) and (adj2.owner not in countries):
                    if adj2.hasUnit:
                        countries.append(adj2.owner)
        for country in countries:
            supports.append(Order("sup",self,country))
        return supports

    def isAdjacentTo(self,territory):
        for adj in self.adj:
            if adj == territory:
                return True
        return False

    def adjacentUnitNumberFrom(self,country):
        count = 0
        for adj in self.adj:
            if adj.owner == country and adj.hasUnit:
                count += 1
        return count

    def hasAdjacentEnemyUnit(self):
        for adj in self.adj:
            if (adj.owner is not None) and adj.hasUnit and adj.owner != self.owner:
                return True
        return False

    def countAdjacentOtherSCs(self):
        count = 0
        for adj in self.adj:
            if adj.hasSC and adj.owner != self.owner:
                count += 1
        return count

    def findDistanceToFront(self):
        adjs = [self]
        count = 0
        while True:
            for i in range(len(adjs)):
                adjProv = adjs[i]
                if adjProv.owner is not self.owner:
                    return count
                for adj in adjProv.adj:
                    adjs.append(adj)
            count += 1
        return 10000
