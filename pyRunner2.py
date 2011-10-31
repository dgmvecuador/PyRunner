#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       pyRunner.py
#
#       Copyright 2010 dhatch387 (David Hatch) <dhatch387@gmail.com>
#
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import pygame
from pygame.locals import*
#import key names
from pygame.key import *
import os
import platform
import random
import sys
import math
import ConfigParser
from menu import *
import classes
if platform.system() == 'Windows':
    os.environ['SDL_VIDEODRIVER'] = 'windib'
# Change the mixer to proper values.
pygame.mixer.pre_init(44100,-16,2, 1024)
pygame.init()

###OPTIMIZATION DOTO
# check collision
# use render groups and only update needed
# hardware accel on fullscreen?
# use surface.fill for drawing filled rects
# surface.convert on all surfaces
##CHANGELOG 0.6:
#David:
#-level design code
#-fixed lag problem
#-added progress bar for inv
#-fixed crashes
#Brian:
#-shield and invisibility cubes
##CHANGELOG 0.7:
#David:
#-fixed significant bug where program would slow down when many cubes
#were picked up in a row. was an error in pygame.sprite.GroupSingle class
##CHANGELOG 0.8:
#Brian:
#-added in turrets,gun and bullets
##CHANGELOG 0.9:
#David:
#-inserted modified and improved levling code
#-created endMenu
#Brian:
#-fixed error in gun programming, now reloads

##VARS
##VARS DEFINED IN init()
screen = None
##VARS DEFINED IN gameInit()
mainLevelManager = None
gunner = None
background = None
clock = None
keepGoing = False
runner1 = None
max_height = None
min_height = None
rungroup = None
blockMinHeight = None
blockMaxHeight = None
#GROUPS
blockGroup = None
cubeGroup = None
invGroup = None
shieldGroup = None
turretGroup = None
gunGroup = None
effectsGroup = None
bulletGroup = None
gunnerGroup = None
ammoInd = None
shieldsInd = None
speedInd = None
score = None
frame_count = None
displayFrame = None
target_rate = None
invInd = None
gameMode = None
#HIGH SCORE
highScore = None
score_type = None

