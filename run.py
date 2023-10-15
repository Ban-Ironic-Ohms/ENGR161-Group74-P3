import script.movement as movement
import time

movement.forward(30)
time.sleep(0.5)
print("turning")
movement.turn(1)
time.sleep(.5)
movement.turn(-1)
time.sleep(1)
print("stoppping")
movement.allStop()
