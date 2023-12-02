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
import brickpi3
import script.cargo as cargo
import statistics
# import movement as mv
mpu9250 = MPU9250()

L_LIGHT_SENSOR = 2
R_LIGHT_SENSOR = 0

# higher makes it eaisier to sense a black like
# lower makes it eaiser to sense a white color
LIGHT_SENSOR_RATIO = float(input("How far between the black and white point will we sense the line: "))

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)

def queryAccel(absolute=False):
    if absolute:
        a = mpu9250.readAccel()
        return abs(a()['x']) + abs(a()['y']) + abs(a()['z'])
    else:
        return mpu9250.readAccel()
    
def queryGyro():
    return mpu9250.readGyro()

def queryMag(absolute=True):
    if absolute:
        a = mpu9250.readMagnet()
        return a['x']         
        # return abs(a['x']) + abs(a['y']) + abs(a['z'])
    else:
        return mpu9250.readMagnet()

def queryUltrasonic():
    try:
        value = BP.get_sensor(BP.PORT_1)
        return float(value)
    except brickpi3.SensorError as error:
        print(error)
        return

def queryLightSensors(both=True): 
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
    
def onLine(calValues, prev_data = None):
    # returns 0 for on line
    # 1 for deviating right
    # -1 for deviating left
    # False for both deviating :(
    
    l_sensor_value = grovepi.analogRead(L_LIGHT_SENSOR)
    r_sensor_value = grovepi.analogRead(R_LIGHT_SENSOR)
    print(f"Left: {l_sensor_value} Right: {r_sensor_value}")
    
    change_threshold = 10
    
    l_on_line = False
    r_on_line = False
    
    prev_data_l = prev_data[0]
    prev_data_r = prev_data[1]
    print(prev_data)
    if prev_data_l:
        delta_data = [prev_data_l[i] - prev_data_r[i] for i in range(len(prev_data_l))]
        running_av = statistics.mean(delta_data)    # gives the average difference between sensor values (can be + or -)
        delta = l_sensor_value - r_sensor_value     # positive when l_sensor is on white, r_sensor is black
        
        print(f"checking if bot is on line. past 5 delta data {delta_data} w/ av of {running_av}\current delta {delta}")
        
        if delta - running_av > change_threshold:   # triggers when R on black, therefore need to turn right
            print("large delta on right sensor, robot will now turn right")
            # print(f"CURRNETLY L LIST: {prev_data_l}")
            
            prev_data_l = prev_data_l[1:]
            # prev_data_r = prev_data_r[1:]
            
            prev_data_l.append(l_sensor_value)
            # prev_data_r.append(r_sensor_value)
            
            # print(f"NEW L LIST: {prev_data_l}")
            return (-1, (prev_data_l, prev_data_r))
        elif delta - running_av < -change_threshold:  # triggers when L on black, therefore turn left
            print("large delta on left sensor, robot will now turn left")
            # print(f"CURRNETLY R LIST: {prev_data_r}")
            
            # prev_data_l = prev_data_l[1:]
            prev_data_r = prev_data_r[1:]
            
            # prev_data_l.append(l_sensor_value)
            prev_data_r.append(r_sensor_value)
            
            # print(f"NEW R LIST: {prev_data_r}")
            return (1, (prev_data_l, prev_data_r))
        else:
            prev_data_l = prev_data_l[1:].append(l_sensor_value)
            prev_data_r = prev_data_r[1:].append(r_sensor_value)
            return (0, prev_data)
            
        
    
    # if not prev_data_l:
    #     if l_sensor_value - calValues.leftBlackPoint > LIGHT_SENSOR_RATIO * (calValues.leftWhitePoint - calValues.leftBlackPoint):
    #         l_on_line = True
    #     if r_sensor_value - calValues.rightBlackPoint > LIGHT_SENSOR_RATIO * (calValues.rightWhitePoint - calValues.rightBlackPoint):   
    #         r_on_line = True
        
    #     if l_on_line and r_on_line:
    #         print("On Line!")
    #         return 0
    #     if not l_on_line: # left sensor sees line, deviating to the right
    #         print("Deviating right")
    #         return 1
    #     if not r_on_line: # right sensor sees line, deviating left
    #         print("Deviating left")
    #         return -1
    #     else:
    #         return False

# many sensors need calibration!
def calibrate(IMU, LightSensor, UltrasonicSensor, *kwargs):
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
        
        def getUltrasolic():
            print(queryUltrasonic())
            value = input("US value: ")
            if not value:
                return getUltrasolic()
            else:
                return float(value)
            
        print("Enter the value that corresponds to a detected magnet, or press RETURN to see a new reading")
        # IMU = IMU(getMagTh())
        IMU = IMU(1)
        
        print("Enter the value that corresponds to a WHITE paper on the LEFT sensor, or press RETURN to see a new reading")
        # lwhite = getWhitePoint()
        lwhite = 1
        
        print("Enter the value that corresponds to a WHITE paper on the RIGHT sensor, or press RETURN to see a new reading")
        # rwhite = getWhitePoint()
        rwhite = 1
        
        print("Enter the value that corresponds to a BLACK paper on the LEFT sensor, or press RETURN to see a new reading")
        # lblack = getBlackPoint()
        lblack = 1
        
        print("Enter the value that corresponds to a BLACK paper on the RIGHT sensor, or press RETURN to see a new reading")
        # rblack = getBlackPoint()
        rblack = 1
        
        print("Place the MACRO ~10cm from the base of the hill, then enter the reading from the utrasonic sensor")
        # UltrasonicSensor = UltrasonicSensor(getUltrasolic())
        UltrasonicSensor = UltrasonicSensor(1)
                
        LightSensor = LightSensor(lwhite, rwhite, lblack, rblack)
        
        return [IMU, LightSensor, UltrasonicSensor]
        # return [LightSensor]

