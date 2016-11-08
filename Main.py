import pygame
import sys
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

# For the paintball spawn
BallSpawn = False

# Defining colours for later use
White = (255,255,255)
Red = (255,100,100)
Black =(0,0,0)

# Item Counters
paintballammocounter = 9
paintgrenadecounter = 0
rubbishcounter = 0

Textfont = pygame.font.SysFont("impact", 60)
Fontimg = Textfont.render(str(paintballammocounter), 1, Red)


# Importing the art
Background = pygame.image.load("maptest.png")
Character = pygame.image.load("Art-assets/Character.png")
RoombaModel = pygame.image.load("Art-assets/Roomba (passive) hitbox reduced.png")
Rubbishart = pygame.image.load("Art-assets/Roomba (passive) hitbox reduced.png")
Paintballammo = pygame.image.load("Art-assets/Roomba (hostile) hitbox reduced.png")
Paintgrenade = pygame.image.load("character2.png")

# Draws the screen
screen = pygame.display.set_mode((Width, Height))

# Adds the clock
Clock = pygame.time.Clock()


class Items:
    """Class for the items"""
    def __init__(self, Xpos, Ypos, itemkind):
        self.pos_x = Xpos
        self.pos_y = Ypos
        self.item = itemkind

    def draw(self):
        if self.item == 1:
            screen.blit(Rubbishart, (X + self.pos_x, Y + self.pos_y))
        if self.item == 0:
            screen.blit(Paintballammo, (X + self.pos_x, Y + self.pos_y))
        if self.item == 2:
            screen.blit(Paintgrenade, (X + self.pos_x, Y + self.pos_y))

    def update(self):
        if CharacterPos[0]-64<X + self.pos_x<CharacterPos[0]+64:
            if CharacterPos[1]-64<Y + self.pos_y<CharacterPos[1]+64:
                listItems.remove(self)
                return self.item


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
Roomba1 = Roomba(0 ,0, 200, 90)
roombas.append(Roomba1)

Roomba2 = Roomba(600, -400, 500, 0)
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
    rect = (0, 650, 70, 70)
    pygame.draw.rect(screen, Black, rect)
    Fontimg = Textfont.render(str(paintballammocounter), 1, Red)
    screen.blit(Fontimg, (10, 650))

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
        pygame.draw.circle(screen, Red, BallPos, 5)

    # Updates the display
    pygame.display.flip()


# When Running is not true it will quit
pygame.quit()
sys.exit()