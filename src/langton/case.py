"""!
@brief langton.case package
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""

import pygame
from utils import color

class Case:
    """!@brief Represent a Case"""
    
    def __init__(self, size=(1, 1), pos=(0, 0)):
        """!@brief Construct Case object
        @param size Pixel size of the case (pygame)
        @param pos Position of the case
        """
        self.screen = pygame.display.get_surface()
        self.cur_color = color.dic["white"]
        self.w, self.h = size
        self.x, self.y = pos
        
    def set_color(self, colour):
        """!@brief Set a color the the Case
        @param colour A tuple of int representing a rgb color
        """
        self.cur_color = self.validate_color(colour)

    def get_color(self):
        """!@brief get the Case color
        @return the Case color
        """
        return self.cur_color

    def validate_color(self, colour):
        """!@brief Verify if it's a valid colour
        @param colour A tuple of int representing a rgb colour
        @return The valide colour
        @exception Exception Not a valid colour
        """
        if len(colour) == 3:
            for i in colour:
                if i < 0 or i > 255:
                    raise(Exception("Invalide element in colour argument"))
        else:
            raise(Exception("Invalide length of colour argument"))
        return colour

    def draw(self):
        """!@brief draw the Case"""
        pygame.draw.rect(
            self.screen,
            self.get_color(),
            pygame.Rect(self.x*self.w,
                        self.y*self.h,
                        self.w,
                        self.h))
