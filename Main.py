import pygame, sys
from pygame.locals import *

pygame.init()

Running = True   #Needed for the main loop

Width = 1280     #Screen size
Height = 720

Y = 0   #For the character movement and map tracking
X = 0
XDirection = 0   # 3 states, 0 = not moving, 1 = moving one direction, 2 = moving opposite direction
YDirection = 0   # 3 states, 0 = not moving, 1 = moving one direction, 2 = moving opposite direction

White = (255,255,255)      # Defines the colour white
Red = (255,100,100)     #Defines the colour Red for later use
Background = pygame.image.load("maptest.png")      #Map Image, Placeholder
Character = pygame.image.load("character2.png")     #Character image, Currently just a placeholder
RoombaModel = pygame.image.load("Art-assets/Roomba (passive).png")
screen = pygame.display.set_mode((Width, Height))      #Draws the screen
Clock = pygame.time.Clock()   #Adds the clock

BallSpawn = False  #For the paintball spawn



class Roomba:
    def __init__(self):
        # Choose a random position
        self.pos_x = X
        self.pos_y = Y

        # Choose a random speed
        self.speed_x = 0
        self.speed_y = 2

        self.rotate = 0


    def update(self):
        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        # Bounce off the walls
        if self.pos_x < 0 or self.pos_x > Width:
            self.speed_x = -self.speed_x

        if self.pos_y < 0 or self.pos_y > Height:
            self.speed_y = -self.speed_y
            self.rotate += 180

    def draw(self):

        RoombaRotate = pygame.transform.rotate(RoombaModel, self.rotate)
        screen.blit(RoombaRotate, (X + self.pos_x, Y + self.pos_y))

roombas = []

# Create balls
num_roombas = 1
for ball_index in xrange(num_roombas):
    shape = Roomba
    new_roomba = shape()
    roombas.append(new_roomba)
print roombas

#MainLoop
while Running:
    Clock.tick(60)     #60 fps
    for event in pygame.event.get():
            if event.type == QUIT:
                Running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                Running = False
            if event.type == KEYDOWN and event.key == K_s:  #On keypress S it will move the screen up
                YDirection = 1
            if event.type == KEYDOWN and event.key == K_w: #On keypress w it will move the screen down
                YDirection = 2
            if event.type == KEYDOWN and event.key == K_d:  #On keypress S it will move the screen up
                XDirection = 1
            if event.type == KEYDOWN and event.key == K_a: #On keypress w it will move the screen down
                XDirection = 2



    if YDirection is 1:       #Changes the direction depending on key pressed
        Y = Y - 2
    elif YDirection is 2:
        Y = Y + 2
    if XDirection is 1:
        X = X - 2
    elif XDirection is 2:
        X = X + 2

    execfile("Character.py")  #Executes the Character python file
    screen.fill(White)   #Fills Screen white
    screen.blit(Background, (X, Y))     #Draws the background in relation to the player
    screen.blit(Character2, (Width/2 - 32, Height/2 - 32))    #Draws the character in the center of the screen
    for roomba in roombas:
        roomba.update()
        roomba.draw()
    if BallSpawn is True:     #Draws a paintball if conditions are met
        pygame.draw.circle(screen, Red, BallPos, 5)

    pygame.display.flip()       #Updates the display

pygame.quit()      #When Running is not true it will quit
sys.exit()