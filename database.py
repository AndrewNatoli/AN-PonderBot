from pymongo import MongoClient
import os
import threading
from time import sleep

__author__ = 'andrew'

"""
    This got really messy when a motor test forced the robot to shut down and the MongoDB Service was corrupted.
    Tried to do mongod --repair and all the other things they said to do on the website but it didn't work.
    Rather re-compile MongoDB I decided to make a workaround because this will probably happen again somewhere
    in the development cycle.

    Don't hate me for this awful doing.
    Please.
    I'm just trying to make a happy little robot even though it keeps trying to kill itself :(
"""


class MongoDB(threading.Thread):
    def __init__(self):
        super(MongoDB, self).__init__()
    def run(self):
        os.system("sudo service mongod stop")
        print "Starting MongoDB"
        os.system("sudo mongod")

# Start MognoDB
mongod = MongoDB()
mongod.start()

# Wait a little bit and then we'll try connecting to it!
# If we can't connect, repair the mongo db, restart it and then try the connection again.
# If it doesn't work... just.... let the program explode.
sleep(3)
try:
    print "Connecting to MongoDB"
    client = MongoClient()
    db = client.ponderbot
    print "Connected!"
except Exception:
    print "Failed to connect to MongDB. Attempting repair..."
    os.system("sudo mongod --repair")
    print "Starting over..."
    mongod = MongoDB()
    mongod.start()
    sleep(3)
    try:
        print "Connecting to MongoDB (take 2)"
        client = MongoClient()
        db = client.ponderbot
        print "Connected!"
    except Exception:
        print "Database is being a jerk. Exploding the program."
        os.system("sudo mongod --shutdown")