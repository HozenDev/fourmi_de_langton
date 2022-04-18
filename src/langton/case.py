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
    
    def __init__(self, size=(1, 1)):
        """!@brief Construct Case object
        @param size Pixel size of the case (pygame)
        """
        self.cur_color = color.dic["white"] # color for the case
        self.w = size[0] # width of the rect of the case
        self.h = size[1] # height of the rect of the case
        
    def set_color(self, colour):
        """!@brief Set a color the the Case
        @param colour A tuple of int representing a rgb color
        """
        self.cur_color = self.validate_color(colour)

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
