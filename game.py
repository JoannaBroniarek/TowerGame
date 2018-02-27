from mapp import *
from towers import *
from rivals import *
from simulation import *
import sys
import time

# co gdzie sie znajduje i jakie importy
# czyszczenie mapy ze wszystkich przeciwnikow po bitwie
"""
for field in mapa.iter_path:
    field.remove_content()
"""
# usun nieporzebne fragmenty kodu
# ustaw rozne zasiegi
# nie moga byc dwie wieze na jednym polu
#cos jest nie tak z numeracja pol na mapie

class Instruction(object):
    @staticmethod
    def help():
        print "\nF - Fortress:\n -- kills mainly flying rivals\n -- the special effect 'shrapnels' gives a chance to kill flying rivals"
        print "A - Alkazar:\n -- kills only flying rivals\n -- there is no special effect"
        print "R - ArcherTower:\n -- kills only overland rivals\n -- the special effect 'poisonous arrows'"
        print "M - MagicTower:\n -- kills only overland rivals\n -- the special effect 'poleaxing'"

class Cykl(object):
    game_active = True
    counter = 0
    loops = 5   #number of simulations
    @classmethod
    def execute(cls, map_, inter, BP):
        Instruction.help()
        while cls.game_active == True and cls.loops >= 0:
            BP.start()
            print "\n\t T -> Build a Tower\tB -> Start a Battle\tQ -> Quit.\n"
            n = raw_input("\n\n T, Q or B ?: ")
            print
            if n == "Q":
                cls.game_active = False
                print "The end"
            elif n == "T":
                if cls.counter == 0 :
                    simulator = Simulator()
                    RivalWave.simulator = simulator
                    RivalWave.create(map_)
                    inter.show(map_, "bp") ####
                    cls.counter += 1
                BP.set_tower(map_)
                inter.show(map_, "bp") ####
            elif n == "B":
                simulator.start()
                RivalWave.generate(map_)
                #RivalWave.create(map_)#the next wave
                inter.show(map_, "sim")
                try:
                    simulator.execute_all(map_, inter)
                    inter.show(map_, "sim")
                except Defeat:
                    Cykl.game_active = False
                    inter.show(map_, "sim")
                    print "\n Game over \n"
                except Victory:
                    print "\n You won the battle !!! \n"
                finally:
                    cls.loops -= 1
                    cls.counter = 0
                    rest = [e for e in simulator.queue if e[0] == simulator.now and e[0] == simulator.now + 1 ]
                    print rest
                    for r in rest:
                        if "remove_content" in str(r[1]):
                            r[1]()
                    map_.clear()
                    inter.show(map_, "sim")


class InitialElements(object):
    @staticmethod
    def set():
        mapa = Map()
        mapa.create_path()
        mapa.create_wall()
        inter = Interface()
        BP = BuildingPhase()
        Cykl()
        Cykl.execute(mapa, inter, BP)

if __name__ == '__main__':
    print '\n' * 10
    print ("Welcome to the Tower Game\n\n" +
           "To make a play, hit enter\n\n" +
           "Have fun ;)\n\n")
    raw_input(".... (hit enter) ...")
    InitialElements.set()
