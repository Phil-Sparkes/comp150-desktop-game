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

# Used for delay between shooting paintballs and grenades
PaintBallDelay = 0
GrenadeDelay = 0

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

# Font
TextFont = pygame.font.SysFont("impact", 60)

# Importing the art
Background = pygame.image.load("maptest.png")
CharacterModel = pygame.image.load("character2.png")
RoombaModel = pygame.image.load("Art-assets/RoombaBlue.png")
RoombaModelHostile = pygame.image.load("Art-assets/RoombaRed.png")
RubbishArt = pygame.image.load("Art-assets/Rubbish.png")
PaintballAmmo = pygame.image.load("Art-assets/Ammo.png")
PaintGrenade = pygame.image.load("Art-assets/Grenade.png")

BananaPeel = pygame.image.load("Art-assets/Rubbish\Banana peel.png")
BeerBottle = pygame.image.load("Art-assets/Rubbish/Beer bottle.png")
WaterBottle = pygame.image.load("Art-assets/Rubbish/Bottle.png")
GarbageCan = pygame.image.load("Art-assets/Rubbish/Garbage can.png")
RustyCan = pygame.image.load("Art-assets/Rubbish/Rusty Can.png")

# Draws the screen
screen = pygame.display.set_mode((Width, Height))

# Adds the clock
Clock = pygame.time.Clock()


