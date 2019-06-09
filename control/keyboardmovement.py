import RPi.GPIO as gpio
from drivepwm import *
import curses
import os
from ultrasonic import *
from servo import *
import power
import orientation

# intializes curses globally.

stdscr = curses.initscr()

# start motion. Note - make sure visudo config file is updated for user to skip password authentication)
os.system("sudo service motion start")

def keyboard():

    # power saving - turn off idle services
    result = power.powercheck()
    if result is True:
        power.poweroff()
        time.sleep(3)     # give time for voltage to normalize

    sec = .1 #time per

    # set up curses
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    degree = 0

    # get default magnet calibration data
    calibratedtime, C, ymax, normal = orientation.checkmagnetdata()

    while 1:
        c = stdscr.getch()
        if c == ord('w'):
            forward(sec)
        elif c == ord('s'):
            reverse(sec)
        elif c == ord('a'):
            pivotleft(sec)
        elif c == ord('d'):
            pivotright(sec)
        elif c == ord('q'):
            partialleft(sec, 50)
        elif c == ord('e'):
            partialright(sec, 50)
        elif c == ord('g'):
            coordsample, angle = orientation.getmedianmagnet(C, ymax, normal)
            print("Angle =", angle)
        elif c == ord('x'):
            stop(sec)
        elif c == ord('r'):
            break
        elif c == ord('p'):
            print("Hello World")
        elif c == ord('f'):
            dx = getdist_ultrasonic()
            print(dx)
        elif c == curses.KEY_LEFT:
            degree = degree - 15
            degree = movebydegree(sec, degree)
        elif c == 350: #unicode integer for keypad center
            degree = movebydegree(sec, 0)
        elif c == curses.KEY_RIGHT:
            degree = degree + 15
            degree = movebydegree(sec, degree)
    endkeyboard()

def endkeyboard():
    #reset settings
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    #cleanup curses
    curses.endwin()
    #reset motor
    endmotor()
    #reset servo
    endservo()
    #cleanup GPIO
    gpio.cleanup()

    #exit motion (webcam)
    os.system("sudo service motion stop")

if __name__ == "__main__":
    keyboard()
    # endkeyboard()