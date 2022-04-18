"""!
@brief langton.fourmi package
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""

import pygame
from utils import color

class Fourmi :
    """!@brief Represent a Fourmi de Langton"""
    
    def __init__(self, coords=(0, 0), taille=4, speed=1, direction=0,
                 color=[(255, 255, 255), (0, 0, 0)], behavior="LR"):
        """!@brief Constuct Fourmi object
        This is the constructor of the Fourmi object.
        @param coords coordinate where ant takes place (default (0, 0))
        @param taille number of pixels represent an ant (default 4)
        @param speed number of case ant moving (default 1)
        @param direction index of first direction (default 0 ("up"))
        @param color list of tuple represent the list of color used for
        behavior (default: (255, ...), (0, ...))
        @param behavior string representation of the ant behavior (default:
        'LR')
        """
        # Ant position #
        self.x = int(coords[0]) # current position
        self.y = int(coords[1])
        self.begin_x = int(coords[0]) # save begin position
        self.begin_y = int(coords[1])
        # Ant movement #
        self.speed = speed # ant speed (pixel per movement)
        self.rotation = ['up', 'right', 'down', 'left'] # ant list rotation
        self.nb_direction = len(self.rotation) # length of rotation available
        self.begin_direction = direction%self.nb_direction #save init direction
        self.index_direction = self.begin_direction #current index of direction
        self.direction = self.rotation[self.index_direction]
        # Graphics attributes #
        self.screen = pygame.display.get_surface()
        self.taille = taille
        self.out = False
        # Ant behavior #
        self.color = color
        self.behavior = behavior

    def set_out(self):
        """!@brief Ant is out
        This method makes the ant out. She can't do anything anymore.
        """
        self.out = True

    def is_out(self):
        """!@brief Ask if fourmi is out
        This method return the out state of the ant.
        @return boolean
        """
        return self.out
        
    def one_step(self, case):
        """!@brief An ant complete movement
        This method make the ant follows a complete movement (rotate, change
        color, move).
        @param case Case where the ant begin its step
        """
        self.rotate(case)
        self.inverse_color_case(case)
        self.conduct()

    def reset(self):
        """!@brief Reset the Ant
        This method hard reset the ant at its beginning direction, position.
        """
        self.index_direction = self.begin_direction
        self.x = self.begin_x
        self.y = self.begin_y
        self.direction = self.rotation[self.index_direction]
        self.draw()
        
    def inverse_color_case(self, case):
        """!@brief Inverse Case color
        This method change the color of the case where the ant is.
        @param case Case where the ant is
        """
        index = self.color.index(case.cur_color)
        case.set_color(self.color[(index+1)%len(self.color)])
        
    def rotate(self, case):
        """!@brief Rotation the ant
        This method rotate the ant following the ant's behavior.
        @param case Case where the ant is.
        """
        index = self.color.index(case.cur_color)
        index_behavior = self.behavior[index]
        if index_behavior == 'L':
            self.rotate_left()
        elif index_behavior == 'R':
            self.rotate_right()
        
    def conduct(self) :
        """!@brief Move the ant following its conduct
        This method moves the ant compare to the conduct wanted. Here the ant
        move in the direction where it watches.
        """
        if self.direction == 'up' :
            self.move_up()
        elif self.direction == 'down' :
            self.move_down()
        elif self.direction == 'left' :
            self.move_left()
        elif self.direction == 'right' :
            self.move_right()
            
    def move(self, coords=(0, 0)):
        """!@brief Vectorial ant movement
        This method reprensent primitive ant movement. It's update the x and y
        of the ant.
        @param coords A tuple represents a movement vector (default (0,0))
        """
        self.x += int(coords[0])
        self.y += int(coords[1])

    def move_down(self):
        """!@brief Ant move down
        This method calls move() with a down vector (0, y).
        """
        self.move((0, self.speed))

    def move_up(self):
        """!@brief Ant move up
        This method calls move() with a up vector (0, -y).
        """
        self.move((0, -self.speed))
        
    def move_right(self):
        """!@brief Ant move right
        This method calls move() with a right vector (x, 0).
        """
        self.move((self.speed, 0))

    def move_left(self):
        """!@brief Ant move left
        This method calls move() with a left vector (-x, 0).
        """
        self.move((-self.speed, 0))

    def rotate_right(self):
        """!@brief Ant rotate left
        This method rotate the ant in its right. It means the index of the
        current rotation is increment by one in the list of rotation.
        """
        self.direction = \
            self.rotation[(self.index_direction+1)%self.nb_direction]
        self.index_direction += 1

    def rotate_left(self):
        """!@brief Ant rotate left
        This method rotate the ant in its left. It means the index of the
        current rotation is decrement by one in the list of rotation.
        """
        self.direction = \
            self.rotation[(self.index_direction-1)%self.nb_direction]
        self.index_direction -= 1

    def draw(self):
        """!@brief Ant draw
        This method draw the ant with pyGame draw.rect function. Ant color is
        red.
        """
        pygame.draw.rect(self.screen, color.dic["red"], pygame.Rect(self.x,
                                                       self.y,
                                                       self.taille,
                                                       self.taille))
        
    def __str__(self):
        """!@brief Ant string representation
        This method redefine the ant's toString() representation
        """
        return f"Fourmi a coord: {self.x}, {self.y}" \
            + f" rotation {self.direction}"
