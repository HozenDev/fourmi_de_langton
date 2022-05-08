"""!
@brief InputBox package
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""

import pygame
from utils import color

from buttons import Button

class InputBox(Button):
    """!@brief Represent an InputBox"""

    def __init__(self, pos, size, text='', fun=None, max_len=5):
        super().__init__(pos, size, text=text, fun=fun)
        # RECT #
        self.int_rect = pygame.Rect(pos[0]+5, pos[1]+5, size[0]-10, size[1]-10)
        # COLORS #
        self.color = color.INACTIVE_IB_COLOR
        self.inactive_color = color.INACTIVE_IB_COLOR
        self.active_color = color.ACTIVE_IB_COLOR
        self.disable_color = color.DISABLE_IB_COLOR
        self.int_color = color.dic["white"]
        self.text_color = color.TEXT_IB_COLOR
        # TEXT #
        self.max_len = max_len
        
    def handle_event(self, event):
        if self.b_disable:
            return;
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color= self.active_color if self.active else self.inactive_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if self.fun is not None:
                        self.fun(self.text)
                    else:
                        print("Button has no function.")
                    self.text = ''
                    self.active = False
                    self.color = self.inactive_color
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                if len(self.text) > self.max_len:
                    self.txt_surf = self.font.render("-" + self.text[len(self.text)-self.max_len+1:],
                                                     True,
                                                     self.text_color)
                else:
                    self.txt_surf = self.font.render(self.text, True, self.text_color)

    def draw(self, screen):
        try:            
            pygame.draw.rect(screen,
                             self.color,
                             self.rect,
                             border_radius=self.border_radius) 
            pygame.draw.rect(screen,
                             self.int_color,
                             self.int_rect,
                             border_radius=self.border_radius)
        except Exception:
            print("You need to update PyGame.")
            pygame.draw.rect(screen,
                             self.color,
                             self.rect) 
            pygame.draw.rect(screen,
                             self.int_color,
                             self.int_rect)
        text_w = self.txt_surf.get_width()
        text_h = self.txt_surf.get_height()               
        screen.blit(self.txt_surf,
                    (self.rect.x+self.rect.w/2-text_w/2, self.rect.y+self.rect.h/2-text_h/2))
