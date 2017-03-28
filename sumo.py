#!/usr/bin/env python3
''' 
Sumo robot
Holds initially for 3secs while scanning
Then alternates between searching and charging
'''
from ev3dev.ev3 import *
import time

#Important declarations and assignments
button = Button();
sonic = UltrasonicSensor();
gyro = GyroSensor();
gyro.mode = 'GYRO-ANG';
headedDirection = gyro.value();
rightMotor = LargeMotor('outA');
leftMotor = LargeMotor('outD');

#Important 'Constants'
TURN_SPEED = 1000;
MINIMUM_DETECT_DISTANCE = 650;
FORWARD_LENIANCY = 1;

#Global Variables
mobile = False;

#Prints this so we know program is not stuck building
print("Initialization Complete");

def checkManualExit():
    if (button.check_buttons(buttons=['left','right'])):
        stopMotors();
        exit();
    return True;

def stopMotors():
	leftMotor.stop();
	rightMotor.stop();

#Keeps the robot moving in the direction it was facing since last turn
def moveForward(speed):
    if (gyro.value() - headedDirection > FORWARD_LENIANCY):
        leftMotor.run_timed(speed_sp = speed * 0.9, time_sp = 10000);
        rightMotor.run_timed(speed_sp = speed, time_sp = 10000);
    elif (gyro.value() - headedDirection < -FORWARD_LENIANCY):
        rightMotor.run_timed(speed_sp = speed * 0.9, time_sp = 10000);
        leftMotor.run_timed(speed_sp = speed, time_sp = 10000);
    else:
        leftMotor.run_timed(speed_sp = speed, time_sp = 10000);
        rightMotor.run_timed(speed_sp = speed, time_sp = 10000);

def keepTurning(direction):
    leftMotor.run_forever(speed_sp=-TURN_SPEED*direction, stop_action="hold");
    rightMotor.run_forever(speed_sp=TURN_SPEED*direction, stop_action="hold");

def initialHold():
    global mobile;
    start = time.time();
    while (time.time() - start < 3.0):
        pass;
    mobile = True;
    print("Mobilized");

def charge():
    moveForward(-800);

def scanForOpponent():
    global headed_direction;
    stopMotors();
    while (sonic.value() > MINIMUM_DETECT_DISTANCE):
        keepTurning(1);   
    stopMotors();
    headed_direction = gyro.value();
    print("Opponent Found");

begin = False;
#Main Below Here
while (not begin):
    if (button.check_buttons(buttons=['enter'])):
        begin = True;
        print("Holding 3 Seconds");
while (checkManualExit()):
    if (not mobile):
        initialHold();
    if (sonic.value() <= MINIMUM_DETECT_DISTANCE):
        charge();
    else: 
        scanForOpponent();
    
