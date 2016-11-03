import pygame
import sys
from pygame.locals import *

pygame.init()

# Needed for the main loop
Running = True

# Screen size
Width = 1280
Height = 720

# For the character movement and map tracking
Y = 0
X = 0

CharacterSpeed = 5

# For the paintball spawn
BallSpawn = False

# Defining colours for later use
White = (255,255,255)
Red = (255,100,100)

# Importing the art
Background = pygame.image.load("maptest.png")
Character = pygame.image.load("character2.png")     #
RoombaModel = pygame.image.load("Art-assets/Roomba (passive).png")

# Draws the screen
screen = pygame.display.set_mode((Width, Height))

# Adds the clock
Clock = pygame.time.Clock()


class Roomba:
    def __init__(self):
        # Choose a position
        self.pos_x = X
        self.pos_y = Y

        # Choose a speed
        self.speed_x = 0
        self.speed_y = 2

        self.rotate = 0


    def update(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        # Turn around
        if self.pos_x < 0 or self.pos_x > Width:
            self.speed_x = -self.speed_x
            self.rotate += 180

        if self.pos_y < 0 or self.pos_y > Height:
            self.speed_y = -self.speed_y
            self.rotate += 180

    def draw(self):
        # Draws the roomba
        RoombaRotate = pygame.transform.rotate(RoombaModel, self.rotate)
        screen.blit(RoombaRotate, (X + self.pos_x, Y + self.pos_y))

# List of Roomba's
roombas = []


# Create roombas
num_roombas = 1
for ball_index in xrange(num_roombas):
    new_roomba = Roomba()
    roombas.append(new_roomba)

# MainLoop
while Running:
    Clock.tick(60)

    pressed = pygame.key.get_pressed()

    # Character movement
    if pressed[pygame.K_w]:
        Y += CharacterSpeed
    if pressed[pygame.K_s]:
        Y -= CharacterSpeed
    if pressed[pygame.K_a]:
        X += CharacterSpeed
    if pressed[pygame.K_d]:
        X -= CharacterSpeed

    for event in pygame.event.get():
            if event.type == QUIT:
                Running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                Running = False


    # Executes the Character python file
    execfile("Character.py")

    # Updates the positions on the screen
    screen.fill(White)
    screen.blit(Background, (X, Y))
    screen.blit(Character2, (Width/2 - 32, Height/2 - 32))

    # Draws the Roomba's
    for roomba in roombas:
        roomba.update()
        roomba.draw()

    # Draws a paintball if conditions are met
    if BallSpawn is True:
        pygame.draw.circle(screen, Red, BallPos, 5)

    # Updates the display
    pygame.display.flip()


# When Running is not true it will quit
pygame.quit()
sys.exit()