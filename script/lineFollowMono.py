
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import script.movement as mv


BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.


BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_COLOR_COLOR_COMPONENTS)
def followLine(speed):
    try:
        while True:
            check_dir = 0
            try:
                print(BP.get_sensor(BP.PORT_1)) # print the color
                print(BP.get_sensor(BP.PORT_1)[2])
                line_color = BP.get_sensor(BP.PORT_1)[2]
                if line_color < 70:
                    mv.lf(speed)
                    mv.rf(speed)
                    check_dir = 0
                else:
                    # FIND THE LINE
                    if check_dir == 1:
                        check_dir = -1
                        mv.rf(speed * 1.5)
                        mv.lf(speed * 0.75)
                        curr = time.time()
                        while time.time() < curr + 0.3:
                            if line_color < 70:
                                break
                            time.sleep(0.02)
                    else:
                        check_dir = 1
                        mv.lf(speed * 1.5)
                        mv.rf(speed * 0.75)
                        curr = time.time()
                        while time.time() < curr + 0.3:
                            if line_color < 70:
                                break
                            time.sleep(0.02)
                        
                        
                
                
            except brickpi3.SensorError as error:
                print(error)
            
            time.sleep(0.5)  

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.