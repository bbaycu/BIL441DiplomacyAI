import copy
import os
import random
import shutil

from AI import AI
from Map import Map
from Order import Order


class Game:
    moveOrders = []
    supportOrders = []
    isMoveTurn = True
    def playTheGame(self):
        moves = None
        for i in range(75):
            for country in self.map.countries.values():
                moves = country.getMoves()
                orders = random.choice(moves)
                self.addOrders(orders)
            self.resolveOrders()
            for country in self.map.countries.values():
                builds = country.getPossibleBuilds()
                if len(builds) > 0:
                    self.addOrders(random.choice(builds))
            for country in self.map.countries.values():
                country.updateTrustAtEndOfTurn()
            self.resolveOrders()
            if self.gameIsFinished():
                return
        print("Game drawn")

    def gameIsFinished(self):
        for country in self.map.countries.values():
            if country.scCount > 17:
                print("Game won by ", country.name)
                return True
        return False

    def copy(self):
        game2 = copy.deepcopy(self)
        game2.isMainGame = False
        return game2

    def addOrders(self,orderList):
        for order in orderList:
            if order.type == "mov":
                self.moveOrders.append(order)
            else:
                self.supportOrders.append(order)
                self.moveOrders.append(Order("mov",order.origin,order.origin))


    def resolveOrders(self):
        self.count += 1
        if self.isMoveTurn:
            self.__cutSupports()
            self.__countSupportForMovesAndInvalidateInsufficientlySupportedMoves()
            self.__resolveMoves()
        else:
            self.__doBuildsAndDisbands()

        self.isMoveTurn = not self.isMoveTurn

        if self.isMainGame:
            self.map.paintMap()
            self.map.paintUnits(self.count)
        self.moveOrders = []
        self.supportOrders = []

    def __doBuildsAndDisbands(self):
        for order in self.supportOrders:
            if order.type == "bui":
                order.origin.hasUnit = True
                order.origin.owner.units.append(order.origin)
            elif order.type == "rem":
                order.origin.hasUnit = False
                order.origin.owner.units.remove(order.origin)
            else:
                print("Wrong Order Type")

    def __cutSupports(self):
        for sorder in self.supportOrders:
            for morder in self.moveOrders:
                if (morder.arg == sorder.origin) and (sorder.origin != morder.origin):
                    sorder.isvalid = False
                    if sorder.arg is not None:
                        sorder.origin.owner.updateTrust(morder.origin.owner, -0.15 / AI.TRUST_DECAY_MULTIPLIER)

    def __countSupportForMovesAndInvalidateInsufficientlySupportedMoves(self):
        for sorder in self.supportOrders:
            if sorder.arg is not None:
                sorder.arg.updateTrust(sorder.origin.owner, -0.2 / AI.TRUST_DECAY_MULTIPLIER)
            if sorder.isvalid:
                for morder in self.moveOrders:
                    if sorder.origin.isAdjacentTo(morder.arg) and morder.origin.owner != sorder.arg:
                        morder.strength += 1
                        morder.origin.owner.updateTrust(sorder.origin.owner, 0.2 / AI.TRUST_DECAY_MULTIPLIER)

        for morder1 in self.moveOrders:
            for morder2 in self.moveOrders:
                if (morder1.arg == morder2.arg) and (morder1 is not morder2):
                    if morder1.strength <= morder2.strength:
                        self.__invalidateMoveOrder(morder1)

    def __invalidateMoveOrder(self,order):
        order.isvalid = False
        for morder in self.moveOrders:
            if morder is order:
                continue
            if morder.arg is order.origin:
                if not morder.isvalid:
                    break
                if morder.origin.owner is order.origin.owner:
                    self.__invalidateMoveOrder(morder)
                else:
                    if morder.strength < 2:
                        self.__invalidateMoveOrder(morder)

    def __resolveMoves(self):
        for order in self.moveOrders:
            if order.isvalid:
                order.origin.hasUnit = False
                order.origin.owner.units.remove(order.origin)
                order.origin.owner.units.append(order.arg)
                order.arg.nextOwner = order.origin.owner
                for adj in order.arg.adj:
                    if adj.hasSC and adj.owner is not None:
                        adj.owner.updateTrust(order.origin.owner, -0.25 / AI.TRUST_DECAY_MULTIPLIER)
        for order in self.moveOrders:
            if order.isvalid:
                if order.arg.hasSC and order.arg.owner != order.origin.owner:
                    order.origin.owner.scCount += 1
                    if order.arg.owner is not None:
                        order.arg.owner.scCount -= 1
                if order.arg.hasUnit:
                    order.arg.owner.units.remove(order.arg)
                order.arg.owner = order.arg.nextOwner
                order.arg.hasUnit = True

    def __init__(self,isMainGame):

        self.isMainGame = isMainGame
        self.map = Map()
        for sc in self.map.supplycenters:
            if sc.owner is not None:
                sc.owner.scCount +=1
            if sc.hasUnit:
                sc.owner.units.append(sc)
        self.count = 0
        if isMainGame:
            shutil.rmtree(os.path.join("Game", "Moves"))
            os.mkdir(os.path.join("Game", "Moves"))
            self.map.paintMap()
            self.map.paintUnits(0)
