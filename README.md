# robotika
python framework for a raspberry pi robot
version 5

## Component List
* raspberry pi 3 b+
* 7.4 V Power Supply (2x Lithium Ion 18650 in Series + Protection Board with Balance Charging)
* 3.7 V Power Supply (1-2 Lithium Ion 18650 in Parallel - included in RPi UPS)
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

## Required Python Libraries
* Python3
* RPi.GPIO
* curses (keyboard control)
* numpy (advanced math functions)
* matplotlib (advanced math functions)
* FaBo9Axis_MPU9250 (MPU 9250 library)
