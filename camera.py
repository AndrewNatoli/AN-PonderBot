import picamera
__author__ = 'andrew'

class Camera:

    def __init__(self):
        cam = picamera.PiCamera()

    def testCapture(self):
        cam.capture("test.jpg")


