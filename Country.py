import itertools
from Order import Order
from collections import deque


class Country:
    TRUST_DECAY_MULTIPLIER = 1/3
    def __init__(self, name, color, gamemap):
        self.name = name
        self.color = color
        self.units = []
        self.trust = {}
        self.scCount = 0
        self.map = gamemap

    def getPositionValue(self):
        point = 0
        for territory in self.map.territories.values():
            if territory.owner == self:
                if territory.hasSC:
                    point += 20
                if territory.hasUnit:
                    for adj in territory.adj:
                        if adj.owner != self and adj.hasSC:
                            point += 3

    def getPossibleBuilds(self):
        count = 0
        willBuild = False
        willRemove = False
        for sc in self.map.supplycenters:
            if sc.owner == self:
                count += 1

        if count > len(self.units):
            willBuild = True
        elif count < len(self.units):
            willRemove = True
        provlist = []
        if willBuild:
            for sc in self.map.supplycenters:
                if not sc.hasUnit and sc.owner == self:
                    provlist.append(sc)
        elif willRemove:
            provlist = self.units.copy()

        buildNum = abs(count - len(self.units))
        movesets = []
        if willBuild or willRemove:
            for combination in list(itertools.combinations(provlist, buildNum)):
                moveset = []
                for province in combination:
                    if willBuild:
                        moveset.append(Order("bui", province))
                    else:
                        moveset.append(Order("rem", province))
                movesets.append(moveset)
        return movesets

    def _getPossibleMovesForUnits(self, units):
        movesets = deque()
        movesets.append([])
        for unit in units:
            temp = len(movesets)
            for i in range(temp):
                moveset = movesets.popleft()
                for order in unit.getPossibleMoves() + unit.getPossibleSupports():
                    if self.__orderIsOk(order):
                        movesets.append(moveset + [order])
        return movesets

    def updateTrust(self, country, change):
        if country is not self and country is not None:
            self.trust[country] += change

    def updateTrustAtEndOfTurn(self):
        for country in self.map.countries.values():
            if country is self:
                continue
            self.trust[country] *= self.TRUST_DECAY_MULTIPLIER
            if self.trust[country] > 1:
                self.trust[country] = 1
            elif self.trust[country] < -1:
                self.trust[country] = -1

    # For every possible order, add only moves that could potentially increase or maintain
    # positional value on successful move
    def __orderIsOk(self, order):
        if order.type == "mov" and order.origin.owner == order.arg.owner:
            if not (order.arg.hasSC and order.arg.hasAdjacentEnemyUnit()):
                if order.origin.countAdjacentOtherSCs() < order.arg.countAdjacentOtherSCs():
                    return False
        return True

    def _getSupplyCenters(self):
        scs = []
        for territory in self.map.supplycenters:
            if territory.owner is self:
                scs.append(territory)
        return scs
