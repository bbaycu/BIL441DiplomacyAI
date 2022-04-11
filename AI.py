from Country import Country
from Order import Order
import itertools

class AI(Country):

    def __init__(self, name, color, gamemap):
        super().__init__(name, color, gamemap)
        self.approach = {}

    def getMoves(self):
        self.decideApproachesToCountries()
        moveTargets = self.selectMoveTargets()
        unitlist = self.units.copy()
        ordersets = []

        # Create different local movesets
        for target in moveTargets:
            newset = []
            ordersets.append(newset)
            for adj in target.adj:
                if adj.owner is self and adj.hasUnit:
                    supports = []
                    moveorder = Order("mov", adj, target)
                    if adj in unitlist:
                        unitlist.remove(adj)
                    for adj2 in target.adj:
                        if adj2.owner is self and adj2.hasUnit and adj2 is not adj:
                            supports.append(Order("sup", adj2, target.owner))
                    for i in range(len(supports)+1):
                        for combination in itertools.combinations(supports, i):
                            newset.append([moveorder]+list(combination))

        #Combine the local movesets
        movesets = ordersets[0].copy()
        for i in range(len(ordersets)-1):
            removeList = []
            addList = []
            newset = ordersets[i+1]
            for moveset in movesets:
                for orderset in newset:
                    containsMove = False
                    for move in moveset:
                        for order in orderset:
                            if order.origin is move.origin:
                                containsMove = True
                                break
                    if not containsMove:
                        addList.append(moveset+orderset)
                        if moveset not in removeList:
                            removeList.append(moveset)
            for removed in removeList:
                movesets.remove(removed)
            for added in addList:
                movesets.append(added)
        # Add missing units by selecting them a quick path to the front
        for unit in unitlist:
            minDistance = 1000
            selectedDestination = None
            for adj in unit.adj:
                newvalue = adj.findDistanceToFront()
                if newvalue < minDistance:
                    minDistance = newvalue
                    selectedDestination = adj
            for moveset in movesets:
                moveset.append(Order("mov",unit,selectedDestination))

        return movesets

    def selectMoveTargets(self):
        # Determine where movable territories are
        territories = []
        for unit in self.units:
            for adj in unit.adj:
                if adj not in territories:
                    territories.append(adj)

        # Determine how good of a choice each move would provide
        movepoints = []
        for i in range(len(territories)):
            territory = territories[i]
            count = 0
            if territory.hasSC and territory.owner is not self:
                count += 10
            if territory.adjacentUnitNumberFrom(self) > territory.adjacentUnitNumberFrom(territory.owner):
                count += 10 * (
                            territory.adjacentUnitNumberFrom(self) - territory.adjacentUnitNumberFrom(territory.owner))
            for adj in territory.adj:
                if adj.hasSC:
                    count += 5
                if territory.owner is not self and territory.owner is not None:
                    count -= 8 * self.approach[territory.owner]
            count /= territory.findDistanceToFront()

            if territory.owner is self or territory.owner is None:
                movepoints.append(count)
            else:
                movepoints.append(count * self.approach[territory.owner])

        # Sort the lists based on points
        sortedmoves = [x for _, x in sorted(zip(movepoints, territories), key=lambda pair: pair[0])]

        # Find some threshold where we can say the move is a good choice
        movePlacesToBeConsidered = len(self.units) * 1.7
        moves = []
        for i in range(round(movePlacesToBeConsidered)):
            moves.append(sortedmoves[len(sortedmoves) - 1 - i])
        return moves

    def decideApproachesToCountries(self):
        maxsc = 0
        c1 = None
        for country in self.map.countries.values():
            if country.scCount > maxsc:
                maxsc = country.scCount
                c1 = country

        if maxsc >= 15:  # If one country is winning, all countries gangs up on him
            countries = self.map.countries.values()
            self.approach[c1] = Approach.DEFCON1
            countries.remove(c1)
            for country in countries:
                self.approach[country] = Approach.DEFCON5
        else:  # Otherwise all countries mind their own business
            maxthreat = 0
            attackSelection = None
            for country in self.map.countries.values():
                if country is not self:
                    threat = self.findThreatValue(country)
                    if threat > maxthreat:
                        maxthreat = threat
                        attackSelection = country
                    if threat > 0.85:
                        self.approach[country] = Approach.DEFCON5
                    elif threat > 0.62:
                        self.approach[country] = Approach.DEFCON4
                    elif threat > 0.38:
                        self.approach[country] = Approach.DEFCON3
                    elif threat > 0.15:
                        self.approach[country] = Approach.DEFCON2
                    else:
                        self.approach[country] = Approach.DEFCON1
            # Just in case there is no decision to attack the country that poses the most threat to you, attack
            self.approach[attackSelection] = Approach.DEFCON1
            # For relatively small countries, don't care about their response
            for country in self.map.countries.values():
                if country is not self:
                    if country.scCount * 3.5 < self.scCount:
                        self.approach[country] = Approach.DEFCON1

    def findThreatValue(self, country):
        countArmies = 0
        countSCs = 0
        for sc in self._getSupplyCenters():
            isCloseToCountry = False
            for adjclose in sc.adj:
                for adjfar in adjclose.adj:
                    if adjfar.owner is country:
                        isCloseToCountry = True
                        if adjfar.hasUnit:
                            countArmies += 1
            if isCloseToCountry:
                countSCs += 1

        if self.trust[country] == -1:
            return 3
        if countSCs != 0:  # If we fully trust the neighbour, we are able to tolerate 2to1 army ratio
            return countArmies / countSCs / (self.trust[country] + 1)
        else:
            return 0  # If there are no nearby units, that means they are no threat to us


class Approach:  # Definitions below are the aim, but not the definite values to achieve the aim. It's more of a guideline
    DEFCON5 = 0  # Help when possible
    DEFCON4 = 0.25  # Don't have any armies at border
    DEFCON3 = 0.5  # Have minimal army presence
    DEFCON2 = 0.75  # Fully defend the border but don't attack
    DEFCON1 = 1  # Attack
