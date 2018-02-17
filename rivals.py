from mapp import *
import sys

class Rival(object):
    def __str__(self):
        return self.sign

    def shot(self):
        self.score -= 1
        if self.score == 0:
            self.map.delete_rival(self)

    def have_effect(self, tower): #special effect in case of being shot
        pass

class Paratrooper(Rival):
    def __init__(self, map_):
        self.name = "Paratrooper"
        self.sign = "P"
        self.score = 5
        self.time = 1
        self.airly = True
        self.credits = 10
        self.map = map_

class Knight(Rival):
    def __init__(self, map_):
        self.name = "Knight"
        self.sign = "K"
        self.score = 4
        self.time = 3
        self.airly = False
        self.credits = 12
        self.map = map_

class Viking(Rival):
    def __init__(self, map_):
        self.name = "Viking"
        self.sign = "V"
        self.score = 6
        self.time = 2
        self.airly = False
        self.credits = 7
        self.map = map_

class Dragon(Rival):
    def __init__(self, map_):
        self.name = "Dragon"
        self.sign = "D"
        self.score = 8
        self.time = 2
        self.airly = True
        self.credits = 15
        self.map = map_

class Speeder(Rival):
    def __init__(self, map_):
        self.name = "Speeder"
        self.sign = "S"
        self.score = 3
        self.time = 5
        self.airly = False
        self.credits = 20
        self.map = map_

class RivalFactory(object):
    rivals = {"paratrooper":Paratrooper, "knight":Knight, "viking":Viking, "dragon":Dragon, "speeder":Speeder}
    @classmethod
    def create(cls, type_, map_):
        return cls.rivals[type_](map_)
