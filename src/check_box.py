import pygame
import time

from color import *
from button import Button

class CheckBox(Button):
    def __init__(self, pos, size, text='', fun=None):
        super().__init__(pos, size, text=text, fun=fun)
        """Rect"""
        # self.check_rect = pygame.Rect(pos[0], pos[1], 20, 20)
        """Font resizing"""
        self.font = pygame.font.Font(None, size[1])
        self.txt_surf = self.font.render(text, True, self.text_color) # surface txt        
        """Colors"""
        self.color = INACTIVE_CB_COLOR
        self.inactive_color = INACTIVE_CB_COLOR
        self.active_color = ACTIVE_CB_COLOR
        self.disable_color = DISABLE_CB_COLOR
        self.disable_active_color = DISABLE_ACTIVE_CB_COLOR
        self.text_color = TEXT_IB_COLOR
        """Time"""
        self.delay = 1_000_000 # en ns
        self.active_time = time.time_ns()

    def disable(self):
        """Disable the button"""
        if not self.b_disable:
            self.b_disable = True
            if self.active:
                self.color = self.disable_active_color
            else:
                self.color = self.disable_color
        
    def handle_event(self, event):
        if self.b_disable:
            return;
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):

                self.active = not self.active
                self.color = self.active_color if self.active else self.inactive_color

                if self.fun is not None:
                    self.fun()
                else:
                    print("CheckBox has no function.")

    def draw(self, screen):
        try:
            pygame.draw.rect(screen,
                             self.color,
                             self.rect,
                             border_radius=self.border_radius)
        except Exception:
            print("You need to update PyGame.")
            pygame.draw.rect(screen,
                             self.color,
                             self.rect)
        text_h = self.txt_surf.get_height()
        screen.blit(self.txt_surf,
                    (self.rect.x+self.rect.w+10, self.rect.y+self.rect.h/2-text_h/2))
