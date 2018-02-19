from mapp import *
from towers import *
from rivals import *
from simulation import *
import sys
import time

class Cykl(object):
  game_active = True
  counter = 0
  loops = 5   #number of simulations
  @classmethod
  def execute(cls, map_):
      while cls.game_active == True and cls.loops >= 0:
          BP.start()
          n = raw_input("\n\n T, Q or B ?: ")
          if n == "Q":
              cls.game_active = False
              print "The end"
          elif n == "T":
              if cls.counter == 0:
                  RivalWave.create(map_)
                  inter.show(mapa,"bp")
                  cls.counter += 1
              BP.set_tower(map_)
              inter.show(mapa,"bp")
          elif n == "B":
              simulator = Simulator()
              simulator.start()
              RivalWave.generate(simulator, map_)
              inter.show(map_, "sim")
              try:
                  simulator.execute_all(map_)
                  inter.show(map_, "sim")
              except Defeat:
                  Cykl.game_active = False
                  inter.show(map_, "sim")
                  print "\n Game over \n"
              except Victory:
                  print "\n You won the battle !!! \n"
              cls.loops -= 1
              cls.counter = 0
          else:
              print "Wrong command"

if __name__ == '__main__':
    print '\n' * 10
    print ("Welcome to the Tower Game\n\n" +
           "To make a play, hit enter\n\n" +
           "Have fun ;)\n\n")
    raw_input(".... (hit enter) ...")

    mapa = Map()
    mapa.create_path()
    mapa.create_wall()
    inter = Interface()
    BP = BuildingPhase()
    Cykl()
    Cykl.execute(mapa)




    '''
    while game_active == True:
        n = raw_input("\n\n T, Q or B ?: ")
        if n == "Q":
            game_active = False
            print "The end"
        elif n == "T":      #BUILDING PHASE
            BP.start()
            BP.set_tower(mapa)
            inter.show(mapa,"bp", player)
        elif n == "B":
            simulator = Simulator(200)
            RivalWave.generate(simulator, mapa)
            inter.show(mapa, "sim")
            simulator.execute_all()
            inter.show(mapa, "sim")
        else:
            print "Wrong command"

    '''





'''Simulation: (Fighting phase)

#time.sleep(0.001) # jak szybko wyswietlane sa zmiany
#sys.stdout.flush() #nic nie zapamietuje, wszystko wyswietla

sim = Simulator(400) #560 obejscie sciezki - uogolnij to gdyby rozmiary sie zmienily
# SYMULATION of walking for a test rival "P"
t = sim.now
lastfield = None
for field in mapa.iter_path():
    sim.add_event(t, field.add_content, p)
    if lastfield is not None:
        sim.add_event(t, lastfield.remove_content)
    lastfield = field
    t+=1
sim.add_event(t, lastfield.remove_content)
# why I cannot remove a few fields? - it depends on how many steps I have
# jak dodaje zawartosc do pola nastepnego to musze usuwac z poprzedniego
sim.execute_all()
'''
