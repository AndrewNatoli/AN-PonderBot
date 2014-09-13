import database
import camera
from raspirobot import *

__author__ = 'andrew'

print "Hello World!"

database.db.test.find()

camera = camera.Camera()
camera.testCapture()

raspirobot = RaspiRobot()
raspirobot.start()