# Sound class
def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('Resources', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', fullname
        raise SystemExit, message
    return sound

#Music support:
def prepare_music_file(name):
    fullname = os.path.join('Resources', 'music', name)
    try:
        pygame.mixer.music.load(fullname)
        #print "Music file %s loaded!" % fullname
    except pygame.error:
        print "File %s not found! (%s)" % (fullname, pygame.get_error())
    return

def music_play():
    pygame.mixer.music.play(-1)

def music_stop():
    pygame.mixer.music.stop()

def is_music_playing():
    return pygame.mixer.music.get_busy()


#debug function
_debug = False
_die = True
def debug(printstring):
    if _debug:
        print printstring

def init():
    #create screen
    global screen
    global clock
    global score_type
    if(_debug):
        screen = pygame.display.set_mode((600, 820))
    else:
        screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    # Ignore mouse motion (greatly reduces resources when not needed)
    pygame.event.set_blocked(pygame.MOUSEMOTION)

    # Hide the mouse cursor
    pygame.mouse.set_visible(False)

    # Load config file
    #highScoreLoad()

    clock = pygame.time.Clock()

def gameInit():
    global screen
    ##VARS DEFINED IN gameInit()
    global mainLevelManager
    global gunner
    global background
    global clock
    global keepGoing
    global runner1
    global rungroup
    global max_height
    global min_height
    global blockMinHeight
    global blockMaxHeight
    #GROUPS
    global blockGroup
    global cubeGroup
    global invGroup
    global shieldGroup
    global turretGroup
    global gunGroup
    global effectsGroup
    global bulletGroup
    global gunnerGroup
    global ammoInd
    global shieldsInd
    global speedInd
    global score
    global frame_count
    global displayFrame
    global target_rate
    global invInd
    #Globals defined in mainMenu()
    global gameMode
    global score_type
    ##INITIALIZATION CODE
    mainLevelManager = levelManager()
    gunner = pygame.image.load(os.path.join(\
            "Resources","Gunner.bmp"))
    gunner = gunner.convert()
    gunner.set_colorkey((0,0,0))
    background = pygame.Surface((screen.get_width(), screen.get_height()))
    pygame.draw.rect(background, (10,10,10), background.get_rect())
    #only nessecary if not fullscreen
    pygame.display.set_caption("pyRunner 2D")
    keepGoing = True
    #create our runner and a group to hold it
    runner1 = runner(screen)
    rungroup = pygame.sprite.GroupSingle(runner1)
    #calculate window borders based on size
    #create window borders
    height = screen.get_height()
    border_height = (height-800)/2.0
    #min_border_height stores minimum height for borders
    min_border_height = 70
    if border_height < min_border_height:
        #minimum border of 50px
        max_height = min_border_height
        min_height = height-min_border_height
        border_height = min_border_height
    max_height = border_height
    min_height = height - border_height
    #create our borders
    pygame.draw.rect(background, (255,255,255),\
                     pygame.rect.Rect(0,border_height, screen.get_width(), \
                                      0))
    pygame.draw.rect(background, (255,255,255),\
                     pygame.rect.Rect(0, min_height,\
                                      screen.get_width(), 0))
    #choose block border heights
    blockMinHeight = min_height - 45
    blockMaxHeight = max_height + 45
    ##INITIALIZE REZ GROUPS
    #initialize a block group of our randomRezGroup class (subclass of pygame.
    #sprite.group
    blockGroup = randomRezGroup(block,maxRezHeight=blockMaxHeight,minRezHeight=blockMinHeight)
    cubeGroup = randomRezGroup(scoreCube,maxRezHeight=blockMaxHeight,minRezHeight=blockMinHeight)
    invGroup = randomRezGroup(invCube,maxRezHeight=blockMaxHeight,minRezHeight=blockMinHeight)
    shieldGroup = randomRezGroup(shieldCube,maxRezHeight=blockMaxHeight,minRezHeight=blockMinHeight)
    turretGroup = randomRezGroup(turret,maxRezHeight = blockMaxHeight,minRezHeight=blockMinHeight)
    gunGroup = randomRezGroup(gunCube,maxRezHeight = blockMaxHeight,minRezHeight = blockMinHeight)
    effectsGroup = WorkingSingle() #group to store effects in
    bulletGroup = pygame.sprite.RenderUpdates()
    gunnerGroup = pygame.sprite.RenderUpdates()
    ##LEVEL CREATION AND DESIGN
    if gameMode == "endurance":
        add = mainLevelManager.add
        add(level({blockGroup:[2,100,200,75,True],cubeGroup:[1,700,2000,300,True],
                   invGroup:[1,2000,5000,300,False],shieldGroup:[1,1000,3000,300,False],
                   turretGroup:[1,1000,2000,300,False],gunGroup:[1,50,50,50,False]},6,800))
        add(level({},7,800))
        add(level({blockGroup:[3,100,200,75,True]},7,1200))
        add(level({shieldGroup:[1,4000,7000,300,True]},8,800))
        add(level({gunGroup:[1,3000,7000,300,True]},8,600))
        add(level({invGroup:[1,5000,10000,300,True]},8,1200))
        add(level({turretGroup:[1,3000,5000,300,True]},8,3500))
        add(level({turretGroup:[1,2000,4000,300,True]},8,2000))
        add(level({blockGroup:[1,100,200,75,True],shieldGroup:[1,450,600,300,True]},16,600))
        add(level({blockGroup:[3,75,200,75,True],shieldGroup:[1,4000,7000,300,True]},9,3200))
        add(level({blockGroup:[4,50,250,75,True],shieldGroup:[1,450,600,300,True],invGroup:[1,6000,8000,300,True]},11,4000))

    elif gameMode == "challenge":
        mainLevelManager.add(level({blockGroup:[3,75,200,75,True],cubeGroup:[1,700,2000,300,True],\
                                    invGroup:[1,10000,20000,300,True],shieldGroup:[1,8000,15000,300,True],turretGroup:[1,2000,4000,300,True]\
                                    ,gunGroup:[1,6500,14000,300,True]},9,800))
    #create a shield indicator
    ammoInd = ammoIndicator()
    ammoInd.setAmmo(10)
    shieldsInd = shieldIndicator()
    shieldsInd.setShield(3)
    speedInd = progressIndicator((0,255,0),"Speed:   ")
    mainLevelManager.setIndicator(speedInd)
    #make first level active
    mainLevelManager.setLevel(1)
    #blit the background to the screen to start with
    screen.blit(background, (0,0))
    #create a variable to store distance
    score = 0
    #keep track of the number of frames
    frame_count = 0
    #do we want to display a framerate?
    displayFrame = False
    #target frame rate
    target_rate = 70
    #the next chosen row
    #tracking of last row
    invInd = progressIndicator((255,255,255),"")


def main():
    global screen
    ##VARS DEFINED IN gameInit()
    global mainLevelManager
    global gunner
    global background
    global clock
    global keepGoing
    global runner1
    global rungroup
    global blockMinHeight
    global blockMaxHeight
    #GROUPS
    global blockGroup
    global cubeGroup
    global invGroup
    global shieldGroup
    global turretGroup
    global gunGroup
    global effectsGroup
    global bulletGroup
    global gunnerGroup
    global ammoInd
    global shieldsInd
    global speedInd
    global score
    global frame_count
    global displayFrame
    global target_rate
    global invInd
    global score_type
    #run loop
    while 1:
        #check to make sure our runner still exists
        if not rungroup.sprite:
            break
        #target_rate is the max possible frame rate
        clock.tick(target_rate)
        #check how long the user has beem playing and if they have\
        #been playing long enough make the speed faster
        ##LEVELING CODE[OLD]##
##            if frame_count == 800: #Level 2
##                scroller.dx += 1
##                debug("lvl2")
##            elif frame_count == 1200: #Level 3
##                scroller.dx += 1
##                debug("Go Faster")
##            elif frame_count == 3200:
##                scroller.dx += 1
##            elif frame_count == 6400:
##                scroller.dx += 1
        #tell the levelManager we have a new frame
        mainLevelManager.frame()
        #get events registered
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitGame()
                return
            #this is here so we can quit
            if event.type == pygame.KEYUP:
                if event.dict["key"] == K_ESCAPE:
                    pause()
                    return
                #toggle frame rate display w/ key f
                if event.dict["key"] == K_f:
                    if displayFrame:
                        displayFrame = False
                        screen.blit(background,(0,0))
                    else:
                        displayFrame = True
                if event.dict["key"] == K_p:
                    pause()
                    return
                if event.dict["key"] == K_SPACE:
                    rungroup.sprite.last_shot = 10
                else:
                    pass
        if rungroup.sprite: #if runner dies before our loop is over we don't
            #want an error
            groupcollide = pygame.sprite.groupcollide
            groupcollide(gunnerGroup,blockGroup,True,True)
            groupcollide(gunnerGroup,cubeGroup,True,True)
            groupcollide(gunnerGroup,shieldGroup,True,True)
            groupcollide(gunnerGroup,invGroup,True,True)
            groupcollide(gunnerGroup,turretGroup,True,True)
            groupcollide(gunnerGroup,gunGroup,True,True)
            groupcollide(bulletGroup,blockGroup,False,True)
            groupcollide(bulletGroup,cubeGroup,False,True)
            groupcollide(bulletGroup,shieldGroup,False,True)
            groupcollide(bulletGroup,invGroup,False,True)
            groupcollide(bulletGroup,gunGroup,False,True)

            collided = pygame.sprite.spritecollide(rungroup.sprite,bulletGroup,True)
            for x in collided:
                rungroup.sprite.hit()
            #delete blocks that intercept cubes
            pygame.sprite.groupcollide(cubeGroup,blockGroup, False,True)
            collidedSprites = pygame.sprite.spritecollide(rungroup.sprite,cubeGroup,True)
            for x in collidedSprites:
                x.hit()
                score += x.score
            pygame.sprite.groupcollide(invGroup,blockGroup,True,False)
            pygame.sprite.groupcollide(invGroup,cubeGroup,False,True)
            collidedSprites = pygame.sprite.spritecollide(rungroup.sprite,invGroup,True)
            for x in collidedSprites:
                x.hit()
                rungroup.sprite.invinc()
                debug("Invincible")
            pygame.sprite.groupcollide(shieldGroup,blockGroup,True,False)
            pygame.sprite.groupcollide(shieldGroup,cubeGroup,False,True)
            collidedSprites = pygame.sprite.spritecollide(rungroup.sprite,shieldGroup,True)
            for x in collidedSprites:
                x.hit()
                if not rungroup.sprite.shield == 3:
                    rungroup.sprite.shield +=1
                debug("Shield")
            #check for colisions between runner and sprites in block group
            collidedSprites = pygame.sprite.spritecollideany(rungroup.sprite, blockGroup)
            if not collidedSprites:
                collidedSprites = pygame.sprite.spritecollideany(rungroup.sprite, turretGroup)
            if collidedSprites and _die:
                #reduce shields
                rungroup.sprite.hit()
            pygame.sprite.groupcollide(gunGroup,blockGroup,False,True)
            pygame.sprite.groupcollide(gunGroup,cubeGroup,False,True)
            pygame.sprite.groupcollide(gunGroup,shieldGroup,False,True)
            pygame.sprite.groupcollide(gunGroup,invGroup,False,True)
            collided = pygame.sprite.spritecollide(rungroup.sprite,gunGroup,True)
            for x in collided:
                rungroup.sprite.gun += 1
                rungroup.sprite.ammo = 10
        #increment distance
        score +=  .5
        #increment the number of frames
        frame_count += 1
        #choose distance font
        scoreFont = pygame.font.Font(None, 40)
        #get a surface with the font on it
        fontSurface = scoreFont.render("{0:n}".format(round(score)), True,\
                                          (255,255,255))
        #rect for the new font
        fontRect = pygame.rect.Rect(0,0,fontSurface.get_width()+5,\
                                    fontSurface.get_height())
        ##BEFORE DOING ANY NEW DRAWING, CLEAR ALL SPRITES
        rungroup.update()
        blockGroup.update()
        cubeGroup.update()
        effectsGroup.update()
        gunnerGroup.update()
        invGroup.update()
        gunGroup.update()
        turretGroup.update()
        shieldGroup.update()
        bulletGroup.update()
        invGroup.clear(screen,background)
        gunGroup.clear(screen,background)
        gunnerGroup.clear(screen,background)
        turretGroup.clear(screen,background)
        bulletGroup.clear(screen,background)
        shieldGroup.clear(screen,background)
        rungroup.clear(screen, background)
        blockGroup.clear(screen,background)
        cubeGroup.clear(screen, background)
        effectsGroup.clear(screen,background)
        #clear the previous font
        screen.blit(background,(0,0),fontRect)
        #draw the new font
        screen.blit(fontSurface,(0,0))
        #optional framerate display
        if displayFrame:
            frameFont = pygame.font.Font(None, 40)
            frameSurface = frameFont.render("{0:n}".format(round(\
                                                clock.get_fps())),\
                                               True, (255,255,255))
            #find the rect for the new surface
            x = 0
            y = screen.get_height()-frameSurface.get_height()
            frameRateRect = frameSurface.get_rect().move(x,y)
            frameRateRect.width += 10
            #clear previous font
            screen.blit(background, (0, y),\
                                     frameRateRect)
            #draw new font
            screen.blit(frameSurface, (0, y))
        #set the shields to appropriate value (runner's shield)
        if rungroup.sprite:
            shieldsInd.setShield(rungroup.sprite.shield)
        if rungroup.sprite:
            ammoInd.setAmmo(rungroup.sprite.ammo)
        #add in shield indicator display
        ammoIndicatorRect = fontRect
        ammoIndicatorRect.top += (fontSurface.get_height() + 15)#put 10 px below font
        ammoIndicatorRect = ammoIndicatorRect.move(200,7)
        shieldIndicatorRect = fontRect
        shieldIndicatorRect.top += (fontSurface.get_height() - 40)#put 10 px below font
        speedIndicatorRect = shieldIndicatorRect.move(0,20)
        invIndicatorRect = pygame.rect.Rect(0,0,105,15)
        dispRect = pygame.display.get_surface().get_rect()
        invIndicatorRect.centerx = dispRect.centerx
        invIndicatorRect.centery = dispRect.centery
        #draw all groups on screen
        screen.blit(background,ammoIndicatorRect, ammoIndicatorRect)
        screen.blit(background, shieldIndicatorRect,shieldIndicatorRect)
        screen.blit(background,speedIndicatorRect,speedIndicatorRect)
        screen.blit(background,invIndicatorRect,invIndicatorRect)
        if rungroup.sprite:
            if rungroup.sprite.inv:
                invInd.setPercentage((rungroup.sprite.invCount/float(800))*100)
        #check to make sure the cubes arent spawned over the blocks
        rungroup.draw(screen)
        gunGroup.draw(screen)
        gunnerGroup.draw(screen)
        turretGroup.draw(screen)
        bulletGroup.draw(screen)
        blockGroup.draw(screen)
        cubeGroup.draw(screen)
        invGroup.draw(screen)
        shieldGroup.draw(screen)
        screen.blit(ammoInd.getSurface(),ammoIndicatorRect)
        screen.blit(shieldsInd.getSurface(),shieldIndicatorRect) #blit new
        screen.blit(speedInd.getSurface(),speedIndicatorRect)
        if rungroup.sprite:
            if rungroup.sprite.inv:
                screen.blit(invInd.getSurface(),invIndicatorRect)
        effectsGroup.draw(screen)
        pygame.display.update()
    #end the game
    endMenu()

def pause():
    global selected
    global menu
    global clock
    global screen
    global score_type
    menu = cMenu(0, 0, 10, 10, 'vertical', 5, screen,
            [('Continue', 1, None),
             ("Restart", 3, None),
             ('Exit',       2, None)])

    # Center the menu on the draw_surface (the entire screen here)
    menu.set_center(True, True)
    # Center the menu on the draw_surface (the entire screen here)
    menu.set_alignment('center', 'center')
    # Create the state variables (make them different so that the user event is
    # triggered at the start of the "while 1" loop so that the initial display
    # does not wait for user input)
    state = 0
    prev_state = 1
    # rect_list is the list of pygame.Rect's that will tell pygame where to
    # update the screen (there is no point in updating the entire screen if only
    # a small portion of it changed!)
    rect_list = []
    # The main while loop
    while True:
        # Check if the state has changed, if it has, then post a user event to
        # the queue to force the menu to be shown at least once
        if prev_state != state:
            pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
            prev_state = state
        # Get the next event
        e = pygame.event.wait()
        # Update the menu, based on which "state" we are in - When using the menu
        # in a more complex program, definitely make the states global variables
        # so that you can refer to them by a name
        if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
            if state == 0:
                rect_list, state = menu.update(e, state)
            elif state == 1:
                screen.blit(background,menu.contained_rect,menu.contained_rect)
                main()
                return
            elif state == 3:
                gameInit()
                main()
            else:
                debug("exit")
                mainMenu()
                return
        # Quit if the user presses the exit button
        if e.type == pygame.QUIT:
            quitGame()
            return

        # Update the screen
        pygame.display.update(rect_list)


def endMenu():
    global selected
    global menu
    global clock
    global screen
    global highScore
    global score
    global score_type
    if score > highScore:
        highScore = score
    ranking(score)
    menu = cMenu(0, 0, 10, 10, 'horizontal', 5, screen,
               [('Play Again', 1, None),
                ('Exit',2, None)])

    # Center the menu on the draw_surface (the entire screen here)
    menu.set_center(True, True)
    # Center the menu on the draw_surface (the entire screen here)
    menu.set_alignment('center', 'center')
    # Create the state variables (make them different so that the user event is
    # triggered at the start of the "while 1" loop so that the initial display
    # does not wait for user input)
    state = 0
    prev_state = 1
    # rect_list is the list of pygame.Rect's that will tell pygame where to
    # update the screen (there is no point in updating the entire screen if only
    # a small portion of it changed!)
    rect_list = []
    font = pygame.font.Font(None, 30)
    fontSurface = font.render("Your score is: {0:n}".format(int(score)),True,(255,255,255))
    highScoreSurface = font.render("High Score: {0:n}".format(round(highScore)),True,(255,255,255))
    # The main while loop
    while 1:
      # Check if the state has changed, if it has, then post a user event to
      # the queue to force the menu to be shown at least once
      if prev_state != state:
         pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
         prev_state = state
      # Get the next event
      e = pygame.event.wait()
      # Update the menu, based on which "state" we are in - When using the menu
      # in a more complex program, definitely make the states global variables
      # so that you can refer to them by a name
      if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
         if state == 0:
            rect_list, state = menu.update(e, state)

            rect_list.append(screen.blit(fontSurface,(screen.get_rect().centerx-(fontSurface.get_width()/2.), \
                             (screen.get_rect().centery)-60,0,0)))

            rect_list.append(screen.blit(highScoreSurface,(screen.get_rect().centerx-(highScoreSurface.get_width()/2.), \
            (screen.get_rect().centery)-(fontSurface.get_height())-80)))

            for i in xrange(2,11):
                scores = font.render(get_scores(str(i)),True,(255,255,255))
                rect_list.append(screen.blit(scores,(screen.get_rect().centerx-(scores.get_width()/2.), \
                (screen.get_rect().centery)-(fontSurface.get_height())+(i*25))))

         elif state == 1:
            debug("start game")
            state = 0
            gameInit()
            main()
            return
         else:
            debug("exit")
            mainMenu()
            return

      # Quit if the user presses the exit button
      if e.type == pygame.QUIT:
            quitGame()
            return

      # Update the screen
      pygame.display.update(rect_list)

def mainMenu():
    global selected
    global menu
    global clock
    global screen
    global gameMode
    global score_type
    screen.fill((0,0,0))
    pygame.display.update()
    menu = cMenu(0, 0, 0, 10, 'vertical', 5, screen,
               [('Play Game', 1, None),
                #('High Scores',2,None),
                ('About',3,None),
                ('How to play',8,None),
                ('Quit',       4, None)])

    # Center the menu on the draw_surface (the entire screen here)
    menu.set_center(True, True)
    # Center the menu on the draw_surface (the entire screen here)
    menu.set_alignment('center', 'center')
    # Create the state variables (make them different so that the user event is
    # triggered at the start of the "while 1" loop so that the initial display
    # does not wait for user input)
    state = 0
    prev_state = 1
    # rect_list is the list of pygame.Rect's that will tell pygame where to
    # update the screen (there is no point in updating the entire screen if only
    # a small portion of it changed!)
    rect_list = []
    title = pygame.image.load(os.path.join("Resources","pyRunnerTitle.gif"))
    title = title.convert()

    # Test if it is playing a music
    if is_music_playing():
        music_stop()

    # Prepare music for menu
    prepare_music_file("menu.ogg")
    music_play()

    # The main while loop
    while 1:
      # Check if the state has changed, if it has, then post a user event to
      # the queue to force the menu to be shown at least once
      if prev_state != state:
         pygame.event.post(pygame.event.Event(EVENT_CHANGE_STATE, key = 0))
         prev_state = state

      # Get the next event
      e = pygame.event.wait()
      # Update the menu, based on which "state" we are in - When using the menu
      # in a more complex program, definitely make the states global variables
      # so that you can refer to them by a name
      if e.type == pygame.KEYDOWN or e.type == EVENT_CHANGE_STATE:
        if state == 0:
            rect_list, state = menu.update(e, state)
        elif state == 1:
            screen.fill((0,0,0))
            rect_list.append(screen.get_rect())
            menu = cMenu(0,0,20,10,'vertical',5,screen,
            [('Endurance',6,None),
            ('Challenge',5,None),
            ('Back',7,None)])
            menu.set_center(True, True)
            menu.set_alignment('center', 'center')
            state = 0
            prev_state = 1
        elif state == 3:
            screen.fill((0,0,0))
            rect_list.append(screen.get_rect())
            menu = cMenu(0,0,20,10,'vertical',5,screen,[(u'Code by Brian Erying, David Hatch and Diego Estévez',7,None),\
                                                        ('Images by Dan Austin',7,None),\
                                                        ('Press enter to return',7,None)])
            menu.set_center(True, True)
            menu.set_alignment('center', 'center')
            menu.set_selected_color((255,255,255))
            state = 0
            prev_state = 1
        elif state == 4:
            debug("exit")
            quitGame()
            return
        elif state == 5:
            gameMode = 'challenge'

            # Stop and play the correct music
            music_stop()
            prepare_music_file("challenge_new.ogg")
            music_play()
            # Set game type for score
            score_type = 'challenge'
            highScoreLoad()

            gameInit()
            main()
            return

        elif state == 6:
            gameMode = 'endurance'

            # Stop and play the correct music
            music_stop()
            prepare_music_file("endurance_new.ogg")
            music_play()
            # Set game type for score
            score_type = 'endurance'
            highScoreLoad()

            gameInit()
            main()
            return
        elif state == 7:
            screen.fill((0,0,0))
            rect_list.append(screen.get_rect())
            menu = cMenu(0, 0, 20, 10, 'vertical', 5, screen,
                        [('Play Game', 1, None),
                         #r('High Scores',2,None),
                         ('About',3,None),
                         ('How to play',8,None),
                         ('Quit', 4, None)])
            # Center the menu on the draw_surface (the entire screen here)
            menu.set_center(True, True)
            # Center the menu on the draw_surface (the entire screen here)
            menu.set_alignment('center', 'center')
            state = 0
            prev_state = 1
        elif state == 8:
            screen.fill((0,0,0))
            rect_list.append(screen.get_rect())
            menu = cMenu(0,0,0,5,'vertical',10,screen,[('How to play:',7,None),\
                                                        ('Use the up and down arrow keys to avoid the solid blocks, enemies, and bullets.',7,None),\
                                                        ('Gain points and special abilities from the hollow cubes.',7,None),\
                                                        ('',7,None),\
                                                        ('Special abilities:',7,None),\
                                                        ('Light blue = extra shield',7,None),\
                                                        ('Red = gun',7,None),\
                                                        ('White = invincibility',7,None),\
                                                        ('',7,None),\
                                                        ('Press enter to return',7,None)])
            menu.set_center(True, True)
            menu.set_alignment('center', 'center')
            menu.set_selected_color((255,255,255))
            state = 0
            prev_state = 1
      # Quit if the user presses the exit button
    if e.type == pygame.QUIT:
        quitGame()
        return
        rect_list.append(screen.blit(title,(screen.get_rect().centerx - title.get_rect().centerx,0)))

    # Update the screen
    pygame.display.update(rect_list)

def highScoreLoad():
    global highScore
    #score_type is set when the mode of play is determined ("challenge" for example).
    global score_type

    #If the file does not exist, create it
    if ( os.path.isfile('pyRunner.cfg') is False ):
        config = ConfigParser.RawConfigParser()
        with open('pyRunner.cfg', 'wb') as configfile:
            config.write(configfile)

    #If the section does not exist, create it.
    config = ConfigParser.ConfigParser()
    config.readfp(open('pyRunner.cfg'))
    if not ( config.has_section(score_type) ):
        # Creating the needed section.
        config.add_section(score_type)
        for i in xrange(1,11):
            config.set(score_type, str(i), "0")
        with open('pyRunner.cfg', 'wb') as configfile:
            config.write(configfile)

    highScore = config.getint(score_type,"1")

def ranking(score):
    global score_type
    replaced_score = ""

    config = ConfigParser.ConfigParser()
    config.readfp(open('pyRunner.cfg'))

    for i in xrange(1, 11):
        if ( int(score) > int(config.get(score_type, str(i))) ):
            #store the value I am about to replace
            replaced_score = config.get(score_type, str(i))
            #replace the value in the list
            config.set(score_type, str(i), str(int(score)))
            with open('pyRunner.cfg', 'wb') as configfile:
                config.write(configfile)
                #find the replaced score's new place in the list
                ranking(replaced_score)
                #immediatly end the loop when the recursion unwinds
                break

def get_scores(standing):
    global score_type

    config = ConfigParser.ConfigParser()
    config.readfp(open('pyRunner.cfg'))
    if ( config.has_section(score_type) ):
        return '%-10s%s' % (standing, config.get(score_type, standing))

def quitGame():
    pygame.display.quit()
      
if __name__ == "__main__":
    init()
    mainMenu()