class CharacterClass:
    def __init__(self):
        # positions the player in the center of the screen
        self.pos_x = Width / 2
        self.pos_y = Height / 2

        # Player rotation
        self.rotation = 0

        # Item counters
        self.paint_ball_ammo = 9
        self.paint_grenade = 5
        self.rubbish = 0

        # Paintball properties
        self.ball_position = (self.pos_x, self.pos_y)
        self.ball_spawn = False
        self.ball_speed = (0, 0)
        self.ball_colour = Red

        # Paint Grenade properties
        self.grenade_position = (self.pos_x, self.pos_y)
        self.grenade_spawn = False
        self.grenade_speed = (0, 0)
        self.grenade_timer = 0

    def rotate(self):
        """Rotates the player to follow the mouse"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x2 = mouse_x - self.pos_x
        mouse_y2 = mouse_y - self.pos_y
        self.rotation = (math.atan2(mouse_x2, mouse_y2) * 57.2958) + 180

    def update(self):
        if self.ball_spawn:
            # Updates the position of the ball
            self.ball_position = (self.ball_position[0] +  self.ball_speed[0]), (self.ball_position[1] + self.ball_speed[1])
            self.paintball_hit()

        if self.grenade_spawn:
            # Updates the position of the grenade
            self.grenade_position = (self.grenade_position[0] + self.grenade_speed[0]), (self.grenade_position[1] + self.grenade_speed[1])

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
        if self.ball_spawn:
            pygame.draw.circle(screen, self.ball_colour, self.ball_position, 5)

        if self.grenade_spawn:
            # Paint grenades will last for 700 ticks before disapearing
            if pygame.time.get_ticks() - 700 > self.grenade_timer:
                self.grenade_spawn = False
                self.grenade_explosion()
                # Draws paint grenade
            pygame.draw.circle(screen, Red, self.grenade_position, 15)

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
        screen.blit(GarbageCan, (83, 580))
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

    def shoot_paint_ball(self, PaintBallDelay):
        """Shoots the paintball gun"""
        mouse_press = pygame.mouse.get_pressed()[0]
        if not pygame.time.get_ticks() - 500 < PaintBallDelay:
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

                    # Gets the sum of the vector and divides by 20 (increases the speed)
                    vector_total = ((math.sqrt(vector[0] ** 2)) + (math.sqrt(vector[1] ** 2))) / 20

                    # Divides the vector by this new vector
                    vector = (vector[0] / vector_total), (vector[1] / vector_total)

                    # Generates the ball speed as a result
                    self.ball_speed = (int(vector[0]), (int(vector[1])))

                    PaintBallDelay = pygame.time.get_ticks()

        return PaintBallDelay

    def paintball_hit(self):
        """Checks if paintball comes into contact with a Roomba"""
        for roomba in roombas:
            if roomba.pos_x + X < self.ball_position[0] < roomba.pos_x + X + 64:
                if roomba.pos_y + Y < self.ball_position[1] < roomba.pos_y + Y + 64:
                    print "hit"

    def paint_grenade_throw(self, GrenadeDelay):
        """Code for throwing paint grenades"""
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE] and self.paint_grenade > 0 and self.grenade_spawn is False:
            if not pygame.time.get_ticks() - 1000 < GrenadeDelay:
                    # Decreases the grenade count
                    self.paint_grenade -= 1
                    self.grenade_spawn = True

                    # Gets the initial position of the grenade
                    self.grenade_position = (self.pos_x, self.pos_y)

                    # Creates a vector
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    vector = sub((mouse_x, mouse_y), self.grenade_position)

                    # Gets the sum of the vector and divides by 10 (increases the speed)
                    vector_total = ((math.sqrt(vector[0] ** 2)) + (math.sqrt(vector[1] ** 2))) / 10

                    # Divides the vector by this new vector
                    vector = (vector[0] / vector_total), (vector[1] / vector_total)

                    # Generates the ball speed as a result
                    self.grenade_speed = (int(vector[0]), (int(vector[1])))

                    GrenadeDelay = pygame.time.get_ticks()

                    # takes the current tick so it can explode after 700 more ticks
                    self.grenade_timer = pygame.time.get_ticks()

        return GrenadeDelay

    def grenade_explosion(self):
        """The explosion of the grenade"""
        # draws a rectangle for the blast radius
        GrenadeExplosion = (self.grenade_position[0] - 200, self.grenade_position[1] - 200, 400, 400)
        pygame.draw.rect(screen, Yellow, GrenadeExplosion)
        # checks for roombas caught in the explosion
        for roomba in roombas:
            if roomba.pos_x + X - 200 < self.grenade_position[0]< roomba.pos_x + X + 200:
                if roomba.pos_y + Y - 200 < self.grenade_position[1] < roomba.pos_y + Y + 200:
                    print "Ka-boom!"
                    roombas.remove(roomba)

class Items:
    """Class for the items"""
    def __init__(self, xpos, ypos, itemkind):
        self.pos_x = xpos
        self.pos_y = ypos
        self.item = itemkind
        self.detected = False

        # selects a random rubbish item
        rubbish_types = (BananaPeel, BeerBottle, WaterBottle, RustyCan)
        self.random_rubbish = (random.choice(rubbish_types))

    def draw(self):
        """draws the items on the screen"""
        if self.item == 1:
            screen.blit(self.random_rubbish, (X + self.pos_x, Y + self.pos_y))
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

        self.detect = 0

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

        if self.pos_y < self.start_y or self.pos_y > self.dest_y:
            self.speed_y = -self.speed_y


        if self.detect == 1:
            # faces player
            vector = sub((self.pos_x + X, self.pos_y + Y), CharacterPos)
            self.rotate = (math.atan2(vector[0], vector[1]) * 57.2958) + 180

        else:
            # Rotates roomba depending on which direction it's going
            if self.speed_y == 2:
                self.rotate = 0
            elif self.speed_y == -2:
                self.rotate = 180
            elif self.speed_x == 2:
                self.rotate = 90
            elif self.speed_x == -2:
                self.rotate = 270

    def draw(self):
        """Draws the Roomba's, Will draw red roomba if player has been detected"""
        if self.detect == 1 or self.detect == 2:
            roomba_rotate = pygame.transform.rotate(RoombaModelHostile, self.rotate)
        else:
            roomba_rotate = pygame.transform.rotate(RoombaModel, self.rotate)
        screen.blit(roomba_rotate, (X + self.pos_x, Y + self.pos_y))

    def collision(self):
        """Checks for collision with the player"""
        if CharacterPos[0] - 50 < X + self.pos_x + 47 < CharacterPos[0] + 50:
            if CharacterPos[1] - 50 < Y + self.pos_y + 47 < CharacterPos[1] + 50:
                print "game over"

    def detects(self):
        """Checks if roomba detects player or items"""
        # Creates a vector
        vector = sub((self.pos_x + X, self.pos_y + Y), CharacterPos)
        if self.detect == 2:
            for item in listItems:
                pass
                #print item.detected
                #if item.detected:
                #vector = sub((self.pos_x + X, self.pos_y + Y), (item.pos_x, item.pos_y))
                #print "here"
        vector_x = vector[0]
        vector_y = vector[1]
        vector_x += Width/2
        vector_y += Height/2

        # Creates the four points for the roomba cone of view
        point1 = (vector_x - 20, vector_y)
        point2 = (vector_x + 20, vector_y)
        point3 = (vector_x + 150, vector_y + 300)
        point4 = (vector_x - 150, vector_y + 300)

        # Rotates the points for the cone of view
        point1 = rotatePoint((self.pos_x + X, self.pos_y + Y), point1, -self.rotate)
        point2 = rotatePoint((self.pos_x + X, self.pos_y + Y), point2, -self.rotate)
        point3 = rotatePoint((self.pos_x + X, self.pos_y + Y), point3, -self.rotate)
        point4 = rotatePoint((self.pos_x + X, self.pos_y + Y), point4, -self.rotate)

        # moves the cone of view so its centered on the roomba
        point1 = (int(point1[0]) + 32, int(point1[1]) + 32)
        point2 = (int(point2[0]) + 32, int(point2[1]) + 32)
        point3 = (int(point3[0]) + 32, int(point3[1]) + 32)
        point4 = (int(point4[0]) + 32, int(point4[1]) + 32)

        # Creates a polygon out of the points
        area = point1,point2,point3,point4
        # Draws the polygon in red
        pygame.draw.polygon(screen, Red, area)
        # Gets the colour of the pixel at the character position
        detect_player = screen.get_at(CharacterPos)

        # Checks if any items are being detected by each roomba
        for item in listItems:
            if 0 < (X + item.pos_x) < Width:
                if 0 < Y + item.pos_y < Height:
                    detect_item = screen.get_at((X + item.pos_x, Y + item.pos_y))
                    if detect_item == Red:
                        item.detected = True
                    else:
                         item.detected = False

        # Draws the polygon in blue so that its no longer red for the next roomba(otherwise all the roombas detect player when one does)
        pygame.draw.polygon(screen, Blue, area)

        # if a roomba is detecting an item it will return
        for item in listItems:
            if item.detected:
                self.detect = 2
                return

        # Checks if player is detected
        if detect_player == Red:
            self.detect = 1
            return

        # sets to detect to 0 if it hasn't detected anything
        self.detect = 0