def reaquire(deviationDirection, calValues, prev_data):
    mv.allStop()
    # print(f"called reaquire with prev data {prev_data}")
    if deviationDirection == 1: # deviating right, need to start with reaquire left
        mv.lf(-0.5 * LargeLegoMotor.base_speed)
        mv.rf(LargeLegoMotor.base_speed)
        time.sleep(0.05)
        # mv.fw(LargeLegoMotor.base_speed)
        # time.sleep(0.1)
        
    if deviationDirection == -1:
        mv.lf(LargeLegoMotor.base_speed)
        mv.rf(-0.5 * LargeLegoMotor.base_speed)
        time.sleep(0.05)
        # mv.fw(LargeLegoMotor.base_speed)
        # time.sleep(0.1)
        
    if deviationDirection == False:
        print("BOTH SENSORS DETECT A BLACK LINE")
        pass

    q = onLine(calValues, prev_data)
    deviationDirection = q[0]
    prev_data = q[1]
    
    if deviationDirection != 0:
        return reaquire(deviationDirection, calValues, prev_data)
    
    return prev_data

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
    
def initializeDelta():
    print("getting some baseline data")
    prev_data_l = []
    prev_data_r = []
    i = 0
    while i <= 4:
        l_sensor_value = grovepi.analogRead(L_LIGHT_SENSOR)
        r_sensor_value = grovepi.analogRead(R_LIGHT_SENSOR)
        prev_data_l.append(l_sensor_value)
        prev_data_r.append(r_sensor_value)
        i += 1
    print((prev_data_r, prev_data_r))
    return (prev_data_l, prev_data_r)
    
def navigateCourse(LightSensor, UltrasonicSensor, IMU, timestep, speed, mag_count, hill_count, prev_data = None):
    if not prev_data:
        prev_data = initializeDelta()
    # print(f"calling online with prevdata {prev_data}")
    q = onLine(LightSensor, prev_data)
    deviationDirection = q[0]
    # print(f"deviation direction: {deviationDirection}")
    if deviationDirection == 0:
        # US_val = queryUltrasonic()
        # if hill_count < 1:
        #     if US_val < UltrasonicSensor.hillDist: # only goes on first hill
        #         print(f"saw a hill! Hill count going from {hill_count} to {hill_count + 1}")
        #         hill_count += 1
        #         speed *= 1.2            # NOTE: this can be changed to better climb the hill
        
        # if hill_count == 1:
        #     if US_val > UltrasonicSensor.hillDist:
        #         print("and we are over the hill!")
        #         hill_count += 1
        #         speed *= (1)/(1.2)      # NOTE: change it here as well
        
        # MAG_val = queryMag()
        # if MAG_val > IMU.magThreshold:
        #     print("hit a magnet")
        #     mag_count += 1
        
        # if mag_count == 3:              # NOTE: change the 3 to however many magnet we see
        #     print("deploying because we saw the nth magnet")
        #     cargo.sleepFwDeploy(4)
        
        mv.lf(speed)
        mv.rf(speed)
        # print(f"BRECKREO TEH SWITCHAROO: {prev_data}")
        prev_data_l = prev_data[0][1:]
        prev_data_r = prev_data[1][1:]
        # print(f"SPLITTING: {prev_data_l}, {prev_data_r}")
        l_sensor_value = grovepi.analogRead(L_LIGHT_SENSOR)
        r_sensor_value = grovepi.analogRead(R_LIGHT_SENSOR)
        # print(f"APPENDING: init indexed list: {prev_data_l} w/ data types {type(prev_data_l[2])}  adding {l_sensor_value} of type {type(l_sensor_value)} gives {prev_data_l[1:].append(l_sensor_value)}")
        prev_data_l.append(l_sensor_value)
        prev_data_r.append(r_sensor_value)
        prev_data = (prev_data_l, prev_data_r)
        # print(f" WE WENT STRAIGHT new prvdata is {prev_data}")
        
    else:
        print("Reaquiring...")
        # print(f"calling reaquire prev data {prev_data}")
        prev_data = reaquire(deviationDirection, LightSensor, prev_data)
        
        # print(f"finished reaquire: prev data is {prev_data}")
     
    time.sleep(timestep)
    navigateCourse(LightSensor, UltrasonicSensor, IMU, timestep, speed, mag_count, hill_count, prev_data)




# LightSensor = calibrate(IMU, LightSensor, UltrasonicSensor)[0]
# print(LightSensor)
# followLine(LightSensor, 0.5)