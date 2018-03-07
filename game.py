from mapp import *
from towers import *
from rivals import *
from simulation import *
import sys
import time

class WrongValueError(Exception):
    pass

class BuildingPhase(object):
    game = None

    @classmethod
    def set_game(cls, game):
        cls.game = game

    @staticmethod
    def take_input(map_):
        towertype  = raw_input("Please, choose a type of tower: ")
        if towertype not in ["F", "A", "R", "M"]:
            raise WrongValueError
        column = int(raw_input("The column number: "))
        if column not in range(map_.width):
            raise WrongValueError
        row = int(raw_input("The row number: "))
        if row not in range(int(map_.length / 2)):
            raise WrongValueError
        return (towertype, column, row)

    @classmethod
    def set_tower(cls, map_):
        print " F - Fortress (o), A - Alkazar (o), R - ArcherTower (f), M - MagicTower (f)"
        print " [o - overground, f - flying] \n"
        correct = False
        while not correct:
            try:
                p = cls.take_input(map_)
                correct = True
            except WrongValueError:
                print "Wrong Value"
        scaledrow = p[2]*2 + 1
        column = p[1]
        towertype = p[0]
        field = map_.get_field(column, scaledrow, "wall")
        try:
            tower = TowerFactory.create(towertype, column, scaledrow, map_)
            field.check_content()
            field.add_content(tower)
            game.delete_credits(tower.value)
            tower.observe_fields()
            game.add_tower(tower)
        except Exception as e:
            print "\n\n\n You cannot build here! \n\n\n"

    @classmethod
    def start(cls):
        print "\nThis is a Building Phase. You can build your towers on the map.\n"


class Game(object):
    def __init__(self):
        self.credits = 50
        self.towers = []

    @staticmethod
    def help():
        print "\n Towers: \n"
        print "F - Fortress:\n -- kills mainly flying rivals\n -- the special effect 'shrapnels' gives a chance to kill flying rivals"
        print "A - Alkazar:\n -- kills only flying rivals\n -- there is no special effect"
        print "R - ArcherTower:\n -- kills only overland rivals\n -- the special effect 'poisonous arrows'"
        print "M - MagicTower:\n -- kills only overland rivals\n -- the special effect 'poleaxing'"
        print "\n Rivals: \n"
        print " -- flying: Paratrooper, Dragon"
        print " -- overland: Knight, Viking, Speeder"

    def set(self):
        mapa = Map()
        mapa.create_path()
        mapa.create_wall()
        inter = Interface()
        inter.set_game(self)
        BP = BuildingPhase()
        BP.set_game(self)
        Cykl()
        Cykl.execute(mapa, inter, BP)

    def add_credits(self, value):
        self.credits += value

    def delete_credits(self, value):
        tmp = self.credits - value
        if tmp < 0:
            raise Exception("\n\nYou do not have enought credits!!\nYou can start a battle. \n\n")
        else:
            self.credits -= value

    def add_tower(self, tower):
        self.towers.append(tower)


class Cykl(object):
    game_active = True
    counter = 0
    loops = 5   #number of simulations
    @classmethod
    def execute(cls, map_, inter, BP):
        Game.help()
        while cls.game_active == True and cls.loops >= 0:
            if cls.counter == 0 :
                simulator = Simulator()
                RivalWave.set_map(map_)
                RivalWave.simulator = simulator
                RivalWave.create()
                inter.show(map_, "bp")
                cls.counter += 1
            BP.start()
            print "\n\t T -> Build a Tower\tB -> Start a Battle\tQ -> Quit.\n"
            n = raw_input("\n\n T, Q or B ?: ")
            print
            if n == "Q":
                cls.game_active = False
                print "The end"
            elif n == "T":
                BP.set_tower(map_)
                inter.show(map_, "bp")
            elif n == "B":
                simulator.start()
                RivalWave.generate()
                inter.show(map_, "sim")
                info = "Hmmmm"
                try:
                    simulator.execute_all(map_, inter)
                except Defeat:
                    Cykl.game_active = False
                    inter.show(map_, "sim")
                    info = "\n Game over \n"
                except Victory:
                    info = "\n You won the battle !!! \n"
                finally:
                    cls.loops -= 1
                    cls.counter = 0
                    inter.show(map_, "sim")
                    map_.clear()
                    inter.show(map_, "sim")
                    print info


if __name__ == '__main__':
    print '\n' * 10
    print ("Welcome to the Tower Game\n\n" +
           "To make a play, hit enter\n\n" +
           "Have fun ;)\n\n")
    raw_input(".... (hit enter) ...")
    game = Game()
    game.set()
