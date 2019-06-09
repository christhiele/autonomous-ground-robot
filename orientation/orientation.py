import FaBo9Axis_MPU9250
import time
import numpy as np

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
    print("Collected %d magnetometer samples in %d seconds. %10.2f percent were invalid. %10.2f valid samples collected per second" % (count, magnettime, ratee, rate))

def getmedianmagnet(C, ymax, normal):
    #get three samples
    coordsample1, angle1 = getcleanmagnet(C, ymax, normal)
    coordsample2, angle2 = getcleanmagnet(C, ymax, normal)
    coordsample3, angle3 = getcleanmagnet(C, ymax, normal)

    #convert angles to np array and find median
    angles = np.array((angle1, angle2, angle3),dtype=float)
    medianangle = np.median(angles)

    #return coordsample with the median angle
    if medianangle == angle1:
        return coordsample1, angle1
    elif medianangle == angle2:
        return coordsample2, angle2
    elif medianangle == angle3:
        return coordsample3, angle3
    else:
        return ArithmeticError

def getcleanmagnet(C, ymax, normal):
    testvlenerror = 0
    while True:
        #get coordinates
        t_loop_start = time.time()
        coordsample = getmagnet()

        # test data for null values
        if coordsample['x'] == 0 and coordsample['y'] == 0 and coordsample['z'] == 0:
            # print("Error - Invalid Sample Magnetic Coordinates. Resampling.")
            waitdelay(t_loop_start, .15)
            continue #restart loop

        coordsample = [coordsample['x'], coordsample['y'], coordsample['z']]  # convert from dictionary to list
        coordsample = np.array(coordsample, dtype=float)  # convert from list to np array

        angle, vlenymax, vlensample = getangle(C, ymax, coordsample, normal)

        # test data for sanity (vector length comparison)
        result = testvlen(vlenymax, vlensample)
        if result is False:
            # print("Error - Invalid Vector Length. Resampling.")
            waitdelay(t_loop_start, .15)
            testvlenerror += 1
            if testvlenerror > 2:
                break #end loop
            else:
                continue #restart loop
        elif result is True:
            break #end loop

    #delay for GC and refresh
    waitdelay(t_loop_start, .15)

    return coordsample, angle

def checkmagnetdata():
    f = open("magnetdata.txt", "r")
    fl = f.readlines()
    for idx,value in enumerate(fl):
        # print(idx, value)
        if idx == 1:
            calibratedtime = value.rstrip() # strip to remove /n and other ending spaces in string
        elif idx == 2:
            C = value.rstrip()
        elif idx == 3:
            ymax = value.rstrip()
        elif idx == 4:
            normal = value.rstrip()
    # print(calibratedtime, C, ymax, normal)

    # remove proxy brackets from string
    C = C.replace("[", "")
    C = C.replace("]", "")
    ymax = ymax.replace("[", "")
    ymax = ymax.replace("]", "")
    normal = normal.replace("[", "")
    normal = normal.replace("]", "")

    # convert strings to lists
    C = C.split(", ")
    ymax = ymax.split(", ")
    normal = normal.split(", ")

    # convert to np arrays
    C = np.array(C, dtype=float)
    ymax = np.array(ymax, dtype=float)
    normal = np.array(normal, dtype=float)

    # convert constants to float
    calibratedtime = float(calibratedtime)

    # print(calibratedtime, C, r, ymax, normal)

    return calibratedtime, C, ymax, normal

def waitdelay(t_loop_start, default):
    t_loop_diff = time.time() - t_loop_start
    waittime = default - t_loop_diff
    if waittime < 0:
        waittime = 0
    time.sleep(waittime)

def getangle(C, coordmax, coordsample, normal):
    u = coordmax - C
    v = coordsample - C
    n = normal
    angle = np.arctan2(np.dot(n, np.cross(u, v)), np.dot(u, v))
    angle = np.degrees(angle)

    vlenymax = getvectorlength(u)
    vlensample = getvectorlength(v)

    return angle, vlenymax, vlensample

def getvectorlength(vector):
    x = vector[0]
    y = vector[1]
    z = vector[2]
    vlen = np.sqrt(x ** 2 + y ** 2 + z ** 2)  # vector length = SQRT(x^2 + y^2 +z^2)
    # print(vlen, x, y, z)
    return vlen

def testvlen(vlenymax, vlensample):
    #very rough approximation since the vector length is of a 2D->3D transforamtion of the projected circle, meaning the vector lengths will likely not be the same regardless. But since some variability is inevitbale with sensor, saving processing power for a rough estimate seemed best.

    errortrigger = 0.50  # 50% change from base radius of projected circle

    diff = abs(vlensample - vlenymax) / vlenymax
    # print(vlensample,vlenymax,diff)
    if diff > errortrigger:
        return False
    else:
        return True

if __name__ == "__main__":
    # testmagnet(.13)
    calibratedtime, C, ymax, normal = checkmagnetdata()
    coordsample, angle = getmedianmagnet(C, ymax, normal)
    print(coordsample, angle)