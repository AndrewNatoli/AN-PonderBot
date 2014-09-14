import database
import os
from cli import *
from camera import *
from raspirobot import *
from time import sleep

__author__ = 'andrew'

okToRun = True
toDo = "test"

print "Hello World!"

database.db.test.find()

#Command line interface
cli = CLI()
cli.start()

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
    if raspirobot.okToRun and camera.okToRun and cli.okToRun:
        okToRun = True
        sleep(1)
    else:
        print "Something is amiss... STOPPING ROBOT."
        okToRun = False

# Shut down
cli.kill()
raspirobot.kill()
camera.kill()
os.system("sudo mongod --shutdown")