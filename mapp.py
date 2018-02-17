# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 11:26:59 2018

@author: Asia
"""
from faza_natarcia import *
from operator import attrgetter


class Field(object):
    def __init__(self, x, y, sign, map_):
        self.sign = sign
        self.content = None #obiekt wiezy lub ludzika ktory ma trybut sign = "X"
        self.x = x
        self.y = y
        self.map = map_

    def __str__(self):
        if self.content:
            return "%s"%(str(self.content.sign))
        return self.sign
        #return "("+str(self.x)+","+str(self.y)+")"

    def add_content(self, content):
        self.content = content

    def remove_content(self):
        self.content = None

class Map(object):
    def __init__(self):
        self.width = 44
        self.length = 16
        '''
        self.path_fields = [Field(x, y, ".", self) \
                           for x in range(0,self.width) \
                           for y in range(0, self.length + 1, 2)] \
                           + [Field(0, y, ".", self) \
                           for y in range(3, self.length, 4)] \
                           + [Field(self.width, y, ".", self) \
                           for y in range(1, self.length, 4)]
        self.wall_fields = [Field(x, y, "#", self) \
                       for x in range(1, self.width - 1) \
                       for y in range(1, self.length + 1, 2)] \
                       + [Field(self.width, y, "#", self) \
                       for y in range(3, self.length + 1, 4)] \
                       + [Field(0, y, "#", self) \
                       for y in range(1, self.length + 1, 4)] \
        '''
        self.rivals_on_board = []


    def create_path(self): # w odpowiedniej kolejnosci
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

    def create_wall(self): # w odpowiedniej kolejnosci
        self.wall_indexes = []
        r1 = range(1, self.width)
        r2 = list(reversed(range(0, self.width - 1)))
        for y in range(1, self.length + 1, 2):
            if y in range(1, self.length + 1, 4):
                r = r1
            else: r = r2
            for x in r:
                self.wall_indexes.append((x,y))
        self.wall = [Field(x, y, "#", self) for (x,y) in self.wall_indexes]

    def get_wall_field(self, x, y): #get an appropriate field from the wall fields
        try:
            for field in self.wall:
                if field.y == y and field.x == x:
                    return field
        except ValueError:
            print "This field doesn`t exist."

    def iter_path(self):
	    return iter(self.path)

    def get_rivals(self):
        return self.rivals_on_board

    def delete_rival(self, rival):
        #self.rivals_on_board[]
        pass

    def __str__(self):
        result = "_" * self.width + "\n"
        self.fields = sorted(self.path + self.wall, key=attrgetter('y', 'x'))
        for i in self.fields:
            if self.fields.index(i) % self.width == 0 and self.fields.index(i) != 0:
                result += "|\n"
                result += "|"
            result += str(i)
        result += "|\n" + "_" * self.width + "|\n"
        return result
