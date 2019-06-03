import RPi.GPIO as gpio
from drivepwm import *
import os
import FaBo9Axis_MPU9250
import time
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np


# power saving - turn off idle services
os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind")  # turn off usb + ethernet
os.system("sudo /opt/vc/bin/tvservice -o")  # turnoff hdmi
os.system("sudo rfkill block bluetooth")

#set up MPU 9250 (orientation: magnetometer)
mpu9250 = FaBo9Axis_MPU9250.MPU9250()

time.sleep(3) #give time for voltage to normalize

def calibratemagnet():
    #initialize
    partial = 100
    sec = .1

    dx = []
    dy = []
    dz = []

    # start pivot
    pivotpartialright(sec, partial)


    # get magnet data for 20 seconds
    t_end = time.time() + 20
    while time.time() < t_end:
        dx, dy, dz = addmagnet(dx, dy, dz)

    #end
    stop(sec) #stop motor
    endcalibratemagnet() #clean up

    #print x,y,z for debugging
    print("Lists for debugging...")
    print("dx =", dx)
    print("dy =", dy)
    print("dz =", dz)

    #create graph

    dx = np.array(dx)
    dy = np.array(dy)
    dz = np.array(dz)

    ax = plt.axes(projection='3d')
    ax.scatter3D(dx, dy, dz, c=dz, cmap='Greens')
    plt.savefig('foox.png', bbox_inches='tight')
    ax.scatter3D(dx, dy, dz, c=dy, cmap='Greens')
    plt.savefig('fooy.png', bbox_inches='tight')
    ax.scatter3D(dx, dy, dz, c=dz, cmap='Greens')
    plt.savefig('fooz.png', bbox_inches='tight')

def pivotpartialright(sec,partial):
    p1dc = 0
    p2dc = partial
    p3dc = partial
    p4dc = 0
    move(sec, p1dc, p2dc, p3dc, p4dc)

def addmagnet(dx, dy, dz):
    mag = mpu9250.readMagnet()
    if mag['x'] != 0 and mag['y'] != 0 and mag['z'] != 0:
        dx.append(mag['x'])
        dy.append(mag['y'])
        dz.append(mag['z'])
        # print("mx = ", (mag['x']))
        # print("my = ", (mag['y']))
        # print("mz = ", (mag['z']))
    time.sleep(0.1)
    return dx, dy, dz

def endcalibratemagnet():
    # reset motor
    endmotor()

    #cleanup GPIO
    gpio.cleanup()

    #restart idle services
    os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/bind") #usb + ethernet
    os.system("sudo /opt/vc/bin/tvservice -p") #hdmi
    os.system("sudo rfkill unblock bluetooth") #bluetooth

if __name__ == "__main__":
    calibratemagnet()
    # endcalibratemagnet()