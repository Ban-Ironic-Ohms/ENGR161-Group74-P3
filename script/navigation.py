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
# LIGHT_SENSOR_RATIO = float(input("How far between the black and white point will we sense the line: "))
CHANGE_THR = int(input("Change threshold: "))
SITE = int(input("Which site to drop cargo at? (A: 1, B: 2, C: 3) - "))
# RUN_ULTRASONIC = 

BP = brickpi3.BrickPi3()
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)

def queryAccel(absolute=False):
    if absolute:
        a = mpu9250.readAccel()
        return abs(a()['x']) + abs(a()['y']) + abs(a()['z'])
    else:
        return mpu9250.readAccel()
    
def queryGyro():
    return mpu9250.readGyro()['x']

def queryMag(absolute=True):
    if absolute:
        a = mpu9250.readMagnet()
        print(a)
        # print(abs(a['x']) + a['z'])
        return abs(a['z'])         
        # return abs(a['x']) + abs(a['y']) + abs(a['z'])
    else:
        return mpu9250.readMagnet()

def queryUltrasonic():
    try:
        value = BP.get_sensor(BP.PORT_1)
        return float(value)
    except Exception as error:
        print(error)
        BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        time.sleep(4)
        return 20

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
    
    change_threshold = CHANGE_THR
    
    l_on_line = False
    r_on_line = False
    
    prev_data_l = prev_data[0]
    prev_data_r = prev_data[1]
    print(prev_data)

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
        IMU = IMU(getMagTh())
        # IMU = IMU(1)
        
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
        
        print("Place the MACRO ~3cm from an obstacle, then enter the reading from the utrasonic sensor")
        # UltrasonicSensor = Ultraso
        # nicSensor(getUltrasolic())
        UltrasonicSensor = UltrasonicSensor(-1)
                
        LightSensor = LightSensor(lwhite, rwhite, lblack, rblack)
        
        return [IMU, LightSensor, UltrasonicSensor]
        # return [LightSensor]

def reaquire(deviationDirection, calValues, prev_data, timestep, UltrasonicSensor):
    # mv.allStop()
    # print(f"called reaquire with prev data {prev_data}")
    while USObstacle(UltrasonicSensor):
        mv.allStop()
        time.sleep(0.5)
    
    if deviationDirection == 1: # deviating right, need to start with reaquire left
        mv.lf(-0.5 * LargeLegoMotor.base_speed)
        mv.rf(1.1 * LargeLegoMotor.base_speed)
        time.sleep(0.05)
        # mv.fw(LargeLegoMotor.base_speed)
        # time.sleep(0.1)
        
    if deviationDirection == -1:
        mv.lf(1.1 * LargeLegoMotor.base_speed)
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
        time.sleep(timestep)
        return reaquire(deviationDirection, calValues, prev_data, timestep, UltrasonicSensor)
    
    return prev_data

def followLine(LightSensor, timestep):
    deviationDirection = onLine(LightSensor)
    if deviationDirection == 0:
        mv.lf(LargeLegoMotor.base_speed)
        mv.rf(LargeLegoMotor.base_speed)
    else:
        print("Reaquiring...")
        reaquire(deviationDirection, LightSensor, None, timestep)
     
    time.sleep(timestep)
    followLine(LightSensor, timestep)
    
def initializeDelta(timestep):
    print("getting some baseline data")
    prev_data_l = []
    prev_data_r = []
    
    i = 0
    while i <= int((1 / timestep) / 2):
        l_sensor_value = grovepi.analogRead(L_LIGHT_SENSOR)
        r_sensor_value = grovepi.analogRead(R_LIGHT_SENSOR)
        prev_data_l.append(l_sensor_value)
        prev_data_r.append(r_sensor_value)
        i += 1
    print((prev_data_r, prev_data_r))
    return (prev_data_l, prev_data_r)

def obstacleTraverse(speed):
    start = time.time()
    print("RUNNING TRAVERSE" * 1000)
    while time.time() - start < 4:
        # increase speed linearly from current speed to 1.8x speed over 4 sec
        mv.fw(speed * (1 + (0.8 * (time.time() - start)) / 3))
        # with .15 sec intervals to jerk the robot
        time.sleep(0.15)
    # reset motors to base speed
    mv.fw(speed)
    return

