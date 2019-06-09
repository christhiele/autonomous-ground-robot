import FaBo9Axis_MPU9250
import time
import sys

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

def getmagnet():
    mag = mpu9250.readMagnet()
    # print(mag)
    return mag #return np array

def gettemp():
    temp = mpu9250.readTemperature()
    return temp

def getaccel():
    accel = mpu9250.readAccel()
    print("ax = ", (accel['x']))
    print("ay = ", (accel['y']))
    print("az = ", (accel['z']))
    return accel

def getgyro():
    gyro = mpu9250.readGyro()
    print("gx = ", (gyro['x']))
    print("gy = ", (gyro['y']))
    print("gz = ", (gyro['z']))
    return gyro

def testmagnet(delay):
    #this function collects 30 seconds of magnet information at a specified speed (via delay in seconds). It calculates invalid sample percent and number of valid samples collected per second. It does not auto adjust, and depends on a new input by the user each attempt. For this user's RPi, the ideal number was .13, which gets 0% invalid, and is near max speed.

    count = 0
    counte = 0

    magnettime = 30 # can adjust magnet test time, default 30
    t_end = time.time() + magnettime

    while True:
        mag = mpu9250.readMagnet()

        # temp = mpu9250.readTemperature()
        # print("temp = ", temp)
        if mag['x'] == 0 and mag['y'] == 0 and mag['z'] == 0:
            counte += 1
        else:
            # print(mag['x'],mag['y'],mag['z'])
            pass
        count += 1
        time.sleep(delay) # minimum amount to avoid excessive 0-0-0 magnet results (for this function)

        # time break condition
        if time.time() > t_end:
            break

    ratee = (counte / count) * 100
    rate = (count-counte)/magnettime
    print("Collected %d magnetometer samples. %10.2f percent were invalid samples. %10.2f valid samples collected per second." % (count, ratee, rate))

if __name__ == "__main__":
    testmagnet(.13)