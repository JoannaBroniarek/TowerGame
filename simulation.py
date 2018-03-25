from heapq import heappop, heappush
from rivals import *
import sys

class Simulator(object):
    def __init__(self):
        self.now = 0
        self.queue = []

    def start(self):
        print "\n Simulation of the battle... \n\n"

    def add_event(self, time, method, *args):
        heappush(self.queue, (time, method, args))

    def execute(self):
        self.now, event, args = heappop(self.queue)
        event(*args)

    def execute_all(self, interface):
        while True:
            #sys.stdout.flush()
            self.execute()
            interface.show("sim")
