import script.movement as mv
import time
import script.lineFollow as lineFollow
import script.cargo as cargo
import script.lineFollowMono as lf
from script.IMU import readPrint
import script.nthPathDeploy as ndep
import script.chooseLeftRight as clr

# import script.IMU as IMU 

# lineFollow.followSolid()
# IMU.readGraph()
# IMU.readPrint()
try:
    while True:
        # CARGO DROP
        # ndep.nthDeploy(2, 15)
        # raise Exception(KeyboardInterrupt)
        
        # 
        # mv.rf(0)
        # mv.lf(15)
        # time.sleep(8)
        
        # 
        
        # choose LEFT OR RIGHT (0 is staight 1 is left)
        clr.choosePath(1, 15)
        
        

        
except KeyboardInterrupt:
    print("pressed ctrl+c")
    mv.allStop()