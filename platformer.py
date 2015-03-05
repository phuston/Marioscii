""" A Collaboratively-Coded Clone of Flappy Bird """

import pygame
import random
import time

# Global constants
 
# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
 
# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600


class MariosciiModel():
    """ Represents game state of Marioscii game """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mario = Mario(0,100)

    def update(self, delta_t):
        """ Updates the model and its constituent parts """
        self.mario.update(delta_t)

class Mario():
    """ Represents player in game """
    def __init__(self,pos_x,pos_y):
        """ Initialize a mario at the specified position
            pos_x, pos_y """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 20
        self.vel_y = 0
        # TODO: don't depend on relative path
        self.image = pygame.Surface([40,60])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect.move(self.pos_x, self.pos_y))

    def update(self, delta_t):
        """ update mario due to passage of time """
        self.pos_x += self.vel_x*delta_t
        self.pos_y += self.vel_y*delta_t
        self.vel_y += 100*delta_t

    def flap(self):
        self.vel_y = -40

    def go_left(self):
        self.vel_x = 20

    def go_right(self): 
        self.vel_x = -20

class MariosciiView():
    def __init__(self, model, width, height):
        """ Initialize view for Marioscii """
        pygame.init()
        # to retrieve width and height use screen.get_size()
        self.screen = pygame.display.set_mode((width, height))
        # this is used for figuring out where to draw stuff
        self.model = model

    def draw(self):
        """ Redraw the full game window """
        self.screen.fill((0,51,102))
        self.model.mario.draw(self.screen)
        pygame.display.update()

class Marioscii():
    """ The main Marioscii class """

    def __init__(self):
        self.model = MariosciiModel(640, 480)
        self.view = MariosciiView(self.model, 640, 480)
        self.controller = PygameKeyboardController(self.model)

    def run(self):
        last_update = time.time()
        while True:
            self.view.draw()
            self.controller.process_events()
            delta_t = time.time() - last_update
            self.model.update(delta_t)
            last_update = time.time()

class PygameKeyboardController():
    def __init__(self, model):
        self.model = model
        self.space_pressed = False

    def process_events(self):
        pygame.event.pump()
        while True:
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    done = True # Flag that we are done so we exit this loop
     
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.model.mario.go_left()
                    if event.key == pygame.K_RIGHT:
                        self.model.mario.go_right()
                    if event.key == pygame.K_UP:
                        self.model.mario.jump()
     
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.model.mario.vel_x < 0:
                        self.model.mario.stop()
                    if event.key == pygame.K_RIGHT and self.model.maril.vel_ > 0:
                        self.model.mario.stop()
if __name__ == '__main__':
    marioscii = Marioscii()
    marioscii.run()