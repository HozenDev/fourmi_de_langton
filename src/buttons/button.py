"""!
@brief Button package
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""

import pygame
from utils import color

class Button:
    """!@brief Represent a Button"""
    
    def __init__(self, pos, size, text='', fun=None):
        """!@brief Construct Button object
        @param pos A tuple position of top left button corner
        @param size A tuple represent the size of button (width, height)
        @param text String affiliate to the button
        @param fun Function reference for button event
        """
        # RECTANGLE #
        self.rect = pygame.Rect(pos, size) # rect collison button
        # COLORS #
        self.inactive_color = color.INACTIVE_BUTTON_COLOR # when button inactive
        self.active_color = color.ACTIVE_BUTTON_COLOR # when button is clicked on 
        self.disable_color = color.DISABLE_BUTTON_COLOR
        # self.disable_color = DISABLE_BUTTON_COLOR # when button disabled
        self.color = color.INACTIVE_BUTTON_COLOR # current color
        self.text_color = color.TEXT_BUTTON_COLOR # text inside color
        self.hover_color = color.HOVER_BUTTON_COLOR # when mouse on the button
        # TEXT #
        self.text = text # string text
        self.font = pygame.font.Font(None, 32) # font of the text
        self.txt_surf = self.font.render(text, True, self.text_color) # surface txt
        # STATE #
        self.active = False # if button is active
        self.b_disable = False
        # FUNCTION #
        self.fun = fun # fonction reference
        # STYLE #
        self.border_radius = 4 # round corners of the button

    def enable(self):
        """!@brief Enable the button
        This method enable the button (the user can click on it).
        """
        if self.b_disable:
            self.b_disable = False
            self.color = self.inactive_color
        
    def disable(self):
        """!@brief Disable the button
        This method disable the button (the user can't click on it).
        """
        if not self.b_disable:
            self.b_disable = True
            self.color = self.disable_color # disable color
            
    def draw(self, screen):
        """!@brief Draw the button
        This method draw the button rectangle with pyGame draw.rect function
        and the text with screen.blit function.
        @param screen Pygame screen object where the button with be draw
        @exception Exception Used if pyGame is under update
        """
        try:
            pygame.draw.rect(screen,
                             self.color,
                             self.rect,
                             border_radius=self.border_radius)
        except Exception:
            print("Mettez a jour PyGame")
            pygame.draw.rect(screen,
                             self.color,
                             self.rect)
        text_w = self.txt_surf.get_width()
        text_h = self.txt_surf.get_height()
        screen.blit(self.txt_surf,
                    (self.rect.x+self.rect.w/2-text_w/2,
                     self.rect.y+self.rect.h/2-text_h/2))

    def handle_event(self, event):
        """!@brief User input method
        This method operate users input with event.type pyGame attributs

        @param event Event user input
        """
        if self.b_disable:
            return;
        if event.type == pygame.MOUSEBUTTONDOWN:
            """mouse click down"""
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.color = self.active_color
                if self.fun is not None:
                    self.fun()
        elif event.type == pygame.MOUSEBUTTONUP:
            """mouse click up"""
            self.active = False
            if self.rect.collidepoint(event.pos):
                self.color = self.hover_color
            else :
                self.color = self.inactive_color
        elif event.type == pygame.MOUSEMOTION:
            """mouse hover"""
            if self.rect.collidepoint(event.pos):
                if self.active:
                    self.color = self.active_color
                else:
                    self.color = self.hover_color
            else:
                self.color = self.inactive_color
        
    def get_pos(self):
        """!@brief Get the button top left position
        @return A tuple of the position (x, y)
        """
        return (self.rect.x, self.rect.y)

    def get_size(self):
        """!@brief Get the button size
        @return A tuple of the size (w, h)
        """
        return (self.rect.w, self.rect.h)
