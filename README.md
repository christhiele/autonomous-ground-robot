# robotika
python framework for a raspberry pi autonomous robot
version 5

## Functions
- [x] Motors (Forward/Backwards, Pivot, & Turn)
- [x] Servo
- [x] Camera
- [x] Accelerometer
- [x] Gyroscope
- [x] Magnetmeter
- [ ] Distance Sensor (was working, currently not)
 
## Advanced Functions
- [x] Terminal Keyboard Control
- [x] 7.4V Charging On/Off
- [x] Video Streaming on Local Network
- [ ] Relative Compass Positioning
- [ ] GUI Overlay
- [ ] Automatic Location Mapping
- [ ] Automatic Power Docking

## Required Linux Dependencies
* Python3
* Motion

## Required Python Libraries
* RPi.GPIO
* curses (keyboard control)
* numpy (location mapping)
* matplotlib (location mapping)
* FaBo9Axis_MPU9250 (Accelerometer, Gyroscope, & Magnetometer data from mpu9250)

## Component List
* raspberry pi 3 b+
* 7.4 V Power Supply (2 Lithium Ion 18650 Batteries in Series + Protection Board with Balance Charging)
* 3.7 V Power Supply (1-2 Lithium Ion 18650 Batteries in Parallel - included in RPi UPS)
* RPi UPS PowerPack (for easy UPS support and RPI stability)
* 7.4 -> 5 V Step Down Converter (Power Servos, Sensors)
* 5 -> 7.4 V Step Up Converter (Recharging 7.4V)
* Motor Control Board
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
* 3V - Accelerometer, Gyroscope, & Magnetometer
* Ground (Pin 9)(3v) - Accelerometer, Gyroscope, & Magnetometer
* Ground (Pin 14)(5V) - Breadboard Power
