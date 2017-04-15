#!/usr/bin/env python3
''' 
Sumo Robot Program
Written by "Oh Boy" Group for ENGG1000, UNSW 
'''
# Required Libraries
from ev3dev.ev3 import *
import time

# Inputs for EV3 
button = Button();
sonic = UltrasonicSensor();
color = ColorSensor();

# Outputs for EV3
rightMotor = LargeMotor('outA');
leftMotor = LargeMotor('outD');

#Sensor Modes
color.mode='COL-REFLECT';

#Important 'Constants'
TURN_SPEED = 350;
MINIMUM_DETECT_DISTANCE = 800;
MINIMUM_COLOR_THRESHOLD = 1;
SONAR_CHECK_LENGTH = 5;
FORWARD_LENIANCY = 1;

#Global Variables
mobile = False;

#Prints this and set LEDS so we know program is not stuck building
print("Initialization Complete. Waiting for 'Right' Button Press.");
Leds.set_color(Leds.LEFT, Leds.ORANGE);
Leds.set_color(Leds.RIGHT, Leds.GREEN);

# Class to organise functions related to the Tracking System
class Tracking(object):
    def __init__(self):
        self.sonar_distances = [];

    # Adds a sonar value to the front of the list. Removes old ones from the back. Keeps size of SONAR_CHECK_LENGTH.
    def addSonarValue(self, value):
        self.sonar_distances.insert(0, value);
        if (len(self.sonar_distances) > SONAR_CHECK_LENGTH):
            self.sonar_distances.pop();

    # Will clear out all of the current values being kept by the tracker
    def flushValues(self):
        for i in range(0, len(self.sonar_distances)):
            self.sonar_distances.pop();
	
    # Defines the target as being lost when all (SONAR_CHECK_LENGTH) values are greater than the MINIMUM_DETECT_DISTANCE.
    # This way if the robot is correctly charging the opponent and recieves one or two 'junk' values from the
    # sonar - it won't start turning due to a false SONAR reading.
    def targetLost(self):
        lost = True;
        for i in range(0, len(self.sonar_distances)):
            if (self.sonar_distances[i] < MINIMUM_DETECT_DISTANCE):
                lost = False;
        return lost;

    def targetFound(self):
        found = True*(len(self.sonar_distances) == SONAR_CHECK_LENGTH);
        for i in range(0, len(self.sonar_distances)):
            if (self.sonar_distances[i] > MINIMUM_DETECT_DISTANCE):
                found = False;
        return found;

    def getNumberStored(self):
        return len(self.sonar_distances);

    # Used for debugging. Simply prints all of the current values that are being stored
    def printValues(self):
        for i in range(0, len(self.sonar_distances)):
            print(self.sonar_distances[i]);
        
# Declaration and Initialisation of the Tracking Object
opp_tracker = Tracking();

# Simply checks if the 'backspace' button is pressed. If true, stop the motors and exit the program.
def checkManualExit():
    if (button.check_buttons(buttons=['backspace'])): 
        stopMotors();
        exit();
    return True;

# Stops the wheel motors immediately.
def stopMotors():
	leftMotor.stop();
	rightMotor.stop();

# Run the motors for 0.5 seconds. This can also be called continuously to keep the motors running 'forever'.
def runMotors(left, right):
    leftMotor.run_timed(speed_sp = left, time_sp = 500);
    rightMotor.run_timed(speed_sp = right, time_sp = 500);

# Move the robot forward.
def moveForward(speed):
    runMotors(-speed, -speed);	# Negative value supplied as robot is 'rear-wheeled'.  

# Takes in a plus/minus 1 direction argument. With +1 specifying a clockwise turn and -1 specifying an anti-clockwise turn
# The robot will continue to turn in that direction until a different motor action is requested.
def keepTurning(direction, speed):
    leftMotor.run_forever(speed_sp=-speed*direction, stop_action="hold");
    rightMotor.run_forever(speed_sp=speed*direction, stop_action="hold");

# The 'initial' mandatory 3 second hold. Is also designed to perform other actions in this time if need be.
def initialHold():
    global mobile;
    start = time.time();
    while (time.time() - start < 3.0):
        #May put things here
        pass;
    mobile = True;
    print("Mobilized");

# Simply moves the robot forward at max speed. This happens when the robot has found the target.
def charge():
    moveForward(1000);

# Runs when the targetLost() returns True. This will turn the robot until the tracker shows SONAR_CHECK_LENGTH number of values in a row
# that are less than the MINIMUM_DETECT_DISTANCE.
# The turning is then stopped and the program is taken back to the main loop.
def scanForOpponent():
    stopMotors();
    while (not opp_tracker.targetFound()):     
        keepTurning(1, TURN_SPEED * 0.8);   
        opp_tracker.addSonarValue(sonic.value());
    stopMotors();   
    print("Opponent Found");

begin = False;
# Main Program Loop is BELOW
while (not begin):
    # Wait for right button to be pressed.  
    if (button.check_buttons(buttons=['right'])):
        begin = True;
        Leds.set_color(Leds.LEFT, Leds.GREEN);
        print("Holding 3 Seconds");
# The program will terminate if buttons specified in checkManualExit() are pressed.
while (checkManualExit()):
    # Wait for three seconds initially.
    if (not mobile):
        initialHold();
    # Always feeding the tracker with new sonic values.	
    opp_tracker.addSonarValue(sonic.value());  
    # Below is where the robot chooses and alternates between the main 'Scanning' and 'Charging' phase.
    if (opp_tracker.targetLost() or opp_tracker.getNumberStored() != SONAR_CHECK_LENGTH):
        scanForOpponent();
    else: 
        charge();
