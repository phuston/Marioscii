"""
Created on Sun Mar 2 11:37 2015
@author: Patrick Huston
@author: Bill Wong
"""

import pygame
import random
from AudioSampler import AudioSampler
from Motion_Tracker import Motion_Tracker
import numpy as np
import time
import pygcurse
import sys

# Screen dimensions
SCREEN_WIDTH  = 80
SCREEN_HEIGHT = 50

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)

level1 = np.array([(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])



class MariosciiModel():
    """ Represents game state of Marioscii game """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mario = Mario(1,5)
        self.level = Level(level1)
        self.audio_sample = AudioSampler(3000)

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.mario.update(delta_t)

class MariosciiView():
    def __init__(self, model, width, height):
        """ Initialize view for Marioscii """
        pygame.init()
        self.screen = pygcurse.PygcurseWindow(SCREEN_WIDTH, SCREEN_HEIGHT, fullscreen=False)
        pygame.display.set_caption('Pygcurse Marioscii')
        self.screen.autoupdate = False

        # this is used for figuring out where to draw stuff
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill(bgcolor=BLACK)
        self.model.mario.draw(self.screen)
        self.model.level.draw(self.screen)
        self.screen.update()


class Marioscii():
    """ The main Marioscii class """

    def __init__(self):
        self.model = MariosciiModel(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view = MariosciiView(self.model, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.controller = PygameController(self.model)

    def run(self):
        last_update = time.time()
        while True:
            self.view.draw()
            self.controller.process_events()
            delta_t = time.time() - last_update
            self.model.update(delta_t)
            last_update = time.time()


class Mario(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        """ Initialize a mario at the specified position
            pos_x, pos_y """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 0
        self.vel_y = 0

    def draw(self, screen):
        screen.putchar('@', int(self.pos_x), int(self.pos_y), RED)

    def update(self, delta_t):
        """ update mario due to passage of time """
        self.pos_x += self.vel_x*delta_t
        self.pos_y += self.vel_y*delta_t

    def go_left(self):
        self.vel_x = -20

    def go_right(self): 
        self.vel_x = 20

    def jump(self):
        self.y_vel = -20

    def stop(self):
        self.vel_x = 0
        self.vel_y = 0

class Level(pygame.sprite.Sprite):
    def __init__(self, map):
        pygame.sprite.Sprite.__init__(self)
        self.map = map

    def draw(self, screen):
        for row in xrange(len(self.map)):
            for x in range(len(self.map[row])):
                if self.map[row][x] == 1:
                    screen.putchar('#',x,row)

class PygameController():
    def __init__(self, model):
        self.model = model
        self.space_pressed = False

    def process_events(self):
        pygame.event.pump
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LEFT:
                    self.model.mario.go_left()
                if event.key == pygame.K_RIGHT:
                    self.model.mario.go_right()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.model.mario.vel_x < 0:
                    self.model.mario.stop()
                if event.key == pygame.K_RIGHT and self.model.mario.vel_x > 0:
                    self.model.mario.stop()

pygame.init()

if __name__ == '__main__':
    marioscii = Marioscii()
    marioscii.run()