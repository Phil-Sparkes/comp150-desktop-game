import pygame, math

ObjectPos = (Width/2, Height/2)

(MouseX, MouseY) = pygame.mouse.get_pos()     # Gets the position of the mouse

def sub(u, v):             #Function for finding the vector
    return [ u[i]-v[i] for i in range(len(u)) ]

MouseX2 = MouseX
MouseY2 = MouseY                        #Used for rotation tracking mouse
MouseX2 = MouseX2 - ObjectPos[0]
MouseY2 = MouseY2 - ObjectPos[1]

Rotation = (math.atan2(MouseX2, MouseY2) * 57.2958) + 180  #rotation equation

Character2 = pygame.transform.rotate(Character, Rotation)     # The code that does the rotation

MousePress,lele,lele = pygame.mouse.get_pressed()       #checks if mouse button 1 is pressed, ignore the "lele"

if MousePress ==1:           #If Mouse button 1 is pressed
    BallSpawn = True
    BallPos = (Width/2, Height/2)    #Gets the initial position of the ball
    BallSpeed = (0,0)             #sets the speed of the ball

    Vector = sub((MouseX, MouseY), (BallPos))          #Creates a vector
    VectorTotal = ((math.sqrt(Vector[0]**2)) + (math.sqrt(Vector[1]**2))) / 20          #gets the sum of the vector and divides by 20
    Vector = (Vector[0] / VectorTotal),(Vector[1] / VectorTotal)              #dividves the vector by this new vector
    BallSpeed = (int(Vector[0]),(int(Vector[1])))               #generates the ballspeed as a result

if BallSpawn is True:

    BallPos = (BallPos[0] + BallSpeed[0]),(BallPos[1] + BallSpeed[1])    #Updates the position of the ball


