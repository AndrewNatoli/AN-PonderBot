"""
    Contains logic for bump switches, sonar and motor control
"""

__author__ = 'andrew'
import threading
from rrb2 import *
from time import sleep

bacon = True

class RaspiRobot(threading.Thread):

    okToRun = False

    def __init__(self):
        super(RaspiRobot, self).__init__()
        print "Created Raspi Robot"
        try:
            self.rr = RRB2()
            self.rr.set_led1(True)
            sleep(0.1)
            self.rr.set_led2(True)
            sleep(0.1)
            self.rr.set_led1(False)
            self.rr.set_led2(False)
            self.okToRun = True
            print "Raspi Robot Initialized."
        except Exception:
            self.okToRun = False
            print "Failed to initialize RaspiRobot Board"

    def run(self):
        print "Running Raspi Robot"
        while self.okToRun == True:
            print "OK."

    def kill(self):
        print "Killed Raspi Robot Thread."
        self.okToRun = False


