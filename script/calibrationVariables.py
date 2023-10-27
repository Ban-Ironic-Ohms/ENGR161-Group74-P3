class LargeLegoMotor:
    power_to_speed = 1.27 # takes power in the given units and gives speed in cm/s
    delta_encoder_to_position = 10 # takes change in encoder position and gives a change in position in cm
    
    
class SmallLegoMotor:
    full_turn_from_zero = 30 # gives a change in encoder value that turns the wheels fully one way or another 
    # 1/4 turn
