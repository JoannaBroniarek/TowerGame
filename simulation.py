from heapq import heappop, heappush
from rivals import *

class WaveGenerator(object):
    def generate(self):
        wave = RivalWave.create
        for rival in range(len(wave)):
            yield rival

class Simulator(object):
    def __init__(self, steps):
        self.now = 0
        self.queue = []
        self.steps = steps

    def add_event(self, time, method, *args):
        heappush(self.queue, (self.now + time, method, args))
        #self.queue.append((time, method, args))

    def execute(self):
        self.now, event, args = heappop(self.queue)
        event(*args)

    def execute_all(self):
        if not self.queue:
            raise RuntimeError() #albo bez nawiasow
        for i in range(self.steps): #It should last as long as any event is in the queue
            time.sleep(0.001)
            self.execute()


#kolejne wydarzenia to dodawanie i usuwanie zawartosci kolejnych pol na mapie



'''
class Simulator(object):
    """Simulation environment"""

    def __init__(self):
        self.now = 0
        self.queue = []
        self.processes = []
        self.steps = 1000

    def reset(self):
        self.now = 0
        self.queue = []
        for p in self.processes:
            p.reset()
            p.activate()

    def schedule(self, delay, event):
        heappush(self.queue, (self.now + delay, event))

    def peek(self):
        return self.queue[0][0]

    def _step(self):
        self.now, event = heappop(self.queue)
        event()

    def step(self):
        if not self.queue:
            raise RuntimeError('no generators defined')
        self._step()

    def run(self):
        if not self.queue:
            raise RuntimeError('no generators defined')
        while self.now < self.steps:
            self._step()
'''
