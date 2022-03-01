import pygame
from case import Case
import random
from color import *

class Plateau :
    def __init__(self, taille=(1, 1), res=(32, 32)):
        self.w = taille[0] # width of plateau
        self.h = taille[1] # height of plateau
        self.schema = [[Case((res[0], res[1])) # schema of plateau
                        for j in range(self.w)]
                       for i in range(self.h)]
        """Init graphics"""
        self.screen = pygame.display.get_surface()
        
    def random_schema(self):
        for line in self.schema:
            for i in line:
                r = random.choice(i.color)
                i.set_color(r)

    def blank_schema(self):
        self.reset()
                
    def reset(self):
        for line in self.schema:
            for i in line:
                i.set_color('white')
        self.draw()
        
    def draw(self, start=[0,0], end=[None, None]):
        if end[0] == None:      # if end_x not setting in draw()
            end[0] = self.w
        if end[1] == None:      # if end_y not setting  in draw()
            end[1] = self.h
        else :
            """Handle plateau borders"""
            if start[0] < 0:
                start[0] = 0
            if start[1] < 0:
                start[1] = 0
            if end[0] > self.w:
                end[0] = self.w
            if end[1] > self.h:
                end[1] = self.h

            """Draw loops"""
            for i in range(start[1], end[1]):
                for j in range(start[0], end[0]):
                    """Draw the rectangle of a case"""
                    pygame.draw.rect(
                        self.screen,
                        color_dic[self.schema[i][j].color[self.schema[i][j].cur_color]],
                        pygame.Rect(j*self.schema[i][j].w,
                                    i*self.schema[i][j].h,
                                    self.schema[i][j].w,
                                    self.schema[i][j].h))

    def get_case(self, x, y, res):
        """Get the case in specifics coordinates"""
        case = self.schema[y//res][x//res]
        return case
        
    def __str__(self):
        """redefine toString() method"""
        s = ""
        for i in self.schema:
            for j in i:
                s += f"{j.color[j.cur_color]} "
            s += f"\n"
        return s
