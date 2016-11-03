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
    def __init__(self, Xpos, Ypos, Distance, Rotation):
        # Choose a position
        self.pos_x = Xpos
        self.pos_y = Ypos

        self.start_x = Xpos
        self.start_y = Ypos

        self.dest_x = Xpos + Distance
        self.dest_y = Ypos + Distance

        self.rotate = Rotation

        # Choose a speed
        if self.rotate == 90 or self.rotate == 270:
            self.speed_x = 2
            self.speed_y = 0
        else:
            self.speed_x = 0
            self.speed_y = 2



    def update(self):

        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        # Turn around

        if self.pos_x < self.start_x or self.pos_x > self.dest_x:
            self.speed_x = -self.speed_x
            self.rotate += 180

        if self.pos_y < self.start_y or  self.pos_y > self.dest_y:
            self.speed_y = -self.speed_y
            self.rotate += 180

    def draw(self):
        # Draws the roomba
        RoombaRotate = pygame.transform.rotate(RoombaModel, self.rotate)
        screen.blit(RoombaRotate, (X + self.pos_x, Y + self.pos_y))

# List of Roomba's
roombas = []


# Create roombas
Roomba1 = Roomba(0 ,0, 200, 90)
roombas.append(Roomba1)

Roomba2 = Roomba(600, -400, 500, 0)
roombas.append(Roomba2)

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