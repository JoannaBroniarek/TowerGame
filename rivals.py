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
            self.map.player.add_credits(self.credits)

    def have_effect(self, tower): #special effect in case of being shot
        pass

    def go(self, simulator, t):
        lastfield = None
        for field in self.map.iter_path():
            simulator.add_event(t, field.add_content, self)
            if lastfield is not None:
                simulator.add_event(t, lastfield.remove_content)
            lastfield = field
            t += self.time
        simulator.add_event(t, lastfield.remove_content)


class Paratrooper(Rival):
    def __init__(self, map_):
        self.name = "Paratrooper"
        self.sign = "P"
        self.score = 7
        self.time = 3
        self.airly = True
        self.credits = 10
        self.map = map_

class Knight(Rival):
    def __init__(self, map_):
        self.name = "Knight"
        self.sign = "K"
        self.score = 9
        self.time = 3
        self.airly = False
        self.credits = 12
        self.map = map_

class Viking(Rival):
    def __init__(self, map_):
        self.name = "Viking"
        self.sign = "V"
        self.score = 6
        self.time = 5
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
        self.score = 8
        self.time = 1
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
    wave =[]
    #counter = 0

    @classmethod
    def create(cls, map_): #algorithm of the rival wave creating
        if cls.counter < 2:
            for i in range(1, randint(2,3)):
                cls.wave.append(RivalFactory.create(choice(cls.airly + cls.groundbased), map_))
        elif cls.counter == 2 or cls.counter == 3:
            cls.wave.append(RivalFactory.create(choice(cls.airly), map_))
            for i in range(3, randint(3, 5)):
                cls.wave.append(RivalFactory.create(choice(cls.groundbased), map_))
        else:
            for i in range(2, randint(3, 6)):
                cls.wave.append(RivalFactory.create(choice(cls.airly), map_))
                cls.wave.append(RivalFactory.create(choice(cls.groundbased), map_))
        #cls.counter+=1

    @classmethod
    def generate(cls, simulator, map_):
        time = simulator.now
        '''
        if cls.counter == 0:
            cls.create(map_)
            cls.counter += 1
        '''
        wave = sorted(cls.wave, key=attrgetter('time'))
        for rival in wave:
            map_.add_rival(rival)
            rival.go(simulator, time)
            time += 1
        cls.wave = []
        cls.create(map_) #the next wave
