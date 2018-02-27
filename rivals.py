from mapp import *
from random import *
from operator import attrgetter
import sys

class Rival(object):
    def __str__(self):
        return self.sign

    def shot(self):
        self.score -= 1
        if self.score <= 0:
            self.map.delete_rival(self)
            RivalWave.simulator.delete_rival(self)
            self.map.player.add_credits(self.credits)

    def go(self, time):
        for field in self.map.iter_path():
            RivalWave.simulator.add_event(time, field.add_content, self)
            RivalWave.simulator.add_event(time + 1, field.remove_content)
            time += self.time
        RivalWave.simulator.add_event(time, field.end)


class Paratrooper(Rival):
    def __init__(self, map_):
        self.name = "Paratrooper"
        self.sign = "P"
        self.score = 7
        self.time = 4
        self.airly = True
        self.resistance = False
        self.credits = 10
        self.map = map_


class Knight(Rival):
    def __init__(self, map_):
        self.name = "Knight"
        self.sign = "K"
        self.score = 14
        self.time = 3
        self.airly = False
        self.resistance = False
        self.credits = 12
        self.map = map_


class Viking(Rival):
    def __init__(self, map_):
        self.name = "Viking"
        self.sign = "V"
        self.score = 15
        self.time = 5
        self.airly = False
        self.resistance = True #resistant to special effects
        self.credits = 7
        self.map = map_


class Dragon(Rival):
    def __init__(self, map_):
        self.name = "Dragon"
        self.sign = "D"
        self.score = 11
        self.time = 2
        self.airly = True
        self.resistance = False
        self.credits = 15
        self.map = map_


class Speeder(Rival):
    def __init__(self, map_):
        self.name = "Speeder"
        self.sign = "S"
        self.score = 8
        self.time = 1
        self.resistance = False
        self.airly = False
        self.credits = 20
        self.map = map_


class RivalFactory(object):
    rivals = {"paratrooper":Paratrooper, "knight":Knight, "viking":Viking, "dragon":Dragon, "speeder":Speeder}
    @classmethod
    def create(cls, type_, map_):
        return cls.rivals[type_](map_)


class RivalWave(object):
    airly = ["paratrooper", "dragon"]
    groundbased = ["knight", "viking", "speeder"]
    counter = 0
    wave = []
    simulator = None
    @classmethod
    def create(cls, map_): #algorithm of the rival wave creating
        print cls.counter
        if cls.counter < 2:
            for i in range(1, randint(2,3)):
                cls.wave.append(RivalFactory.create(choice(cls.airly + cls.groundbased), map_))
        elif cls.counter == 2 or cls.counter == 3:
            cls.wave.append(RivalFactory.create(choice(cls.airly), map_))
            for i in range(randint(3, 5)):
                cls.wave.append(RivalFactory.create(choice(cls.groundbased), map_))
        else:
            for i in range(randint(3, 7)):
                cls.wave.append(RivalFactory.create(choice(cls.airly), map_))
                cls.wave.append(RivalFactory.create(choice(cls.groundbased), map_))
        cls.counter += 1

    @classmethod
    def generate(cls, map_):
        time = cls.simulator.now
        wave = sorted(cls.wave, key=attrgetter('time'))
        for rival in wave:
            print (rival, time)
            map_.add_rival(rival)
            rival.go(time)
            time += 2
        cls.wave = []
