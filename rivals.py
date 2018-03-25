from mapp import *
from random import *
from operator import attrgetter
import sys


class Rival(object):
    def __str__(self):
        return self.sign

    def shot(self):
        if self.dead:
            return
        self.score -= 1
        if self.score <= 0:
            map_ = RivalWave.map_
            map_.delete_rival(self)
            self.dead = True
            RivalWave.game.add_credits(self.credits)


class Paratrooper(Rival):
    def __init__(self):
        self.name = "Paratrooper"
        self.sign = "P"
        self.score = 7
        self.time = 4
        self.airly = True
        self.resistance = False
        self.credits = 10
        self.dead = False


class Knight(Rival):
    def __init__(self):
        self.name = "Knight"
        self.sign = "K"
        self.score = 14
        self.time = 3
        self.airly = False
        self.resistance = False
        self.credits = 12
        self.dead = False


class Viking(Rival):
    def __init__(self):
        self.name = "Viking"
        self.sign = "V"
        self.score = 10
        self.time = 4
        self.airly = False
        self.resistance = True #resistant to special effects
        self.credits = 7
        self.dead = False


class Dragon(Rival):
    def __init__(self):
        self.name = "Dragon"
        self.sign = "D"
        self.score = 11
        self.time = 2
        self.airly = True
        self.resistance = False
        self.credits = 15
        self.dead = False


class Speeder(Rival):
    def __init__(self):
        self.name = "Speeder"
        self.sign = "S"
        self.score = 8
        self.time = 1
        self.resistance = False
        self.airly = False
        self.credits = 20
        self.dead = False


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
    game = None
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
    def go(cls, time, rival):
        for field in cls.map_.iter_path():
            cls.simulator.add_event(time, field.add_content, rival, cls.simulator)
            cls.simulator.add_event(time + 1, field.remove_content)
            time += rival.time
        cls.simulator.add_event(time, field.end, rival)

    @classmethod
    def generate(cls):
        time = cls.simulator.now
        wave = sorted(cls.wave, key=attrgetter('time'))
        for rival in wave:
            print (rival, time)
            cls.map_.add_rival(rival)
            cls.go(time, rival)
            time += 7
        cls.wave = []

    @classmethod
    def set_map(cls, map_):
        cls.map_ = map_

    @classmethod
    def set_game(cls, game):
        cls.game = game
