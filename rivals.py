from mapp import *
from random import *
from operator import attrgetter
from game import *
import sys

class Rival(object):
    def __str__(self):
        return self.sign

    def shot(self):
        self.score -= 1
        if self.score <= 0:
            map_ = RivalWave.map_
            map_.delete_rival(self)
            RivalWave.simulator.delete_rival(self)
            game.add_credits(self.credits)

    def go(self, time):
        map_ = RivalWave.map_
        for field in map_.iter_path():
            RivalWave.simulator.add_event(time, field.add_content, self)
            RivalWave.simulator.add_event(time + 1, field.remove_content)
            time += self.time
        RivalWave.simulator.add_event(time, field.end)


class Paratrooper(Rival):
    def __init__(self):
        self.name = "Paratrooper"
        self.sign = "P"
        self.score = 7
        self.time = 4
        self.airly = True
        self.resistance = False
        self.credits = 10


class Knight(Rival):
    def __init__(self):
        self.name = "Knight"
        self.sign = "K"
        self.score = 14
        self.time = 3
        self.airly = False
        self.resistance = False
        self.credits = 12


class Viking(Rival):
    def __init__(self):
        self.name = "Viking"
        self.sign = "V"
        self.score = 15
        self.time = 5
        self.airly = False
        self.resistance = True #resistant to special effects
        self.credits = 7


class Dragon(Rival):
    def __init__(self):
        self.name = "Dragon"
        self.sign = "D"
        self.score = 11
        self.time = 2
        self.airly = True
        self.resistance = False
        self.credits = 15


class Speeder(Rival):
    def __init__(self):
        self.name = "Speeder"
        self.sign = "S"
        self.score = 8
        self.time = 1
        self.resistance = False
        self.airly = False
        self.credits = 20


class RivalFactory(object):
    rivals = {"paratrooper":Paratrooper, "knight":Knight, "viking":Viking, "dragon":Dragon, "speeder":Speeder}
    @classmethod
    def create(cls, type_):
        return cls.rivals[type_]()


class RivalWave(object):
    airly = ["paratrooper", "dragon"]
    groundbased = ["knight", "viking", "speeder"]
    counter = 0
    wave = []
    simulator = None
    map_ = None
    @classmethod
    def create(cls): #algorithm of the rival wave creating
        print cls.counter
        if cls.counter < 2:
            for i in range(1, randint(2,3)):
                cls.wave.append(RivalFactory.create(choice(cls.airly + cls.groundbased)))
        elif cls.counter == 2 or cls.counter == 3:
            cls.wave.append(RivalFactory.create(choice(cls.airly)))
            for i in range(randint(3, 5)):
                cls.wave.append(RivalFactory.create(choice(cls.groundbased)))
        else:
            for i in range(randint(3, 7)):
                cls.wave.append(RivalFactory.create(choice(cls.airly)))
                cls.wave.append(RivalFactory.create(choice(cls.groundbased)))
        cls.counter += 1

    @classmethod
    def generate(cls):
        time = cls.simulator.now
        wave = sorted(cls.wave, key=attrgetter('time'))
        for rival in wave:
            print (rival, time)
            cls.map_.add_rival(rival)
            rival.go(time)
            time += 5
        cls.wave = []

    @classmethod
    def set_map(cls, map_):
        cls.map_ = map_
