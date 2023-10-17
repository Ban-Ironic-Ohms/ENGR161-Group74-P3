import sys
sys.path.append("..") # Adds higher directory to python modules path.

import script.movement as mv
print("POC #1 TASK #1 -- Follow a straight line over obsticles")
speed = float(input("What speed, in cm/s, is required for this test? Should be a value between 15 and 30 cm/s "))

mv.forward(speed)