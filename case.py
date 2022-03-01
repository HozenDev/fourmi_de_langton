import pygame

class Case:
    def __init__(self, size=(1, 1)):
        self.color = ['white', 'black'] # color available
        self.cur_color = self.color.index('white') # color for the case
        self.w = size[0] # width of the rect of the case
        self.h = size[1] # height of the rect of the case
        
    def set_color(self, color):
        """Set a color in color available list"""
        try :
            self.cur_color = self.color.index(color)
        except Exception:
            print("Error in color indexage in case")
            raise
