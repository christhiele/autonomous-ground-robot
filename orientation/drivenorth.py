import RPi.GPIO as gpio
import orientation
import processmagnet
import drivepwm
import calibratemagnet
import time
import numpy as np
import power

def magnetmain():
    # power saving - turn off idle services (power transfer)
    result = power.powercheck()
    if result is True:
        power.poweroff()
        time.sleep(3)     # give time for voltage to normalize

    # gather pre-existing magnet data
    print("Verifying existing magnet data...")
    calibratedtime, C, ymax, normal = checkmagnetdata()

    #recalibrate test : old data
    lastcalibrated = time.time() - float(calibratedtime)
    lastcalibratedadj = lastcalibrated / (60*60*24) #adjust from seconds to days\
    if lastcalibratedadj > 1:
        print("Verify Date: FAIL - Recalibrating")
        calibratedtime, C, ymax, normal = recalibratemagnet()
    else:
        print("Verify Date: PASS")

    #recalibrate test : distorted data
    coordsample = orientation.getmagnet()
    coordsample = [coordsample['x'], coordsample['y'], coordsample['z']]
    coordsample = np.array(coordsample, dtype=float)  # already input as list
    angle, vlenymax, vlensample  = getangle(C, ymax, coordsample, normal)
    result = testvlen(vlenymax, vlensample)
    if result is False:
        print("Verify Initial Distortion: FAIL - Recalibrating")
        calibratedtime, C, ymax, normal = recalibratemagnet()
        angle, vlenymax, vlensample = getangle(C, ymax, coordsample, normal) #redo angle, vlen calcs
        result = True
    else:
        print("Verify Initial Distortion: PASS")

    print("Verification Complete. Starting Pivot to North...")

    # start pivoting
    pivoting = True
    testvlenfails = 0 #set errorflag to 0

    while pivoting is True:
        # get sample mag coordinates
        coordsample = orientation.getmagnet()
        coordsample = [coordsample['x'], coordsample['y'], coordsample['z']]
        coordsample = np.array(coordsample, dtype=float)  # already input as list

        # process various data
        angle, vlenymax, vlensample = getangle(C, ymax, coordsample, normal)

        # test data for sanity (vector length comparison), 1 strike, restart loop, 2 strikes, abort loop
        result = testvlen(vlenymax, vlensample)
        if result is False and testvlenfails < 2:
            continue #ignore result and get a new sample

        elif result is False and testvlenfails > 1:
            drivepwm.stop(.1) # stop pivot
            pivoting = False #break out of loop
        elif result is True:
            testvlenfails = 0 #reset error count

        print("Pivoting at angle %10.2f degrees" % angle)
        if -10 < angle < 10:
            drivepwm.stop(.1)
            pivoting = False # break out of loop
        elif 10 <= angle <= 45:
            drivepwm.pivotpartialright(.1, 50)
        elif angle > 45:
            drivepwm.pivotpartialright(.1, 75)
        elif -10 >= angle >= -45:
            drivepwm.pivotpartialleft(.1, 50)
        elif angle < -45:
            drivepwm.pivotpartialleft(.1, 75)

    # recalibrate and restart
    if testvlenfails > 1:
        print("Error - Projected vs Actual Vector Length exceeds 25% difference. Restarting.")
        calibratedtime, C, ymax, normal = recalibratemagnet()
        magnetmain()
    else: #else to ensure doesn't repeat if recalibration triggers.

        #cleanup
        drivepwm.endmotor()
        reset()

        #print finished note
        print("Finished Pivoting North - Current Angle is %s" % angle)

def reset():
    gpio.cleanup()

def recalibratemagnet():
    dx, dy, dz = calibratemagnet.calibratemagnet()
    processmagnet.processmagnet(dx, dy, dz)
    calibratedtime, C, ymax, normal = checkmagnetdata()
    return calibratedtime, C, ymax, normal


def getangle(C, coordmax, coordsample, normal):
    # print(type(C), type(coordmax), type(coordsample), type(normal))
    # print(C, coordmax, coordsample, normal)
    # print(C, coordmax, coordsample, normal)
    # print(type(C), type(coordmax), type(coordsample), type(normal))

    u = coordmax - C
    v = coordsample - C
    n = normal
    angle = np.arctan2(np.dot(n, np.cross(u, v)), np.dot(u, v))
    angle = np.degrees(angle)

    vlenymax = getvectorlength(u)
    vlensample = getvectorlength(v)
    # print(C)
    # print(u, vlenymax)
    # print(v, vlensample)

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
    # print(type(vlenymax), type(vlensample))

    #convert data
    # vlen = float(vlen)
    # r = float(vlen)

    diff = abs(vlensample - vlenymax) / vlenymax
    # print(vlensample,vlenymax,diff)
    if diff > errortrigger:
        return False
    else:
        return True


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

