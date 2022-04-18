"""!
@brief langton.plateau
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""
import pygame
import random
import numpy as np

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
        self.w = taille[0] # width of plateau
        self.h = taille[1] # height of plateau)
        self.schema = [[Case((res[0], res[1])) # schema of plateau
                        for j in range(self.w)]
                       for i in range(self.h)]
        # SCREEN #
        self.screen = pygame.display.get_surface()
        # BEHAVIOR #
        self.behavior = behavior
        self.color = color
        
    def random_schema(self):
        """!@brief Random color schema"""
        for line in self.schema:
            for i in line:
                r = random.choice(self.color)
                i.set_color(r)
        self.draw()
                
    def reset(self):
        """!@brief default color schema"""        
        for line in self.schema:
            for i in line:
                i.set_color(color.dic["white"])
        self.draw()

    def draw_case(self, pos):
        x, y = pos
        pygame.draw.rect(
            self.screen,
            self.schema[x][y].cur_color,
            pygame.Rect(y*self.schema[x][y].w,
                        x*self.schema[x][y].h,
                        self.schema[x][y].w,
                        self.schema[x][y].h))        
        
    def draw_ant(self, pos):
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

            for i in range(start[1], end[1]):
                for j in range(start[0], end[0]):
                    self.draw_case((i, j))

    def get_case(self, x, y, res):
        """!@brief Get a Case in a position
        @param x Horizontal position of the Case
        @param y Vertical position of the Case
        @param res Resolution of the Case
        """
        case = self.schema[y//res][x//res]
        return case

    def set_behavior(self, color, behavior):
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
