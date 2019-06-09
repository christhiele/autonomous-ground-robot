import RPi.GPIO as gpio
import drivepwm
import os
import orientation
import time
import power


def startcalibration():
    # power saving - turn off idle services
    result = power.powercheck()
    if result is True:
        power.poweroff()
        time.sleep(3)     # give time for voltage to normalize


def calibratemagnet():
    #initialize
    startcalibration()

    #set up static variables
    dc = 100 # set duty cycle to control speed of pivot, 0 - 100, although friction will functionally scramble the data if set too low.
    sec = .1 #since each turn is fixed until told to stop (or alt commands), sec is only used to force a delay between function calls to smooth motor operation.
    pivottime = 20 #set pivot time for test, default 20 seconds

    dx = []
    dy = []
    dz = []

    # start pivot
    drivepwm.pivotpartialright(sec, dc)

    # get magnet data for 20 seconds
    t_end = time.time() + pivottime
    while time.time() < t_end:
        dx, dy, dz = addmagnet(dx, dy, dz)

    #end
    drivepwm.stop(sec) #stop motor
    endcalibratemagnet() #clean up

    # print x,y,z for debugging
    # print("Lists for debugging...")
    # print("dx =", dx)
    # print("dy =", dy)
    # print("dz =", dz)

    return dx, dy, dz #return lists of x, y, and z magnetic coordinates

def addmagnet(dx, dy, dz):
    mag = orientation.getmagnet()
    if mag['x'] != 0 and mag['y'] != 0 and mag['z'] != 0:
        dx.append(mag['x'])
        dy.append(mag['y'])
        dz.append(mag['z'])
        # print("mx = ", (mag['x']))
        # print("my = ", (mag['y']))
        # print("mz = ", (mag['z']))
    time.sleep(0.13) # minimum to avoid excessive 0-0-0 magnetmeter results
    return dx, dy, dz

def endcalibratemagnet():
    # reset motor
    drivepwm.endmotor()

if __name__ == "__main__":
    calibratemagnet()
    #cleanup GPIO here b/c don't want to cleanup when upstream or parallel GPIO streams are still in use
    gpio.cleanup()
    # power.poweron()
