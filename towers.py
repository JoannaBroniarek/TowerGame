from abc import ABCMeta , abstractmethod
from mapp import *

#To do:
# tworzenie efektow dla wiez
# tower.shoot

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
        self.name = "Fortress"
        self.parameters = (x,y)
        self.time = 1
        self.reach = [(x, y) for x in (x-1, x, x+1) for y in (y-1, y, y+1)]
        self.airlyreach = False
        self.effect = None
        self.board = map_
        self.sign = "F"
        self.value = 4

    def produce_effect(self):
        pass

class Alkazar(Tower):
    def __init__(self, x, y, map_):
        self.name = "Alkazar"
        self.parameters = (x,y)
        self.time = 2
        self.reach = [(x, y) for x in (x-1, x, x+1) for y in (y-1, y, y+1)]
        self.airlyreach = False
        self.effect = None
        self.board = map_
        self.sign = "A"
        self.value = 4

class ArcherTower(Tower): # change the reach
    def __init__(self, x, y, map_):
        self.name = "Archer Tower"
        self.parameters = (x,y)
        self.time = 3
        self.reach = [(x, y) for x in (x-1, x, x+1) for y in (y-1, y, y+1)]
        self.airlyreach = True
        self.effect = None
        self.board = map_
        self.sign = "R"
        self.value = 4

class MagicTower(Tower): #change the reach
    def __init__(self, x, y, map_):
        self.name = "Magic Tower"
        self.parameters = (x,y)
        self.time = 3
        self.reach = [(x, y) for x in (x-1, x, x+1) for y in (y-1, y, y+1)]
        self.airlyreach = True
        self.effect = None
        self.board = map_
        self.sign = "M"
        self.value = 4

class TowerFactory(object):
    towers = {"F":Fortress, "A":Alkazar, "R":ArcherTower, "M":MagicTower}
    @classmethod
    def create(cls, type_, x, y, map_):
        return cls.towers[type_](x, y, map_)

class BuildingPhase(object):
    @classmethod
    def set_tower(cls, map_):
        print " F - Fortress, A - Alkazar, R - ArcherTower, M - MagicTower"
        towertype  = raw_input("Please, choose a type of tower: ")
        column = int(raw_input("The column number: ")) - 1
        row = int(raw_input("The row number: "))
        scaledrow = row*2 + 1
        field = map_.get_wall_field(column, scaledrow)
        try:
            tower = TowerFactory.create(towertype, column, scaledrow, map_)
            Player.delete_credits(tower.value)
            field.add_content(tower)
            Player.add_tower(tower)
        except Exception as e:
            print e
            # ustawiamy tylko na murach! <- try/except

    @classmethod
    def start(cls):
        print "\nThis is a Building Phase. You can build your towers on the map."
