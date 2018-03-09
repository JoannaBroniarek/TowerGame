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
        elif len(args) > 0 and args[0] not in map_.rivals_on_board and isinstance(args[0], Rival):
            pass
        else:
            event(*args)

    def execute_all(self, map_, interface):
        if not self.queue:
            raise RuntimeError
        while True:
            time.sleep(0.01)
            sys.stdout.flush()
            self.execute(map_)
            interface.show(map_, "sim")
