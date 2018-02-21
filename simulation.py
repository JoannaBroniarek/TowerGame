from heapq import heappop, heappush
from rivals import *
import time
import sys

class Defeat(Exception):
    pass

class Victory(Exception):
    pass

class Simulator(object):
    def __init__(self):
        self.now = 0
        self.queue = []
        #self.steps = steps

    def start(self):
        print "\n Simulation of the battle... \n\n"

    def add_event(self, time, method, *args):
        heappush(self.queue, (time, method, args))

    def execute(self, map_):
        self.now, event, args = heappop(self.queue)
        if not map_.rivals_on_board :
            raise Victory()
        elif not self.queue:
            raise Defeat()
        else:
            event(*args)

    def execute_all(self, map_, interface):
        if not self.queue:
            raise RuntimeError() #albo bez nawiasow
        while True: #It should last as long as any event is in the queue
            time.sleep(0.01)
            sys.stdout.flush()
            self.execute(map_)
            interface.show(map_, "sim")
