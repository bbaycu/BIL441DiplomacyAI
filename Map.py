from Territory import Territory
from AI import AI
from PIL import Image, ImageDraw

class Map:
    countries = {}
    territories = {}
    supplycenters = []
    img = Image.open(R"Game/map.png").convert("RGB")

    def __init__(self):
        self.countries["England"] = AI("England", (255, 51, 204), self)
        self.countries["France"] = AI("France", (0, 0, 255), self)
        self.countries["Germany"] = AI("Germany", (153, 153, 153), self)
        self.countries["Russia"] = AI("Russia", (204, 51, 255), self)
        self.countries["Austria"] = AI("Austria", (255, 51, 51), self)
        self.countries["Italy"] = AI("Italy", (51, 204, 51), self)
        self.countries["Turkey"] = AI("Turkey", (255, 255, 77), self)
        for c1 in self.countries.values():
            for c2 in self.countries.values():
                if c2 is not c1:
                    c1.trust[c2] = 0
        self.defineProvinces()
        self.addAdjacencies()
        for territory in self.territories.values():
            if territory.hasSC:
                self.supplycenters.append(territory)

    def paint(self,territory,color):
        if not territory.isSea:
            ImageDraw.floodfill(self.img, territory.center, color, thresh=25)

    def paintMap(self):
        for territory in self.territories.values():
            if (territory.owner is not None) and (not territory.isSea):
                self.paint(territory, territory.owner.color);

    def paintUnits(self,count):
        img2 = self.img.copy()
        for ter in self.territories.values():
            if ter.hasUnit:
                for i in range(7):
                    for j in range(10):
                        if(Territory.soldierShape[i][j]==True):
                            img2.putpixel((ter.center[0]+j,ter.center[1]+i),(0,0,0))
                        else:
                            img2.putpixel((ter.center[0] + j, ter.center[1] + i), ter.owner.color)
        img2.save("./Game/Moves/"+str(count)+".png")

    def defineProvinces(self):
        eng = self.countries.get("England");
        fra = self.countries.get("France");
        ger = self.countries.get("Germany");
        rus = self.countries.get("Russia")
        aus = self.countries.get("Austria");
        ita = self.countries.get("Italy");
        tur = self.countries.get("Turkey");

        self.territories["spa"] = Territory("spa", None, True, False, (175, 659))
        self.territories["por"] = Territory("por", None, True, False, (115, 627))
        self.territories["naf"] = Territory("naf", None, False, False, (194, 805))
        self.territories["tun"] = Territory("tun", None, True, False, (390, 809))

        self.territories["gas"] = Territory("gas", fra, False, False, (265, 585))
        self.territories["mar"] = Territory("mar", fra, True, False, (322, 608))
        self.territories["bre"] = Territory("bre", fra, True, False, (268, 516))
        self.territories["par"] = Territory("par", fra, True, False, (295, 527))
        self.territories["pic"] = Territory("pic", fra, False, False, (316, 479))
        self.territories["bur"] = Territory("bur", fra, False, False, (346, 540))

        self.territories["pie"] = Territory("pie", ita, False, False, (392, 603))
        self.territories["tus"] = Territory("tus", ita, False, False, (428, 643))
        self.territories["ven"] = Territory("ven", ita, True, False, (445, 629))
        self.territories["rom"] = Territory("rom", ita, True, False, (457, 683))
        self.territories["apu"] = Territory("apu", ita, False, False, (495, 685))
        self.territories["nap"] = Territory("nap", ita, True, False, (502, 726))

        self.territories["bel"] = Territory("bel", None, True, False, (359, 485))
        self.territories["hol"] = Territory("hol", None, True, False, (368, 446))

        self.territories["mun"] = Territory("mun", ger, True, False, (409, 523))
        self.territories["ruh"] = Territory("ruh", ger, False, False, (390, 486))
        self.territories["kie"] = Territory("kie", ger, True, False, (430, 459))
        self.territories["ber"] = Territory("ber", ger, True, False, (476, 421))
        self.territories["sil"] = Territory("sil", ger, False, False, (523, 476))
        self.territories["pru"] = Territory("pru", ger, False, False, (530, 436))

        self.territories["boh"] = Territory("boh", aus, False, False, (488, 515))
        self.territories["trl"] = Territory("trl", aus, False, False, (476, 557))
        self.territories["tri"] = Territory("tri", aus, True, False, (524, 625))
        self.territories["vie"] = Territory("vie", aus, True, False, (509, 558))
        self.territories["bud"] = Territory("bud", aus, True, False, (602, 577))
        self.territories["gal"] = Territory("gal", aus, False, False, (612, 512))

        self.territories["lon"] = Territory("lon", eng, True, False, (313, 425))
        self.territories["wal"] = Territory("wal", eng, False, False, (265, 410))
        self.territories["yor"] = Territory("yor", eng, False, False, (302, 391))
        self.territories["lvp"] = Territory("lvp", eng, True, False, (278, 347))
        self.territories["cly"] = Territory("cly", eng, False, False, (280, 298))
        self.territories["edi"] = Territory("edi", eng, True, False, (297, 336))

        self.territories["den"] = Territory("den", None, True, False, (442, 349))
        self.territories["swe"] = Territory("swe", None, True, False, (521, 337))
        self.territories["nwy"] = Territory("nwy", None, True, False, (432, 297))
        self.territories["fin"] = Territory("fin", None, False, False, (623, 239))

        self.territories["stp"] = Territory("stp", rus, True, False, (795, 204))
        self.territories["lvn"] = Territory("lvn", rus, False, False, (626, 374))
        self.territories["mos"] = Territory("mos", rus, True, False, (747, 365))
        self.territories["war"] = Territory("war", rus, True, False, (566, 461))
        self.territories["ukr"] = Territory("ukr", rus, False, False, (695, 501))
        self.territories["sev"] = Territory("sev", rus, True, False, (784, 505))

        self.territories["rum"] = Territory("rum", None, True, False, (687, 613))
        self.territories["ser"] = Territory("ser", None, True, False, (589, 674))
        self.territories["bul"] = Territory("bul", None, True, False, (672, 653))
        self.territories["gre"] = Territory("gre", None, True, False, (605, 771))
        self.territories["alb"] = Territory("alb", None, False, False, (571, 697))

        self.territories["con"] = Territory("con", tur, True, False, (685, 684))
        self.territories["smy"] = Territory("smy", tur, True, False, (748, 754))
        self.territories["ank"] = Territory("ank", tur, True, False, (803, 679))
        self.territories["arm"] = Territory("arm", tur, False, False, (923, 685))
        self.territories["syr"] = Territory("syr", tur, False, False, (917, 773))

        self.territories["bar"] = Territory("bar", None, False, True, (710, 48))
        self.territories["nrg"] = Territory("nrg", None, False, True, (432, 92))
        self.territories["nat"] = Territory("nat", None, False, True, (128, 197))
        self.territories["bot"] = Territory("bot", None, False, True, (586, 319))
        self.territories["bal"] = Territory("bal", None, False, True, (543, 379))
        self.territories["ska"] = Territory("ska", None, False, True, (448, 322))
        self.territories["nth"] = Territory("nth", None, False, True, (355, 317))
        self.territories["hel"] = Territory("hel", None, False, True, (401, 388))
        self.territories["eng"] = Territory("eng", None, False, True, (238, 461))
        self.territories["iri"] = Territory("iri", None, True, True, (207, 423))
        self.territories["mid"] = Territory("mid", None, False, True, (48, 556))
        self.territories["wes"] = Territory("wes", None, False, True, (275, 736))
        self.territories["lyo"] = Territory("lyo", None, False, True, (330, 670))
        self.territories["tyn"] = Territory("tyn", None, False, True, (420, 720))
        self.territories["ion"] = Territory("ion", None, False, True, (519, 791))
        self.territories["adr"] = Territory("adr", None, False, True, (501, 663))
        self.territories["aeg"] = Territory("aeg", None, False, True, (657, 777))
        self.territories["eas"] = Territory("eas", None, False, True, (771, 812))
        self.territories["bla"] = Territory("bla", None, False, True, (756, 636))

    def addAdjacencies(self):
        self.territories["spa"].adj.extend( (self.territories["por"],self.territories["gas"],self.territories["mar"],
                                             self.territories["mid"],self.territories["wes"],self.territories["lyo"],
                                             self.territories["spa"]))
        self.territories["por"].adj.extend( (self.territories["spa"], self.territories["mid"],self.territories["por"]) )
        self.territories["naf"].adj.extend( (self.territories["mid"], self.territories["wes"], self.territories["tun"],
                                             self.territories["naf"]) )
        self.territories["tun"].adj.extend( (self.territories["naf"], self.territories["wes"], self.territories["tun"],
                                             self.territories["tyn"],self.territories["ion"]) )

        self.territories["gas"].adj.extend( (self.territories["spa"], self.territories["mar"],self.territories["bur"],
                                             self.territories["par"],self.territories["bre"],self.territories["mid"]
                                             ,self.territories["gas"]) )
        self.territories["mar"].adj.extend( (self.territories["gas"],self.territories["spa"],self.territories["bur"],
                                             self.territories["pie"],self.territories["lyo"],self.territories["mar"]))
        self.territories["bre"].adj.extend( (self.territories["gas"],self.territories["par"],self.territories["pic"],
                                             self.territories["mid"],self.territories["eng"],self.territories["bre"]))
        self.territories["par"].adj.extend( (self.territories["bre"],self.territories["gas"],self.territories["par"],
                                             self.territories["pic"],self.territories["bur"]) )
        self.territories["pic"].adj.extend( ( self.territories["bre"],self.territories["par"],self.territories["bur"],
                                              self.territories["bel"],self.territories["eng"],self.territories["pic"]) )
        self.territories["bur"].adj.extend( [self.territories["pic"],self.territories["par"],self.territories["gas"],
                                             self.territories["mar"],self.territories["mun"],self.territories["bur"],
                                             self.territories["ruh"],self.territories["bel"]] )

        self.territories["pie"].adj.extend( (self.territories["mar"],self.territories["tus"],self.territories["trl"],
                                             self.territories["ven"],self.territories["lyo"],self.territories["pie"]))
        self.territories["tus"].adj.extend( ( self.territories["pie"],self.territories["ven"],self.territories["rom"],
                                              self.territories["lyo"],self.territories["tyn"],self.territories["tus"]) )
        self.territories["ven"].adj.extend( (self.territories["pie"],self.territories["tus"],self.territories["rom"],
                                             self.territories["apu"],self.territories["tri"],self.territories["trl"],
                                             self.territories["adr"],self.territories["ven"]) )
        self.territories["rom"].adj.extend( ( self.territories["ven"],self.territories["apu"],self.territories["nap"],
                                              self.territories["tus"],self.territories["tyn"],self.territories["rom"]) )
        self.territories["apu"].adj.extend( (self.territories["nap"],self.territories["rom"],self.territories["ven"],
                                             self.territories["adr"],self.territories["ion"],self.territories["apu"]) )
        self.territories["nap"].adj.extend( (self.territories["rom"],self.territories["ion"],self.territories["tyn"],
                                             self.territories["apu"],self.territories["nap"]) )

        self.territories["bel"].adj.extend( (self.territories["pic"],self.territories["bur"],self.territories["ruh"],
                                             self.territories["hol"],self.territories["nth"],self.territories["eng"]
                                             ,self.territories["bel"]) )
        self.territories["hol"].adj.extend( (self.territories["bel"],self.territories["ruh"],self.territories["kie"],
                                             self.territories["nth"],self.territories["hel"],self.territories["hol"]) )

        self.territories["mun"].adj.extend( (self.territories["bur"],self.territories["ruh"],self.territories["kie"],
                                             self.territories["ber"],self.territories["sil"],self.territories["boh"],
                                             self.territories["trl"],self.territories["mun"]) )
        self.territories["ruh"].adj.extend( (self.territories["bur"],self.territories["bel"],self.territories["hol"],
                                             self.territories["kie"],self.territories["mun"],self.territories["ruh"]) )
        self.territories["kie"].adj.extend( (self.territories["hol"],self.territories["ruh"],self.territories["mun"],
                                             self.territories["ber"],self.territories["bal"],self.territories["den"],
                                             self.territories["hel"],self.territories["kie"]) )
        self.territories["ber"].adj.extend( (self.territories["kie"], self.territories["mun"],self.territories["sil"],
                                             self.territories["pru"],self.territories["bal"],self.territories["ber"]) )
        self.territories["sil"].adj.extend( (self.territories["ber"],self.territories["mun"],self.territories["boh"],
                                             self.territories["gal"],self.territories["war"],self.territories["pru"]
                                             ,self.territories["sil"]) )
        self.territories["pru"].adj.extend( (self.territories["ber"],self.territories["sil"],self.territories["war"],
                                             self.territories["lvn"],self.territories["bal"],self.territories["pru"]) )

        self.territories["boh"].adj.extend( (self.territories["sil"],self.territories["mun"],self.territories["trl"],
                                             self.territories["vie"],self.territories["gal"],self.territories["boh"]) )
        self.territories["trl"].adj.extend( (self.territories["pie"],self.territories["ven"],self.territories["tri"],
                                             self.territories["vie"],self.territories["boh"],self.territories["mun"]
                                             ,self.territories["trl"]) )
        self.territories["tri"].adj.extend( (self.territories["ven"],self.territories["trl"],self.territories["vie"],
                                             self.territories["bud"],self.territories["ser"],self.territories["alb"],
                                             self.territories["adr"],self.territories["tri"]) )
        self.territories["vie"].adj.extend( (self.territories["boh"],self.territories["trl"],self.territories["tri"],
                                             self.territories["bud"],self.territories["gal"],self.territories["vie"]) )
        self.territories["bud"].adj.extend( (self.territories["vie"],self.territories["tri"],self.territories["ser"],
                                             self.territories["rum"],self.territories["gal"],self.territories["bud"]) )
        self.territories["gal"].adj.extend( (self.territories["boh"],self.territories["vie"],self.territories["bud"],
                                             self.territories["rum"],self.territories["ukr"],self.territories["war"],
                                             self.territories["sil"],self.territories["gal"]) )

        self.territories["lon"].adj.extend( (self.territories["yor"],self.territories["wal"],self.territories["eng"],
                                             self.territories["nth"],self.territories["lon"]) )
        self.territories["wal"].adj.extend( (self.territories["lvp"],self.territories["yor"],self.territories["lon"],
                                             self.territories["eng"],self.territories["iri"],self.territories["wal"]) )
        self.territories["yor"].adj.extend( (self.territories["edi"],self.territories["lvp"],self.territories["wal"],
                                             self.territories["lon"],self.territories["nth"],self.territories["yor"]) )
        self.territories["lvp"].adj.extend( (self.territories["wal"],self.territories["yor"],self.territories["edi"],
                                             self.territories["cly"],self.territories["nat"],self.territories["iri"]
                                             ,self.territories["lvp"]) )
        self.territories["cly"].adj.extend( (self.territories["nat"],self.territories["nrg"],self.territories["lvp"],
                                             self.territories["edi"],self.territories["cly"]) )
        self.territories["edi"].adj.extend( (self.territories["cly"],self.territories["lvp"],self.territories["yor"],
                                             self.territories["nrg"],self.territories["nth"],self.territories["edi"]) )

        self.territories["den"].adj.extend( (self.territories["ska"],self.territories["nth"],self.territories["hel"],
                                             self.territories["kie"],self.territories["bal"],self.territories["swe"]
                                             ,self.territories["den"]) )
        self.territories["swe"].adj.extend( (self.territories["nwy"],self.territories["den"],self.territories["fin"],
                                             self.territories["ska"],self.territories["bal"],self.territories["bot"]
                                             ,self.territories["swe"]) )
        self.territories["nwy"].adj.extend( (self.territories["ska"],self.territories["nth"],self.territories["nrg"],
                                             self.territories["bar"],self.territories["stp"],self.territories["fin"],
                                             self.territories["swe"],self.territories["nwy"]) )
        self.territories["fin"].adj.extend( (self.territories["nwy"],self.territories["swe"],self.territories["stp"],
                                             self.territories["bot"],self.territories["fin"]) )

        self.territories["stp"].adj.extend( (self.territories["bar"],self.territories["nwy"],self.territories["fin"],
                                             self.territories["bot"],self.territories["lvn"],self.territories["mos"]
                                             ,self.territories["stp"]) )
        self.territories["lvn"].adj.extend( (self.territories["bot"],self.territories["bal"],self.territories["pru"],
                                             self.territories["war"],self.territories["mos"],self.territories["stp"]
                                             ,self.territories["lvn"]) )
        self.territories["mos"].adj.extend( (self.territories["stp"],self.territories["lvn"],self.territories["war"],
                                             self.territories["ukr"],self.territories["sev"],self.territories["mos"]) )
        self.territories["war"].adj.extend( (self.territories["lvn"],self.territories["pru"],self.territories["sil"],
                                             self.territories["gal"],self.territories["ukr"],self.territories["mos"]
                                             ,self.territories["war"]) )
        self.territories["ukr"].adj.extend( (self.territories["mos"],self.territories["war"],self.territories["gal"],
                                             self.territories["rum"],self.territories["sev"],self.territories["ukr"]) )
        self.territories["sev"].adj.extend( (self.territories["mos"],self.territories["ukr"],self.territories["rum"],
                                             self.territories["bla"],self.territories["arm"],self.territories["sev"]) )

        self.territories["rum"].adj.extend( (self.territories["sev"],self.territories["ukr"],self.territories["gal"],
                                             self.territories["bud"],self.territories["ser"],self.territories["bul"],
                                             self.territories["bla"],self.territories["rum"]) )
        self.territories["ser"].adj.extend( (self.territories["bud"],self.territories["tri"],self.territories["alb"],
                                             self.territories["rum"],self.territories["bul"],self.territories["gre"]
                                             ,self.territories["ser"]) )
        self.territories["bul"].adj.extend( (self.territories["rum"],self.territories["ser"],self.territories["gre"],
                                             self.territories["aeg"],self.territories["con"],self.territories["bla"]
                                             ,self.territories["bul"]) )
        self.territories["gre"].adj.extend( (self.territories["bul"],self.territories["ser"],self.territories["alb"],
                                             self.territories["ion"],self.territories["aeg"],self.territories["gre"]) )
        self.territories["alb"].adj.extend( (self.territories["tri"],self.territories["ser"],self.territories["gre"],
                                             self.territories["ion"],self.territories["adr"],self.territories["alb"]) )

        self.territories["con"].adj.extend( (self.territories["bul"],self.territories["ank"],self.territories["smy"],
                                             self.territories["bla"],self.territories["aeg"],self.territories["con"]) )
        self.territories["smy"].adj.extend( (self.territories["con"],self.territories["ank"],self.territories["arm"],
                                             self.territories["syr"],self.territories["eas"],self.territories["aeg"]
                                             ,self.territories["smy"]) )
        self.territories["ank"].adj.extend( (self.territories["con"],self.territories["smy"],self.territories["arm"],
                                             self.territories["bla"],self.territories["ank"]) )
        self.territories["arm"].adj.extend( (self.territories["ank"],self.territories["smy"],self.territories["sev"],
                                             self.territories["syr"],self.territories["bla"],self.territories["arm"]) )
        self.territories["syr"].adj.extend( (self.territories["arm"],self.territories["smy"],self.territories["eas"]
                                             ,self.territories["syr"]) )

        self.territories["bar"].adj.extend( (self.territories["stp"],self.territories["nwy"],self.territories["nrg"]
                                             ,self.territories["bar"]) )
        self.territories["nrg"].adj.extend( (self.territories["bar"],self.territories["nwy"],self.territories["nth"],
                                             self.territories["edi"],self.territories["cly"],self.territories["nat"]
                                             ,self.territories["nrg"]) )
        self.territories["nat"].adj.extend( (self.territories["nrg"],self.territories["cly"],self.territories["lvp"],
                                             self.territories["iri"],self.territories["mid"],self.territories["nat"]) )
        self.territories["bot"].adj.extend( (self.territories["stp"],self.territories["fin"],self.territories["swe"],
                                             self.territories["bal"],self.territories["lvn"],self.territories["bot"]) )
        self.territories["bal"].adj.extend( (self.territories["lvn"],self.territories["pru"],self.territories["ber"],
                                             self.territories["kie"],self.territories["den"],self.territories["swe"],
                                             self.territories["bot"],self.territories["bal"]) )
        self.territories["ska"].adj.extend( (self.territories["nwy"],self.territories["swe"],self.territories["den"],
                                             self.territories["nth"],self.territories["ska"]) )
        self.territories["nth"].adj.extend( (self.territories["nrg"],self.territories["nwy"],self.territories["ska"],
                                             self.territories["den"],self.territories["hel"],self.territories["hol"],
                                             self.territories["bel"],self.territories["eng"],self.territories["lon"],
                                             self.territories["yor"],self.territories["edi"],self.territories["nth"]) )
        self.territories["hel"].adj.extend( (self.territories["hol"],self.territories["kie"],self.territories["den"],
                                             self.territories["nth"],self.territories["hel"]) )
        self.territories["eng"].adj.extend( (self.territories["lon"],self.territories["wal"],self.territories["iri"],
                                             self.territories["mid"],self.territories["bre"],self.territories["pic"],
                                             self.territories["bel"],self.territories["nth"],self.territories["eng"]) )
        self.territories["iri"].adj.extend( (self.territories["nat"],self.territories["mid"],self.territories["eng"],
                                             self.territories["wal"],self.territories["lvp"],self.territories["iri"]) )
        self.territories["mid"].adj.extend( (self.territories["nat"],self.territories["iri"],self.territories["eng"],
                                             self.territories["bre"],self.territories["gas"],self.territories["spa"],
                                             self.territories["por"],self.territories["wes"],self.territories["naf"]
                                             ,self.territories["mid"]) )
        self.territories["wes"].adj.extend( (self.territories["spa"],self.territories["mid"],self.territories["naf"],
                                             self.territories["tun"],self.territories["tyn"],self.territories["lyo"]
                                             ,self.territories["wes"]) )
        self.territories["lyo"].adj.extend( (self.territories["mar"],self.territories["spa"],self.territories["wes"],
                                             self.territories["tyn"],self.territories["tus"],self.territories["pie"]
                                             ,self.territories["lyo"]) )
        self.territories["tyn"].adj.extend( (self.territories["lyo"],self.territories["wes"],self.territories["tun"],
                                             self.territories["ion"],self.territories["nap"],self.territories["rom"],
                                             self.territories["tus"],self.territories["tyn"]) )
        self.territories["ion"].adj.extend( (self.territories["tun"],self.territories["tyn"],self.territories["nap"],
                                             self.territories["apu"],self.territories["adr"],self.territories["alb"],
                                             self.territories["gre"],self.territories["aeg"],self.territories["eas"]
                                             ,self.territories["ion"]) )
        self.territories["adr"].adj.extend( (self.territories["alb"],self.territories["tri"],self.territories["ven"],
                                             self.territories["apu"],self.territories["ion"],self.territories["adr"]) )
        self.territories["aeg"].adj.extend( (self.territories["bul"],self.territories["gre"],self.territories["ion"],
                                             self.territories["eas"],self.territories["smy"],self.territories["con"]
                                             ,self.territories["aeg"]) )
        self.territories["eas"].adj.extend( (self.territories["smy"],self.territories["aeg"],self.territories["ion"],
                                             self.territories["syr"],self.territories["eas"]) )
        self.territories["bla"].adj.extend( (self.territories["sev"],self.territories["rum"],self.territories["bul"],
                                             self.territories["con"],self.territories["ank"],self.territories["arm"]
                                             ,self.territories["bla"]) )