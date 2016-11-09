import pygame
import sys
import random
from pygame.locals import *

pygame.init()

# Needed for the main loop
Running = True

# Screen size
Width = 1280
Height = 720

CharacterPos = (Width/2, Height/2)

temptime = 0

# For the character movement and map tracking
Y = 0
X = 0

CharacterSpeed = 5

# Defining colours for later use
White = (255, 255, 255)
Red = (255, 0, 0)
Green = (0, 255, 0)
Blue = (0, 0, 255)
Yellow = (255, 255, 0)
Black = (0, 0, 0)

# Rectangles
rect = (0, 650, 70, 70)
rect2 = (80, 650, 70, 70)
rect3 = (160, 650, 70, 70)

# For the paintball spawn
BallSpawn = False
BallColour = Red

# Item Counters
paintballammocounter = 9
paintgrenadecounter = 0
rubbishcounter = 0

# Font
Textfont = pygame.font.SysFont("impact", 60)

# Importing the art
Background = pygame.image.load("maptest.png")
Character = pygame.image.load("Art-assets/Character.png")
RoombaModel = pygame.image.load("Art-assets/Roomba (passive) hitbox reduced.png")
Rubbishart = pygame.image.load("Art-assets/Rubbish.png")
Paintballammo = pygame.image.load("Art-assets/Ammo.png")
Paintgrenade = pygame.image.load("Art-assets/Grenade.png")

# Draws the screen
screen = pygame.display.set_mode((Width, Height))

# Adds the clock
Clock = pygame.time.Clock()

class Items:
    """Class for the items"""
    def __init__(self, xpos, ypos, itemkind):
        self.pos_x = xpos
        self.pos_y = ypos
        self.item = itemkind

    def draw(self):
        if self.item == 1:
            screen.blit(Rubbishart, (X + self.pos_x, Y + self.pos_y))
        if self.item == 0:
            screen.blit(Paintballammo, (X + self.pos_x, Y + self.pos_y))
        if self.item == 2:
            screen.blit(Paintgrenade, (X + self.pos_x, Y + self.pos_y))

    def update(self):
        # Player collision with item
        if CharacterPos[0] - 64 < X + self.pos_x < CharacterPos[0] + 64:
            if CharacterPos[1] - 64 < Y + self.pos_y < CharacterPos[1] + 64:
                listItems.remove(self)
                return self.item


class Roomba:
    def __init__(self, x_pos, y_pos, distance, rotation):
        # Choose a position
        self.pos_x = x_pos
        self.pos_y = y_pos

        self.start_x = x_pos
        self.start_y = y_pos

        self.dest_x = x_pos + distance
        self.dest_y = y_pos + distance

        self.rotate = rotation

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
        roomba_rotate = pygame.transform.rotate(RoombaModel, self.rotate)
        screen.blit(roomba_rotate, (X + self.pos_x, Y + self.pos_y))


def wall_check(direction):
    """Checks if wall in direction player is going, False if wall, True if not"""
    if direction == "up":
        colour = screen.get_at((Width/2, Height/2 - 30))
        if colour == (0, 0, 0, 255):
            return False
    if direction == "down":
        colour = screen.get_at((Width/2, Height/2 + 30))
        if colour == (0, 0, 0, 255):
            return False
    if direction == "left":
        colour = screen.get_at((Width/2 - 30, Height/2))
        if colour == (0, 0, 0, 255):
            return False
    if direction == "right":
        colour = screen.get_at((Width/2 + 30, Height/2))
        if colour == (0, 0, 0, 255):
            return False
    return True

# List of Roomba's
roombas = []

# List of Items
listItems = []

# Create items
Paintballammo1 = Items(400, 400, 0)
listItems.append(Paintballammo1)

Paintballammo2 = Items(0, 400, 0)
listItems.append(Paintballammo2)

Rubbish1 = Items(0, 0, 1)
listItems.append(Rubbish1)

Paintgrenade1 = Items(300, 300, 2)
listItems.append(Paintgrenade1)

# Create roombas
Roomba1 = Roomba(0, 0, 200, 90)
roombas.append(Roomba1)

Roomba2 = Roomba(600, -400, 500, 90)
roombas.append(Roomba2)

Roomba3 = Roomba(200, -200, 300, 0)
roombas.append(Roomba3)

Roomba4 = Roomba(500, 800, 1000, 90)
roombas.append(Roomba4)

Roomba5 = Roomba(400, -400, 400, 0)
roombas.append(Roomba5)

Roomba6 = Roomba(500, -400, 300, 0)
roombas.append(Roomba6)

# MainLoop
while Running:
    Clock.tick(60)

    pressed = pygame.key.get_pressed()

    # Character movement
    if pressed[pygame.K_w] and wall_check("up"):
        Y += CharacterSpeed
    if pressed[pygame.K_s] and wall_check("down"):
        Y -= CharacterSpeed
    if pressed[pygame.K_a] and wall_check("left"):
        X += CharacterSpeed
    if pressed[pygame.K_d] and wall_check("right"):
        X -= CharacterSpeed


    # Quit
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

    # Updates the text
    Fontimg = Textfont.render(str(paintballammocounter), 1, Yellow)
    Fontimg2 = Textfont.render(str(rubbishcounter), 1, Yellow)
    Fontimg3 = Textfont.render(str(paintgrenadecounter), 1, Yellow)

    # centers the text
    if paintballammocounter > 9:
        fontcenter = 10
    else:
        fontcenter = 20

    # Draw the characters
    screen.blit(Character2, (Width/2 - 32, Height/2 - 32))

    # Draws the Roombas
    for roomba in roombas:
        roomba.update()
        roomba.draw()

    # Draws the Items and keeps track of how many the player has
    for item in listItems:
        item.draw()
        itemcounter = item.update()
        if itemcounter == 0:
            paintballammocounter += 3
        if itemcounter == 1:
            rubbishcounter += 1
        if itemcounter == 2:
            paintgrenadecounter += 1

    # Draws a paintball if conditions are met
    if BallSpawn is True:
        pygame.draw.circle(screen, BallColour, BallPos, 5)

    # Draws the HUD
    pygame.draw.rect(screen, Black, rect)
    pygame.draw.rect(screen, Black, rect2)
    pygame.draw.rect(screen, Black, rect3)

    # Draw the text
    screen.blit(Fontimg, (fontcenter, 650))
    screen.blit(Fontimg2, (100, 650))
    screen.blit(Fontimg3, (180, 650))

    # Draw the icons
    screen.blit(Paintballammo, (3, 580))
    screen.blit(Rubbishart, (83, 580))
    screen.blit(Paintgrenade, (163, 580))

    # Updates the display
    pygame.display.flip()


# When Running is not true it will quit
pygame.quit()
sys.exit()
