import pygame
import math



# Gets the position of the character
CharacterPos = (Width/2, Height/2)

# Gets the position of the mouse
(MouseX, MouseY) = pygame.mouse.get_pos()

# Function for finding the vector
def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

# Used for rotation tracking mouse
MouseX2 = MouseX
MouseY2 = MouseY
MouseX2 = MouseX2 - CharacterPos[0]
MouseY2 = MouseY2 - CharacterPos[1]

# Rotation equation
Rotation = (math.atan2(MouseX2, MouseY2) * 57.2958) + 180

# The code that does the rotation
Character2 = pygame.transform.rotate(Character, Rotation)

# Checks if mouse button 1 is pressed, ignore the "lele"
MousePress,lele,lele = pygame.mouse.get_pressed()

# If Mouse button 1 is pressed
if not pygame.time.get_ticks() - 500 < temptime:
    if MousePress ==1:
        if paintballammocounter > 0:
            paintballammocounter -= 1
            BallSpawn = True

            # Gets the initial position of the ball
            BallPos = (Width/2, Height/2)

            # Sets the speed of the ball
            BallSpeed = (0,0)

            # Creates a vector
            Vector = sub((MouseX, MouseY), (BallPos))

            # Gets the sum of the vector and divides by 20
            VectorTotal = ((math.sqrt(Vector[0]**2)) + (math.sqrt(Vector[1]**2))) / 20

            # Dividves the vector by this new vector
            Vector = (Vector[0] / VectorTotal),(Vector[1] / VectorTotal)

            # Generates the ballspeed as a result
            BallSpeed = (int(Vector[0]),(int(Vector[1])))

            temptime = pygame.time.get_ticks()


if BallSpawn is True:
    # Updates the position of the ball
    BallPos = (BallPos[0] + BallSpeed[0]),(BallPos[1] + BallSpeed[1])


