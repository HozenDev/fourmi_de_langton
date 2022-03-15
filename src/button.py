import pygame
from color import *

class Button:
    def __init__(self, pos, size, text='', fun=None):
        """Rect"""
        self.rect = pygame.Rect(pos, size) # rect collison button
        """Colors"""
        self.inactive_color = INACTIVE_BUTTON_COLOR # when button inactive
        self.active_color = ACTIVE_BUTTON_COLOR # when button is clicked on 
        self.disable_color = DISABLE_BUTTON_COLOR
        # self.disable_color = DISABLE_BUTTON_COLOR # when button disabled
        self.color = INACTIVE_BUTTON_COLOR # current color
        self.text_color = TEXT_BUTTON_COLOR # text inside color
        self.hover_color = HOVER_BUTTON_COLOR # when mouse on the button
        """Text inside"""
        self.text = text # string text
        self.font = pygame.font.Font(None, 32) # font of the text
        self.txt_surf = self.font.render(text, True, self.text_color) # surface txt
        """State"""
        self.active = False # if button is active
        self.b_disable = False
        """Fonction Pointer"""
        self.fun = fun # fonction reference
        """Style"""
        self.border_radius = 4 # round corners of the button

    def enable(self):
        if self.b_disable:
            self.b_disable = False
            self.color = self.inactive_color
        
    def disable(self):
        """Disable the button"""
        if not self.b_disable:
            self.b_disable = True
            self.color = self.disable_color # disable color
            
    def draw(self, screen):
        """Draw surface rectangle and text inside the button"""
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
                    (self.rect.x+self.rect.w/2-text_w/2, self.rect.y+self.rect.h/2-text_h/2))

    def handle_event(self, event):
        """Handle event : down, up, motion (hover)"""
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
        """return the top left position of the button rect"""
        return (self.rect.x, self.rect.y)

    def get_size(self):
        """return the size of the button rect"""
        return (self.rect.w, self.rect.h)
