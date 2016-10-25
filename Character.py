import pygame
screen.blit(Character, ((Width/2 - 32), (Height/2 - 32)))
pygame.transform.rotate(Character, 90)
pygame.display.flip()

(MouseX, MouseY) = pygame.mouse.get_pos()


print MouseX
print MouseY