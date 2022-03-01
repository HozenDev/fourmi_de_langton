import pygame
from color import *
from button import Button

class Menu:

    def __init__(self, pos, size, btn_list=[]):
        self.rect = pygame.Rect(pos, size)
        self.color = MENU_COLOR
        self.btn_list = btn_list

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for x in self.btn_list:
            x.draw(screen)
        
