import RPi.GPIO as gpio
from drivepwm import *
import curses
import os
from ultrasonic import *
from servo import *

# intializes curses globally.

stdscr = curses.initscr()

# power saving - turn off idle services
os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind")  # turn off usb + ethernet
os.system("sudo /opt/vc/bin/tvservice -o")  # turnoff hdmi
os.system("sudo rfkill block bluetooth")

# start motion. Note - make sure visudo config file is updated for user to skip password authentication)
os.system("sudo service motion start")

def keyboard():
    sec = .1 #time per

    curses.noecho() #set up curses
    curses.cbreak()
    stdscr.keypad(1)

    degree = 0

    while 1:
        c = stdscr.getch()
        if c == ord('w'):
            forward(sec)
        elif c == ord('s'):
            reverse(sec)
        elif c == ord('a'):
            partialleft(sec, 0)
        elif c == ord('d'):
            partialright(sec, 0)
        elif c == ord('q'):
            partialleft(sec, 50)
        elif c == ord('e'):
            partialright(sec, 50)
        elif c == ord('z'):
            pivotleft(sec)
        elif c == ord('c'):
            pivotright(sec)
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

    #restart idle services
    os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/bind") #usb + ethernet
    os.system("sudo /opt/vc/bin/tvservice -p") #hdmi
    os.system("sudo rfkill unblock bluetooth") #bluetooth

if __name__ == "__main__":
    # keyboard()
    endkeyboard()