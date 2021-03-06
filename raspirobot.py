"""
    Contains logic for bump switches, sonar and motor control
"""

__author__ = 'andrew'
import os
import threading
import config
from rrb2 import *
from time import sleep
from enum import Enum
from random import randint

bacon = True

class RaspiRobot(threading.Thread):

    class Incidents(Enum):
        nothing = -1
        wentForward = 0
        wentReverse = 1
        turnedLeft = 2
        turnedRight = 3
        crashedForward = 4
        crashedLeft = 5
        crashedRight = 6

    class Directions(Enum):
        stopped = -1
        forward = 0
        reverse = 1
        left = 2
        right = 3

    okToRun = False             # Keeps the thread alive


    timeSinceDistanceScan = 0 # The amount of ticks since we last checked the sonar reading


    direction = Directions.stopped

    lastIncident = Incidents.nothing

    moveTime = 0                # How many iterations have we been moving for?
    stopTime = 0                # Stop moving after this many iterations of the run loop

    leftCollision = False       # Status of left lever switch used as a collision detector
    rightCollision = False      # Status of right lever switch used as a collision detector

    distance = 9001             # Distance reading from the sonar

    active = False              # Whether or not we SHOULD move.


    def __init__(self):
        super(RaspiRobot, self).__init__()
        print "Created Raspi Robot. MWAH HAWH HAWH!"
        try:
            self.rr = RRB2()
            self.led1(True)
            sleep(0.1)
            self.led1(False)
            sleep(0.1)
            self.led1(False)
            self.led2(False)
            self.okToRun = True
            print "Raspi Robot Initialized."
            print "Start with \"start\" command!"
        except Exception:
            self.okToRun = False
            print "Failed to initialize RaspiRobot Board"

    # Run the robot!
    def run(self):
        print "Running Raspi Robot"
        while self.okToRun:
            if self.active:
                self.doMotion()
            else:
                print "Robot stopped. Sleep for three seconds."
                sleep(3)

    # Use CLI command "start" to start the robot
    def startMoving(self):
        print "RasPi Robot: startMoving"
        self.active = True
        self.okToRun = True

    # Make the robot stop moving
    def stopMoving(self):
        self.active = False

    def doMotion(self):
        # Check the sonar reading every fifty iterations
        if self.timeSinceDistanceScan >= 20:
            self.distance = self.rr.get_distance()
            self.timeSinceDistanceScan = 0

        # Increment the timeSinceDistanceScan
        self.timeSinceDistanceScan += 1

        # Check for side collisions first
        self.leftCollision = self.rr.sw1_closed()
        self.rightCollision = self.rr.sw2_closed()

        if self.leftCollision or self.rightCollision:
            # Did we move forward into something?
            if self.direction == self.Directions.forward:
                print "Crashed into something while moving forward."
                self.lastIncident = self.Incidents.crashedForward
                self.reverse(200)
            """ Going in reverse is handled by the timer """
            # Stopped?
            if self.direction == self.Directions.stopped:
                # Which switch did it?
                if self.leftCollision and not self.rightCollision:
                    # Try turning right...
                    self.right(200)
                elif self.rightCollision and not self.leftCollision:
                    # Try turning left...
                    self.left(200)
                else:
                    # Keep backing up....
                    self.reverse(200)

        # Are we moving? Should we stop?
        if self.direction != self.Directions.stopped:
            self.moveTime += 1

            # If we've been going in a certain direction for too long, stop ourselves.
            if self.moveTime >= self.stopTime:
                # Reset our move counter... JUST IN CASE. 2014-10-15 Attempt to fix infinite reverse bug.
                self.moveTime = 0;

                # First, we'll stop...
                howMoved = self.direction

                # We were going backwards...
                if howMoved == self.Directions.reverse:
                    # Why were we going in reverse?
                    if self.lastIncident == self.Incidents.crashedForward:
                        # We crashed while moving forward...
                        if self.leftCollision or self.rightCollision:
                            # We're STILL crashed? Ugh! Get free somehow!
                            if self.leftCollision and not self.rightCollision:
                                self.rr.right(0.5, config.__MAX_SPEED__)
                            elif self.rightCollision and not self.leftCollision:
                                self.rr.left(0.5, config.__MAX_SPEED__)
                            else: # Both are pressed... try to wiggle free.
                                self.rr.right(0.5, config.__MAX_SPEED__)
                                self.rr.left(0.5, config.__MAX_SPEED__)
                                self.reverse(250)
                        else:
                            # We're free!
                            self.lastIncident = self.Incidents.nothing
                            # Turn randomly...
                            choose = randint(1,2)
                            if choose == 1:
                                self.left(200)
                            else:
                                self.right(200)
                    # Did we crash while turning?
                    elif self.lastIncident == self.Incidents.crashedLeft or self.lastIncident == self.Incidents.crashedRight:

                        # We had crashed while turning left before backing up!
                        if self.lastIncident == self.Incidents.crashedLeft:
                            self.rr.right(0.5, config.__MAX_SPEED__) # Pauses the thread while this happens...
                            self.lastIncident = self.Incidents.nothing # Reset the incident
                            # Crashed right while turning right
                            if self.rr.sw2_closed():
                                self.lastIncident = self.Incidents.crashedRight
                                self.reverse(randint(200,450))
                            # No we didn't!
                            else:
                                # There's an obstacle closer than 10cm
                                if self.rr.get_distance() < 10:
                                    while self.rr.get_distance() < 10:
                                        self.rr.right(0.5)
                                        if self.rr.sw2_closed():
                                            self.lastIncident = self.Incidents.crashedRight
                                            self.reverse(randint(200,500))
                                            break  # Quit this little distance check loop
                                    # If we didn't crash right while in that loop... move forward!
                                    if self.lastIncident is not self.Incidents.crashedRight:
                                        self.forward(randint(200, 400))
                                # Obstacle further than 10cm
                                else:
                                    self.lastIncident = self.Incidents.nothing
                                    self.forward(randint(200, 400))

                        # We crashed while turning to the right somehow!
                        elif self.lastIncident == self.Incidents.crashedRight:
                            self.rr.left(0.5, config.__MAX_SPEED__) # Pauses the thread while this happens...
                            self.lastIncident = self.Incidents.nothing # Reset the incident
                            # Crashed right while turning right
                            if self.rr.sw1_closed():
                                self.lastIncident = self.Incidents.crashedLeft
                                self.reverse(randint(200,450))
                            # No we didn't!
                            else:
                                # There's an obstacle closer than 10cm
                                if self.rr.get_distance() < 10:
                                    while self.rr.get_distance() < 10:
                                        self.rr.left(0.5)
                                        if self.rr.sw1_closed():
                                            self.lastIncident = self.Incidents.crashedLeft
                                            self.reverse(randint(200, 500))
                                            break  # Quit this little distance check loop
                                    # If we didn't crash right while in that loop... move forward!
                                    if self.lastIncident is not self.Incidents.crashedLeft:
                                        self.forward(randint(200, 400))
                                # Obstacle further than 10cm
                                else:
                                    self.lastIncident = self.Incidents.nothing
                                    self.forward(randint(200, 400))
                        else:
                            print "Not sure how we ended up here.... (side crash --> reverse --> motion expiry)"
                    # We weren't backing up because of an incident. It was for the funsies! (or sonar or something)
                    else:
                        # If NOW we have a collision...
                        if self.leftCollision or self.rightCollision:
                            # Left Collision
                            if self.leftCollision and not self.rightCollision:
                                # Try moving right
                                self.rr.right(0.5,config.__MAX_SPEED__)
                                # If there's still a collision
                                if self.leftCollision or self.rightCollision:
                                    # Back up and report the incident
                                    self.reverse(randint(200,400))
                                    self.lastIncident = self.Incidents.crashedLeft
                                # No collision.
                                else:
                                    # Reverse if close to something
                                    if self.rr.get_distance() < 10:
                                        self.reverse(randint(200,400))
                                    # Forward if not
                                    else:
                                        self.forward(randint(200,400))
                            # If we had a collision from the right... handle it just about the same way
                            elif self.rightCollision and not self.leftCollision:
                                self.rr.left(0.5,config.__MAX_SPEED__)
                                if self.leftCollision or self.rightCollision:
                                    self.reverse(randint(200,400))
                                    self.lastIncident = self.Incidents.crashedRight
                                else:
                                    if self.rr.get_distance() < 10:
                                        self.reverse(randint(200,400))
                                    else:
                                        self.forward(randint(200,400))
                        # No collision! Check distance and do things that way.
                        else:
                            if self.distance > 10:
                                choose = randint(1,4)
                                if choose == 1 or choose == 2:
                                    self.forward(randint(200,400))
                                elif choose == 3:
                                    self.left(randint(100,400))
                                else:
                                    self.right(randint(100,400))
                            else:
                                choose = randint(1,3)
                                if choose == 1:
                                    self.reverse(randint(100,400))
                                elif choose == 2:
                                    self.left(randint(100,300))
                                else:
                                    self.right(randint(100,300))




                # We were moving forward...
                if howMoved == self.Directions.forward:
                    # Something further than 10cm...
                    if self.distance > 10:
                        if not self.leftCollision and not self.rightCollision:
                            choose = randint(1, 9)
                            if choose == 7:
                                self.left(randint(40, 150))
                            elif choose == 8:
                                self.left(randint(40, 150))
                            elif choose == 9:
                                self.reverse(randint(40,150))
                            else:
                                self.forward(randint(200, 400))
                        else:
                            self.lastIncident = self.Incidents.crashedForward
                            if self.leftCollision and not self.rightCollision:
                                self.right(250)
                            elif self.rightCollision and not self.leftCollision:
                                self.left(250)
                            else:
                                self.reverse(randint(250, 450))
                    # Closer than 10cm...
                    else:
                        # Bumpers are clear
                        if not self.leftCollision and not self.rightCollision:
                            choose = randint(1,3)
                            if choose == 1:
                                self.left(250)
                            elif choose == 2:
                                self.right(250)
                            else:
                                self.reverse()
                        # Closer than 10cm and side collision
                        else:
                            self.lastIncident = self.Incidents.crashedForward
                            # Crashed left
                            if self.leftCollision and not self.rightCollision:
                                self.right(randint(200, 300))
                            # Crashed Right
                            elif self.rightCollision and not self.leftCollision:
                                self.left(randint(200, 300))
                            # Hit both sensors...
                            else:
                                self.reverse(randint(200, 400))

                # We were turning left
                if howMoved == self.Directions.left:
                    # Something's further than 10cm away
                    if self.distance > 10:
                        # Bumpers are clear...
                        if not self.leftCollision and not self.rightCollision:
                            self.forward(200)
                        # Side collision! D:
                        else:
                            self.lastIncident = self.Incidents.crashedLeft
                            self.reverse(randint(200,400))

                    # Something's closer than 10cm away
                    else:
                        # Keep turning left
                        if not self.leftCollision and not self.rightCollision:
                            self.left(250)
                        # Side collision!
                        else:
                            self.lastIncident = self.Incidents.crashedLeft
                            self.reverse(randint(200,400))


                # We were turning right
                if howMoved == self.Directions.right:
                    # Something is further than 10cm away
                    if self.distance > 10:
                        # Bumpers are clear...
                        if not self.leftCollision and not self.rightCollision:
                            self.forward(200)
                        # Side collision! D:
                        else:
                            self.lastIncident = self.Incidents.crashedRight
                            self.reverse(randint(200, 400))

                    # Something is closer than 10cm away
                    else:
                        # Keep turning right
                        if not self.leftCollision and not self.rightCollision:
                            self.right(250)
                        # Side collision!
                        else:
                            self.lastIncident = self.Incidents.crashedRight
                            self.reverse(randint(200, 400))

            # These checks will happen WHILE we're moving
            else:
                # Check the distance
                if self.distance <= 20:
                    # Are we moving forward?
                    if self.direction == self.Directions.forward:
                        # This will force the robot to stop and carry out post-motion behavior.
                        print "Something is in the way. Stop moving forward."
                        self.moveTime = self.stopTime
                elif self.distance > 20:
                    # If we're moving in reverse and there's a clear path ahead
                    if self.direction == self.Directions.reverse:
                        if not self.leftCollision and not self.rightCollision:
                            self.moveTime = self.stopTime
                elif self.leftCollision or self.rightCollision:
                    if self.leftCollision and not self.rightCollision:
                        self.right(randint(100,300))
                        self.lastIncident = self.Incidents.crashedLeft
                    elif self.rightCollision and not self.leftCollision:
                        self.left(randint(100,300))
                        self.lastIncident = self.Incidents.crashedRight
                    elif self.rightCollision and self.leftCollision:
                        self.reverse(randint(100,300))
                        self.lastIncident = self.Incidents.crashedForward
                    else:
                        print "Not sure how we ended up here (gibberish code sdf2hewdfsu9)"




    # Start moving forward
    def forward(self,time=200):
        self.stop()
        try:
            print "Revving up..."
            self.rr.set_motors(config.__MAX_SPEED__,0,config.__MAX_SPEED__,0)
            self.direction = self.Directions.forward
            self.stopTime = time
            print "Moving forward for " + str(time) + " ticks."
        except Exception, e:
            print "Can't move forward!"
            print e
            self.stop()


    # Start moving in reverse
    def reverse(self,time=200):
        self.stop()
        try:
            self.rr.set_motors(config.__MAX_SPEED__,1,config.__MAX_SPEED__,1)
            self.direction = self.Directions.reverse
            self.stopTime = time
            print "Backing up for " + str(time) + " ticks."
        except Exception, e:
            print "Can't back up!"
            print e
            self.stop()

    # Turn left
    def left(self,time=200):
        self.stop()
        try:
            self.rr.set_motors(config.__MAX_SPEED__,1,config.__MAX_SPEED__,0)
            self.direction = self.Directions.left
            self.stopTime = time
            print "Turning left for " + str(time) + " ticks."
        except Exception, e:
            print "Can't turn left!"
            print e
            self.stop()

    # Turn right
    def right(self,time=200):
        self.stop()
        try:
            self.rr.set_motors(config.__MAX_SPEED__,0,config.__MAX_SPEED__,1)
            self.direction = self.Directions.right
            self.stopTime = time
            print "Turning right for " + str(time) + " ticks."
        except Exception, e:
            print "Can't turn right!"
            print e
            self.stop()

    # Stop the robot. If we can't, shut it down.
    def stop(self):
        self.moveTime = 0
        self.stopTime = 0
        try:
            self.rr.stop()
            print "Stopped."
        except Exception:
            print "WARNING: Couldn't stop robot!"
            for i in range(0,100):
                try:
                    self.rr.stop()
                    print "OK: Regained control."
                    return  # We're clear.
                except Exception:
                    pass
            # If we've lost control entirely then shut down the system.
            os.system("sudo shutdown -h 0 PonderBot lost control of RaspiRobot board.")


    # First LED on the board
    def led1(self,boolean):
        self.rr.set_led1(boolean)


    # Second LED on the board
    def led2(self,boolean):
        self.rr.set_led2(boolean)


    # The extra LED sitting in the first open collector output
    def led3(self,boolean):
        self.rr.set_oc1(boolean)

    def kill(self):
            print "Killed Raspi Robot Thread."
            self.okToRun = False


