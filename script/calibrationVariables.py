class LargeLegoMotor:
    power_to_speed = 1.27 # takes power in the given units and gives speed in cm/s
    delta_encoder_to_position = 10 # takes change in encoder position and gives a change in position in cm
    time_to_angle = 10
    base_seped = 15
    
class SmallLegoMotor:
    full_turn_from_zero = 20 # gives a change in encoder value that turns the wheels fully one way or another 
    # 1/4 turn

class IMU:
    def __init__(self, magThreshold) -> None:
        self.magnetThreshold = magThreshold

class LightSensor:
    def __init__(self, leftWhitePoint, rightWhitePoint, leftBlackPoint, rightBlackPoint) -> None:
        self.leftWhitePoint = leftWhitePoint
        self.rightWhitePoint = rightWhitePoint
        
        self.leftBlackPoint = leftBlackPoint
        self.rightBlackPoint = rightBlackPoint
        
    def __str__(self) -> str:
        return f"lwhite: {self.leftWhitePoint} rwhite: {self.rightWhitePoint}\nlblack: {self.leftBlackPoint} rblack:{self.rightBlackPoint}"
