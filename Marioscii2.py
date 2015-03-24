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

# Define global events
NEXTLEVEL = pygame.USEREVENT + 1
next_level_event = pygame.event.Event(NEXTLEVEL, message="Next Level!")
QUIT = pygame.USEREVENT + 2 
quit_event = pygame.event.Event(QUIT, message="Quit.")


# Define global tiled level arrays
level0 = np.array(
   [(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])

level1 = np.array(
   [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    (0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0),
    (1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0),
    (1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])

level2 = np.array(
   [(2, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0),
    (1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])

level3 = np.array(
   [(1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1),
    (1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1),
    (1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1),
    (1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1),
    (1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1),
    (1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1),
    (1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 2, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)])

all_levels = [level0, level1, level2, level3]


class MariosciiModel():
    """ Represents game state of Marioscii game """
    def __init__(self, width, height):
        # Define model components - levels, character, motion tracker, audio sampler
        self.levels = all_levels
        self.current_level = 0
        self.width = width
        self.height = height
        self.tiles = pygame.sprite.Group()
        self.level = Level(self.levels[self.current_level])
        self.mario = Mario(400,300,self.level.tiles)
        self.motion_track = Motion_Tracker()
        self.audio_sample = AudioSampler(10000)

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.mario.update(delta_t)

    def advance(self):
        """Advances to next level when target tile reached"""
        self.current_level += 1
        self.level = Level(self.levels[self.current_level])
        self.mario.tiles = self.level.tiles

class MariosciiView():
    """ Representents view state of Marioscii game """
    def __init__(self, model, width, height):
        """ Initialize view for Marioscii """
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,0,0)) #Set background to black
        self.model.mario.draw(self.screen) 
        self.model.level.draw(self.screen)
        pygame.display.update()


class Marioscii():
    """ The main Marioscii class that runs the game """
    def __init__(self):
        self.model = MariosciiModel(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.view = MariosciiView(self.model, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.controller = PygameController(self.model)
        self.clock = pygame.time.Clock()

    def run(self):
        """ Runs the game """
        last_ticks = 0.0
        done = False

        while not done:
            t = pygame.time.get_ticks() # Get current time
            dt = (t - last_ticks) / 1000.0 # Get change in time
            last_ticks = t 

            done = self.controller.process_events() # Process all events
            self.model.update(dt) # Update model based on events
            self.view.draw() # Draw view

            self.clock.tick(25) # Change in time


class Mario(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,tiles):
        """ Initialize a mario at the specified position
            pos_x, pos_y """

        pygame.sprite.Sprite.__init__(self)

        # Set relevant state variables
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.x_vel = 0
        self.y_vel = 0
        self.acc_x = 0
        self.acc_y = 600

        self.tiles = tiles
        self.onGround = False

        self.image = pygame.image.load('img/mario.png')
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(pos_x,pos_y)

    def draw(self, screen):
        # Draw mario with transparent background - convert_alpha
        screen.blit(self.image.convert_alpha(), self.rect)

    def update(self, dt):
        """ update mario due to passage of time """

        # If mario not on ground - jumping - initiate gravity effect
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
        """ Handle collisions between character and tiles """
        for tile in self.tiles:

            # If character in collision with block
            if pygame.sprite.collide_rect(self, tile):

                # Post advance to next level if collided tile is an exit tile
                if isinstance(tile, ExitTile):
                    pygame.event.post(next_level_event)

                # If character is moving right, set right of character to left of tile
                if x_vel > 0: self.rect.right = tile.rect.left

                # If character moving left, set left of character to right of tile
                if x_vel < 0: self.rect.left = tile.rect.right

                # If character falling when collides
                if y_vel > 0:
                    self.rect.bottom = tile.rect.top
                    self.onGround = True
                    self.y_vel = 0

                # If character moving upward when collides
                if y_vel < 0: 
                    self.rect.top = tile.rect.bottom

    def go_left(self):
        self.x_vel = -200

    def go_right(self): 
        self.x_vel = 200

    def jump(self):
        if self.onGround:
            self.y_vel = -350

    def stop(self):
        self.x_vel = 0


class Level(pygame.sprite.Sprite):
    """ Represents a level """
    def __init__(self, map):
        pygame.sprite.Sprite.__init__(self)
        self.map = map
        self.tiles = pygame.sprite.Group()

        # Creates map of tiles from inputted np array
        for row in xrange(len(self.map)):
            for x in range(len(self.map[row])):

                # For each element in array, create relevant tile
                if self.map[row][x] == 1:
                    tile = Tile(x*50, row*50)
                    self.tiles.add(tile)
                if self.map[row][x] == 2:
                    tile = ExitTile(x*50, row*50)
                    self.tiles.add(tile)
                if self.map[row][x] == 3:
                    tile = TitleTile(x*50, row*50)
                    self.tiles.add(tile)
                if self.map[row][x] == 4:
                    tile = DirectionsTile(x*50, row*50)
                    self.tiles.add(tile)

    def draw(self, screen):
        for tile in self.tiles:
            tile.draw(screen)

class Tile(pygame.sprite.Sprite):
    """ Represents tile """
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)

        self.x_pos = x_pos
        self.y_pos = y_pos

        "audio/filename.wav"
        self.image = pygame.image.load('img/groundTile.png')
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(self.x_pos, self.y_pos)

    def draw(self, screen):
        screen.blit(self.image.convert_alpha(), self.rect)

class ExitTile(Tile):
    """ Child of tile class representing exit tile """
    def __init__(self, x_pos, y_pos):
        Tile.__init__(self, x_pos, y_pos)
        self.image = pygame.image.load('img/exitTile.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x_pos, self.y_pos)

class TitleTile(Tile):
    """ Child of tile class representing title tile on menu """
    def __init__(self, x_pos, y_pos):
        Tile.__init__(self, x_pos, y_pos)
        self.image = pygame.image.load('img/title.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x_pos, self.y_pos)

class DirectionsTile(Tile):
    """ Child of tile class representing directions tile on menu """
    def __init__(self, x_pos, y_pos):
        Tile.__init__(self, x_pos, y_pos)
        self.image = pygame.image.load('img/directions.png')
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(self.x_pos, self.y_pos)

class PygameController():
    """ Represents controller for Marioscii game """

    def __init__(self, model):
        self.model = model

    def process_events(self):
        done = False
        pygame.event.pump
        for event in pygame.event.get():

            # If event type calls for level advancement 
            if event.type == NEXTLEVEL:
                self.model.advance()
            if event.type == QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.model.mario.go_left()
                if event.key == pygame.K_RIGHT:
                    self.model.mario.go_right()
                if event.key == pygame.K_SPACE:
                    self.model.mario.jump()
                if event.key == pygame.K_q:
                    pygame.event.post(quit_event)
                    
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

        # Motion event processing
        x_mov = self.model.motion_track.get_movement() 
        if x_mov:
            if x_mov < 60:
                self.model.mario.go_right()
            if x_mov >= 60:
                self.model.mario.go_left()

        return done

if __name__ == '__main__':
    # Create game instance, then run it!
    marioscii = Marioscii()
    marioscii.run()
