from abc import ABCMeta , abstractmethod
from mapp import *
from random import randint


class Tower(object): #(ABCMeta): # pomysl - zrobic z tego klase abstrakcyjna ! ok
    def observe_fields(self):
        for parameters in self.reach:
            self.board.get_field(parameters[0], parameters[1], "path").add_observer(self)
    #@abstractmethod
    def shoot(self, field):
        rival = field.content
        rival.shot()

    #@abstractmethod
    def notify(self, field): #kazda wieza obseruje pola w swoim zasiegu
        if self.airlyreach == field.content.airly:
            self.shoot(field)
            if not field.content.resistance:
                self.produce_effect(field, RivalWave.simulator)
    #@abstractmethod
    def __str__(self):
        return self.sign

class Fortress(Tower):
    def __init__(self, x, y, map_):
        self.name = "Fortress"
        self.parameters = (x,y)
        self.time = 1
        self.reach = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y+1), (x, y+1), (x+1, y+1)]
        self.airlyreach = False
        self.effect = None
        self.board = map_
        self.sign = "F"
        self.value = 4

    def produce_effect(self, field, simulator):#bron odlamkowa, dostaje nawet ten latajacy
        ind = self.board.rivals_on_board.index(field.content)
        t = simulator.now
        if ind > 0:
            simulator.add_event(t, self.board.rivals_on_board[ind - 1].shot)
        if ind < len(self.board.rivals_on_board):
            simulator.add_event(t, self.board.rivals_on_board[ind + 1].shot)


class Alkazar(Tower):
    def __init__(self, x, y, map_):
        self.name = "Alkazar"
        self.parameters = (x,y)
        self.time = 2
        self.reach = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y+1), (x, y+1), (x+1, y+1)]
        self.airlyreach = False
        self.effect = None
        self.board = map_
        self.sign = "A"
        self.value = 4

    def produce_effect(self, field, simulator):
        return

class ArcherTower(Tower): # change the reach
    def __init__(self, x, y, map_):
        self.name = "Archer Tower"
        self.parameters = (x,y)
        self.time = 3
        self.reach = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y+1), (x, y+1), (x+1, y+1)]
        self.airlyreach = True
        self.effect = None
        self.board = map_
        self.sign = "R"
        self.value = 4

    def produce_effect(self, field, simulator): #zatrute strzaly
        t = simulator.now
        simulator.add_event(t + 1, field.content.shot)
        simulator.add_event(t + 2, field.content.shot)

class MagicTower(Tower): #change the reach
    def __init__(self, x, y, map_):
        self.name = "Magic Tower"
        self.parameters = (x,y)
        self.time = 3
        self.reach = [(x-1, y-1), (x, y-1), (x+1, y-1), (x-1, y+1), (x, y+1), (x+1, y+1)]
        self.airlyreach = True
        self.effect = None
        self.board = map_
        self.sign = "M"
        self.value = 4

    def produce_effect(self, field, simulator): #bron ogluszajaca
        for event in simulator.queue:
            if event[2] == field.content:
                event[0] += 1


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
        field = map_.get_field(column, scaledrow, "wall")
        try:
            tower = TowerFactory.create(towertype, column, scaledrow, map_)
            Player.delete_credits(tower.value)
            field.add_content(tower)
            tower.observe_fields()
            Player.add_tower(tower)
        except Exception as e:
            print "\n\n\nError!!!!!\n\n\n", e
            # ustawiamy tylko na murach! <- try/except

    @classmethod
    def start(cls):
        print "\nThis is a Building Phase. You can build your towers on the map."
