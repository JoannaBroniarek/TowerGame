from mapp import *
from towers import *
from rivals import *
from simulation import *
import sys
import time

if __name__ == '__main__':
    print '\n' * 10
    print ("Welome to Tower Game\n\n" +
           "To make a play, type the relevent number and hit enter\n\n" +
           "Have fun ;)\n\n")
    raw_input(".... (hit enter) ...")

    game_active = True
    player = Player()
    mapa = Map()
    mapa.create_path()
    mapa.create_wall()
    i = Interface()
    i.show(mapa, player)

    while game_active == True:
        n = raw_input("\n\n T, Q or B ?: ")
        if n == "Q":
            game_active = False
            print "The end"
        elif n == "T":
            #BUILDING PHASE
            BF = BuildingPhase()
            BF.start()
            BF.set_tower(mapa)
            i.show(mapa, player)
        elif n == "B":
            break



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
