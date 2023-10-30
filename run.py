import script.movement as mv
import time
import script.lineFollow as lineFollow
# import script.IMU as IMU 

# lineFollow.followSolid()
# IMU.readGraph()
# IMU.readPrint()
try:
    while True:
        lineFollow.followSolid(20)
        # mv.turn(-3)
        # time.sleep(1)
        # mv.turn(3)
        # time.sleep(1)
        
except KeyboardInterrupt:
    mv.allStop()
    exit()