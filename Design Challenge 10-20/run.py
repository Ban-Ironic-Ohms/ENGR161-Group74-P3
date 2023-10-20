# Refrenced example from https://github.com/DexterInd/GrovePi/blob/master/Software/Python/grove_ultrasonic.py

import time
import brickpi3
import grovepi

BP = brickpi3.BrickPi3()

ultrasonic_sensor_port = 2 # assign ultrasonic sensor port to D2

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)  # Configure port 1 sensor type

L_MOTOR_PORT = BP.PORT_B
R_MOTOR_PORT = BP.PORT_C

speed_to_5cms = 8.43
speed_to_1cms = 4.1

# Before touch sensor is pressed, your program will be stuck in this loop
print("Press touch sensor on port 1 to run motors")
value = 0
while not value:
    try:
        value = BP.get_sensor(BP.PORT_1)
    except brickpi3.SensorError:
        value = 0
print("Starting...")

# Main logic    
try:
    while True:
        print(f"Ultrasonic give reading of {grovepi.ultrasonicRead(ultrasonic_sensor_port)}")
        
        if grovepi.ultrasonicRead(ultrasonic_sensor_port) > 28: # we choose a cruise distance of 30 which corresponds to a sensor value of 28
            print("All is normal")
            BP.set_motor_power(L_MOTOR_PORT, speed_to_5cms)
            BP.set_motor_power(R_MOTOR_PORT, speed_to_5cms)
        elif grovepi.ultrasonicRead(ultrasonic_sensor_port) > 13: # we chose a collisoin avoidance distance of 15cm, which corresponds to 13 USD (ultrasonicdistance)
            print("slowing down")
            BP.set_motor_power(L_MOTOR_PORT, speed_to_1cms)
            BP.set_motor_power(R_MOTOR_PORT, speed_to_1cms)
        else: # Runs if gets closer than 15cm
            print("AHAHHAHHAHAHHAH we are all gonna die")
            BP.set_motor_power(L_MOTOR_PORT, 11)
            BP.set_motor_power(R_MOTOR_PORT, 0)
            time.sleep(4)
            BP.set_motor_power(L_MOTOR_PORT, 11)
            BP.set_motor_power(R_MOTOR_PORT, 11)
            time.sleep(7)
            BP.set_motor_power(L_MOTOR_PORT, 0)
            BP.set_motor_power(R_MOTOR_PORT, 0)
            raise SystemError

        time.sleep(.1) # hold each loop/iteration for .1 seconds



except IOError as error:
    print(error)
except TypeError as error:
    print(error)
except SystemError:
    print("Terminating program -- car came too close to something")
except KeyboardInterrupt:
    print("You pressed ctrl+C...")

# use reset_all() to return all motors and sensors to resting states
BP.reset_all()