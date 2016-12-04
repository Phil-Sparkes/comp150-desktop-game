import pygame
import sys
import random
import math
import winsound
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
ProjectileDelay = 0

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
CollisionColour = (81, 10, 1)

# Rectangles
HudBox = [(0, 650, 70, 70), (80, 650, 70, 70), (160, 650, 70, 70)]

# Font
TextFont = pygame.font.SysFont("impact", 60)

# Importing the art
BackgroundLarge = pygame.image.load("Art-assets/Map.png")
Background = pygame.transform.scale(BackgroundLarge, (5000, 5000))
ScientistModel = pygame.image.load("Art-assets/Characters/Scientist.png")
RoombaModel = pygame.image.load("Art-assets/Enemies/Roomba (passive).png")
RoombaModelHostile = pygame.image.load("Art-assets/Enemies/Roomba (hostile).png")
PaintballAmmoIcon = pygame.image.load("Art-assets/Paintgun-ammo/AmmoIcon.png")
PaintballAmmo = pygame.image.load("Art-assets/Paintgun-ammo/Ammo.png")
PaintGrenadeIcon = pygame.image.load("Art-assets/Grenade/Icon.png")
PaintGrenade = pygame.image.load("Art-assets/Grenade/Grenade.png")

BananaPeel = pygame.image.load("Art-assets/Rubbish\Banana peel.png")
BeerBottle = pygame.image.load("Art-assets/Rubbish/Beer bottle.png")
WaterBottle = pygame.image.load("Art-assets/Rubbish/Bottle.png")
GarbageCan = pygame.image.load("Art-assets/Rubbish/Garbage can.png")
RustyCan = pygame.image.load("Art-assets/Rubbish/Rusty Can.png")

CharacterAnim = [(pygame.image.load("Animations/char1.png")),
                 (pygame.image.load("Animations/char2.png")),
                 (pygame.image.load("Animations/char3.png")),
                 (pygame.image.load("Animations/char4.png")),
                 (pygame.image.load("Animations/char5.png"))]


# Draws the screen
screen = pygame.display.set_mode((Width, Height))

# Adds the clock
Clock = pygame.time.Clock()


