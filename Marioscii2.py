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
from pygame.locals import *

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)

# Events
NEXTLEVEL = pygame.USEREVENT + 1
QUIT = pygame.USEREVENT + 2

level1 = np.array([(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0),
                   (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0),
                   (0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
                   (0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
                   (0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0),
                   (0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 2),
                   (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])

# win = pygcurse.PygcurseWindow(WINWIDTH, WINHEIGHT, fullscreen=False)
# pygame.display.set_caption('Pygcurse Dodger')
# win.autoupdate = False

class MariosciiModel():
    """ Represents game state of Marioscii game """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = pygame.sprite.Group()
        self.level = Level(level1)
        self.mario = Mario(20,20,self.level.tiles)
        self.motion_track = Motion_Tracker()
        self.audio_sample = AudioSampler(15000)

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
        done = False

        while not done:
            t = pygame.time.get_ticks()
            # delta time in seconds.
            dt = (t - last_ticks) / 1000.0
            last_ticks = t

            done = self.controller.process_events()
            self.model.update(dt)
            self.view.draw()

            self.clock.tick(25)


class Mario(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,tiles):
        """ Initialize a mario at the specified position
            pos_x, pos_y """

        pygame.sprite.Sprite.__init__(self)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x_vel = 0
        self.y_vel = 0
        self.acc_x = 0
        self.acc_y = 450

        self.tiles = tiles
        self.onGround = False
        self.jumpRatio = 10000

        self.image = pygame.image.load('img/mario.png')
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image.convert_alpha(), self.rect)

    def update(self, dt):
        """ update mario due to passage of time """

        if not self.onGround:
            self.y_vel += self.acc_y*dt

        # x-axis updates and collisions
        self.rect.x += self.x_vel*dt
        self.collide(self.x_vel, 0)

        self.x_vel = 0

        # y-axis updates and collisions
        self.rect.y += self.y_vel*dt
        self.onGround = False
        self.collide(0, self.y_vel)

    def collide(self, x_vel, y_vel):
        for tile in self.tiles:
            if pygame.sprite.collide_rect(self, tile):
                if isinstance(tile, ExitTile):
                    pygame.event.post(pygame.event.Event(NEXTLEVEL))
                if x_vel > 0: self.rect.right = tile.rect.left
                if x_vel < 0: self.rect.left = tile.rect.right
                if y_vel > 0:
                    self.rect.bottom = tile.rect.top
                    self.onGround = True
                    self.y_vel = 0
                if y_vel < 0: self.rect.top = tile.rect.bottom

    def go_left(self):
        self.x_vel = -150

    def go_right(self): 
        self.x_vel = 150

    def jump(self):
        if self.onGround:
            self.y_vel = -300

    def stop(self):
        self.x_vel = 0

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
                if self.map[row][x] == 2:
                    tile = ExitTile(x*50, row*50)
                    self.tiles.add(tile)

    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)

class Tile(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)

        self.x_pos = x_pos
        self.y_pos = y_pos

        self.image = pygame.image.load('img/groundTile.png')
        # self.image = pygame.Surface([50,50])
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x_pos, self.y_pos)

    def draw(self, screen):
        screen.blit(self.image.convert_alpha(), self.rect)

class ExitTile(Tile):
    def __init__(self, x_pos, y_pos):
        Tile.__init__(self, x_pos, y_pos)
        self.image.fill(GREEN)

class PygameController():
    def __init__(self, model):
        self.model = model

    def process_events(self):
        done = False
        pygame.event.pump
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.model.mario.go_left()
                if event.key == pygame.K_RIGHT:
                    self.model.mario.go_right()
                if event.key == pygame.K_SPACE:
                    self.model.mario.jump()
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.model.mario.x_vel < 0:
                    self.model.mario.stop()
                if event.key == pygame.K_RIGHT and self.model.mario.x_vel > 0:
                    self.model.mario.stop()
                if event.key == pygame.K_SPACE and self.model.mario.y_vel > 0:
                    self.model.mario.stop()


        # Audio event processing
        if self.model.audio_sample.is_above_trigger():
            self.model.mario.jump()

        # audio_trigger = self.model.audio_sample.get_level()
        # if audio_trigger:
        #     self.model.mario.jump(audio_trigger)

        # Motion event processing
        x_mov = self.model.motion_track.get_movement() 
        if x_mov:
            if x_mov < 70:
                self.model.mario.go_right()
            if x_mov >= 70:
                self.model.mario.go_left()

        return done

if __name__ == '__main__':
    marioscii = Marioscii()
    marioscii.run()