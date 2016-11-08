import pygame
import sys
from pygame.locals import *

Running = True

Width = 1280
Height = 720

TitleScreen = pygame.image.load("TitleScreen.png")

TitleScreen2 = pygame.transform.scale(TitleScreen, (Width, Height))

screen = pygame.display.set_mode((Width, Height))
screen.blit(TitleScreen2,(0,0))
pygame.display.flip()

while Running:
    for event in pygame.event.get():
        if event.type == QUIT:
            Running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            Running = False
        if event.type == KEYDOWN and event.key == K_RETURN:
            execfile("Main.py")

pygame.quit()
sys.exit()