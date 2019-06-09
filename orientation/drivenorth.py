import RPi.GPIO as gpio
import orientation
import processmagnet
import drivepwm
import calibratemagnet
import time
import numpy as np

def pivottoangle():
    # pivots to specified angle
    pass

def pivottonorth():
    #pivots to north - based on shortest possible route.


    # gather pre-existing magnet data
    print("Verifying existing magnet data...")
    calibratedtime, C, ymax, normal = orientation.checkmagnetdata()

    #recalibrate test : old data
    lastcalibrated = time.time() - float(calibratedtime)
    lastcalibratedadj = lastcalibrated / (60*60*24) #adjust from seconds to days\
    if lastcalibratedadj > 1:
        print("Verify Date: FAIL - Recalibrating")
        calibratedtime, C, ymax, normal = recalibratemagnet()
    else:
        print("Verify Date: PASS")

    print("Verification Complete. Starting Pivot to North...")

    # start pivoting
    olddirection = "E"
    directionerror = 0

    while True:
        # get sample mag coordinates
        coordsample, angle = orientation.getmedianmagnet(C, ymax, normal)

        print("Pivoting at angle %10.2f degrees" % angle)

        # declare pivot direction
        if angle >= 10:
            newdirection = "L"
        elif angle <= 10:
            newdirection = "R"
        else:
            pass

        # test if directional change
        if olddirection == "E":  # empty
            pass
        elif newdirection != olddirection:
            directionerror += 1
        else:
            directionerror = 0

        if directionerror == 1:
            continue

        # set movement
        if abs(angle) < 10:
            drivepwm.stop(.01)
            break # break out of loop
        elif 10 <= abs(angle) < 30:
            pivotpartialbidirect(.01, 50, newdirection)
        elif 30 <= abs(angle) <= 90:
            pivotpartialbidirect(.01, 75, newdirection)
        elif abs(angle) > 90:
            pivotpartialbidirect(.01, 100, newdirection)

        # set old direction for next loop
        olddirection = newdirection

    #cleanup
    drivepwm.endmotor()
    reset()

    #print finished note
    print("Finished Pivoting North - Current Angle is %s" % angle)

def pivotpartialbidirect(sec,dc,direction):
    if direction == "L":
        drivepwm.pivotpartialleft(sec, dc)
    elif direction == "R":
        drivepwm.pivotpartialright(sec, dc)

def testpivot():
    try:
        calibratedtime, C, ymax, normal = orientation.checkmagnetdata()

    except:
        calibratedtime, C, ymax, normal = recalibratemagnet()

    # start pivoting
    pivoting = True
    pivotspeed = 100 #below 50 = 0.

    testvlenfails = 0  # set errorflag to 0
    # start pivot
    drivepwm.pivotpartialright(.1, pivotspeed)

    pivottime = 20
    t_end = time.time() + pivottime

    oldangle = 0.0

    rotation_delay = 2

    while pivoting is True:
        #time break condition
        if time.time() > t_end:
            drivepwm.stop(.1)
            pivoting = False

        # get sample mag coordinates
        coordsample, angle = orientation.getmedianmagnet(C, ymax, normal)

         # test data for sanity (angle change direction comparison)
        rotation_delay = testangle(oldangle,angle,rotation_delay,pivotspeed)

        #change sampleangle to oldangle
        oldangle = angle


    # cleanup
    drivepwm.endmotor()
    reset()

    # print finished note
    print("Finished Testing Pivot - Current Angle is %s" % angle)



def testangle(oldangle, sampleangle,rotation_delay,pivotspeed):
    anglediff = sampleangle - oldangle
    if anglediff > 0:
        rotation = "Clockwise/Increase"
        print("Pivoting at %d percent speed at angle %10.2f degrees [%s]" % (pivotspeed,sampleangle,rotation))
        rotation_delay = 2 # reset counter

    elif -200 < anglediff < 0:
        rotation = "Counter-Clockwise/Decrease"
        print("Pivoting at %d percent speed at angle %10.2f degrees [%s] - ERROR" % (pivotspeed,sampleangle,rotation))
        rotation_delay = rotation_delay - 1
    elif -200 > anglediff:
        rotation = "Flip"
        print("Pivoting at %d percent speed at angle %10.2f degrees [%s]" % (pivotspeed,sampleangle,rotation))
        rotation_delay = 2 # reset counter
    elif anglediff == 0:
        rotation = "Centered"
        rotation_delay = 2 # reset counter

    if rotation_delay > 0:
        pass
    else:
        print("Error - 3 Consecutive Directional Errors Found...")

    return rotation_delay


def recalibratemagnet():
    dx, dy, dz = calibratemagnet.calibratemagnet()
    processmagnet.processmagnet(dx, dy, dz)
    calibratedtime, C, ymax, normal = orientation.checkmagnetdata()
    return calibratedtime, C, ymax, normal

def waitdelay(t_loop_start, default):
    t_loop_diff = time.time() - t_loop_start
    waittime = default - t_loop_diff
    if waittime < 0:
        waittime = 0
    time.sleep(waittime)

def reset():
    gpio.cleanup()

if __name__ == "__main__":
    pivottonorth()
    # recalibratemagnet()
    # testpivot()
    # reset()