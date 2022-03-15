import pygame
from game import Game

if __name__ == '__main__' :

    pygame.init()

    game = Game(
        # size_screen=(1000, 720),
        # size_plateau=(720, 720),
        res=6,
        draw_step=1)

    game.start()
    
    pygame.quit()
