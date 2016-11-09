import pygame
import sys
import random
import math
from pygame.locals import *

pygame.init()

# Needed for the main loop
Running = True

# Screen size
Width = 1280
Height = 720

CharacterPos = (Width/2, Height/2)

# Used for delay between shooting paintballs
TempTime = 0

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
Nothing = (0,0,0,0)

# Rectangles
rect = (0, 650, 70, 70)
rect2 = (80, 650, 70, 70)
rect3 = (160, 650, 70, 70)

# Font
TextFont = pygame.font.SysFont("impact", 60)

# Importing the art
Background = pygame.image.load("maptest.png")
CharacterModel = pygame.image.load("Art-assets/Character.png")
RoombaModel = pygame.image.load("Art-assets/Roomba (passive) hitbox reduced.png")
RubbishArt = pygame.image.load("Art-assets/Rubbish.png")
PaintballAmmo = pygame.image.load("Art-assets/Ammo.png")
PaintGrenade = pygame.image.load("Art-assets/Grenade.png")

# Draws the screen
screen = pygame.display.set_mode((Width, Height))

# Adds the clock
Clock = pygame.time.Clock()


class CharacterClass:
    def __init__(self):
        self.pos_x = Width / 2
        self.pos_y = Height / 2

        # Player rotation
        self.rotation = 0

        # Item counters
        self.paint_ball_ammo = 9
        self.paint_grenade = 0
        self.rubbish = 0

        # Paintball properties
        self.ball_position = (self.pos_x, self.pos_y)
        self.ball_spawn = False
        self.ball_speed = (0, 0)
        self.ball_colour = Red

    def rotate(self):
        """Rotates the player to follow the mouse"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x2 = mouse_x - self.pos_x
        mouse_y2 = mouse_y - self.pos_y
        self.rotation = (math.atan2(mouse_x2, mouse_y2) * 57.2958) + 180

    def shoot_paint_ball(self, TempTime):
        """Shoots the paintball gun"""
        mouse_press = pygame.mouse.get_pressed()[0]
        if not pygame.time.get_ticks() - 500 < TempTime:
            if mouse_press == 1:
                if self.paint_ball_ammo > 0:
                    # Decreases the ammo count
                    self.paint_ball_ammo -= 1
                    self.ball_spawn = True

                    # Sets the colour of the ball
                    self.ball_colour = random.choice([Red, Green, Blue, Yellow])

                    # Gets the initial position of the ball
                    self.ball_position = (self.pos_x, self.pos_y)

                    # Creates a vector
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    vector = sub((mouse_x, mouse_y), self.ball_position)

                    # Gets the sum of the vector and divides by 20
                    vector_total = ((math.sqrt(vector[0] ** 2)) + (math.sqrt(vector[1] ** 2))) / 20

                    # Divides the vector by this new vector
                    vector = (vector[0] / vector_total), (vector[1] / vector_total)

                    # Generates the ball speed as a result
                    self.ball_speed = (int(vector[0]), (int(vector[1])))

                    TempTime = pygame.time.get_ticks()

        return TempTime

    def update(self):
        if self.ball_spawn is True:
            # Updates the position of the ball
            self.ball_position = (self.ball_position[0] + self.ball_speed[0]), (self.ball_position[1] + self.ball_speed[1])

        # Draws the character
        character_rotation = pygame.transform.rotate(CharacterModel, self.rotation)
        screen.blit(character_rotation, (Width / 2 - 32, Height / 2 - 32))

        # Draws the Items and keeps track of how many the player has
        for item in listItems:
            item.draw()
            item_counter = item.update()
            if item_counter == 0:
                self.paint_ball_ammo += 3
            if item_counter == 1:
                self.rubbish += 1
            if item_counter == 2:
                self.paint_grenade += 1

        # Draws a paintball if conditions are met
        if self.ball_spawn is True:
            pygame.draw.circle(screen, self.ball_colour, self.ball_position, 5)

        # Draws the HUD
        pygame.draw.rect(screen, Black, rect)
        pygame.draw.rect(screen, Black, rect2)
        pygame.draw.rect(screen, Black, rect3)

        # Updates the text
        fontimg = TextFont.render(str(self.paint_ball_ammo), 1, Yellow)
        fontimg2 = TextFont.render(str(self.rubbish), 1, Yellow)
        fontimg3 = TextFont.render(str(self.paint_grenade), 1, Yellow)

        # centers the text
        if self.paint_ball_ammo > 9:
            font_center = 10
        else:
            font_center = 20

        # Draw the text
        screen.blit(fontimg, (font_center, 650))
        screen.blit(fontimg2, (100, 650))
        screen.blit(fontimg3, (180, 650))

        # Draw the icons
        screen.blit(PaintballAmmo, (3, 580))
        screen.blit(RubbishArt, (83, 580))
        screen.blit(PaintGrenade, (163, 580))

    def player_movement(self, x, y):
        """Player movement, returns an X and Y value"""
        # Checks what keys are being pressed
        pressed = pygame.key.get_pressed()

        # Direction character is moving in
        if pressed[pygame.K_w] and wall_check("up"):
            y += CharacterSpeed
        if pressed[pygame.K_s] and wall_check("down"):
            y -= CharacterSpeed
        if pressed[pygame.K_a] and wall_check("left"):
            x += CharacterSpeed
        if pressed[pygame.K_d] and wall_check("right"):
            x -= CharacterSpeed

        return x, y


class Items:
    """Class for the items"""
    def __init__(self, xpos, ypos, itemkind):
        self.pos_x = xpos
        self.pos_y = ypos
        self.item = itemkind

    def draw(self):
        """draws the items on the screen"""
        if self.item == 1:
            screen.blit(RubbishArt, (X + self.pos_x, Y + self.pos_y))
        if self.item == 0:
            screen.blit(PaintballAmmo, (X + self.pos_x, Y + self.pos_y))
        if self.item == 2:
            screen.blit(PaintGrenade, (X + self.pos_x, Y + self.pos_y))

    def update(self):
        """detects collision with the player"""
        if CharacterPos[0] - 64 < X + self.pos_x < CharacterPos[0] + 64:
            if CharacterPos[1] - 64 < Y + self.pos_y < CharacterPos[1] + 64:
                # Removes the item from the list
                listItems.remove(self)
                # Returns a value corresponding to the item picked up
                return self.item


class Roomba:
    def __init__(self, x_pos, y_pos, distance, rotation):
        """Roomba class takes:
        x and y coordinates for starting position
        distance for how far it travels
        rotation for which way it goes"""
        self.pos_x = x_pos
        self.pos_y = y_pos

        self.start_x = x_pos
        self.start_y = y_pos

        self.dest_x = x_pos + distance
        self.dest_y = y_pos + distance

        self.rotate = rotation

        # Which direction the roomba is going in
        if self.rotate == 90 or self.rotate == 270:
            self.speed_x = 2
            self.speed_y = 0
        else:
            self.speed_x = 0
            self.speed_y = 2

    def update(self):

        # Changes the position depending on the speed

        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        # Turn around

        if self.pos_x < self.start_x or self.pos_x > self.dest_x:
            self.speed_x = -self.speed_x
            self.rotate += 180

        if self.pos_y < self.start_y or self.pos_y > self.dest_y:
            self.speed_y = -self.speed_y
            self.rotate += 180

    def draw(self):
        """Draws the Roomba's"""
        roomba_rotate = pygame.transform.rotate(RoombaModel, self.rotate)
        screen.blit(roomba_rotate, (X + self.pos_x, Y + self.pos_y))

    def collision(self):
        """Checks for collision with the player"""
        if CharacterPos[0] - 50 < X + self.pos_x + 47 < CharacterPos[0] + 50:
            if CharacterPos[1] - 50 < Y + self.pos_y + 47 < CharacterPos[1] + 50:
                print "game over"

    def detect(self):
        """Checks if roomba detects player"""
        if self.speed_y == 2:
            #area = (X + self.pos_x - 107, Y + self.pos_y + 30, 296, 390)
            if X + self.pos_x - 107 < CharacterPos[0] < X + self.pos_x + 283:
                if Y + self.pos_y + 30 < CharacterPos[1] < Y + self.pos_y + 420:
                    print "detected down"
                    return True
        if self.speed_y == -2:
            #area = (X + self.pos_x - 107, Y + self.pos_y + 90, 296, -390)
            if X + self.pos_x - 107 < CharacterPos[0] < X + self.pos_x + 283:
                if Y + self.pos_y - 300 < CharacterPos[1] < Y + self.pos_y + 90:
                    print "detected up"
                    return True
        if self.speed_x == 2:
            #area = (X + self.pos_x + 30, Y + self.pos_y - 107, 390, 296)
            if X + self.pos_x + 30 < CharacterPos[0] < X + self.pos_x + 420:
                if Y + self.pos_y - 107 < CharacterPos[1] < Y + self.pos_y + 189:
                    print "detected right"
                    return True
        if self.speed_x == -2:
            #area = (X + self.pos_x + 90, Y + self.pos_y - 107, -390, 296)
            if X + self.pos_x - 300 < CharacterPos[0] < X + self.pos_x + 90:
                if Y + self.pos_y - 107 < CharacterPos[1] < Y + self.pos_y + 189:
                    print "detected left"
                    return True
        #pygame.draw.rect(screen, Red, area)


