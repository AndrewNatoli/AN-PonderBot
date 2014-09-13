import database
import camera

__author__ = 'andrew'

print "Hello World!"

database.db.test.find()

camera = camera.Camera()
camera.testCapture()