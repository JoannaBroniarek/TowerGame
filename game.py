from towers import *
from mapp import *
from rivals import *
from simulation import *
import sys
import time
'''
if __name__ == '__main__':
    print '\n' * 10
    print ("Welome to Tower Game\n\n" +
           "To make a play, type the relevent number and hit enter\n\n" +
           "Have fun ;)\n\n")
    raw_input(".... (hit enter) ...")
'''
# create and show an empty map
mapa = Map()
mapa.create_path()
mapa.create_wall()
print mapa

'''
#BUILDING PHASE
print "This is a Building Phase. You can build your towers on the map"
tower  = raw_input("Please, choose a type of tower: ")
column = raw_input("The column number: ")
row = raw_input("The row number: ")
'''
for i in dir(BuildingPhase):
    print(i)



#A=BuildingPhase()
#a.start
#BuildingPhase.set_tower(mapa)


t = TowerFactory.create("F", 3, 4, mapa)
p = RivalFactory.create("paratrooper", mapa)


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
