import pygame
import sys
from pygame.locals import *

Running = True

Width = 1280
Height = 720

GameOverScreen = pygame.image.load("Art-assets/GameOverScreen.png")

screen = pygame.display.set_mode((Width, Height), pygame.FULLSCREEN)
screen.blit(GameOverScreen,(0,0))
pygame.display.flip()

while Running:
    for event in pygame.event.get():
        if event.type == QUIT:
            Running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            Running = False

pygame.quit()
sys.exit()