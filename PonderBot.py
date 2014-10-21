# import database
import os
from cli import *
from camera import *
from raspirobot import *
from time import sleep

__author__ = 'andrew'

okToRun = True
toDo = "test"

def do_task(task):
    print "Got a task: " + str(task)
    if task[0] == "capture":
        camera.capture(task[1])
    if task[0] == "start":
        raspirobot.startMoving()
    if task[0] == "stop":
        raspirobot.stopMoving()


""" Run the program! """

print "Hello World!"
print "======================================================="
print "PonderBot v" + str(config.__VERSION__) + " by Andrew Natoli"
print "AndrewNatoli@AndrewNatoli.com"
print "http://AndrewNatoli.com"
print "USE THIS SOFTWARE AT YOUR OWN RISK. I'm not responsible"
print "if this breaks anything!"
print "======================================================="


#Database is initialized when we import the database module so this will work ;)
# database.db.test.find()

#Command line interface
cli = CLI()
cli.start()

#Initialize the camera
camera = Camera()
camera.start()

#Initialize and run the RaspiRobot thread
raspirobot = RaspiRobot()
raspirobot.start() # We used to check okToRun before calling this but now the thread does that itself.

#Capture a test photo
camera.capture("test.jpg")

# Spin up an infinite loop or something
while okToRun:
    # Make sure everything is going alright...
    if raspirobot.okToRun and camera.okToRun and cli.okToRun:
        # Look for something to do!
        if len(cli.stack) > 0:
            try:
                do_task(cli.stack.pop())
            except Exception, e:
                print "Failed to handle task: " + str(e)
        else:
            # If there's nothing to do sleep for a second.
            sleep(1)
    else:
        print "Something is amiss... STOPPING ROBOT."
        okToRun = False


# Shut down
cli.kill()
raspirobot.kill()
camera.kill()
os.system("sudo mongod --shutdown")