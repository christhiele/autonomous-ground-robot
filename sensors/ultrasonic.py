import RPi.GPIO as gpio
import time

# Ultrasonic Ranging Module / Distance Sensor HC - SR04, takes TRIG (raspberry pi to sensor), and outputs ECHO (sensor to raspberry pi @ 5V, be sure to have appropriate resistors set up)

TRIG = 21
ECHO = 18

# def init_ultrasonic():

gpio.setmode(gpio.BCM)

gpio.setup(TRIG, gpio.OUT)
gpio.setup(ECHO, gpio.IN)

def getdist_ultrasonic():
    timeout = time.time() + .1
    gpio.output(TRIG,True)
    time.sleep(0.0001) # no need to extend signal.
    gpio.output(TRIG, False)

    start = time.time()
    end = time.time()

    while gpio.input(ECHO) == False:
        start = time.time()
        if time.time() > timeout:
            break

    while gpio.input(ECHO) == True:
        end = time.time()
        if time.time() > timeout:
            break

    difftime = end - start

    # distance = velocity * time. Speed of sound at 20C (68F) and 0% humidity is 343 m/s. Distance is round trip (sonar) so is divided by 2.

    if difftime >.09:
        distance = 0
    else:
        distance = (17150 * difftime)
    return distance

def reset_ultrasonic():
    gpio.cleanup()

if __name__ == "__main__":
    dx = getdist_ultrasonic()
    print('Distance: {} centimeters'.format(dx))
    print(dx)
    reset_ultrasonic()
