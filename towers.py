from abc import ABCMeta , abstractmethod

class BuildingPhase(object):
    @classmethod
    def set_tower(cls, map_):
        tower  = raw_input("Please, choose a type of tower: ")
        column = int(raw_input("The column number: "))
        row = int(raw_input("The row number: "))
        field = map_.get_wall_field(column, row)
        field.add_content(tower)
        #usun kredyty
        # ustawiamy tylko na murach! <- try/except
        return None

    @classmethod
    def update_credits22(cls):
        pass

    @classmethod
    def update_credits111(cls):
        pass

class Tower(object): #(ABCMeta): # pomysl - zrobic z tego klase abstrakcyjna ! ok
    #@abstractmethod
    def notify(self, rival): #kazda wieza obseruje pola w swoim zasiegu
        pass

    #@abstractmethod
    def shoot(self, rival):
        if self.air and rival.is_airly:
            rival.shot()
            #rival.have_effect(self)
    #@abstractmethod
    def __str__(self):
        return self.sign

class Fortress(Tower):
    def __init__(self, x, y, map_):
        self.parameters = (x,y)
        self.time = 1
        self.reach = [(x, y) for x in (x-1, x, x+1) for y in (y-1, y, y+1)]
        self.airlyreach = False
        self.effect = None
        self.board = map_
        self.sign = "F"

    def produce_effect(self):
        pass

class Alkazar(Tower):
    def __init__(self, x, y, map_):
        self.parameters = (x,y)
        self.time = 2
        self.reach = [(x, y) for x in (x-1, x, x+1) for y in (y-1, y, y+1)]
        self.airlyreach = False
        self.effect = None
        self.board = map_
        self.sign = "A"

class ArcherTower(Tower): # change the reach
    def __init__(self, x, y, map_):
        self.parameters = (x,y)
        self.time = 3
        self.reach = [(x, y) for x in (x-1, x, x+1) for y in (y-1, y, y+1)]
        self.airlyreach = True
        self.effect = None
        self.board = map_
        self.sign = "R"

class MagicTower(Tower): #change the reach
    def __init__(self, x, y, map_):
        self.parameters = (x,y)
        self.time = 3
        self.reach = [(x, y) for x in (x-1, x, x+1) for y in (y-1, y, y+1)]
        self.airlyreach = True
        self.effect = None
        self.board = map_
        self.sign = "M"

class TowerFactory(object):
    towers = {"F":Fortress, "A":Alkazar, "R":ArcherTower, "M":MagicTower}
    @classmethod
    def create(cls, type_, x, y, map_):
        return cls.towers[type_](x, y, map_)