class CharacterClass:
    def __init__(self):
        # positions the player in the center of the screen
        self.pos_x = Width / 2
        self.pos_y = Height / 2

        # used for animation
        self.moving = False
        self.frame = 0
        self.keyframe = 0

        # Player rotation
        self.rotation = 0

        # Item counters
        self.paint_ball_ammo = 9
        self.paint_grenade = 1
        self.rubbish = 0

        # Paintball properties
        self.ball_position = (self.pos_x, self.pos_y)
        self.ball_spawn = False
        self.ball_speed = (0, 0)
        self.ball_colour = Red

        # Projectile properties
        self.projectile_spawn = False
        self.projectile_position = (self.pos_x, self.pos_y)
        self.projectile_speed = (0, 0)
        self.projectile_timer = 0
        self.projectile_type = ""

        # Paint Grenade properties
        self.grenade_position = (self.pos_x, self.pos_y)
        self.grenade_spawn = False
        self.grenade_speed = (0, 0)
        self.grenade_timer = 0

        # Rubbish properties
        self.rubbish_position = (self.pos_x, self.pos_y)
        self.rubbish_speed = (0, 0)

        self.rubbish_types = (BananaPeel, BeerBottle, WaterBottle, RustyCan)
        self.random_rubbish = (random.choice(self.rubbish_types))

    def rotate(self):
        """Rotates the player to follow the mouse"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x2 = mouse_x - self.pos_x
        mouse_y2 = mouse_y - self.pos_y
        self.rotation = (math.atan2(mouse_x2, mouse_y2) * 57.2958) + 180

    def update(self):
        if self.ball_spawn:
            # Updates the position of the ball
            self.ball_position = (self.ball_position[0] + self.ball_speed[0]),\
                                 (self.ball_position[1] + self.ball_speed[1])
            self.paintball_hit()

            # Checks if collision with wall
            if not self.collision_items(self.ball_speed, self.ball_position):
                self.ball_spawn = False

        if self.projectile_spawn:
            # Updates the position of the projectile
            self.projectile_position = (self.projectile_position[0] + self.projectile_speed[0]),\
                                       (self.projectile_position[1] + self.projectile_speed[1])

            # Checks if collision with wall
            if not self.collision_items(self.projectile_speed, self.projectile_position):
                self.projectile_spawn = False
                if self.projectile_type == "PaintGrenade":
                    self.grenade_explosion()
                else:
                    self.item_drop()

        # Draws the character
        if self.moving:
            self.character_animation()
        character_rotation = pygame.transform.rotate((CharacterAnim[self.keyframe]), self.rotation)
        screen.blit(character_rotation, (Width / 2 - 32, Height / 2 - 32))

        # Draws the Items and keeps track of how many the player has
        for item in listItems:
            item.draw()
            item_counter = item.player_collision()
            if item_counter == 0:
                self.paint_ball_ammo += 3
            if item_counter == 1:
                self.rubbish += 1
            if item_counter == 2:
                self.paint_grenade += 1
            if item_counter == 3:
                self.rubbish += 3

        # Draws a paintball if conditions are met
        if self.ball_spawn:
            pygame.draw.circle(screen, self.ball_colour, self.ball_position, 5)

        if self.projectile_spawn:

            if self.projectile_type == "PaintGrenade":
                # Paint grenades will last for 700 ticks before disapearing
                if pygame.time.get_ticks() - 700 > self.projectile_timer:
                    self.projectile_spawn = False
                    self.grenade_explosion()
                # Draws paint grenade
                screen.blit(PaintGrenade, self.projectile_position)

            if self.projectile_type == "Rubbish":
                # Rubbish will travel for 700 ticks before dropping to the floor

                if pygame.time.get_ticks() - 700 > self.projectile_timer:

                    self.projectile_spawn = False
                    self.item_drop()
                    self.random_rubbish = (random.choice(self.rubbish_types))
                # Draws Rubbish
                screen.blit(self.random_rubbish, self.projectile_position)

        # Updates the text
        hud_text = [(TextFont.render(str(self.paint_ball_ammo), 1, Yellow)),
                    (TextFont.render(str(self.rubbish), 1, Yellow)),
                    (TextFont.render(str(self.paint_grenade), 1, Yellow))]

        # centers the text
        if self.paint_ball_ammo > 9:
            font_center = 10
        else:
            font_center = 20

        # Draws the HUD
        for x in xrange(len(HudBox)):
            pygame.draw.rect(screen, Black, HudBox[x])

        # Draw the text
        screen.blit(hud_text[0], (font_center, 650))
        screen.blit(hud_text[1], (100, 650))
        screen.blit(hud_text[2], (180, 650))

        # Draw the icons
        screen.blit(PaintballAmmoIcon, (3, 580))
        screen.blit(GarbageCan, (83, 580))
        screen.blit(PaintGrenadeIcon, (163, 580))

    def player_movement(self, x, y):
        """Player movement, returns an X and Y value"""
        # Checks what keys are being pressed
        key_pressed = pygame.key.get_pressed()
        self.moving = False
        # Direction character is moving in
        if key_pressed[pygame.K_w] and wall_check("up", CharacterPos[0], CharacterPos[1]):
            y += CharacterSpeed
            self.moving = True
        if key_pressed[pygame.K_s] and wall_check("down", CharacterPos[0], CharacterPos[1]):
            y -= CharacterSpeed
            self.moving = True
        if key_pressed[pygame.K_a] and wall_check("left", CharacterPos[0], CharacterPos[1]):
            x += CharacterSpeed
            self.moving = True
        if key_pressed[pygame.K_d] and wall_check("right", CharacterPos[0], CharacterPos[1]):
            x -= CharacterSpeed
            self.moving = True

        return x, y

    def shoot_paint_ball(self, paint_ball_delay):
        """Shoots the paintball gun"""
        mouse_press = pygame.mouse.get_pressed()[0]
        if not pygame.time.get_ticks() - 500 < paint_ball_delay:
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

                    paint_ball_delay = pygame.time.get_ticks()

        return paint_ball_delay

    def paintball_hit(self):
        """Checks if paintball comes into contact with a Roomba"""
        for roomba in roombas:
            if roomba.pos_x + X < self.ball_position[0] < roomba.pos_x + X + 64:
                if roomba.pos_y + Y < self.ball_position[1] < roomba.pos_y + Y + 64:
                    roomba.delay = 100
                    self.ball_spawn = False
                    return

    def throw_projectile(self, projectile, projectile_delay, projectile_type):
        """Code for throwing projectiles"""
        if not pygame.time.get_ticks() - 1000 < projectile_delay:
            # Decreases the grenade count
            projectile -= 1
            self.projectile_spawn = True
            self.projectile_type = projectile_type

            # Gets the initial position of the projectiles
            self.projectile_position = (self.pos_x, self.pos_y)

            # Creates a vector
            mouse_x, mouse_y = pygame.mouse.get_pos()
            vector = sub((mouse_x, mouse_y), self.projectile_position)

            # Gets the sum of the vector and divides by 10 (increases the speed)
            vector_total = ((math.sqrt(vector[0] ** 2)) + (math.sqrt(vector[1] ** 2))) / 10

            # Divides the vector by this new vector
            vector = (vector[0] / vector_total), (vector[1] / vector_total)

            # Generates the projectile speed as a result
            self.projectile_speed = (int(vector[0]), (int(vector[1])))

            projectile_delay = pygame.time.get_ticks()

            # takes the current tick so it can explode/drop after 700 more ticks
            self.projectile_timer = pygame.time.get_ticks()
        return projectile, projectile_delay

    def grenade_explosion(self):
        """The explosion of the grenade"""
        # draws a rectangle for the blast radius
        pygame.draw.circle(screen, Yellow, self.projectile_position, 200)
        # checks for roombas caught in the explosion
        for roomba in roombas:
            if roomba.pos_x + X - 200 < self.projectile_position[0] < roomba.pos_x + X + 200:
                if roomba.pos_y + Y - 200 < self.projectile_position[1] < roomba.pos_y + Y + 200:
                    roomba.delay = 200

    def item_drop(self):
        # Creates a new rubbish item

        rubbish = Items(self.projectile_position[0] - X, self.projectile_position[1] - Y, 1, self.random_rubbish)
        listItems.append(rubbish)

    def collision_items(self, item_speed, item_pos,):
        """Checks if items (paintballs, grenades and rubbish) are colliding with walls"""
        if item_speed[0] > 0:
            if not wall_check("right", item_pos[0], item_pos[1]):
                return False
        else:
            if not wall_check("left", item_pos[0], item_pos[1]):
                return False
        if item_speed[1] > 0:
            if not wall_check("down", item_pos[0], item_pos[1]):
                return False
        else:
            if not wall_check("up", item_pos[0], item_pos[1]):
                return False

        return True

    def character_animation(self):
        self.frame += 1

        if self.frame > 5:
            self.keyframe += 1
            self.frame = 0

        if self.keyframe == 5:
            self.keyframe = 0


class Items:
    """Class for the items"""
    def __init__(self, xpos, ypos, item_kind, rubbish_type):
        self.pos_x = xpos
        self.pos_y = ypos
        self.item = item_kind
        self.detected = False
        self.rubbish_type = rubbish_type

        # selects a random rubbish item
        rubbish_types = (BananaPeel, BeerBottle, WaterBottle, RustyCan)
        if self.rubbish_type == "":
            self.rubbish_type = (random.choice(rubbish_types))

    def draw(self):
        """draws the items on the screen"""
        if self.item == 0:
            screen.blit(PaintballAmmo, (X + self.pos_x, Y + self.pos_y))
        if self.item == 1:
            screen.blit(self.rubbish_type, (X + self.pos_x, Y + self.pos_y))
        if self.item == 2:
            screen.blit(PaintGrenade, (X + self.pos_x, Y + self.pos_y))
        if self.item == 3:
            screen.blit(GarbageCan, (X + self.pos_x, Y + self.pos_y))

    def player_collision(self):
        """detects collision with the player"""
        if CharacterPos[0] - 64 < X + self.pos_x < CharacterPos[0] + 64:
            if CharacterPos[1] - 64 < Y + self.pos_y < CharacterPos[1] + 64:
                # Removes the item from the list
                listItems.remove(self)
                # Returns a value corresponding to the item picked up
                return self.item

    def roomba_collision(self, roomba):
        """detects collision with roombas"""
        if roomba.pos_x - 64 + X < X + self.pos_x < roomba.pos_x + 64 + X:
            if roomba.pos_y - 64 + Y < Y + self.pos_y < roomba.pos_y + 64 + Y:
                # Removes the item from the list
                try:
                    listItems.remove(self)
                except:
                    pass


class Roomba:
    def __init__(self, x_pos, y_pos, distance_x, distance_y):
        """Roomba class takes:
        x and y coordinates for starting position
        distance for how far it travels
        rotation for which way it goes"""
        self.pos_x = x_pos
        self.pos_y = y_pos

        self.start_x = x_pos
        self.start_y = y_pos

        self.speed_y = 0
        self.speed_x = 0

        self.dest_x = x_pos + distance_x
        self.dest_y = y_pos + distance_y

        self.rotate = 0

        self.item_detected = 0
        self.detect = 0
        self.returning = False

        self.delay = 0
        self.switch = True

    def move(self):
        if self.switch:
            if self.move_towards_point((self.dest_x + X, self.dest_y + Y)):
                self.switch = False
        else:
            if self.move_towards_point((self.start_x + X, self.start_y + Y)):
                self.switch = True

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
                execfile("Game over screen.py")

    def detects(self):
        """Checks if roomba detects player or items"""
        # Creates a vector
        vector = sub((self.pos_x + X, self.pos_y + Y), CharacterPos)

        vector_x = vector[0]
        vector_y = vector[1]
        vector_x += Width/2
        vector_y += Height/2

        # Creates the four points for the roomba cone of view
        points = [(vector_x - 20, vector_y), (vector_x + 20, vector_y),
                  (vector_x + 150, vector_y + 300), (vector_x - 150, vector_y + 300)]

        for j in xrange(len(points)):
            # Rotates the points for the cone of view
            points[j] = rotate_point((self.pos_x + X, self.pos_y + Y), points[j], -self.rotate)
            # moves the cone of view so its centered on the roomba
            points[j] = (int(points[j][0]) + 32, int(points[j][1]) + 32)

        # Creates a polygon out of the points
        area = points[0], points[1], points[2], points[3]

        # Draws the polygon in red
        pygame.draw.polygon(screen, Red, area)
        # Gets the colour of the pixel at the character position
        detect_player = screen.get_at(CharacterPos)

        # Checks if any items are being detected by each roomba
        for item in listItems:
            if 0 < (X + item.pos_x) < Width and 0 < Y + item.pos_y < Height:
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
                return item

        # Checks if player is detected
        if detect_player == Red:
            self.detect = 1
            return

        # Sets returning to true so roomba will return to position when not detecting player
        if self.detect == 1:
            self.returning = True

        # sets to detect to 0 if it hasn't detected anything
        self.detect = 0

    def chase_player(self):
        self.move_towards_point(CharacterPos)

    def chase_item(self, item):
        """When roombas see items they move towards them"""
        self.move_towards_point((item.pos_x + X, item.pos_y + Y))
        # checks if roomba has reached item
        item.roomba_collision(self)

    def return_to_position(self):
        if self.move_towards_point((self.start_x + X, self.start_y + Y)):
            self.returning = False

    def move_towards_point(self, point):
        """input a point and roomba will head towards the point
         will also rotate to look at the point it is heading towards
         """
        # Creates a vector for the path the roomba will take
        vector = sub((self.pos_x + X, self.pos_y + Y), point)

        # Rotates the roomba to face the point
        self.rotate = (math.atan2(vector[0], vector[1]) * 57.2958) + 180

        # sets moving to true
        can_move = True

        # stop the roombas passing through walls"
        if self.rotate < 45:
            if not wall_check("down", self.pos_x + X + 32, self.pos_y + Y + 32):
                can_move = False
        if 45 < self.rotate < 135:
            if not wall_check("right", self.pos_x + X + 32, self.pos_y + Y + 32):
                can_move = False
        if 135 < self.rotate < 225:
            if not wall_check("up", self.pos_x + X + 32, self.pos_y + Y + 32):
                can_move = False
        if 225 < self.rotate < 315:
            if not wall_check("left", self.pos_x + X + 32, self.pos_y + Y + 32):
                can_move = False
        if 315 < self.rotate < 360:
            if not wall_check("down", self.pos_x + X + 32, self.pos_y + Y + 32):
                can_move = False

        # Moves the roomba
        if vector[0] == 0:
            self.speed_x = 0
        elif vector[0] < 0:
            self.speed_x = 2
        else:
            self.speed_x = -2
        if vector[1] == 0:
            self.speed_y = 0
        elif vector[1] < 0:
            self.speed_y = 2
        else:
            self.speed_y = -2

        if self.detect == 1:
            self.speed_y *= 2
            self.speed_x *= 2

        # If wall sometimes stops roomba from moving
        if not can_move:
            self.speed_x = 0
            self.speed_y = 0

        # Updates the position of the roomba
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        # if roomba has reached point it will return True
        if (self.pos_x + X, self.pos_y + Y) == point:
            return True


def rotate_point(center_point, point, angle):
    """Rotates a point around another center_point. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0] - center_point[0], point[1] - center_point[1]
    temp_point = (temp_point[0] * math.cos(angle) - temp_point[1] * math.sin(angle),
                  temp_point[0] * math.sin(angle) + temp_point[1] * math.cos(angle))
    temp_point = temp_point[0] + center_point[0], temp_point[1] + center_point[1]
    return temp_point
    # http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects


