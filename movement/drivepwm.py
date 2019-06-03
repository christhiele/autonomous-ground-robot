import RPi.GPIO as gpio
import time

#set L298n in1 to rpi gpio
IN1 = 17
IN2 = 22
IN3 = 23
IN4 = 24

gpio.setmode(gpio.BCM)

gpio.setup(IN1, gpio.OUT)
gpio.setup(IN2, gpio.OUT)
gpio.setup(IN3, gpio.OUT)
gpio.setup(IN4, gpio.OUT)

motor_frequency = 400
p1 = gpio.PWM(IN1, motor_frequency)
p2 = gpio.PWM(IN2, motor_frequency)
p3 = gpio.PWM(IN3, motor_frequency)
p4 = gpio.PWM(IN4, motor_frequency)
p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

def move(sec, p1dc, p2dc, p3dc, p4dc):
    p1.ChangeDutyCycle(p1dc)
    p2.ChangeDutyCycle(p2dc)
    p3.ChangeDutyCycle(p3dc)
    p4.ChangeDutyCycle(p4dc)
    time.sleep(sec)

def forward(sec):
    p1dc = 0
    p2dc = 100
    p3dc = 0
    p4dc = 100
    move(sec, p1dc, p2dc, p3dc, p4dc)

def reverse(sec):
    p1dc = 100
    p2dc = 0
    p3dc = 100
    p4dc = 0
    move(sec, p1dc, p2dc, p3dc, p4dc)

def pivotleft(sec):
    p1dc = 100
    p2dc = 0
    p3dc = 0
    p4dc = 100
    move(sec, p1dc, p2dc, p3dc, p4dc)

def pivotright(sec):
    p1dc = 0
    p2dc = 100
    p3dc = 100
    p4dc = 0
    move(sec, p1dc, p2dc, p3dc, p4dc)

def partialleft(sec,dc):
    p1dc = 0
    p2dc = dc
    p3dc = 0
    p4dc = 100
    move(sec, p1dc, p2dc, p3dc, p4dc)

def partialright(sec, dc):
    p1dc = 0
    p2dc = 100
    p3dc = 0
    p4dc = dc
    move(sec, p1dc, p2dc, p3dc, p4dc)

def stop(sec):
    p1dc = 0
    p2dc = 0
    p3dc = 0
    p4dc = 0
    move(sec, p1dc, p2dc, p3dc, p4dc)

def endmotor():
    p1.stop()
    p2.stop()
    p3.stop()
    p4.stop()

def reset():
    gpio.setwarnings(False)
    gpio.cleanup()

if __name__ == "__main__":
    print("forward w/ pwm")
    forward(2)
    print("reverse w/ pwm")
    reverse(2)
    print("pivot left w/ pwm")
    pivotleft(2)
    print("pivot right w/ pwm")
    pivotright(2)
    print("50% left w/ pwm")
    partialleft(2,50)
    print("50% right w/ pwm")
    partialright(2,50)
    endmotor()
    reset()
