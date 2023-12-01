import time
import brickpi3
import grovepi
from script.calibrationVariables import LargeLegoMotor, SmallLegoMotor
from script.MPU9250 import MPU9250

BP = brickpi3.BrickPi3()

mpu9250 = MPU9250()

KICK_MOTOR_PORT = BP.PORT_A
RETAINER_MOTOR_PORT = BP.PORT_D

def queryMag(absolute=True):
    if absolute:
        return abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z'])
    else:
        return mpu9250.readMagnet()

def hold(dir_change = 1):
    BP.set_motor_power(RETAINER_MOTOR_PORT, 2 * dir_change)

def deploy(dir_change = 1, speed = 15):
    BP.set_motor_power(KICK_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed * dir_change)
    BP.set_motor_power(RETAINER_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed * dir_change)
    time.sleep(2)
    BP.set_motor_power(RETAINER_MOTOR_PORT, 0)
    time.sleep(1)
    BP.set_motor_power(KICK_MOTOR_PORT, 0)
    BP.reset_all()
    print('done!')
    
def magDeploy(dir_change, speed, threshold):
    while queryMag() < threshold:
        time.sleep(0.2)
    
    deploy(dir_change, speed)