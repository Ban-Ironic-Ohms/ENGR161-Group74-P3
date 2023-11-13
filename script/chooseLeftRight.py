import script.movement as mv

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)


from script.MPU9250 import MPU9250

mpu9250 = MPU9250()


def choosePath(dir, speed):
    while abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) < 150:
        mv.lf(speed)
        mv.rf(speed)
        time.sleep(0.05)
    
    time.sleep(3)
    
    if dir == 0:
        
        line_color = BP.get_sensor(BP.PORT_1)[2]
        while line_color < 70:
            mv.lf(speed)
            mv.rf(speed)
        
        
        raise KeyboardInterrupt

    if dir == 1:
        mv.rf(15)
        mv.lf(0)
        time.sleep(4)
        
        mv.rf(speed)
        mv.lf(speed)
        time.sleep(8)
        
        mv.lf(15)
        mv.rf(0)
        time.sleep(4)
        
        mv.lf(speed)
        mv.rf(speed)
        time.sleep(10)
        
        
        raise KeyboardInterrupt