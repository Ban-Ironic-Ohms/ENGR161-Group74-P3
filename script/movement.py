# HEADER
# Desc: This file serves as a way for logic to control the rover. It provides 
# simple functions like forward and turn that are highly customizable (speed, 
# power, angles, etc.). It also has a function allStop() that immediatly stops
# all motors. This is most useful in the case of motors running erradically

# ---------- IMPORTS ---------- #
import time
import brickpi3
import grovepi
from script.calibrationVariables import LargeLegoMotor, SmallLegoMotor

# ---------- INITIALIZATION ---------- #
BP = brickpi3.BrickPi3()

L_MOTOR_PORT = BP.PORT_B
R_MOTOR_PORT = BP.PORT_C


T_MOTOR_PORT = BP.PORT_A

all_motors = [L_MOTOR_PORT, R_MOTOR_PORT, T_MOTOR_PORT]

# ---------- GLOBAL VARIABLES ---------- #
BASE_SPEED = 10

turn_state = 0


# ---------- FUNCTIONS ---------- #

# These functions run the left and right motors.      
def lf(speed):
    BP.set_motor_power(L_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed)

def rf(speed):
    BP.set_motor_power(R_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed)
    
    
# This function can either take a position (cm) for the robot to travel and/or
# a speed (cm/s) for it to travel at. Default speed is 15 cm/s
def forward(speed = BASE_SPEED, dir_change = 1):
    speed = speed * dir_change # be able to switch directions

    lf(speed)
    rf(speed)

  
def turn(dir, speed=BASE_SPEED): # defining dir=direction 0 to be straight, +1 as right and -1 as left
    # keeps a state for current turn direction so we can work relativly across multiple function calls
    global turn_state
    
    # change dir to be relative and update turn state, in place
    dir, turn_state = dir - turn_state, dir
    

    


def allStop():
    print("Stopping")    
    for port in all_motors:
        print("setting power 0")
        BP.set_motor_power(port, 0)
    
    BP.reset_all()
    return True
    
    