import atexit
import database
import os
from camera import *
from raspirobot import *
from time import sleep

__author__ = 'andrew'

# Register an exit handler to shut down mongo db.
# Read the database.py documentation to learn why we have this going on....
def exitHandler():
    print "Exit called! Shut down MongoDB"
    os.system("mongod --shutdown")
    print "Hopefully that worked..."

atexit.register(exitHandler)

print "Hello World!"

database.db.test.find()

#Initialize the camera
camera = Camera()
camera.start()

#Initialize and run the RaspiRobot thread
raspirobot = RaspiRobot()
if raspirobot.okToRun == True:
    raspirobot.start()
else:
    print "Can't use Raspi Robot Board. Quitting."
    exit()

#Capture a test photo
camera.capture("test.jpg")

sleep(1)
raspirobot.kill()
camera.kill()