def USObstacle(UltrasonicSensor):
    return False
    dist = queryUltrasonic()
    print(f"\n\nUS DISTNACE READING {dist}\n\n")
    if dist < UltrasonicSensor.hillDist:
        return True
    return False
        
def navigateCourse(LightSensor, UltrasonicSensor, IMU, timestep, speed, mag_count, hill_count, in_magnet = False, in_hill = False, prev_data = None):
    # speed = int((2.2 * speed) + 3.78)
    
    if not prev_data:
        prev_data = initializeDelta(timestep)
        
        
    # print(f"calling online with prevdata {prev_data}")
    q = onLine(LightSensor, prev_data)
    deviationDirection = q[0]
    # print(f"deviation direction: {deviationDirection}")
    if deviationDirection == 0:
        # checking for obstacle in front of MACRO
        while USObstacle(UltrasonicSensor):
            mv.allStop()
            time.sleep(0.5)
        
        
        # check if we are going over a hill/obsticale
        angle_val = queryGyro()
        print(angle_val)
        if angle_val > 10:
            print(f"SAW A HILL!!! #{hill_count + 1}" * 100)
            if not in_hill:
                if hill_count == 3:
                    print("going up hill")
                    obstacleTraverse(speed)
                    hill_count += 1
                    in_hill = True
                else:
                    hill_count += 1
                    print("already not the real hill, anomoly angle change detected")
            else:
                print("IN A HILL CURRENTLY")
        else:
            in_hill = False
        
        MAG_val = queryMag()
        
        # a: 1, b: 2, c: 3
        # SITE
        print(f"checking for a mag! mag_value {MAG_val} vs threshold {IMU.magThreshold}. In a magnet: {in_magnet}. mag num {mag_count}")
        if MAG_val > IMU.magThreshold:
            if in_magnet:
                print("still in the same magnet")
            else:
                print("hit a new magnet")
                in_magnet = True
                mag_count += 1
                # LOGIC based on site
                if SITE == 1:
                    if mag_count == 1:
                        mv.lf(speed)
                        mv.rf(0)
                        time.sleep(3)
                        mv.fw(speed)
                        time.sleep(0.5)
                        cargo.sleepFwDeploy(4)
                        
                    # if mag_count == 2:
                elif SITE == 2:
                    if mag_count == 1:
                        mv.fw(speed * .75)
                        time.sleep(2)
                    if mag_count == 2:
                        mv.lf(speed)
                        mv.rf(0)
                        time.sleep(3)
                        mv.fw(speed)
                        time.sleep(0.5)
                        cargo.sleepFwDeploy(4)
                    # if mag_count == 3:
                elif SITE == 3:
                    if mag_count == 1:
                        mv.fw(speed * .75)
                        time.sleep(2)
                    if mag_count == 2:
                        mv.fw(speed * .75)
                        time.sleep(3)
                        mv.lf(speed)
                        mv.rf(0)
                        time.sleep(3)
                        mv.fw(speed)
                        time.sleep(0.5)
                        cargo.sleepFwDeploy(4)
                    # if mag_count == 3:
        else:
            in_magnet = False
        


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
        prev_data = reaquire(deviationDirection, LightSensor, prev_data, timestep, UltrasonicSensor)
        
        # print(f"finished reaquire: prev data is {prev_data}")
     
    time.sleep(timestep)
    navigateCourse(LightSensor, UltrasonicSensor, IMU, timestep, speed, mag_count, hill_count, in_magnet, in_hill, prev_data)


def speedTest(maxSpeed):
    # takes in speed in cm/s
    
    power = (2.2 * maxSpeed) + 3.78
    start = time.time()
    mv.lf(power)
    mv.rf(power)
    # mv.fw(power)
    while (time.time() - start) * maxSpeed:
        pass
    

# LightSensor = calibrate(IMU, LightSensor, UltrasonicSensor)[0]
# print(LightSensor)
# followLine(LightSensor, 0.5)