def wall_check(direction, position_x, position_y):
    """Checks if wall in direction player is going, False if wall, True if not"""
    try:
        check_distance = 45
        if direction == "up":
            colour = screen.get_at((position_x, position_y - check_distance))
            if colour == CollisionColour:
                return False
        if direction == "down":
            colour = screen.get_at((position_x, position_y + check_distance))
            if colour == CollisionColour:
                return False
        if direction == "left":
            colour = screen.get_at((position_x - check_distance, position_y))
            if colour == CollisionColour:
                return False
        if direction == "right":
            colour = screen.get_at((position_x + check_distance, position_y))
            if colour == CollisionColour:
                return False
        return True
    except:
        return True


def sub(u, v):
    """Function for finding the vector"""
    return [u[i]-v[i] for i in range(len(u))]
    # http://stackoverflow.com/questions/33172753/how-to-have-an-object-run-directly-away-from-mouse-at-a-constant-speed/33173194#33173194


def draw_scientist():
    """Rotates the Scientist to face the point"""
    vector = sub((X + 800, Y - 1250), CharacterPos)
    rotate = (math.atan2(vector[0], vector[1]) * 57.2958)
    scientist_rotate = pygame.transform.rotate(ScientistModel, rotate)
    screen.blit(scientist_rotate, (X + 800, Y - 1250))

