import RPi.GPIO as gpio
import time

# micro servo 9g sg90 - needs custom frequency and GPIO

sg90 = 14

gpio.setmode(gpio.BCM)

gpio.setup(sg90, gpio.OUT)

# set frequency based on datasheet
servo_frequency = 50

servo1 = gpio.PWM(sg90, servo_frequency)
servo1.start(0) #start dc in off (practical, 7 = center)

# period = 1 / frequency = 1 / 50 = .02 sec = 20ms (see datasheet).
# Positions = 1-2 ms dc -> 1ms (left), 1.5ms(center), 2ms(right).
# dc = position / period
# dc = 5 -> 7.5 -> 10 (theoretical)
# actual dc based on testing.

def move(sec, p1dc):
    servo1.ChangeDutyCycle(p1dc)
    time.sleep(sec)
    servo1.ChangeDutyCycle(0)


# degree -> result, practical equation: DC = 1/15 * degree + 7 (basic algebra from set of coordinates)
def movebydegree(sec, degree):
    if degree > 45: # restrict movement to 45 degrees left + right from center
        degree = 45
    elif degree < -45:
        degree = -45
    dc = (degree / -15.0) + 7.0
    move(sec, dc)
    return degree

def fullleft():
    move(2)

def center():
    move(7)

def fullright():
    move(12)

def endservo():
    servo1.stop()

def reset():
    gpio.setwarnings(False)
    gpio.cleanup()

def custom():
    degree = float(input("New degree for servo: "))
    newdegree = movebydegree(.3, degree)

if __name__ == "__main__":
    # reset()
    # print("servo left")
    # left()
    # time.sleep(4)
    # print("servo center")
    # center()
    # time.sleep(4)
    # print("servo right")
    # right()
    # time.sleep(4)
    custom()
    time.sleep(4)
    endservo()
    reset()