def wall_check(direction):
    """Checks if wall in direction player is going, False if wall, True if not"""
    check_distance = 40
    if direction == "up":
        colour = screen.get_at((Width/2, Height/2 - check_distance))
        if colour == (0, 0, 0, 255):
            return False
    if direction == "down":
        colour = screen.get_at((Width/2, Height/2 + check_distance))
        if colour == (0, 0, 0, 255):
            return False
    if direction == "left":
        colour = screen.get_at((Width/2 - check_distance, Height/2))
        if colour == (0, 0, 0, 255):
            return False
    if direction == "right":
        colour = screen.get_at((Width/2 + check_distance, Height/2))
        if colour == (0, 0, 0, 255):
            return False
    return True


def sub(u, v):
    """Function for finding the vector"""
    return [u[i]-v[i] for i in range(len(u))]

# List of Roomba's
roombas = []

# List of Items
listItems = []

# Create character
PlayCharacter = CharacterClass()

# Create items
Paintball_ammo1 = Items(400, 400, 0)
listItems.append(Paintball_ammo1)

Paintball_ammo2 = Items(0, 400, 0)
listItems.append(Paintball_ammo2)

Rubbish1 = Items(0, 0, 1)
listItems.append(Rubbish1)

Paint_grenade1 = Items(300, 300, 2)
listItems.append(Paint_grenade1)

# Create roombas
Roomba1 = Roomba(0, 0, 200, 90)
roombas.append(Roomba1)

Roomba2 = Roomba(600, -400, 500, 90)
roombas.append(Roomba2)

Roomba3 = Roomba(200, -200, 300, 0)
roombas.append(Roomba3)

Roomba4 = Roomba(500, 800, 1000, 90)
roombas.append(Roomba4)

# MainLoop
while Running:
    Clock.tick(60)

    # Updates character position
    X, Y = PlayCharacter.player_movement(X, Y)

    # Quit
    for event in pygame.event.get():
            if event.type == QUIT:
                Running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                Running = False

    # Function for shooting the paintballs
    TempTime = PlayCharacter.shoot_paint_ball(TempTime)

    # Updates the positions on the screen
    screen.fill(White)
    screen.blit(Background, (X, Y))

    # Draws the Roombas
    for roomba in roombas:
        roomba.update()
        roomba.draw()
        roomba.collision()
        roomba.detect()

    # Rotates the Charcter
    PlayCharacter.rotate()
    # Updates the Character and the HUD
    PlayCharacter.update()

    # Updates the display
    pygame.display.flip()


# When Running is not true it will quit
pygame.quit()
sys.exit()
