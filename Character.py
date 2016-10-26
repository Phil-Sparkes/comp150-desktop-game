import pygame, math

(MouseX, MouseY) = pygame.mouse.get_pos()     # Gets the position of the mouse
MouseX2 = MouseX / 7.11111111111111111111111111111111     #Used for rotation tracking mouse

if MouseY < 360:              #makes it rotate all the way around
    MouseX2 = 360 - MouseX2

Character2 = pygame.transform.rotate(Character, MouseX2 + 90)     # The code that does the rotation

MousePress,lele,lele = pygame.mouse.get_pressed()       #checks if mouse button 1 is pressed, ignore the "lele"

if MousePress ==1:           #If Mouse button 1 is pressed
    BallSpawn = True
    BallPosX = Width/2       #Gets the initial position of the ball
    BallPosY = Height / 2
    BallDestX = (MouseX - Width/2)           #Gets the Destination of the ball
    BallDestY = (MouseY - Height/2)
    BallXSpeed = 0             #sets the speed of the ball
    BallYSpeed = 0

    if math.sqrt(BallDestX**2) > math.sqrt(BallDestY**2):       #Checks which value is bigger, the math is there just to convert them to a positive integers
        BallXSpeed = 20            #Sets ball speed
        BallYSpeed = int(math.sqrt(BallDestY**2)/20)
    else:
        BallYSpeed = 20            #sets ball speed
        BallXSpeed =  int(math.sqrt(BallDestX**2) / 20)

if BallSpawn is True:

    if -BallXSpeed/2 <= BallDestX  <= BallXSpeed/2 or -BallYSpeed/2 <= BallDestY  <=  BallYSpeed/2:  #Checks if ball has reaches destination
        pass
    else:                 #this is the main update making the ball move
        if BallDestX > 0:
            BallPosX = BallPosX + BallXSpeed
            BallDestX = BallDestX - BallXSpeed
        else:
            BallPosX = BallPosX - BallXSpeed
            BallDestX = BallDestX + BallXSpeed

        if BallDestY > 0:
            BallPosY = BallPosY + BallYSpeed
            BallDestY = BallDestY - BallYSpeed
        else:
            BallPosY = BallPosY - BallYSpeed
            BallDestY = BallDestY + BallYSpeed