def testangles():

    calibratedtime, C, ymax, normal = checkmagnetdata()

    # start pivoting
    pivoting = True
    testvlenfails = 0  # set errorflag to 0
    # start pivot
    drivepwm.pivotpartialright(.1, 75) #below 50 = 0.

    pivottime = 20
    t_end = time.time() + pivottime

    oldangle = 0.0

    rotation_delay = 2

    while pivoting is True:
        #time break condition
        if time.time() > t_end:
            drivepwm.stop(.1)
            pivoting = False

        #set up dynamic waiting
        t_loop_start = time.time()

        # get sample mag coordinates
        coordsample = orientation.getmagnet()

        # verify sample mag coordinates
        if coordsample['x'] == 0 and coordsample['y'] == 0 and coordsample['z'] == 0:
            print("Error - Invalid Sample Magnetic Coordinates. Resampling.")
            waitdelay(t_loop_start, .15)
            continue #restart loop if empty coordinates

        coordsample = [coordsample['x'], coordsample['y'], coordsample['z']] #convert from dictionary to list
        coordsample = np.array(coordsample, dtype=float)  # convert from list to np array

        # process various data
        angle, vlenymax, vlensample = getangle(C, ymax, coordsample, normal)


        # test data for sanity (vector length comparison), 1 strike, restart loop, 2 strikes, abort loop
        result = testvlen(vlenymax, vlensample)
        if result is False:
            print("Error - Invalid Vector Length. Resampling.")
            waitdelay(t_loop_start, .15)
            continue

        # test data for sanity (angle change direction comparison)
        rotation_delay = testangle(oldangle,angle,rotation_delay)

        #change sampleangle to oldangle
        oldangle = angle


        # wait time for GC and sensor refresh - dynamic
        waitdelay(t_loop_start, .15)



    # cleanup
    drivepwm.endmotor()
    reset()

    # print finished note
    print("Finished Testing Pivot - Current Angle is %s" % angle)


def waitdelay(t_loop_start, default):
    t_loop_diff = time.time() - t_loop_start
    waittime = default - t_loop_diff
    if waittime < 0:
        waittime = 0
    time.sleep(waittime)

def testangle(oldangle, sampleangle,rotation_delay):
    anglediff = sampleangle - oldangle
    anglemulti = sampleangle * oldangle
    if anglediff > 0:
        rotation = "Clockwise/Increase"
        print("Pivoting at 75 percent speed at angle %10.2f degrees [%s]" % (sampleangle,rotation))
        rotation_delay = 2 # reset counter

    elif anglediff < 0:
        rotation = "Counter-Clockwise/Decrease"
        print("Pivoting at 75 percent speed at angle %10.2f degrees [%s] - ERROR" % (sampleangle,rotation))
        rotation_delay = rotation_delay - 1
    elif anglediff == 0:
        rotation = "Centered"
        rotation_delay = 2 # reset counter

    if rotation_delay > 0:
        pass
    else:
        print("Error - 3 Consecutive Directional Errors Found...")

    return rotation_delay

def getsamples():


def getasample():
    #get and scrub first coordinates
    t_loop_start = time.time()
    coordsample = orientation.getmagnet()

    #
    if coordsample['x'] == 0 and coordsample['y'] == 0 and coordsample['z'] == 0:
        print("Error - Invalid Sample Magnetic Coordinates. Resampling.")
        waitdelay(t_loop_start, .13)


    waitdelay(t_loop_start, .13)



    #get and scrub first coordinates
    t_loop_start = time.time()
    coordsample2 = orientation.getmagnet()
    waitdelay(t_loop_start, .13)

    t_loop_start = time.time()
    coordsampl3 = orientation.getmagnet()
    waitdelay(t_loop_start, .13)


    coordsample = [coordsample['x'], coordsample['y'], coordsample['z']]  # convert from dictionary to list
    coordsample = np.array(coordsample, dtype=float)  # convert from list to np array



if __name__ == "__main__":
    # magnetmain()
    # recalibratemagnet()
    testangles()
    # reset()