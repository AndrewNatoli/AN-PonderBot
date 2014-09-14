import database
import os
from camera import *
from raspirobot import *
from time import sleep

__author__ = 'andrew'

okToRun = True
toDo = "test"

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

# Spin up an infinite loop or something
while okToRun:
    # Make sure everything is going alright...
    if raspirobot.okToRun and camera.okToRun:
        okToRun = True
        sleep(1)
    else:
        okToRun = False

# Shut down
raspirobot.kill()
camera.kill()
os.system("sudo mongod --shutdown")