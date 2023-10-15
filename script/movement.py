import time
import brickpi3
import grovepi
from script.calibrationVariables import LargeLegoMotor, SmallLegoMotor

BP = brickpi3.BrickPi3()

L_MOTOR_PORT = BP.PORT_B
R_MOTOR_PORT = BP.PORT_C

T_MOTOR_PORT = BP.PORT_A

all_motors = [L_MOTOR_PORT, R_MOTOR_PORT, T_MOTOR_PORT]

BASE_SPEED = 15

class MotorStallException(Exception):
    def __init__(self, *args: object) -> None:
        print("Motor stalled -- erroring")

# This function can either take a position (cm) for the robot to travel and/or
# a speed (cm/s) for it to travel at. Default speed is 15 cm/s
def forward(speed = BASE_SPEED, position = False):
    
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
            
    except KeyboardInterrupt:
        allStop()
        BP.reset_all()
    except MotorStallException:
        allStop()
        BP.reset_all()
  
def turn(dir): # defining dir=direction 0 to be straight, +1 as right and -1 as left
    # BP.set_motor_limits(T_MOTOR_PORT, 0, 60)    
    
    T_current = BP.get_motor_encoder(T_MOTOR_PORT)
    T_target = T_current + dir * SmallLegoMotor.full_turn_from_zero
    BP.set_motor_position(T_MOTOR_PORT, T_target)
    if dir > 0:
        while BP.get_motor_encoder(T_MOTOR_PORT) < T_target - 5: # wait until the turn is complete to within 5 degrees
            print(f"Turn motor is at {BP.get_motor_encoder(T_MOTOR_PORT)}, target is {T_target}")
            time.sleep(0.1)
    else:
        while BP.get_motor_encoder(T_MOTOR_PORT) > T_target + 5:
            print(f"Turn motor is at {BP.get_motor_encoder(T_MOTOR_PORT)}, target is {T_target}")
            time.sleep(0.1)
        
    

def allStop():
    print("Stopping")    
    for port in all_motors:
        BP.set_motor_power(port, 0)
    BP.reset_all()
    
    