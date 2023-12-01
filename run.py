import script.movement as mv
import time
import script.lineFollow as lineFollow
import script.cargo as cargo
from script.calibrationVariables import *



# import POC2.lineFollowMono as lf
# from script.IMU import readPrint
# import POC2.nthPathDeploy as ndep
# import POC2.chooseLeftRight as clr

import script.navigation as nav

# import script.IMU as IMU 

# lineFollow.followSolid()
# IMU.readGraph()
# IMU.readPrint()

try:
    
    mv.fw(20)
    cargo.magDeploy(400)
    
    # RUN THE NAV FILE
    # LightSensor = nav.calibrate(IMU, LightSensor)[0]
    # nav.followLine(LightSensor, 0.5)
    
    # mv.fw(30)
    # cargo.hold()
    # cargo.deploy(-1, 10)
    # time.sleep(5)
    # mv.allStop()
    # mv.lf(30)
    # mv.rf(10)
    # time.sleep(6)
    # mv.fw(30)
    # time.sleep(3)
    # mv.allStop()
    time.sleep(10)

        
except KeyboardInterrupt:
    print("pressed ctrl+c")
    mv.allStop()