def rotatePoint(centerPoint, point, angle):
    """Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0] - centerPoint[0], point[1] - centerPoint[1]
    temp_point = (temp_point[0] * math.cos(angle) - temp_point[1] * math.sin(angle), temp_point[0] * math.sin(angle) + temp_point[1] * math.cos(angle))
    temp_point = temp_point[0] + centerPoint[0], temp_point[1] + centerPoint[1]
    return temp_point
    # http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects


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
Paintball_ammo1 = Items(800, 600, 0)
listItems.append(Paintball_ammo1)

Paintball_ammo2 = Items(800, 500, 0)
listItems.append(Paintball_ammo2)

Rubbish1 = Items(20, 40, 1)
listItems.append(Rubbish1)

Paint_grenade1 = Items(900, 600, 2)
listItems.append(Paint_grenade1)

# Create roombas

Roomba1 = Roomba(0, 0, 200, 90)
roombas.append(Roomba1)

Roomba2 = Roomba(600, -400, 500, 90)
roombas.append(Roomba2)

Roomba3 = Roomba(200, -200, 300, 0)
roombas.append(Roomba3)

Roomba4 = Roomba(500, 800, 300, 0)
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
    PaintBallDelay = PlayCharacter.shoot_paint_ball(PaintBallDelay)
    GrenadeDelay = PlayCharacter.paint_grenade_throw(GrenadeDelay)
    #for roomba in roombas:
        #roomba.update()
        #roomba.detects()
    # Updates the positions on the screen
    screen.fill(White)
    screen.blit(Background, (X, Y))

    # Draws the Roombas
    for roomba in roombas:
        roomba.update()
        roomba.detects()
        roomba.draw()
        roomba.collision()

    # Rotates the Charcter
    PlayCharacter.rotate()
    # Updates the Character and the HUD
    PlayCharacter.update()

    # Updates the display
    pygame.display.flip()


# When Running is not true it will quit
pygame.quit()
sys.exit()
