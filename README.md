# Autonomous Ground Robot
python framework for an autonomous ground robot with raspberry pi

version 5

## Basic Functions
- [x] Motors (Forward/Backwards, Pivot, & Turn)
- [x] Servo
- [x] Camera
- [x] Accelerometer
- [x] Gyroscope
- [x] Magnetmeter
- [ ] Distance Sensor (was working, currently not)
- [x] Power Control (7.4V Charging On/Off via RPi 5V USB + Step Up Converter)

 
## Advanced Functions
- [x] Terminal Keyboard Control
- [x] Java Keyboard Control on Local Network
- [ ] Java GUI on Local Network
- [x] Video Streaming on Local Network
- [x] Compass Positioning (with Calibration)
- [ ] Speed Display/Control
- [ ] Automatic Impact Detection
- [ ] Automatic Location Mapping
- [ ] Automatic Power Control (Monitor)
- [ ] Automatic Power Control (Dock)
- [ ] Automatic Power Control (Constant Voltage/Constant Current Lithium Ion Charging) (7.4V)
- [x] Automatic Power Control (Constant Voltage/Constant Current Lithium Ion Charging) (3.7V) 
- [ ] Automatic Power Control (UPS) (7.4V)
- [x] Automatic Power Control (UPS) (3.7V)

## Required Linux Dependencies
* Python3

## Required Python Libraries
* RPi.GPIO
* curses (keyboard control)
* numpy (location mapping)
* matplotlib (location mapping)
* FaBo9Axis_MPU9250 (Accelerometer, Gyroscope, & Magnetometer data from mpu9250)

## Component List
* Raspberry Pi 3 B+
* 7.4 V Power Supply (2 Lithium Ion 18650 Batteries in Series + Protection Board with Balance Charging)
* 3.7 V Power Supply (1-2 Lithium Ion 18650 Batteries in Parallel - included in RPi UPS)
* RPi UPS PowerPack (for easy UPS support and RPI stability)
* 7.4 -> 5 V Step Down Converter (Power Servos, Sensors)
* 5 -> 7.4 V Step Up Converter (Recharging 7.4V)
* Motor Control Board (e.g. L298n)
* Motors (2x 6V DC gear motors)
* Raspberry Pi Camera
* Servo (e.g. sg90)
* Ultrasonic Sensor (e.g. hc-sro4)
* 3 Axis Accelerometer, Gyroscope, & Magnetometer (e.g. mpu9250)
* Breadboard & Wires

## Breadboard Diagram
![Breadboard Diagram](https://github.com/christhiele/robotika/blob/master/misc/tankv5_bb.png)

## GPIO Assignments (can change by modifying code)
* GPIO 2 - Accelerometer, Gyroscope, & Magnetometer
* GPIO 3 - Accelerometer, Gyroscope, & Magnetometer
* GPIO 4 - Accelerometer, Gyroscope, & Magnetometer
* GPIO 14 - Servo
* GPIO 17 - Motor (via Motor Control Board)
* GPIO 18 - Ultrasonic Sensor (via Breadboard)
* GPIO 21 - Ultrasonic Sensor
* GPIO 22 - Motor (via Motor Control Board)
* GPIO 23 - Motor (via Motor Control Board)
* GPIO 24 - Motor (via Motor Control Board)

## GPIO Assignments (can change without modifying code)
* 5V - Not Used
* 3.3V - Accelerometer, Gyroscope, & Magnetometer
* Ground (Pin 9)(3v) - Accelerometer, Gyroscope, & Magnetometer
* Ground (Pin 14)(5V) - Breadboard Power
