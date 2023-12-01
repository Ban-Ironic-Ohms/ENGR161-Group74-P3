# The navigation script will do three things:
# 1) it will take in data from the sensors like line finders, IMU, and ultrasonic sensor
# 2) it will predict where it is on the hard-coded map
# 3) it will make recommendations as to next actions for the robot

# ------------------- Section 1: Sensors ----------------------------

from script.MPU9250 import MPU9250
from script.calibrationVariables import *
import grovepi
import time
import script.movement as mv
# import movement as mv
mpu9250 = MPU9250()

L_LIGHT_SENSOR = 2
R_LIGHT_SENSOR = 0

LIGHT_SENSOR_RATIO = float(input("How far between the black and white point will we sense the line: "))


def queryAccel(absolute=False):
    if absolute:
        return abs(mpu9250.readAccel()['x']) + abs(mpu9250.readAccel()['y']) + abs(mpu9250.readAccel()['z'])
    else:
        return mpu9250.readAccel()
    
def queryGyro():
    return mpu9250.readGyro()

def queryMag(absolute=True):
    if absolute:
        return abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z'])
    else:
        return mpu9250.readMagnet()

"""
Will later include basic functions for US and light sensor
"""
def queryLightSensors(both=True): # TODO
    if both:
        l_sensor_value = grovepi.analogRead(L_LIGHT_SENSOR)
        r_sensor_value = grovepi.analogRead(R_LIGHT_SENSOR)
        print(f"Left:{l_sensor_value}, Right:{r_sensor_value}")
        return [l_sensor_value, r_sensor_value]
    else:
        l_sensor_value = grovepi.analogRead(L_LIGHT_SENSOR)
        r_sensor_value = grovepi.analogRead(R_LIGHT_SENSOR)
        print(f"Average:{(l_sensor_value + r_sensor_value) / 2}")
        return [(l_sensor_value + r_sensor_value) / 2]
    
def onLine(calValues):
    # returns 0 for on line
    # 1 for deviating right
    # -1 for deviating left
    # False for both deviating :(
    
    l_sensor_value = grovepi.analogRead(L_LIGHT_SENSOR)
    r_sensor_value = grovepi.analogRead(R_LIGHT_SENSOR)
    print(f"Left: {l_sensor_value} Right: {r_sensor_value}")
    
    l_on_line = False
    r_on_line = False
    
    if l_sensor_value - calValues.leftBlackPoint > LIGHT_SENSOR_RATIO * (calValues.leftWhitePoint - calValues.leftBlackPoint):
        l_on_line = True
    if r_sensor_value - calValues.rightBlackPoint > LIGHT_SENSOR_RATIO * (calValues.rightWhitePoint - calValues.rightBlackPoint):   
        r_on_line = True
    
    if l_on_line and r_on_line:
        print("On Line!")
        return 0
    if not l_on_line: # left sensor sees line, deviating to the right
        print("Deviating right")
        return 1
    if not r_on_line: # right sensor sees line, deviating left
        print("Deviating left")
        return -1
    else:
        return False

# many sensors need calibration!
def calibrate(IMU, LightSensor, *kwargs):
    # KWARGS: [magTh, whitePt, blackPt]
    if not kwargs:
        
        def getMagTh():
            print(queryMag(True))    
            magThreshold = input("Magnet detection threshold: ")
            if not magThreshold:
                return getMagTh()
            else:
                return float(magThreshold)
        
        def getWhitePoint():
            print(queryLightSensors())    
            whitePoint = input("White point: ")
            if not whitePoint:
                return getWhitePoint()
            else:
                return float(whitePoint)

        def getBlackPoint():
            print(queryLightSensors())
            blackPoint = input("black point: ")
            if not blackPoint:
                return getBlackPoint()
            else:
                return float(blackPoint)
            
            
        print("Enter the value that corresponds to a detected magnet, or press RETURN to see a new reading")
        IMU = IMU(getMagTh())
        
        print("Enter the value that corresponds to a WHITE paper on the LEFT sensor, or press RETURN to see a new reading")
        lwhite = getWhitePoint()
        
        print("Enter the value that corresponds to a WHITE paper on the RIGHT sensor, or press RETURN to see a new reading")
        rwhite = getWhitePoint()
        
        print("Enter the value that corresponds to a BLACK paper on the LEFT sensor, or press RETURN to see a new reading")
        lblack = getBlackPoint()
        
        print("Enter the value that corresponds to a BLACK paper on the RIGHT sensor, or press RETURN to see a new reading")
        rblack = getBlackPoint()
        
        LightSensor = LightSensor(lwhite, rwhite, lblack, rblack)
        
        # return [IMU, LightSensor]
        return [LightSensor]

def reaquire(deviationDirection, calValues):
    mv.allStop()
    if deviationDirection == 1: # deviating right, need to start with reaquire left
        mv.lf(-0.5 * LargeLegoMotor.base_speed)
        mv.rf(LargeLegoMotor.base_speed)
        time.sleep(0.3)
        mv.fw(LargeLegoMotor.base_speed)
        time.sleep(0.3)
        
    if deviationDirection == -1:
        mv.lf(LargeLegoMotor.base_speed)
        mv.rf(-0.5 * LargeLegoMotor.base_speed)
        time.sleep(0.3)
        mv.fw(LargeLegoMotor.base_speed)
        time.sleep(0.3)
        
    if deviationDirection == False:
        print("BOTH SENSORS DETECT A BLACK LINE")
        pass

    deviationDirection = onLine(calValues)
    if deviationDirection != 0:
        reaquire(deviationDirection, calValues)
    
    return 

def followLine(LightSensor, timestep):
    deviationDirection = onLine(LightSensor)
    if deviationDirection == 0:
        mv.lf(LargeLegoMotor.base_speed)
        mv.rf(LargeLegoMotor.base_speed)
    else:
        print("Reaquiring...")
        reaquire(deviationDirection, LightSensor)
     
    time.sleep(timestep)
    followLine(LightSensor, timestep)

# how this will work
# LightSensor = calibrate(IMU, LightSensor)[0]
# print(LightSensor)
# followLine(LightSensor, 0.5)