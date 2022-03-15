import pygame
from color import *
from button import Button

class Menu:

    def __init__(self, pos, size, btn_list=[], color=MENU_COLOR):
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.btn_list = btn_list

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for x in self.btn_list:
            x.draw(screen)
    
    def disable(self, *args):
        if len(args) == 0:
            args = self.btn_list
        for button in args:
            button.disable()

    def enable(self, *args):
        if len(args) == 0:
            args = self.btn_list         
        for button in args:
            button.enable()

    def handle_event(self, event, *args):
        if len(args) == 0:
            args = self.btn_list
        for button in args:
            button.handle_event(event)
