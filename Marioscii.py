"""
Created on Sun Mar 2 11:37 2015
@author: Patrick Huston
@author: Bill Wong
"""

import pygame
import random
from AudioSampler import AudioSampler

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)

class Mario(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        """ Initialize a mario at the specified position
            pos_x, pos_y """

        pygame.sprite.Sprite.__init__(self)

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.vel_x = 0
        self.vel_y = 0
        # TODO: don't depend on relative path
        self.image = pygame.Surface([20,20])
        self.image.fill(RED)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        screen.blit(self.image, self.rect.move(self.pos_x, self.pos_y))

    def update(self, delta_t):
        """ update mario due to passage of time """
        self.pos_x += self.vel_x*delta_t
        # if self.pos_y < SCREEN_HEIGHT:
        #     self.pos_y = 0
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

    def draw(self, screen):
        #Draw some other shit.
        pass

pygame.init()


audio_sample = AudioSampler(6000)

# Create pygame window
#infoObject = pygame.display.Info()
#screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Marioscii")

# Set clock and stuff
done = False
clock = pygame.time.Clock()

# Initialize sprite
mario = Mario(15, 20)
#my_ground = Ground()
# sprite_group = pygame.sprite.Group(mario)

lastGetTicks = 0.0

# Actually run the game
while not done:

    print audio_sample.is_above_trigger()
    t = pygame.time.get_ticks()
    # delta time in seconds.
    dt = (t - lastGetTicks) / 1000.0
    lastGetTicks = t

    # Event processing
    pygame.event.pump
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                mario.go_left()
            if event.key == pygame.K_RIGHT:
                mario.go_right()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and mario.vel_x < 0:
                mario.stop()
            if event.key == pygame.K_RIGHT and mario.vel_x > 0:
                mario.stop()


    # Audio event processing
    if audio_sample.is_above_trigger():
        mario.go_right()
    else:
        mario.stop()

    mario.update(dt)

    # Drawing
    screen.fill(WHITE)
    mario.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()