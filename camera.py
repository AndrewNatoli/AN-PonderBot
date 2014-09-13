import config
import picamera

__author__ = 'andrew'

class Camera:
    def __init__(self):
        self.cam = picamera.PiCamera()

    def testCapture(self):
        try:
            self.cam.capture(config.__OUTPUT_DIR__ + "test.jpg")
        except Exception:
            print "Could not capture test photo"


