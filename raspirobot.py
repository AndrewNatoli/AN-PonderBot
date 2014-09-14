"""
    Contains logic for bump switches, sonar and motor control
"""

__author__ = 'andrew'
import threading
import os
from rrb2 import *
from time import sleep

bacon = True

class RaspiRobot(threading.Thread):

    okToRun = False             # Keeps the thread alive

    turningLeft = False         # Turning left?
    turningRight = False        # Turning right?
    goingForward = False        # Going forward?
    goingReverse = False        # Going in reverse?

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
        except Exception:
            self.okToRun = False
            print "Failed to initialize RaspiRobot Board"


    # Run the robot!
    def run(self):
        print "Running Raspi Robot"

        self.forward()
        while self.okToRun:
            # Check the sonar reading
            self.distance = self.rr.get_distance()

            self.moveTime += 1

            # If we've been going in a certain direction for too long, stop ourselves.
            if self.moveTime >= self.stopTime:
                print "Move completed."
                self.stop()
            else:
                print self.moveTime + " / " + self.stopTime

            # Check for side collisions first
            self.leftCollision = self.rr.sw1_closed()
            self.rightCollision = self.rr.sw2_closed()

            if self.leftCollision or self.rightCollision:
                # Did we move forward into something?
                if self.goingForward:
                    print "Crashed into something while moving forward. Stopping."
                    self.stop()


    # Start moving forward
    def forward(self,time=200):
        self.stop()
        try:
            self.rr.set_motors(1,0,1,0)
            self.goingForward = True
            self.stopTime = time
            print "Moving forward for " + time + " ticks."
        except Exception:
            print "Can't move forward! D:"
            self.stop()


    # Start moving in reverse
    def reverse(self,time=200):
        self.stop()
        try:
            self.rr.set_motors(1,1,1,1)
            self.goingReverse = True
            self.stopTime = time
            print "Backing up for " + time + " ticks."
        except Exception:
            print "Can't back up!"
            self.stop()


    # Stop the robot. If we can't, shut it down.
    def stop(self):
        self.goingForward = False
        self.goingReverse = False
        self.turningLeft = False
        self.turningRight = False
        self.moveTime = 0
        self.stopTime = 0
        try:
            print "Stopping"
            self.rr.stop()
            return
        except Exception:
            print "WARNING: Couldn't stop robot!"
            for i in range(0,100):
                try:
                    self.rr.stop()
                    print "OK: Regained control."
                    return # We're clear.
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


