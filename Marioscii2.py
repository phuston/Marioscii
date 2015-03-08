"""
Created on Sun Mar 2 11:37 2015
@author: Patrick Huston
@author: Bill Wong
"""

import pygame
import random
from AudioSampler import AudioSampler
# from Motion_Tracker import Motion_Tracker
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
                   (0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                   (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])

# win = pygcurse.PygcurseWindow(WINWIDTH, WINHEIGHT, fullscreen=False)
# pygame.display.set_caption('Pygcurse Dodger')
# win.autoupdate = False

class MariosciiModel():
    """ Represents game state of Marioscii game """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mario = Mario(20,20)
        self.tiles = pygame.sprite.Group()
        self.level = Level(level1)
        # self.motion_track = Motion_Tracker()
        self.audio_sample = AudioSampler(10000)

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
        self.clock = pygame.time.Clock()

    def run(self):
        last_ticks = 0.0

        while True:
            t = pygame.time.get_ticks()
            # delta time in seconds.
            dt = (t - last_ticks) / 1000.0
            last_ticks = t

            self.controller.process_events()
            self.model.update(dt)
            self.view.draw()

            self.clock.tick(50)


class Mario(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        """ Initialize a mario at the specified position
            pos_x, pos_y """

        pygame.sprite.Sprite.__init__(self)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 0
        self.vel_y = 0
        self.acc_x = 0
        self.acc_y = 400

        self.image = pygame.Surface([20,20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = [0, 0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        """ update mario due to passage of time """

        self.vel_x += self.acc_x*dt
        self.vel_y += self.acc_y*dt
        self.rect.x += self.vel_x*dt
        self.rect.y += self.vel_y*dt

    def go_left(self):
        self.vel_x = -100

    def go_right(self): 
        self.vel_x = 100

    def jump(self):
        self.vel_y = -300

    def stop(self):
        self.vel_x = 0

class Level(pygame.sprite.Sprite):
    def __init__(self, map):
        pygame.sprite.Sprite.__init__(self)
        self.map = map
        self.tiles = pygame.sprite.Group()

        for row in xrange(len(self.map)):
            for x in range(len(self.map[row])):
                if self.map[row][x] == 1:
                    tile = Tile(x*50, row*50)
                    self.tiles.add(tile)

    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.image = pygame.Surface([50,50])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x_pos, self.y_pos)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class PygameController():
    def __init__(self, model):
        self.model = model

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
                if event.key == pygame.K_SPACE:
                    self.model.mario.jump()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.model.mario.vel_x < 0:
                    self.model.mario.stop()
                if event.key == pygame.K_RIGHT and self.model.mario.vel_x > 0:
                    self.model.mario.stop()

        # tile_hit_list = pygame.sprite.spritecollide(self.model.mario, self.model.level.tiles, False)
        # # print "Tile hit list", tile_hit_list
        # for tile in tile_hit_list:
        #     # If we are moving right,
        #     # set our right side to the left side of the item we hit
        #     if self.model.mario.vel_x > 0:
        #         self.model.mario.rect.right = tile.rect.left
        #     elif self.model.mario.vel_x < 0:
        #         # Otherwise if we are moving left, do the opposite.
        #         self.model.mario.rect.left = tile.rect.right

        # Check and see if we hit anything
        tile_hit_list = pygame.sprite.spritecollide(self.model.mario, self.model.level.tiles, False)
        for tile in tile_hit_list:

            if self.model.mario.vel_y > 0:
                self.model.mario.rect.bottom = tile.rect.top
            elif self.model.mario.vel_y < 0:
                # Otherwise if we are moving left, do the opposite.
                self.model.mario.rect.top = tile.rect.bottom
            # Stop our vertical movement
            self.model.mario.vel_y = 0

        # Audio event processing
        if self.model.audio_sample.is_above_trigger():
            self.model.mario.jump()

        # # Motion event processing
        # x_mov = self.model.motion_track.get_movement() 

pygame.init()

if __name__ == '__main__':
    marioscii = Marioscii()
    marioscii.run()