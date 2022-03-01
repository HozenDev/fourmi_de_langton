import pygame
from color import *
from button import Button

class InputBox(Button):
    def __init__(self, pos, size, text='', fun=None):
        super().__init__(pos, size, text=text, fun=fun)
        """Rect"""
        self.int_rect = pygame.Rect(pos[0]+5, pos[1]+5, size[0]-10, size[1]-10)
        """Colors"""
        self.color = INACTIVE_IB_COLOR
        self.inactive_color = INACTIVE_IB_COLOR
        self.active_color = ACTIVE_IB_COLOR
        self.disable_color = DISABLE_IB_COLOR
        self.int_color = color_dic["white"]
        self.text_color = TEXT_IB_COLOR
        
    def handle_event(self, event):
        """Text input and pressed reference"""
        if self.b_disable:
            return;
        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.active_color if self.active else self.inactive_color
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.fun(self.text)
                    self.text = ''
                    self.active = False
                    self.color = self.inactive_color
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 5:
                        self.text += event.unicode
                    else:
                        print("Maximum of char : 5")
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
            print("Mettez a jour PyGame")
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
