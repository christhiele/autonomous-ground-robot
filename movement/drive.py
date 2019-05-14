import RPi.GPIO as gpio
import time

#set L298n in1 to rpi gpio
IN1 = 17
IN2 = 22
IN3 = 23
IN4 = 24


def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(IN1, gpio.OUT)
    gpio.setup(IN2, gpio.OUT)
    gpio.setup(IN3, gpio.OUT)
    gpio.setup(IN4, gpio.OUT)

def reverse(sec):
    init()
    gpio.output(IN1, True)
    gpio.output(IN2, False)
    gpio.output(IN3, True)
    gpio.output(IN4, False)
    time.sleep(sec)
    gpio.cleanup()

def forward(sec):
    init()
    gpio.output(IN1, False)
    gpio.output(IN2, True)
    gpio.output(IN3, False)
    gpio.output(IN4, True)
    time.sleep(sec)
    gpio.cleanup()

def pivotleft(sec):
    init()
    gpio.output(IN1, True)
    gpio.output(IN2, False)
    gpio.output(IN3, False)
    gpio.output(IN4, True)
    time.sleep(sec)
    gpio.cleanup()

def pivotright(sec):
    init()
    gpio.output(IN1, False)
    gpio.output(IN2, True)
    gpio.output(IN3, True)
    gpio.output(IN4, False)
    time.sleep(sec)
    gpio.cleanup()

def turnleft(sec):
    init()
    gpio.output(IN1, False)
    gpio.output(IN2, False)
    gpio.output(IN3, False)
    gpio.output(IN4, True)
    time.sleep(sec)
    gpio.cleanup()

def turnright(sec):
    init()
    gpio.output(IN1, False)
    gpio.output(IN2, True)
    gpio.output(IN3, False)
    gpio.output(IN4, False)
    time.sleep(sec)
    gpio.cleanup()

def reset():
    gpio.setwarnings(False)
    init()
    gpio.cleanup()

if __name__ == "__main__":
    print("forward")
    forward(2)
    print("reverse")
    reverse(2)
    print("left")
    turnleft(2)
    print("right")
    turnright(2)
    print("pleft")
    pivotleft(2)
    print("pright")
    pivotright(2)
