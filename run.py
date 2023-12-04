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
    # speed = int(input("what speed to test: "))
    # nav.speedTest(speed)
    # mv.fw(speed)
    # cargo.hold()
    # cargo.magDeploy(200, -1, 20)
    # cargo.deploy(-1, 20)
    
    # RUN THE NAV FILE
    cal = nav.calibrate(IMU, LightSensor, UltrasonicSensor)
    IMU = cal[0]
    LightSensor = cal[1]
    UltrasonicSensor = cal[2]
    timestep = float(input("timestep: "))
    nav.navigateCourse(LightSensor, UltrasonicSensor, IMU, timestep, 40, 0, 0)
    
    # time.sleep(2)
    # mv.lf(30)
    # mv.rf(10)
    # time.sleep(6)
    # mv.fw(30)
    # time.sleep(3)
    time.sleep(30)
    mv.allStop()

        
except KeyboardInterrupt:
    print("pressed ctrl+c")
    mv.allStop()