# Create character
PlayCharacter = CharacterClass()

# List of Roomba's
roombas = []

# List of Items
listItems = []

# Item properties (x coord, y coord, item type, used for throwing rubbish) (0 = AMMO, 2 = GRENADE, 3 = RUBBISH)
ItemSpawn = [(860, 150, 3, ""), (380, 150, 3, ""), (750, -1885, 3, ""),
             (730, -1420, 0, ""), (680, -1420, 0, ""), (630, -1420, 0, ""),
             (730, -1370, 2, "")]

# Roomba Start points and end points (Start point x, Start point y, Travel distance x, Travel distance y)
RoombaSpawn = [(1200, -810, 0, 450), (1300, -840, 0, 500), (1410, -870, 0, 550),
               (1510, -900, 0, 600), (-205, -825, 0, 400), (-90, -480, 0, -400),
               (350, -945, 600, 0), (1000, -1350, 250, 0), (5, -1530, 250, 0),
               (250, -1385, -250, 0), (5, -1290, 250, 0), (250, -1170, -250, 0),
               (1335, -1900, 500, 0), (1335, -1800, 550, 0), (1335, -1700, 600, 0),
               (1335, -1600, 650, 0), (-550, -2350, 0, 600), (-650, -2350, 0, 600),
               (-750, -2350, 0, 600), (-850, -2350, 0, 600), (1750, -2260, 0, 250),
               (1850, -2245, 0, 300), (1950, -2335, 0, 500), (2050, -2400, 0, 700),
               (1500, -2450, -1600, 0), (1400, -2370, -1550, 0), (1300, -2290, -1500, 0),
               (1400, -2210, -1550, 0), (1500, -2140, -1600, 0), (-300, -2950, 0, 400),
               (-400, -2950, 0, 400), (-500, -2950, 0, 400), (-600, -2950, 0, 400),
               (-300, -2850, 0, 400), (-400, -2850, 0, 400), (-500, -2850, 0, 400),
               (-600, -2850, 0, 400), (445, -2995, -500, 0), (900, -3160, 300, 300),
               (970, -2830, 300, -300), (1040, -3160, 300, 300), (1110, -2830, 300, -300),
               (1180, -3160, 300, 300), (1250, -2830, 300, -300)]

