from simulation import *
from operator import attrgetter
from math import ceil
from itertools import izip_longest

class Field(object):
    def __init__(self, x, y, sign, map_):
        self.sign = sign
        self.content = None
        self.x = x
        self.y = y
        self.map = map_
        self.observers = []

    def __str__(self):
        if self.content:
            return "%s"%(str(self.content.sign))
        return self.sign

    def add_content(self, content, *simulator):
        if isinstance(content, Rival) and content.dead == True:
            return
        self.content = content
        if len(self.observers)!=0:
            map(lambda x: self.notify(x, simulator[0]), self.observers)

    def remove_content(self):
        self.content = None

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify(self, observer, simulator):
        observer.notify(self, simulator)

    def check_content(self):
        if type(self.content) != type(None):
            raise Exception

    #def end(self, rival):
    #    if rival.dead == False:
    #        self.map.simulator.add_event(self.map.simulator.now, self.map.game.defeat)


class Map(object):
    def __init__(self, game):
        self.width = 44
        self.length = 16
        self.rivals_on_board = []
        self.path_indexes = None
        self.wall_indexes = None
        self.game = game
        self.simulator = None

    def create_path(self): #right order
        self.path_indexes = []
        for y in range(0, self.length, 2):
            if y%4 == 0:
                for x in range(0, self.width):
                    self.path_indexes.append((x, y))
                self.path_indexes.append((self.width , y+1))
            else:
        		for x in reversed(range(0, self.width)):
        		    self.path_indexes.append((x, y))
        		self.path_indexes.append((0, y+1))
        for x in range(0, self.width):
            self.path_indexes.append((x, self.length))
        self.path = [Field(x, y, ".", self) for (x,y) in self.path_indexes]

    def create_wall(self): #right order
        self.wall_indexes = []
        r1 = range(0, self.width - 1)
        r2 = list(reversed(range(1, self.width)))
        for y in range(1, self.length + 1, 2):
            if y in range(1, self.length + 1, 4):
                r = r1
            else: r = r2
            for x in r:
                self.wall_indexes.append((x,y))
        self.wall = [Field(x, y, "#", self) for (x,y) in self.wall_indexes]

    def set_simulator(self, simulator):
        self.simulator = simulator

    def get_field(self, x, y, where): #get an appropriate field from the wall fields
        d = {"path" : self.path, "wall" : self.wall}
        try:
            for field in d[where]:
                if field.y == y and field.x == x:
                    return field
        except ValueError:
            print "This field doesn`t exist."

    def iter_path(self):
	    return iter(self.path)

    def add_rival(self, rival):
        self.rivals_on_board.append(rival)

    def get_rivals(self):
        return self.rivals_on_board

    def delete_rival(self, rival):
        tmp = self.rivals_on_board
        for r in tmp:
            if r == rival:
                self.rivals_on_board.remove(r)
        if not self.rivals_on_board:
            self.simulator.add_event(self.simulator.now, self.game.victory)

    def clear(self):
        for field in self.iter_path():
            field.remove_content()

    def __str__(self):
        result = "  0"
        for j in range(10, int(ceil(self.width)), 10):
            result += " "*8 + str(j)
        result += "   |\n  " + "_" * self.width + "|\n |"
        self.fields = sorted(self.path + self.wall, key=attrgetter('y', 'x'))
        k = 0
        for i in self.fields:
            if self.fields.index(i) % self.width == 0 and self.fields.index(i) != 0:
                result += "|\n"
                if i.y%2!=0:
                    result += str(k) + "|"
                    k+=1
                else:
                    result += " |"
            result += str(i)
        result += "|\n |" + "_" * self.width + "|"
        return result


class Interface(object):
    def __init__(self):
        self.game = None
        self.map = None

    def set_game(self, game):
        self.game = game

    def set_map(self, map_):
        self.map = map_

    def bp(self): #building phase
        data_credits = self.game.credits
        data_towers = self.game.towers
        data_nextwave = RivalWave.wave
        data = []
        data.append("$: " + str(data_credits))
        data.append("Waves remining: ")
        data.append("~" * 15)
        data.extend([i.name + ": (" + str(i.parameters[0]) + ", " + str((i.parameters[1] - 1) / 2) + ")" for i in data_towers])
        data.append("~" * 15)
        data.append("Next wave: lives | credits")
        data.extend([i.name + ":\t" + str(i.score) + " | " + str(i.credits) for i in data_nextwave])
        return data

    def sim(self): #simulation
        data = []
        data.append("Active units: ")
        data.extend([r.name + ": " + str(r.score) for r in self.map.rivals_on_board])
        return data

    def show(self, phase, *arg):
        d = {"bp": self.bp, "sim": self.sim}
        lines = str(self.map).split('\n')
        data = d[phase](*arg)
        zipped = (pair for pair in izip_longest(lines,data))
        result = "\n".join(["{} {}".format(*[" " if x is None else x for x in i]) for i in zipped])
        print result + "\n"
