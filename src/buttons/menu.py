"""!
@brief Menu package
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""

import pygame
from utils import color

class Menu:
    """!@brief Represent a Menu"""

    def __init__(self, pos, size, btn_list=[], color=color.MENU_COLOR):
        """!@brief Construct a Menu
        @param pos A tuple position of top left Menu corner
        @param size A tuple represent the size of Menu (width, height)
        @param btn_list A list of button in the Menu
        @param color The Color of the Menu
        """
        self.rect = pygame.Rect(pos, size)
        self.color = color
        self.btn_list = btn_list

    def draw(self, screen):
        """!@brief Draw the Menu
        @param screen Screen pyGame attributs
        """
        pygame.draw.rect(screen, self.color, self.rect)
        for x in self.btn_list:
            x.draw(screen)
    
    def disable(self, *args):
        """!@brief Disable some button of Menu
        @param args variadic args which need to be disable
        """
        if len(args) == 0:
            args = self.btn_list
        for button in args:
            button.disable()

    def enable(self, *args):
        """!@brief Enable some button of Menu
        @param args variadic args which need to be enable
        """        
        if len(args) == 0:
            args = self.btn_list         
        for button in args:
            button.enable()

    def handle_event(self, event, *args):
        """!@brief Enable some button of Menu
        @param event User event
        @param args variadic args which need to be handled
        """
        if len(args) == 0:
            args = self.btn_list
        for button in args:
            button.handle_event(event)
