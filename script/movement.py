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


# ---------- CLASSES ---------- #
class MotorStallException(Exception):
    def __init__(self, *args: object) -> None:
        print("Motor stalled -- erroring")


# ---------- FUNCTIONS ---------- #
# This function can either take a position (cm) for the robot to travel and/or
# a speed (cm/s) for it to travel at. Default speed is 15 cm/s
def forward(speed = BASE_SPEED, position = False, dir_change = 1):
    speed = speed * dir_change # be able to switch directions
    
    # Error checking for inputted values for position
    if position:
        if type(position) is not int or type(position) is not float:
            print("You need to pass an int or float as position -- defaulting to speed control")
            position = False
    
    # running until user input stops
    try:
        # case if there is not a set position 
        if not position:
            # our converstion variable goes between the motor power and target speed
            BP.set_motor_power(L_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed)
            BP.set_motor_power(R_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed)
        else:
            # gets current encoder positions
            L_current = BP.get_motor_encoder(L_MOTOR_PORT)
            R_current = BP.get_motor_encoder(R_MOTOR_PORT)
            
            # setting target position based on current and desired position
            # TODO figure out how to set the speed for this operation
            BP.set_motor_position(L_MOTOR_PORT, L_current + position * LargeLegoMotor.delta_encoder_to_position)
            BP.set_motor_position(R_MOTOR_PORT, R_current + position * LargeLegoMotor.delta_encoder_to_position)

    # exceptions call allStop so motors stop
    except KeyboardInterrupt:
        print("this one is getting called in forward")
        allStop()
        BP.reset_all()
    except MotorStallException:
        allStop()
        BP.reset_all()
  
def turn(dir, speed=BASE_SPEED, precise=False): # defining dir=direction 0 to be straight, -1 as right and +1 as left
    # BP.set_motor_limits(T_MOTOR_PORT, 0, 60)
    
    # keeps a state for current turn direction so we can work relativly across multiple function calls
    global turn_state
    
    # change dir to be relative and update turn state, in place
    dir, turn_state = dir - turn_state, dir
    
    # set the motor position to desired position
    T_current = BP.get_motor_encoder(T_MOTOR_PORT)
    T_target = T_current + dir * SmallLegoMotor.full_turn_from_zero
    BP.set_motor_position(T_MOTOR_PORT, T_target)
    
    # runs if we want to WAIT until the turn is complete until we procede
    if precise:
        # error tells us how far from the desired position we can be
        error = 5
        
        # these functions are for turning left or right
        # they will also slowly increase the rate of error bounds, so at SOME point it will end
        if dir > 0:
            while BP.get_motor_encoder(T_MOTOR_PORT) < T_target - error: # wait until the turn is complete to within 5 degrees
                print(f"Turn motor is at {BP.get_motor_encoder(T_MOTOR_PORT)}, target is {T_target}")
                BP.set_motor_power(L_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed * 0.5)
                BP.set_motor_power(R_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed)
                error += 0.2
                time.sleep(0.1)
        else:
            while BP.get_motor_encoder(T_MOTOR_PORT) > T_target + error:
                BP.set_motor_power(R_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed * 0.5)
                BP.set_motor_power(L_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed)
                print(f"Turn motor is at {BP.get_motor_encoder(T_MOTOR_PORT)}, target is {T_target}")
                error += 0.2    
                time.sleep(0.1)
      
def lf(speed):
    BP.set_motor_power(L_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed)

def rf(speed):
    BP.set_motor_power(R_MOTOR_PORT, speed * LargeLegoMotor.power_to_speed)


def allStop():
    print("Stopping")    
    for port in all_motors:
        print("setting power 0")
        BP.set_motor_power(port, 0)
    
    BP.reset_all()
    return True
    
    