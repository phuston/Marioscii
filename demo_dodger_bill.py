# Pygcurse Dodger
# By Al Sweigart al@inventwithpython.com

# This program is a demo for the Pygcurse module.
# Simplified BSD License, Copyright 2011 Al Sweigart

import pygame, random, sys, time, pygcurse
from pygame.locals import *

GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

WINWIDTH = 80
WINHEIGHT = 50
TEXTCOLOR = WHITE
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
BADDIEMINSIZE = 1
BADDIEMAXSIZE = 5
BADDIEMINSPEED = 4
BADDIEMAXSPEED = 1
ADDNEWBADDIERATE = 10


win = pygcurse.PygcurseWindow(WINWIDTH, WINHEIGHT, fullscreen=False)
pygame.display.set_caption('Pygcurse Dodger')
win.autoupdate = False

def main():
    showStartScreen()
    # pygame.mouse.set_visible(False)
    mainClock = pygame.time.Clock()
    gameOver = False

    jumpcounter = 0
    jumpinglist = [0,1,1,1,1,0,0,-1,-1,-1,-1]

    goingleft = False
    goingright = False

    newGame = True
    while True:
        if gameOver and time.time() - 4 > gameOverTime:
            newGame = True
        if newGame:
            newGame = False
            # pygame.mouse.set_pos(win.centerx * win.cellwidth, (win.bottom - 4) * win.cellheight)
            # mousex, mousey = pygame.mouse.get_pos()
            # cellx, celly = win.getcoordinatesatpixel(mousex, mousey)
            cellx, celly = 10, 30
            baddies = []
            baddieAddCounter = 0
            gameOver = False
            score = 0

        win.fill(bgcolor=BLACK)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            # if event.type == MOUSEMOTION and not gameOver:
            #     mousex, mousey = event.pos
            #     cellx, celly = win.getcoordinatesatpixel(mousex, mousey)
            if event.type == KEYDOWN:
                if event.key == K_UP and jumpcounter == 0:   # execute jumping protocol
                    # celly += -1
                    jumpcounter = 1
                # elif event.key == K_DOWN:
                    # celly += 1
                elif event.key == K_LEFT:
                    goingleft = True
                elif event.key == K_RIGHT:
                    goingright = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    goingleft = False
                if event.key == K_RIGHT:
                    goingright = False
        # add new baddies if needed
        # if baddieAddCounter == ADDNEWBADDIERATE:
        #     speed = 100
        #     baddies.append({'size': 1,
        #                     'speed': speed,
        #                     'x': random.randint(0, win.width),  # select random x value to start falling from
        #                     'y': random.randint(0, win.height),
        #                     'movecounter': speed})
        #     baddieAddCounter = 0
        # else:
        #     baddieAddCounter += 1


        # move baddies down, remove if needed
        # for i in range(len(baddies)-1, -1, -1):
        #     if baddies[i]['movecounter'] == 0:
        #         baddies[i]['y'] += 1
        #         baddies[i]['movecounter'] = baddies[i]['speed']
        #     else:
        #         baddies[i]['movecounter'] -= 1

        #     if baddies[i]['y'] > win.height:
        #         del baddies[i]


        # check if hit
        # if not gameOver:
        #     for baddie in baddies:
        #         if cellx >= baddie['x'] \
        #         and celly >= baddie['y'] \
        #         and cellx < baddie['x']+baddie['size'] \
        #         and celly < baddie['y']+baddie['size']:
        #             gameOver = True
        #             gameOverTime = time.time()
        #             break
        #     score += 1

        # draw baddies to screen
        # for baddie in baddies:
        #     win.fill('#', GREEN, BLACK, (baddie['x'], baddie['y'], baddie['size'], baddie['size']))

        # win.fill('#', GREEN, 20, 30)
        win.fill('#', fgcolor='green', region=[20,28,7,3])  #region=[x,y,width,height]
        win.fill('#', fgcolor='green', region=[0,31,80,1])
        # win.fill('#', fgcolor='green', region=[0,0,80,50])
        # print win.getcharatpixel(22,30)

        if not gameOver:
            playercolor = WHITE
        else:
            playercolor = RED
            win.putchars('GAME OVER', win.centerx-4, win.centery, fgcolor=RED, bgcolor=BLACK)

        if goingleft == True:
            cellx -= 1
        if goingright == True:
            cellx += 1

        if jumpcounter > 0: # if we're currently jumping
            # print jumpcounter
            # win.putchar('@', cellx, (celly - jumpinglist[jumpcounter]), playercolor)

            if jumpcounter >= 4 and win.getcharatpixel(cellx, (celly + 1)) == '#':
                # check if platform is right below us
                jumpcounter = 0

            celly -= jumpinglist[jumpcounter]
            jumpcounter += 1
            jumpcounter = jumpcounter % len(jumpinglist)
        # elif jumpcounter == 0: # not jumping
            
        win.putchar('@', cellx, celly, playercolor)



        win.putchars('Score: %s' % (score), win.width - 14, 1, fgcolor=WHITE)
        win.update()
        mainClock.tick(FPS)


def showStartScreen():
    while checkForKeyPress() is None:
        win.fill(bgcolor=BLACK)
        win.putchars('Pygcurse Dodger', win.centerx-8, win.centery, fgcolor=TEXTCOLOR)
        if int(time.time() * 2) % 2 == 0: # flashing
            win.putchars('Press a key to start!', win.centerx-11, win.centery+1, fgcolor=TEXTCOLOR)
        win.update()


def checkForKeyPress():
    # Go through event queue looking for a KEYUP event.
    # Grab KEYDOWN events to remove them from the event queue.
    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        if event.key == K_ESCAPE:
            terminate()
        return event.key
    return None


def terminate():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()