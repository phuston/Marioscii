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

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

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
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])

win = pygcurse.PygcurseWindow(WINWIDTH, WINHEIGHT, fullscreen=False)
pygame.display.set_caption('Pygcurse Dodger')
win.autoupdate = False

class MariosciiModel():
    """ Represents game state of Marioscii game """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mario = Mario(15,20)
        self.level = Level(level1)
        self.audio_sample = AudioSampler(3000)
        self.motion_track = Motion_Tracker()

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.mario.update(delta_t)

class MariosciiView():
    def __init__(self, model, width, height):
        """ Initialize view for Marioscii """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # this is used for figuring out where to draw stuff
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        self.model.mario.draw(self.screen)
        self.model.level.draw(self.screen)
        pygame.display.update()


class Marioscii():
    """ The main Marioscii class """

    def __init__(self):
        self.model = MariosciiModel(800, 600)
        self.view = MariosciiView(self.model, 800, 600)
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

        pygame.sprite.Sprite.__init__(self)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 0
        self.vel_y = 0

        self.image = pygame.Surface([20,20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect.move(self.pos_x, self.pos_y))

    def update(self, delta_t):
        """ update mario due to passage of time """
        self.pos_x += self.vel_x*delta_t
        self.pos_y += self.vel_y*delta_t

    def go_left(self):
        self.vel_x = -60

    def go_right(self): 
        self.vel_x = 60

    def jump(self):
        self.y_vel = -20

    def stop(self):
        self.vel_x = 0
        self.vel_y = 0

class Level(pygame.sprite.Sprite):
    def __init__(self, map):
        pygame.sprite.Sprite.__init__(self)
        self.map = map

        self.tile = pygame.Surface([50,50])
        self.tile.fill(BLACK)

    def draw(self, screen):
        for row in xrange(len(self.map)):
            for x in range(len(self.map[row])):
                if self.map[row][x] == 1:
                    screen.blit(self.tile, (x*50, row*50))

class Tile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,50])
        self.image.fill(BLACK)



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
                if event.key == pygame.K_LEFT:
                    self.model.mario.go_left()
                if event.key == pygame.K_RIGHT:
                    self.model.mario.go_right()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and mario.vel_x < 0:
                    self.model.mario.stop()
                if event.key == pygame.K_RIGHT and mario.vel_x > 0:
                    self.model.mario.stop()


        # Audio event processing
        if self.model.audio_sample.is_above_trigger():
            self.model.mario.go_right()
        else:
            self.model.mario.go_left()

        # Motion event processing
        x_mov, y_mov = self.model.motion_track.get_movement() 

pygame.init()

if __name__ == '__main__':
    marioscii = Marioscii()
    marioscii.run()