# Create roombas
for value in RoombaSpawn:
    roomba = Roomba(value[0], value[1], value[2], value[3])
    roombas.append(roomba)

# Create items
for value in ItemSpawn:
    item = Items(value[0], value[1], value[2], value[3])
    listItems.append(item)

# Plays the soundtrack
winsound.PlaySound("Sound/soundtrack", winsound.SND_ASYNC)

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

    # Functions for throwing projectiles
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_SPACE] and PlayCharacter.paint_grenade > 0 and PlayCharacter.projectile_spawn is False:
        PlayCharacter.paint_grenade, ProjectileDelay = PlayCharacter.throw_projectile(PlayCharacter.paint_grenade, ProjectileDelay, "PaintGrenade")
    if pressed[pygame.K_r] and PlayCharacter.rubbish > 0 and PlayCharacter.projectile_spawn is False:
        PlayCharacter.rubbish, ProjectileDelay = PlayCharacter.throw_projectile(PlayCharacter.rubbish, ProjectileDelay, "Rubbish")
    screen.blit(Background, (X - 1800, Y - 4200))
    # Checks roomba detection
    for roomba in roombas:
        roomba.item_detected = roomba.detects()

    # Draws the background
    screen.blit(Background, (X - 1800, Y - 4200))
    # Moves the Roombas
    for roomba in roombas:
        if roomba.delay < 1:
            if roomba.returning:
                roomba.return_to_position()
            else:
                if roomba.detect == 0:
                    roomba.move()
                elif roomba.detect == 2:
                    roomba.chase_item(roomba.item_detected)
                else:
                    roomba.chase_player()
        else:
            roomba.delay -= 1
        roomba.draw()
        roomba.collision()
    draw_scientist()
    # Rotates the Character
    PlayCharacter.rotate()
    # Updates the Character and the HUD
    PlayCharacter.update()
    # Updates the display
    pygame.display.flip()

# When Running is not true it will quit
pygame.quit()
sys.exit()
