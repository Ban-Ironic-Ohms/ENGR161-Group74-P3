import time
import brickpi3
import grovepi
from script.calibrationVariables import LargeLegoMotor, SmallLegoMotor

BP = brickpi3.BrickPi3()


KICK_MOTOR_PORT = BP.PORT_A
RETAINER_MOTOR_PORT = BP.PORT_D

def deploy():
    BP.set_motor_power(KICK_MOTOR_PORT, 20 * LargeLegoMotor.power_to_speed)
    BP.set_motor_power(RETAINER_MOTOR_PORT, 20 * LargeLegoMotor.power_to_speed)
    time.sleep(0.2)
    BP.set_motor_power(RETAINER_MOTOR_PORT, 0)
    time.sleep(0.1)
    BP.set_motor_power(KICK_MOTOR_PORT, 0)
    BP.reset_all()
    print('done!')
    
