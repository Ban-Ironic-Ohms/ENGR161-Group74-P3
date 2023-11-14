import script.cargo as cargo
import script.movement as mv

from script.MPU9250 import MPU9250
import time

# Initialize the MPU9250 library
mpu9250 = MPU9250()

def nthDeploy(ntar, speed, n=0):

    while abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) < 250:
        print(mpu9250.readMagnet())
        print(abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']))
        mv.lf(speed)
        mv.rf(speed)
        time.sleep(0.2)
    n += 1
    time.sleep(5)
    print(f"saw magnet number {n}")
    if n == ntar:
        mv.rf(0)
        mv.lf(speed)
        time.sleep(8)
        mv.lf(speed)
        mv.rf(speed)
        time.sleep(10)
        cargo.deploy()
        return
        # exit()
        
    else:
        while abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) + abs(mpu9250.readMagnet()['z']) > 250:
            print("waiting")
            mv.lf(speed)
            mv.rf(speed)
            time.sleep(0.2)
            
    nthDeploy(ntar, speed, n)
    return