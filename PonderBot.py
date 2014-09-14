import database
import camera
from raspirobot import *

__author__ = 'andrew'

print "Hello World!"

database.db.test.find()

camera = camera.Camera()
camera.testCapture()

#Initialize and run the RaspiRobot thread
raspirobot = RaspiRobot()
if raspirobot.okToRun == True:
    raspirobot.start()
else:
    print "Can't use Raspi Robot Board. Quitting."
    exit()

from time import sleep
sleep(1)
raspirobot.kill()

if bacon == True:
    print "YES"