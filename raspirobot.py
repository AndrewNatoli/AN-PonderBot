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
        while self.okToRun == True:
            # Check for side collisions first
            self.leftCollision = self.rr.sw1_closed()
            self.rightCollision = self.rr.sw2_closed()

            if self.leftCollision || self.rightCollision:
                # Did we move forward into something?



            # Check the sonar reading
            self.distance = self.rr.get_distance()

    def forward(self,time):
        self.stop()
        print "Moving forward for " + time + " seconds."
        self.rr.forward(time)

    def stop(self):
        self.goingForward = False
        self.goingReverse = False
        self.turningLeft = False
        self.turningRight = False
        try:
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
        if boolean == True || boolean == False:
            self.rr.set_oc1(boolean)
        else:
            print "Invalid parameter for raspirobot.led3"


    # Second LED on the board
    def led2(self,boolean):
        if boolean == True || boolean == False:
            self.rr.set_led1(boolean)
        else:
            print "Invalid parameter for raspirobot.led3"


    # The extra LED sitting in the first open collector output
    def led3(self,boolean):
        if boolean == True || boolean == False:
            self.rr.set_led2(boolean)
        else:
            print "Invalid parameter for raspirobot.led3"


    def kill(self):
        print "Killed Raspi Robot Thread."
        self.okToRun = False


