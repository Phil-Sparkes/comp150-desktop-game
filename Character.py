import pygame

pygame.transform.rotate(Character, 90)
pygame.display.flip()

(MouseX, MouseY) = pygame.mouse.get_pos()
MouseX = MouseX / 7.11111111111111111111111111111111

if MouseY < 360:
    MouseX = 360 - MouseX

Character2 = pygame.transform.rotate(Character, MouseX + 90)


