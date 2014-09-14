import database
from camera import *
from raspirobot import *

__author__ = 'andrew'

print "Hello World!"

database.db.test.find()

#Take a test photo
camera = Camera()
camera.filename = "test2.jpg"
camera.start()

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