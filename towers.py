from abc import ABCMeta , abstractmethod
from mapp import *  
from random import randint

class Tower(object):
    def observe_fields(self):
        for parameters in self.reach:
            self.board.get_field(parameters[0], parameters[1], "path").add_observer(self)

    def shoot(self, field):
        rival = field.content
        rival.shot()

    def notify(self, field):
        if self.airlyreach == field.content.airly:
            self.shoot(field)
            if not field.content.resistance:
                self.produce_effect(field, RivalWave.simulator)

    def __str__(self):
        return self.sign


class Fortress(Tower):
    def __init__(self, x, y, map_):
        self.name = "Fortress"
        self.parameters = (x,y)
        self.time = 1
        self.reach = [(x-p, y+r) for p in (1, 0, -1) for r in (1, -1)]
        self.airlyreach = False
        self.effect = None
        self.board = map_
        self.sign = "F"
        self.value = 4

    def produce_effect(self, field, simulator):#bron odlamkowa, dostaje nawet ten latajacy
        try:
            ind = self.board.rivals_on_board.index(field.content)
            t = simulator.now
            if ind > 0:
                simulator.add_event(t, self.board.rivals_on_board[ind - 1].shot)
            if ind < len(self.board.rivals_on_board) - 1:
                simulator.add_event(t, self.board.rivals_on_board[ind + 1].shot)
        except:
            pass


class Alkazar(Tower):
    def __init__(self, x, y, map_):
        self.name = "Alkazar"
        self.parameters = (x,y)
        self.time = 2
        self.reach = [(x-p, y+r) for p in (1, 0, -1) for r in (1, -1)]
        self.airlyreach = False
        self.effect = None
        self.board = map_
        self.sign = "A"
        self.value = 4

    def produce_effect(self, field, simulator):
        return


class ArcherTower(Tower):
    def __init__(self, x, y, map_):
        self.name = "Archer Tower"
        self.parameters = (x,y)
        self.time = 3
        self.reach = [(x-p, y+r) for p in (2, 1, -1, -2) for r in (1, -1)]
        self.airlyreach = True
        self.effect = None
        self.board = map_
        self.sign = "R"
        self.value = 4

    def produce_effect(self, field, simulator): #zatrute strzaly
        t = simulator.now
        simulator.add_event(t + 1, field.content.shot)
        simulator.add_event(t + 2, field.content.shot)


class MagicTower(Tower):
    def __init__(self, x, y, map_):
        self.name = "Magic Tower"
        self.parameters = (x,y)
        self.time = 3
        self.reach = [(x-p, y+r) for p in (2, 1, 0, -1, -2) for r in (1, -1)]
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
