import pygame,sys
from pygame.locals import *
Running = True
Width = 1280
Height = 720
Y = 0
X = 0
XDirection = 0
YDirection = 0
White = (255,255,255)
Background = pygame.image.load("maptest.png")
Character = pygame.image.load("character.png")
screen = pygame.display.set_mode((1280, 720))


#MainLoop
while Running:
    for event in pygame.event.get():
            if event.type == QUIT:
                Running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                Running = False
            if event.type == KEYDOWN and event.key == K_s:  #On keypress S it will move the screen up
                YDirection = 1
            if event.type == KEYDOWN and event.key == K_w: #On keypress w it will move the screen down
                YDirection = 2
            if event.type == KEYDOWN and event.key == K_d:  #On keypress S it will move the screen up
                XDirection = 1
            if event.type == KEYDOWN and event.key == K_a: #On keypress w it will move the screen down
                XDirection = 2

    if YDirection is 1:
        Y = Y - 1
    elif YDirection is 2:
        Y = Y + 1
    if XDirection is 1:
        X = X - 1
    elif XDirection is 2:
        X = X + 1
    execfile("Character.py")
    screen.fill(White)
    screen.blit(Background, (X, Y))
    screen.blit(Character2, ((Width / 2 - 32), (Height / 2 - 32)))

    pygame.display.flip()

pygame.QUIT()      #When Running is not true it will quit
sys.exit()