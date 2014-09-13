"""
    Contains logic for bump switches, sonar and motor control
"""

__author__ = 'andrew'
import threading
from rrb2 import *

class RaspiRobot(threading.Thread):

    def __init__(self):
        super(RaspiRobot, self).__init__()
        print "Created Raspi Robot"
        self.rr = RRB2()

    def run(self):
        print "Running Raspi Robot"
        self.rr.set_led1(True)


