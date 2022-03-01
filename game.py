import pygame
import time
from plateau import Plateau
from fourmi import Fourmi
from button import Button
from menu import Menu
from color import *
from input_box import InputBox

class Game:
    def __init__(self, size_screen=(640, 480), size_plateau=(480, 480), res=4,
                 draw_step=1, step_number=None):

        """Ratio Init"""
        self.draw_step = draw_step # draw the plateau for every draw_step
        self.size_screen = size_screen # size of the screen
        self.size_plateau = size_plateau # size of the plateau
        self.res = res # resolution of a case / fourmi
        self.step_number = step_number # max step in a game

        """Pygame Attribut Init"""
        self.screen = pygame.display.set_mode(size_screen, pygame.DOUBLEBUF) # screen set
        pygame.display.set_caption("Fourmi de Langton") # title set
        self.clock = pygame.time.Clock() # clock to control the framerate
        self.multiprocessing = (self.draw_step > 10)
        
        """Boolean Init"""
        self.end = False # if simulation end
        self.run = False # simulation loop
        self.playing = False

        """Debug Init"""
        self.debug = False
        self.iteration = 0
        
        """Plateau Init"""
        self.plateau = Plateau(taille=(self.size_plateau[0]//self.res, 
                                       self.size_plateau[1]//self.res),
                               res=(self.res, self.res))
        
        """Fourmi(s) Init"""
        self.nb_fourmi = 0
        self.fourmi_list = []
        
        """Button"""
        self.btn_debug = Button((self.size_screen[0]-260, 20),
                                (100, 50),
                                text="Debug",
                                fun=self.active_debug)
        self.btn_play = Button((self.size_screen[0]-260, self.size_plateau[1]-70),
                               (100, 50),
                               text="Play",
                               fun=self.play)
        self.btn_stop = Button((self.size_screen[0]-120, self.size_plateau[1]-70),
                               (100, 50),
                               text="Stop",
                               fun=self.stop)
        self.btn_reset = Button((self.size_screen[0]-260, 90),
                                (100, 50),
                                text="Reset",
                                fun=self.reset)
        self.btn_next = Button((self.size_screen[0]-260, self.size_plateau[1]-140),
                                (100, 50),
                                text="Next",
                                fun=self.next_step)

        self.btn_add_f = Button((self.size_screen[0]-260, self.size_plateau[1]-210),
                                (100, 50),
                                text="Add",
                                fun=self.add_fourmi)
        
        """InputBox"""
        self.ib_next = InputBox((self.size_screen[0]-120, self.size_plateau[1]-140),
                                (100, 50),
                                fun=self.set_next)
                                
        """Menu"""
        self.menu = Menu((size_plateau[0], 0),
                         (size_screen[0]-size_plateau[0], size_screen[1]),
                         btn_list=[self.btn_debug, self.btn_play, self.btn_stop,
                                   self.btn_reset, self.btn_next, self.btn_add_f,
                                   self.ib_next])
        
        """Simulation"""
        self.it = self.play_iter()
        self.next_time = 1
        
        
    def start(self):
        """Start"""
        
        self.plateau.reset()
        
        # self.plateau.random_schema()
        
        self.plateau.draw()
        self.menu.draw(self.screen)

        for f in self.fourmi_list:
            f.draw()

        while self.start:

            self.btn_play.enable()
            self.btn_stop.enable()
            self.btn_debug.enable()
            self.btn_next.enable()
            self.btn_reset.enable()
            self.ib_next.enable()
            self.btn_add_f.enable()

            if self.nb_fourmi <= 0:
                self.btn_play.disable()
                self.btn_next.disable()
                self.ib_next.disable()
                self.btn_stop.disable()
                self.btn_debug.disable()

            self.handle_event()
            pygame.display.update() # update the screen            
            self.clock.tick(30) # control the max framerate
            
    def stop(self):
        self.run = False

    def add_fourmi(self):
        if not self.run :
            not_click = True
            while not_click:
                self.clock.tick(30) # control the max framerate                
                for event in pygame.event.get():            
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        not_click = False
                        if event.pos[0] >= 0 and event.pos[0] < self.size_plateau[0] \
                           and event.pos[1] >= 0 and event.pos[1] < self.size_plateau[1] :
                            e_x, e_y = event.pos
                            f_x = (e_x//self.res)*self.res
                            f_y = (e_y//self.res)*self.res
                            f_new = Fourmi(coords=(f_x, f_y),
                                           taille=self.res,
                                           speed=self.res,
                                           direction=0)
                            self.fourmi_list.append(f_new)
                            self.nb_fourmi += 1
                            f_new.draw()
                        else:
                            print("fourmi non créée")
                
        else:
            print("Vous ne pouvez pas ajouter de fourmi quand la simulation est active.")

    def reset(self):
        if not self.run :
            self.plateau.reset()

            self.fourmi_list = [].copy()
            self.nb_fourmi = 0

            for f in self.fourmi_list:
                f.reset()
            
            self.iteration = 0
            self.end = False
            self.menu.draw(self.screen)
        else :
            print("Can't reset when simulation is running")

    def next_step(self):
        try:
            if not self.end and not self.run:
                for _  in range(self.next_time):
                    next(self.it)
        except StopIteration:
            print("Simulation ended")
        except Exception:
            print("Already in function")
            
    def play(self):
        try:
            if not self.run:
                if not self.end:
                    self.run = True      
                while self.run:
                    next(self.it)
                if self.end :
                    print("Fin de la simulation")
        except Exception:
            print("Already playing")
            
    def play_iter(self):
        """Game run"""
        
        while self.step_number == None or self.iteration <= self.step_number:

            self.iteration += 1
            self.handle_event()
                
            self.fourmi_step()
            self.fourmi_out()
            self.draw()

            if self.step_number != None and self.iteration >= self.step_number:
                self.end = True
                self.run = True
                
            pygame.display.update() # update the screen
            # self.clock.tick(60) # control the max framerate
            yield;

    def draw(self):
        for f in self.fourmi_list:
            if not self.end and self.iteration % self.draw_step == 0:
                self.plateau.draw(start=[f.x//self.res - self.draw_step,
                                         f.y//self.res - self.draw_step],
                                  end=[f.x//self.res + self.draw_step + 1,
                                       f.y//self.res + self.draw_step + 1])
                f.draw()        
            
    def fourmi_out(self):
        for f in self.fourmi_list:
            if f.x == self.size_plateau[0] \
               or f.y == self.size_plateau[1] \
               or f.x < 0 or f.y < 0:
                self.run = False
                self.end = True
        
    def fourmi_step(self):
        for f in self.fourmi_list:
            case = self.plateau.get_case(f.x, f.y, self.res)
            f.one_step(case)
        
    def handle_event(self):

        for event in pygame.event.get():
            self.btn_debug.handle_event(event)
            self.btn_play.handle_event(event)
            self.btn_stop.handle_event(event)
            if not self.run:
                self.btn_next.handle_event(event)
                self.ib_next.handle_event(event)
                self.btn_reset.handle_event(event)
                self.btn_add_f.handle_event(event)                
            else:
                self.btn_next.disable()
                self.ib_next.disable()
                self.btn_reset.disable()
                self.btn_add_f.disable()
                
            if event.type == pygame.QUIT:
                self.run = False
                self.start = False

        self.menu.draw(self.screen)
                
        if self.debug:
            self.debuging()

    def set_next(self, text):
        try:
            self.next_time = int(text)
        except Exception:
            print("Invalide range of Next")
            
    def active_debug(self):
        self.debug = not self.debug

    def debuging(self):
        # print(f"Iteration : {self.iteration}")
        txt_surf = self.btn_debug.font.render(f"{self.iteration}", True, color_dic["white"])
        pos = list(self.btn_debug.get_pos())
        size = list(self.btn_debug.get_size())
        text_w = txt_surf.get_width() 
        text_h = txt_surf.get_height()
        pos[0], pos[1] = self.size_screen[0]-70-text_w//2, 20 + size[1]//2 - text_h//2
        self.screen.blit(txt_surf, pos)
