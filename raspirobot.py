"""
    Contains logic for bump switches, sonar and motor control
"""

__author__ = 'andrew'
import os
import threading
import config
from rrb2 import *
from time import sleep
from enum import Enum

bacon = True

class RaspiRobot(threading.Thread):

    class Incidents(Enum):
        nothing = -1
        wentForward = 0
        wentReverse = 1
        turnedLeft = 2
        turnedRight = 3
        crashedForward = 4
        crashedLeft = 5
        crashedRight = 6

    class Directions(Enum):
        stopped = -1
        forward = 0
        reverse = 1
        left = 2
        right = 3

    okToRun = False             # Keeps the thread alive


    direction = Directions.stopped

    lastAction = Incidents.nothing

    moveTime = 0                # How many iterations have we been moving for?
    stopTime = 0                # Stop moving after this many iterations of the run loop

    leftCollision = False       # Status of left lever switch used as a collision detector
    rightCollision = False      # Status of right lever switch used as a collision detector

    distance = 9001             # Distance reading from the sonar

    def __init__(self):
        super(RaspiRobot, self).__init__()
        print "Created Raspi Robot"
        try:
            self.rr = RRB2()
            self.led1(True)
            sleep(0.1)
            self.led1(False)
            sleep(0.1)
            self.led1(False)
            self.led2(False)
            self.okToRun = True
            print "Raspi Robot Initialized."
            self.forward()
        except Exception:
            self.okToRun = False
            print "Failed to initialize RaspiRobot Board"


    # Run the robot!
    def run(self):
        print "Running Raspi Robot"
        while self.okToRun:
            # Check the sonar reading
            self.distance = self.rr.get_distance()

            # Check for side collisions first
            self.leftCollision = self.rr.sw1_closed()
            self.rightCollision = self.rr.sw2_closed()

            if self.leftCollision or self.rightCollision:
                # Did we move forward into something?
                if self.self.direction == self.Directions.forward:
                    print "Crashed into something while moving forward."
                    self.lastAction = self.Incidents.crashedForward
                    self.reverse(200)

            # Are we moving? Should we stop?
            if self.direction != self.Directions.stopped:
                self.moveTime += 1

                # If we've been going in a certain direction for too long, stop ourselves.
                if self.moveTime >= self.stopTime:
                    # First, we'll stop...
                    howMoved = self.direction
                    self.stop()

                    # How were we moving?

                        # Why were we going backwards?

    # Start moving forward
    def forward(self,time=200):
        self.stop()
        try:
            print "Revving up..."
            self.rr.set_motors(config.__MAX_SPEED__,0,config.__MAX_SPEED__,0)
            self.direction = self.Directions.forward
            self.stopTime = time
            print "Moving forward for " + str(time) + " ticks."
        except Exception, e:
            print "Can't move forward! D:"
            print e
            self.stop()


    # Start moving in reverse
    def reverse(self,time=200):
        self.stop()
        try:
            self.rr.set_motors(config.__MAX_SPEED__,1,config.__MAX_SPEED__,1)
            self.direction = self.Directions.reverse
            self.stopTime = time
            print "Backing up for " + str(time) + " ticks."
        except Exception:
            print "Can't back up!"
            self.stop()


    # Stop the robot. If we can't, shut it down.
    def stop(self):
        self.moveTime = 0
        self.stopTime = 0
        try:
            self.rr.stop()
            print "Stopped."
        except Exception:
            print "WARNING: Couldn't stop robot!"
            for i in range(0,100):
                try:
                    self.rr.stop()
                    print "OK: Regained control."
                    return  # We're clear.
                except Exception:
                    pass
            # If we've lost control entirely then shut down the system.
            os.system("sudo shutdown -h 0 PonderBot lost control of RaspiRobot board.")


    # First LED on the board
    def led1(self,boolean):
        self.rr.set_oc1(boolean)


    # Second LED on the board
    def led2(self,boolean):
        self.rr.set_led1(boolean)


    # The extra LED sitting in the first open collector output
    def led3(self,boolean):
        self.rr.set_led2(boolean)

    def kill(self):
            print "Killed Raspi Robot Thread."
            self.okToRun = False


