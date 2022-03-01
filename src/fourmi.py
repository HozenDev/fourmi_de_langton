import pygame
from color import *

class Fourmi :
    def __init__(self, coords=(0, 0), taille=4, speed=1, direction=0):
        """ant coordinates"""
        self.x = int(coords[0]) # current position
        self.y = int(coords[1])
        self.begin_x = int(coords[0]) # save begin position
        self.begin_y = int(coords[1])
        """ant movement"""
        self.speed = speed # ant speed (pixel per movement)
        self.rotation = ['up', 'right', 'down', 'left'] # ant list rotation
        self.nb_direction = len(self.rotation) # length of rotation available
        self.begin_direction = direction%self.nb_direction # save of initial direction
        self.index_direction = self.begin_direction # current index of direction
        self.direction = self.rotation[self.index_direction] #
        """Graphics Init"""
        self.screen = pygame.display.get_surface()
        self.taille = taille
        self.out = False

    def set_out(self):
        self.out = True

    def is_out(self):
        return self.out
        
    def one_step(self, case):
        """One finished move of the ant"""
        self.rotate(case)
        self.inverse_color_case(case)
        self.conduct()

    def reset(self):
        """reset ant"""
        self.index_direction = self.begin_direction
        self.x = self.begin_x
        self.y = self.begin_y
        self.direction = self.rotation[self.index_direction]
        self.draw()
        
    def inverse_color_case(self, case):
        """color relations"""
        if case.color[case.cur_color] == "white":
            case.set_color("black")
        elif case.color[case.cur_color] == "black":
            case.set_color("white")    
        
    def rotate(self, case):
        """rotation ant conduct"""
        if case.color[case.cur_color] == "white":
            self.rotate_left()
        elif case.color[case.cur_color] == "black":
            self.rotate_right()
        
    def conduct(self) :
        """bahavior of the ant"""
        if self.rotation[self.index_direction%self.nb_direction] == 'up' :
            self.move_up()
        elif self.rotation[self.index_direction%self.nb_direction] == 'down' :
            self.move_down()
        elif self.rotation[self.index_direction%self.nb_direction] == 'left' :
            self.move_left()
        elif self.rotation[self.index_direction%self.nb_direction] == 'right' :
            self.move_right()
            
    def move(self, coords=(0, 0)):
        """Vectorial move"""
        self.x += int(coords[0])
        self.y += int(coords[1])

    def move_down(self):
        """Vectorial down move"""
        self.move((0, self.speed))

    def move_up(self):
        """Vectorial up move"""
        self.move((0, -self.speed))
        
    def move_right(self):
        """Vectorail right move"""
        self.move((self.speed, 0))

    def move_left(self):
        """Vectorial left move"""
        self.move((-self.speed, 0))

    def rotate_right(self):
        """Ant rotate in right"""
        self.direction = self.rotation[(self.index_direction+1)%self.nb_direction]
        self.index_direction += 1

    def rotate_left(self):
        """Ant rotate in left"""
        self.direction = self.rotation[(self.index_direction-1)%self.nb_direction]
        self.index_direction -= 1

    def draw(self):
        """Draw the ant"""
        pygame.draw.rect(self.screen, color_dic["red"], pygame.Rect(self.x,
                                                       self.y,
                                                       self.taille,
                                                       self.taille))
        
    def __str__(self):
        """Redefine toString() method"""
        return f"Fourmi a coord: {self.x}, {self.y}" \
            + f" rotation {self.direction}"
