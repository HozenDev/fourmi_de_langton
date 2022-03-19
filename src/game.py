import pygame
import time
import random

from plateau import Plateau
from fourmi import Fourmi

from button import Button
from input_box import InputBox
from check_box import CheckBox
from menu import Menu

from color import *
from const import *

class Game:
    def __init__(self,
                 size_screen=DEFAULT_SCREEN_SIZE,
                 size_plateau=DEFAULT_PLATEAU_SIZE,
                 res=DEFAULT_RESOLUTION,
                 draw_step=DEFAULT_DRAW_STEP,
                 step_number=DEFAULT_STEP_NUMBER):

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
        
        """Boolean Init"""
        self.end = False # if simulation end
        self.run = False # simulation loop
        self.playing = False

        """Debug Init"""
        self.debug = False
        self.iteration = 0

        """Color list from behavior"""
        self.behavior = ""
        self.color = []
        self.set_behavior("LR")
        
        """Plateau Init"""
        self.plateau = Plateau(self.behavior,
                               self.color,
                               taille=(self.size_plateau[0]//self.res, 
                                       self.size_plateau[1]//self.res),
                               res=(self.res, self.res))
        
        """Fourmi(s) Init"""
        self.nb_fourmi = 0
        self.fourmi_list = []
        
        """Button"""
        self.btn_debug = Button((self.size_screen[0]-260, 20),
                                BUTTON_SIZE,
                                text="Debug",
                                fun=self.active_debug)
        self.btn_play = Button((self.size_screen[0]-260, self.size_plateau[1]-70),
                               BUTTON_SIZE,
                               text="Play",
                               fun=self.play)
        self.btn_stop = Button((self.size_screen[0]-120, self.size_plateau[1]-70),
                               BUTTON_SIZE,
                               text="Stop",
                               fun=self.stop)
        self.btn_reset = Button((self.size_screen[0]-260, 90),
                                BUTTON_SIZE,
                                text="Reset",
                                fun=self.reset)
        self.btn_next = Button((self.size_screen[0]-260, self.size_plateau[1]-140),
                                BUTTON_SIZE,
                                text="Next",
                                fun=self.next_step)
        self.btn_add_f = Button((self.size_screen[0]-260, self.size_plateau[1]-210),
                                BUTTON_SIZE,
                                text="Add",
                                fun=self.add_fourmi)
        
        """InputBox"""
        self.ib_next = InputBox((self.size_screen[0]-120, self.size_plateau[1]-140),
                                BUTTON_SIZE,
                                fun=self.set_next)
        self.ib_behavior = InputBox((self.size_screen[0]-260, 160),
                                    (240, 50),
                                    fun=self.set_behavior,
                                    max_len=10)

        """CheckBox"""

        self.infinite_ant = False
        self.cb_infinite = CheckBox((self.size_screen[0]-260, 230),
                                    (20, 20),
                                    text="Infinite",
                                    fun=self.infinite)
        
        """Menu"""
        self.menu = Menu((size_plateau[0], 0),
                         (size_screen[0]-size_plateau[0], size_screen[1]),
                         btn_list=[self.btn_debug, self.btn_play, self.btn_stop,
                                   self.btn_reset, self.btn_next, self.btn_add_f,
                                   self.ib_next, self.ib_behavior, self.cb_infinite])
        
        """Simulation"""
        self.it = self.play_iter()
        self.next_time = 1
        
    def start(self):
        """Global start, here when ants aren't running"""
        
        self.plateau.reset()
        
        # self.plateau.random_schema() # set the plateau to random
        
        self.plateau.draw()
        self.menu.draw(self.screen)

        for f in self.fourmi_list:
            f.draw()

        while self.start:

            self.menu.enable() # enable all buttons in the menu

            if self.nb_fourmi <= 0:
                self.menu.disable(self.btn_play,
                                  self.btn_next,
                                  self.ib_next,
                                  self.btn_stop,
                                  self.btn_debug)

            if self.nb_fourmi > 0:
                self.menu.disable(self.ib_behavior)
                
            self.handle_event()
            pygame.display.update() # update the screen            
            self.clock.tick(60) # control the max framerate
            
    def stop(self):
        """Stop the game"""
        self.run = False

    def add_fourmi(self):
        """
        Add a ant on the plateau
        """
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
                                           direction=0,
                                           behavior=self.behavior,
                                           color=self.color)
                            self.fourmi_list.append(f_new)
                            self.nb_fourmi += 1
                            f_new.draw()
                        else:
                            print("Can't create an ant here.")
                
        else:
            print("Can't add an ant when simulation is running..")

    def reset(self):
        """
        Reset the game :
        - delete all ants
        - reset plateau
        - turn global number iteration to 0
        """
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
        """Play iteration of step the user give, default:1"""
        try:
            if not self.end and not self.run:
                for _  in range(self.next_time):
                    next(self.it)
        except StopIteration:
            print("Simulation ended")
        except Exception:
            print("Already in function")
            
    def play(self):
        """Play, infinite loop"""
        try:
            if not self.run:
                if not self.end:
                    self.run = True      
                while self.run:
                    next(self.it)
                if self.end :
                    print("Simulation ended.")
        except Exception:
            print("Already playing")
            
    def play_iter(self):
        """Return the game iterator, calls in next and play button"""
        
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
                if self.infinite_ant:
                    f.x = f.x%self.size_plateau[0]
                    f.y = f.y%self.size_plateau[1]
                else:
                    self.run = False
                    self.end = True
        
    def fourmi_step(self):
        for f in self.fourmi_list:
            case = self.plateau.get_case(f.x, f.y, self.res)
            f.one_step(case)
        
    def handle_event(self):

        for event in pygame.event.get():
            self.menu.handle_event(event,
                                   self.btn_debug,
                                   self.btn_play,
                                   self.btn_stop,
                                   self.cb_infinite)
            
            if not self.run:
                self.menu.handle_event(event,
                                       self.btn_next,
                                       self.ib_next,
                                       self.btn_reset,
                                       self.btn_add_f,
                                       self.ib_behavior)
                
            else:
                self.menu.disable(self.btn_next,
                                  self.ib_next,
                                  self.btn_reset,
                                  self.btn_add_f)
                
            if event.type == pygame.QUIT:
                self.run = False
                self.start = False

        self.menu.draw(self.screen)
                
        if self.debug:
            self.debuging()

    def init_color(self, nb):
        color_list = []
        color = []
        color_list.append(color_dic["white"])
        for _ in range(nb-1):
            for _ in range(3):
                color.append(random.randint(0, 255))
            color_list.append(tuple(color.copy()))
            color = [].copy()
        self.color = color_list.copy()

    """Button fonctions"""

    def active_debug(self):
        self.debug = not self.debug

    def debuging(self):
        # print(f"Iteration : {self.iteration}")
        txt_surf = self.btn_debug.font.render(f"{self.iteration}",
                                              True,
                                              color_dic["white"])
        pos = list(self.btn_debug.get_pos())
        size = list(self.btn_debug.get_size())

        text_w = txt_surf.get_width() 
        text_h = txt_surf.get_height()

        pos = (self.size_screen[0]-70-text_w//2,
               20 + size[1]//2 - text_h//2),

        self.screen.blit(txt_surf, pos)    

    def set_next(self, text):
        try:
            self.next_time = int(text)
            print(f"Set next step to {self.next_time}")
        except Exception:
            print("Invalide next value.")
        
    def set_behavior(self, text):
        for letter in text:
            if letter != "R" and letter != "L":
                print("Invalide behavior, must be a text of 'R' and 'L'.")
                return;
        self.behavior = text
        self.init_color(len(text))
        print(f"Set game behavior to {self.behavior}")
        
    def infinite(self):
        self.infinite_ant = not self.infinite_ant
        print(f"Set infinite board to {self.infinite_ant}")
