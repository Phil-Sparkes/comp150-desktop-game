import pygame
import sys
from pygame.locals import *

Running = True

Width = 1280
Height = 720

TitleScreen = pygame.image.load("TitleScreen/TitleScreen.png")
PlayButton = pygame.image.load("TitleScreen/PlayButton.png")
PlayButtonGlow = pygame.image.load("TitleScreen/PlayButtonGlow.png")
TitleScreenScale = pygame.transform.scale(TitleScreen, (Width, Height))

screen = pygame.display.set_mode((Width, Height))

while Running:
    screen.blit(TitleScreenScale, (0, 0))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if 580 < mouse_x < 730 and 380 < mouse_y < 420:
        screen.blit(PlayButtonGlow, (560, 350))
        mouse_press = pygame.mouse.get_pressed()[0]
        if mouse_press == 1:
            execfile("Main.py")
    else:
        screen.blit(PlayButton, (560, 350))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            Running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            Running = False


pygame.quit()
sys.exit()
