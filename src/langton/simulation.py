"""!
@brief Simulation package
@author Durel Enzo
@author Mallepeyre Nourrane
@version 1.0
"""

import pygame
import time
import random

import langton as lgt
from buttons import Button, Menu, CheckBox, InputBox
from utils import color, const

class Simulation:
    """!@brief Represent a Simulation"""

    def __init__(self,
                 size_screen=const.DEFAULT_SCREEN_SIZE,
                 size_plateau=const.DEFAULT_PLATEAU_SIZE,
                 res=const.DEFAULT_RESOLUTION):
        """!@brief Construct Simulation object
        @param size_screen Size of the window
        @param size_plateau Size of the grid where stand ants
        @param res Number of pixel define size of Case and Fourmi
        """
        self.size_screen = size_screen # size of the screen
        self.size_plateau = size_plateau # size of the plateau
        self.res = res # resolution of a case / fourmi

        # PYGAME #
        self.screen = pygame.display.set_mode(size_screen, pygame.DOUBLEBUF)
        pygame.display.set_caption("Fourmi de Langton") # title set
        self.clock = pygame.time.Clock() # clock to control the framerate
        
        # STATES #
        self.end = False # if simulation end
        self.run = False # simulation loop

        # DEBUG #
        self.debug = False
        self.iteration = 0

        # BEHAVIOR #
        self.behavior = ""
        self.color = []

        # PLATEAU INIT #
        self.plateau = lgt.Plateau(self.behavior,
                                   self.color,
                                   taille=(self.size_plateau[0]//self.res, 
                                           self.size_plateau[1]//self.res),
                                   res=(self.res, self.res))

        self.set_behavior("LR")
        
        # Fourmi(s) Init #
        self.nb_fourmi = 0
        self.fourmi_list = []
        
        # Button #
        self.btn_debug = Button((self.size_screen[0]-260, 20),
                                const.BUTTON_SIZE,
                                text="Debug",
                                fun=self.active_debug)
        self.btn_play = Button((self.size_screen[0]-260,
                                self.size_plateau[1]-70),
                               const.BUTTON_SIZE,
                               text="Play",
                               fun=self.play)
        self.btn_stop = Button((self.size_screen[0]-120,
                                self.size_plateau[1]-70),
                               const.BUTTON_SIZE,
                               text="Stop",
                               fun=self.stop)
        self.btn_reset = Button((self.size_screen[0]-260, 90),
                                const.BUTTON_SIZE,
                                text="Reset",
                                fun=self.reset)
        self.btn_next = Button((self.size_screen[0]-260,
                                self.size_plateau[1]-140),
                                const.BUTTON_SIZE,
                                text="Next",
                                fun=self.next_step)
        self.btn_add_f = Button((self.size_screen[0]-260,
                                 self.size_plateau[1]-210),
                                const.BUTTON_SIZE,
                                text="Add",
                                fun=self.add_fourmi)
        
        # InputBox #
        self.ib_next = InputBox((self.size_screen[0]-120,
                                 self.size_plateau[1]-140),
                                const.BUTTON_SIZE,
                                fun=self.set_next)
        self.ib_behavior = InputBox((self.size_screen[0]-260, 160),
                                    (240, 50),
                                    fun=self.set_behavior,
                                    max_len=10)

        # CheckBox #
        self.cb_infinite = CheckBox((self.size_screen[0]-260, 230),
                                    (20, 20),
                                    text="Infinite",
                                    fun=self.infinite)
        self.cb_random_grid = CheckBox((self.size_screen[0]-260, 270),
                                       (20, 20),
                                       text="Random Grid",
                                       fun=self.set_random_grid)
        self.infinite_ant = False
        self.random_grid = False

        # Menu #
        self.menu = Menu((size_plateau[0], 0),
                         (size_screen[0]-size_plateau[0], size_screen[1]),
                         btn_list=[self.btn_debug, self.btn_play,
                                   self.btn_stop, self.btn_reset,
                                   self.btn_next, self.btn_add_f,
                                   self.ib_next, self.ib_behavior,
                                   self.cb_infinite, self.cb_random_grid])
        
        # Simulation #
        self.it = self.__iter__()
        self.next_time = 1
        
    def start(self):
        """!@brief Global start, here when ants aren't running"""
        
        self.plateau.reset()
        self.menu.draw(self.screen)

        # self.plateau.compare_fun(self.plateau.draw, self.plateau.draw_mp)
        
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
            self.clock.tick(30) # control the max framerate
            
    def stop(self):
        """!@brief Stop the game by set self.run to false"""
        self.run = False

    def add_fourmi(self):
        """!@brief Add an ant on the grid"""
        if not self.run :
            not_click = True
            while not_click:
                self.clock.tick(30) # control the max framerate                
                for event in pygame.event.get():            
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        not_click = False
                        if event.pos[0] >= 0 \
                           and event.pos[0] < self.size_plateau[0] \
                           and event.pos[1] >= 0 \
                           and event.pos[1] < self.size_plateau[1] :
                            e_x, e_y = event.pos
                            f_x = (e_x//self.res)*self.res
                            f_y = (e_y//self.res)*self.res
                            f_new = lgt.Fourmi(coords=(f_x, f_y),
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
        """!@brief Reset the simulation"""
        if not self.run :
            if self.random_grid:
                self.plateau.random()
            else :
                self.plateau.reset()
                
            self.fourmi_list = [].copy()
            self.nb_fourmi = 0
            
            self.iteration = 0
            self.end = False
            self.menu.draw(self.screen)
        else :
            print("Can't reset when simulation is running")

    def next_step(self):
        """!@brief Play simulation iterator next_number times, (default 1)
        @exception StopIteration If Simulation ended
        @exception Exception If Simulation already run
        """
        try:
            if not self.end and not self.run:
                for _  in range(self.next_time):
                    next(self.it)
        except StopIteration:
            print("Simulation ended")
        except Exception:
            print("Already in function")
            
    def play(self):
        """!@brief Play Simulation loop"""
        try:
            if not self.run:
                if not self.end:
                    self.run = True      
                while self.run:
                    next(self.it)
                if self.end :
                    print("Simulation ended.")
        except Exception:
            raise(Exception)
            print("Already playing")
            
    def __iter__(self):
        """!@brief Simulation iterator"""
        
        while True:

            self.iteration += 1
            self.handle_event()
            
            self.fourmi_step()
            self.fourmi_out()            
            self.draw()
            
            pygame.display.update() # update the screen
            # self.clock.tick(60) # control the max framerate
            yield;

    def draw(self):
        """!@brief Draw the map and ants"""
        for f in self.fourmi_list:
            if not self.end:
                self.plateau.draw_ant((f.x//self.res, f.y//self.res))
                f.draw()
            
    def fourmi_out(self):
        """!@brief Check if an ant is out of index of the grid"""
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
        """!@brief Move all ants once"""
        for f in self.fourmi_list:
            case = self.plateau.get_case(f.x, f.y, self.res)
            f.one_step(case)
        
    def handle_event(self):
        """!@brief Event listener user interactions: Button & Keyboard"""

        for event in pygame.event.get():
            self.menu.handle_event(event,
                                   self.btn_debug,
                                   self.btn_play,
                                   self.btn_stop,
                                   self.cb_infinite,
                                   self.cb_random_grid)
            
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

    def init_color(self):
        """!@brief Init random color from simulation behavior"""
        color_list = []
        color_tuple = []
        color_list.append(color.dic["white"])
        for _ in range(len(self.behavior)-1):
            for _ in range(3):
                color_tuple.append(random.randint(0, 255))
            color_list.append(tuple(color_tuple.copy()))
            color_tuple = [].copy()
        self.color = color_list.copy()

    def active_debug(self):
        """!@brief Change boolean value for debug option button"""
        self.debug = not self.debug

    def debuging(self):
        """!@brief Print the total of iteration since the simulation is
        running"""
        # print(f"Iteration : {self.iteration}")
        txt_surf = self.btn_debug.font.render(f"{self.iteration}",
                                              True,
                                              color.dic["white"])
        pos = list(self.btn_debug.get_pos())
        size = list(self.btn_debug.get_size())

        text_w = txt_surf.get_width() 
        text_h = txt_surf.get_height()

        pos = (self.size_screen[0]-70-text_w//2,
               20 + size[1]//2 - text_h//2),

        self.screen.blit(txt_surf, pos)    

    def set_next(self, text):
        """!@brief Set the step for next function"""
        try:
            self.next_time = int(text)
            print(f"Set next step to {self.next_time}")
        except Exception:
            print("Invalide next value.")
        
    def set_behavior(self, text):
        """!@brief Set the behavior before add ants and game start"""
        for letter in text:
            if letter != "R" and letter != "L":
                print("Invalide behavior, must be a text of 'R' and 'L'.")
                return;
        self.behavior = text
        self.init_color()
        self.plateau.set_behavior(self.color, self.behavior)
        print(f"Set simulation behavior to {self.behavior}")
        
    def infinite(self):
        """!@brief Define if ants are in an infinite place"""
        self.infinite_ant = not self.infinite_ant
        if self.infinite_ant and self.end :
            self.end = False
            for f in self.fourmi_list:
                f.x %= self.size_plateau[0]
                f.y %= self.size_plateau[1]
        print(f"Set infinite board to {self.infinite_ant}")

    def set_random_grid(self):
        """!@brief Random Grid CheckBox function"""
        self.random_grid = not self.random_grid
        print(f"Set random grid to {self.random_grid}")
