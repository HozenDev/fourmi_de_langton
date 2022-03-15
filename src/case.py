import pygame
from color import *

class Case:
    def __init__(self, size=(1, 1)):
        self.cur_color = color_dic["white"] # color for the case
        self.w = size[0] # width of the rect of the case
        self.h = size[1] # height of the rect of the case
        
    def set_color(self, color):
        """Set a color in color available list"""
        self.cur_color = self.validate_color(color)

    def validate_color(self, color):
        if len(color) == 3:
            for i in color:
                if i < 0 or i > 255:
                    raise(Exception("Invalide element in color argument"))
        else:
            raise(Exception("Invalide length of color argument"))
        return color
