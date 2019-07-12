import RPi.GPIO as gpio
from drivepwm import *
# from ultrasonic import *
from servo import *
import orientation

degree = 0
sec = .1  # time delay

# get default magnet calibration data
calibratedtime, C, ymax, normal = orientation.checkmagnetdata()

# center camera
degree = movebydegree(sec*3, 0)

def processkey(key):
    global degree
    if key == 'w':
        forward(sec)
    elif key == 's':
        reverse(sec)
    elif key == 'a':
        pivotleft(sec)
    elif key == 'd':
        pivotright(sec)
    elif key == 'q':
        partialleft(sec, 50)
    elif key == 'e':
        partialright(sec, 50)
    elif key == 'x':
        stop(sec)
    elif key == 'g':
        coordsample, angle = orientation.getmedianmagnet(C, ymax, normal)
        print("Angle =", angle)
    elif key == 'c':
        endprocesses()
        return False
    elif key == 'p':
        print("Hello World")
    # elif key =='f':
    #     dx = getdist_ultrasonic()
    #     print(dx)
    elif key == 'ArrowLeft':
        degree = degree - 15
        degree = movebydegree(sec, degree)
    elif key == 'Clear': #translation for keypad center
        degree = movebydegree(sec*3, 0)
    elif key == 'ArrowRight':
        degree = degree + 15
        degree = movebydegree(sec, degree)
    return True

def endprocesses():
    #reset motor
    endmotor()
    #reset servo
    endservo()
    #cleanup GPIO
    gpio.cleanup()

if __name__ == "__main__":
    processkey()
    # endprocesses()