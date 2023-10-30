import time
import grovepi
import script.movement as mv

# Connect the Grove Line Finder to digital port D7
# SIG,NC,VCC,GND
L_LF_PORT = 3
R_LF_PORT = 2

grovepi.pinMode(L_LF_PORT,"INPUT")
grovepi.pinMode(R_LF_PORT,"INPUT")

def followSolid(speed=10):
    while True:
        if grovepi.digitalRead(R_LF_PORT) == 0 and grovepi.digitalRead(L_LF_PORT) == 0:
            print("no lines detected")
            mv.turn(0)
            mv.forward(speed)
        if grovepi.digitalRead(R_LF_PORT) == 1 and grovepi.digitalRead(L_LF_PORT) == 1:\
            print("both lines detected, something BAD has happened")
        elif grovepi.digitalRead(R_LF_PORT) == 1:
            print("line detected by right sensor")
            mv.turn(-1)
            mv.forward(speed)
        elif grovepi.digitalRead(L_LF_PORT) == 1:
            print("line detected by left sensor")
            mv.turn(1)
            mv.forward(speed)
        time.sleep(0.1)