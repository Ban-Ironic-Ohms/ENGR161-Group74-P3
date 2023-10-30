# HEADER
# This allows us to follow a line. Currently, it follows a straight line only, 
# but will include other line types in the future. 

# ---------- IMPORTS ---------- #
import time
import grovepi
import script.movement as mv

# ---------- INITIALIZATION ---------- #
# Connect the Grove Line Finder to digital port D7
# SIG,NC,VCC,GND
L_LF_PORT = 3
R_LF_PORT = 2

# idk why we need this
grovepi.pinMode(L_LF_PORT,"INPUT")
grovepi.pinMode(R_LF_PORT,"INPUT")

# ---------- FUNCTIONS ---------- #
# this function will follow the solid line using two line finders
def followSolid(speed=10):
    while True:
        # if both line finders are not detecting, the rover is straddling the line and should continue straight
        if grovepi.digitalRead(R_LF_PORT) == 0 and grovepi.digitalRead(L_LF_PORT) == 0:
            print("no lines detected")
            mv.turn(0)
            mv.forward(speed)
        # if both lines are detected, then we are at a junction (or something bad)
        if grovepi.digitalRead(R_LF_PORT) == 1 and grovepi.digitalRead(L_LF_PORT) == 1:\
            print("both lines detected, something BAD has happened")
        # turn in the direction that the line finder detects a line
        elif grovepi.digitalRead(R_LF_PORT) == 1:
            print("line detected by right sensor")
            mv.turn(-1)
            mv.forward(speed)
        elif grovepi.digitalRead(L_LF_PORT) == 1:
            print("line detected by left sensor")
            mv.turn(1)
            mv.forward(speed)
        time.sleep(0.1)