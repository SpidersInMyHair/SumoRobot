#!/usr/bin/env python3
''' 
Sumo robot
Holds initially for 3secs while scanning
Then alternates between searching and charging
'''
from ev3dev.ev3 import *
import time

#Inputs
button = Button();
sonic = UltrasonicSensor();
color = ColorSensor();

#Outputs
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
rotate_clock = 1;

#Prints this and set LEDS so we know program is not stuck building
print("Initialization Complete. Waiting for 'Right' Button Press.");
Leds.set_color(Leds.LEFT, Leds.ORANGE);
Leds.set_color(Leds.RIGHT, Leds.GREEN);

class Tracking(object):
    def __init__(self):
        self.sonar_distances = [];

    #Adds a sonar value to the front of the list. Removes old ones from the back. Keeps size of SONAR_CHECK_LENGTH
    def addSonarValue(self, value):
        self.sonar_distances.insert(0, value);
        if (len(self.sonar_distances) > SONAR_CHECK_LENGTH):
            self.sonar_distances.pop();

    # Will clear out all of the current values being kept by the tracker
    def flushValues(self):
        for i in range(0, len(self.sonar_distances)):
            self.sonar_distances.pop();
    
    # Returns the average distance of all the stored SONAR distances
    def getCurrentAverage(self):
        value = 0;
        for i in range(0, len(self.sonar_distances)):
            value += self.sonar_distances[i];
        return value/len(self.sonar_distances);

    # Defines the target as being lost (was just 'charging' it) when all (SONAR_CHECK_LENGTH) values are > MINIMUM_DETECT_DISTANCE
    # This way if the robot is correctly charging the opponent and recieves one or two 'junk' values from the sonar - it won't start turning due to a false SONAR reading
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

    # Returns if there was a 'sudden' decrease in the recently taken sonar scans
    def suddenDecrease(self):
        for i in range(0, len(self.sonar_distances) - 1):
            if (self.sonar_distances[i] > self.sonar_distances[i+1] + 500):
                return 1;
        return 0;

    def getNumberStored(self):
        return len(self.sonar_distances);

    # Used for debugging. Simply prints all of the current values that are being stored
    def printValues(self):
        for i in range(0, len(self.sonar_distances)):
            print(self.sonar_distances[i]);
        
opp_tracker = Tracking();

# Simply checks if both 'up' and 'down' button pressed simultaneously. If true, exit the program.
def checkManualExit():
    if (button.check_buttons(buttons=['backspace'])): 
        stopMotors();
        exit();
    return True;

# Stops the wheel motors
def stopMotors():
	leftMotor.stop();
	rightMotor.stop();

# Run the motors for 0.5 seconds, can also be called continuously to keep the motors running 'forever'
def runMotors(left, right):
    leftMotor.run_timed(speed_sp = left, time_sp = 500);
    rightMotor.run_timed(speed_sp = right, time_sp = 500);

# Move the robot forward. Negative speed is actually given since motors placed 'other-way-around' for rear-drive
def moveForward(speed):
    runMotors(-speed, -speed);       

# Takes in a plus/minus 1 direction argument. With +1 specifying a clockwise turn and -1 specifying an anti-clockwise turn
def keepTurning(direction, speed):
    leftMotor.run_forever(speed_sp=-speed*direction*rotate_clock, stop_action="hold");
    rightMotor.run_forever(speed_sp=speed*direction*rotate_clock, stop_action="hold");

# The 'initial' mandatory 3 second hold. Can also perform actions during this time that do not move body.
def initialHold():
    global mobile;
    start = time.time();
    while (time.time() - start < 3.0):
        #May put things here
        pass;
    mobile = True;
    print("Mobilized");

# Simply moves the robot forward at max speed while updating the tracker object
def charge():
    moveForward(1000);

# Runs when the opponent has been defined as lost 
# Turns the robot until the tracker shows consecutively decreasing values
# When the numbers have been consecutively decreasing, the robot decreasing its turn speed to 'hone' in
def scanForOpponent():
    global rotate_clock;
    stopMotors();
    while (not opp_tracker.targetFound()):     
        keepTurning(1, TURN_SPEED * 0.8);   
        opp_tracker.addSonarValue(sonic.value());
    stopMotors();   
    print("Opponent Found");

begin = False;
# Main Program Loop is Contained Below Here
while (not begin):
    if (button.check_buttons(buttons=['right'])):
        begin = True;
        Leds.set_color(Leds.LEFT, Leds.GREEN);
        print("Holding 3 Seconds");
while (checkManualExit()):
    if (not mobile):
        initialHold();
    print(sonic.value());
    opp_tracker.addSonarValue(sonic.value());
    if (opp_tracker.targetLost() or opp_tracker.getNumberStored() != SONAR_CHECK_LENGTH):
        scanForOpponent();
    else: 
        charge();
