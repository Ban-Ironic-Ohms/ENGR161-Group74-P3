import time
import grovepi
import script.movement as mv

# Connect the Grove Line Finder to digital port D7
# SIG,NC,VCC,GND
L_LF_PORT = 3
R_LF_PORT = 2

grovepi.pinMode(L_LF_PORT,"INPUT")
grovepi.pinMode(R_LF_PORT,"INPUT")

def followSolid():
    while True:
        if grovepi.digitalRead(R_LF_PORT) == 0 and grovepi.digitalRead(L_LF_PORT) == 0:
            print("no lines detected")
            mv.turn(0, 10)
            mv.forward(10)
        if grovepi.digitalRead(R_LF_PORT) == 1:
            print("line detected by right sensor")
            mv.turn(-1, 10)
            mv.forward(10)
        if grovepi.digitalRead(L_LF_PORT) == 1:
            print("line detected by left sensor")
            mv.turn(1, 10)
            mv.forward(10)
        time.sleep(0.05)