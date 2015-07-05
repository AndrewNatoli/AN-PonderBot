# import database
import os
from cli import *
from camera import *
from raspirobot import *
from time import sleep
from speechRunner import *

__author__ = 'andrew'

okToRun = True
toDo = "test"

def do_task(task):
    print "Got a task: " + str(task)
    if task[0] == "capture":
        voice.speak("Taking a photo. Say cheese.")
        camera.capture(task[1])
    if task[0] == "start":
        voice.speak("Executing motor control logic.")
        raspirobot.startMoving()
    if task[0] == "stop":
        voice.speak("Ending motor control logic.")
        raspirobot.stopMoving()
    if task[0] == "say":
        task.pop(0)
        voice.speak(" ".join(task))

# Load the speech engine!
voice = SpeechRunner()
voice.start()
voice.speak("Hello world, I am Ponder.")
sleep(2)

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
voice.speak("Camera is on.")

#Initialize and run the RaspiRobot thread
raspirobot = RaspiRobot()
raspirobot.start() # We used to check okToRun before calling this but now the thread does that itself.
voice.speak("Motor control and sensor logic activated.")

#Capture a test photo
camera.capture("test.jpg")
voice.speak("Took a test picture! Hope it came out nice.")

voice.speak("Current temperature and humidity... oh dear, Andrew broke that sensor.")

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
        voice.speak("Warning! Something is amiss")
        print "Something is amiss... STOPPING ROBOT."
        okToRun = False


# Shut down
voice.speak("Shutting down. Sad face.")
cli.kill()
raspirobot.kill()
camera.kill()
os.system("sudo mongod --shutdown")
voice.kill()
