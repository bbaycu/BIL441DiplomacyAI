class Order:

    def __init__(self, orderType, origin, arg=None):
        self.type = orderType
        self.origin = origin
        self.arg = arg
        self.strength = 1
        self.isvalid = True

    def __str__(self):
        if self.arg is None:
            return str(self.type) + " " + self.origin.name
        else:
            return str(self.type) + " " + self.origin.name + " -> " + self.arg.name

    def findTrustChange(self, country):
        count = 0
        if self.type == "mov":
            if self.arg.owner is country and self.arg.hasUnit:
                count += -0.15
            else:
                for adj in self.arg.adj:
                    if country is adj.owner and adj.hasSC:
                        count += -0.25
        elif self.type == "sup":
            if self.arg is country:
                count += -0.2

        return count
