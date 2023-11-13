from script.MPU9250 import MPU9250
import sys
import time
import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation

# This sample code reads the data from the acceleration, gyro, and magnetic
# sensors, breaks each into their components, and prints one of the results
# to the screen.

# For this code to run, the MPU9250.py library MUST be located on the Pi.

# Initialize the MPU9250 library
mpu9250 = MPU9250()

def readPrint(accelPrint = True, gyroPrint = True, magPrint = True):
    try:
        while True:
            # Performing the actual IMU data reads
            accel = mpu9250.readAccel()
            gyro = mpu9250.readGyro()
            mag = mpu9250.readMagnet()

            # Breaking each data read into X, Y, and Z components
            accel_x = accel['x']
            accel_y = accel['y']
            accel_z = accel['z']
            
            gyro_x = gyro['x']
            gyro_y = gyro['y']
            gyro_z = gyro['z']
            
            mag_x = mag['x']
            mag_y = mag['y']
            mag_z = mag['z']

            # Un-comment the desired print output.
            if accelPrint:
                print(f"accel {accel}")
            if gyroPrint:
                print(f"gyro {gyro}")
            if magPrint:
                print(f"mag {mag}")
            print("\n")
            time.sleep(0.25)

    except KeyboardInterrupt:
        sys.exit()

# def readGraph(accelGraph = True, gyroGraph = True, magGraph = True):
#     try:
#         start_time = time.time()
#         time_data = [i for i in range(200)]
        
#         data = {}
        
#         if accelGraph:
#             data["accel"] = [0 for i in range(200)]
#         if gyroGraph:
#             data["gyro"] = [0 for i in range(200)]
#         if magGraph:
#             data["mag"] = [0 for i in range(200)]
        
#         xlen = 200
#         yrange = [-1, 1]
        
#         fig, ax = plt.subplots(len(data) + 1, 1)
#         for i in range(len(data)):
#             # ax[i][0].set_title(data[i])
#             # ax[1][0].xlabel("Time")
#             # ax[1][0].ylabel("Value")
#             # ax[i][0].set_ylim(yrange)
#             plt.subplot(1, i+1, i+1)
#             plt.plot(time_data, [0 for i in range(200)])

#         def update(i, time_data):
#             data["accel"].append(mpu9250.readAccel())
#             data["accel"] = data["accel"][-xlen:]
#             data["gyro"].append(mpu9250.readGyro())
#             data["gyro"] = data["gyro"][-xlen:]
#             data["mag"].append(mpu9250.readMagnet())
#             data["mag"] = data["mag"][-xlen:]
            
#             time_data.append(time.time() - start_time)
#             time_data = time_data[-xlen:]

#             for i in range(len(data)):
#                 plt.subplot(1, i+1, i+1)
#                 plt.plot(time_data, data[data[i]])
        
#         ani = FuncAnimation(fig, update, fargs=(time_data,), interval=50, blit=True)
#         plt.show()
        
#     except KeyboardInterrupt:
#         sys.exit()