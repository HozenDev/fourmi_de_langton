"""!
@brief langton.plateau
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""
import pygame
import random
import numpy as np
import time
from multiprocessing import Process, Manager
from multiprocessing import cpu_count

from utils import color

from langton import Case

class Plateau :
    """!@brief Represent a Plateau"""

    def __init__(self, behavior, color, taille=(1, 1), res=(4, 4)):
        """!@brief Construct Plateau object
        @param behavior String representation of the Plateau behavior
        @param color A tuple a int reprensent a rgb color
        @param taille tuple represent number of Case (default (1, 1))
        @param res Pixel representation of each Case (default (4, 4))
        """
        self.w, self.h = taille
        self.schema = [[Case(res, (j, i))
                        for j in range(self.w)]
                       for i in range(self.h)]
        # SCREEN #
        self.screen = pygame.display.get_surface()
        # BEHAVIOR #
        self.behavior = behavior
        self.color = color
        # MULTIPROCESSING #
        self.cpu = cpu_count()
        self.ratio = int(self.w/self.cpu)
        self.intervalles = [([i*self.ratio, 0],
                             [(i+1)*self.ratio, self.h])
                            for i in range(self.cpu-1)]
        self.intervalles.append(([self.ratio*(self.cpu-1), 0],
                                 [self.w, self.h]))

    def multiprocessing(self, fun):
        """!@brief create a multiprocess
        @param fun function reference which call in process
        """
        process = [Process(target=fun,
                           args=self.intervalles[i])
                   for i in range(self.cpu)]
        for x in process: x.start()
        for x in process: x.join()

    def draw_mp(self):
        """!@brief draw multiprocessing
        """
        self.multiprocessing(self.draw)

    def reset(self, start=[0, 0], end=[None, None]):
        """!@brief reset schema in white
        @param start list of int index where start to draw (default (0, 0))
        @param end list of int index where end to draw (default (None, None))
        """
        start, end = self.valide_intervalle(start, end)
        for i in range(start[1], end[1]):
            for j in range(start[0], end[0]):
                self.set_color_case((i, j), color.dic["white"])
        self.draw_mp()
        
    def random(self, start=[0, 0], end=[None, None]):
        """!@brief random color schema
        @param start list of int index where start to draw (default (0, 0))
        @param end list of int index where end to draw (default (None, None))
        """
        start, end = self.valide_intervalle(start, end)
        for i in range(start[1], end[1]):
            for j in range(start[0], end[0]):
                r = random.choice(self.color)
                self.set_color_case((i, j), r)
        self.draw_mp()
            
    def set_color_case(self, pos, colour):
        """!@brief set color in a Case
        @param pos tuple of position of the Case
        @param colour colour to set in the Case
        """
        x, y = pos
        self.schema[x][y].set_color(colour)
    
    def draw_case(self, pos):
        """!@brief draw a case in specific schema position
        @param pos tuple of position of the Case
        """
        x, y = pos
        self.schema[x][y].draw()

    def valide_intervalle(self, start, end):
        """!@brief valide start & end in schema
        @param start list of int index where start to draw (default (0, 0))
        @param end list of int index where end to draw (default (None, None))
        @return a valid couple of start & end (valid index)
        """
        if end[0] == None:      # if end_x not setting in draw()
            end[0] = self.w
        if end[1] == None:      # if end_y not setting  in draw()
            end[1] = self.h
        else :
            if start[0] < 0:
                start[0] = start[0]%self.w
            if start[1] < 0:
                start[1] = start[1]%self.h
            if end[0] > self.w:
                end[0] = end[0]%self.w
            if end[1] > self.h:
                end[1] = end[1]%self.h
        return start, end
        
    def draw_ant(self, pos):
        """!@brief draw optimize cases near ant
        @param pos postion of the ant
        """
        y, x = pos
        self.draw_case((x, y))
        self.draw_case((x, (y+1)%self.w))
        self.draw_case((x, (y-1)%self.w))
        self.draw_case(((x+1)%self.h, y))
        self.draw_case(((x-1)%self.h, y))
        
    def draw(self, start=[0,0], end=[None, None]):
        """!@brief default color schema
        @param start list of int index where start to draw (default (0, 0))
        @param end list of int index where end to draw (default (None, None))
        """
        start, end = self.valide_intervalle(start, end)
        for i in range(start[1], end[1]):
            for j in range(start[0], end[0]):
                # self.draw_case((i, j))
                self.schema[i][j].draw()
                
    def get_case(self, x, y, res):
        """!@brief Get a Case in a position
        @param x Horizontal position of the Case
        @param y Vertical position of the Case
        @param res Resolution of the Case
        """
        case = self.schema[y//res][x//res]
        return case

    def set_behavior(self, color, behavior):
        """!@brief Modify grid color & behavior
        @param color list of color
        @param behavior string of the simulation behavior
        """
        self.color = color
        self.behavior = behavior
    
    def __str__(self):
        """!@brief Redefine toString() Plateau method"""
        s = ""
        for i in self.schema:
            for j in i:
                s += f"{j.cur_color} "
            s += f"\n"
        return s
