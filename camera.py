import config
import picamera
import threading

__author__ = 'andrew'

class Camera(threading.Thread):

    filename = "test.jpg"

    def __init__(self):
        self.cam = picamera.PiCamera()
        print "Initialized PiCamera"
        super(Camera, self).__init__()

    def run(self):
        try:
            self.cam.capture(config.__OUTPUT_DIR__ + str(self.filename))
            print "Captured photo: " + config.__OUTPUT_DIR__ + str(self.filename)
        except Exception:
            print "Could not take photo!"


