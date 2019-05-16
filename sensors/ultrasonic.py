import RPi.GPIO as GPIO
import time

# Ultrasonic Ranging Module / Distance Sensor HC - SR04, takes TRIG (raspberry pi to sensor), and outputs ECHO (sensor to raspberry pi @ 5V, be sure to have appropriate resistors set up)

def getdistance(TRIG, ECHO):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG,True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == False:
        start = time.time()

    while GPIO.input(ECHO) == True:
        end = time.time()

    difftime = end - start

    # distance = velocity * time. Speed of sound at 20C (68F) and 0% humidity is 343 m/s. Distance is round trip (sonar) so is divided by 2.

    distance = (17150 * difftime)

    GPIO.cleanup()

    return distance


if __name__ == "__main__":
    TRIG = 4
    ECHO = 18
    dx = getdistance(TRIG,ECHO)
    print('Distance: {} centimeters'.format(dx))
