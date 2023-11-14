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
        # ndep.nthDeploy(1, 70)
        
        # IF NEEDED
        cargo.deploy()
        
        # raise Exception(KeyboardInterrupt)
        

        
        
        # choose LEFT OR RIGHT (0 is staight 1 is left)
        # clr.choosePath(1, 40)
        
        
        

        
except KeyboardInterrupt:
    print("pressed ctrl+c")
    mv.allStop()