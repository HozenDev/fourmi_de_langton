"""!
@brief first program to be execute
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""

import pygame

from langton import Simulation

if __name__ == '__main__' :

    pygame.init()

    simulation = Simulation(res=4)

    simulation.start()
    
    pygame.quit()
