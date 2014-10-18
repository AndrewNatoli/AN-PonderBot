import config
import picamera
import threading

__author__ = 'andrew'

class Camera(threading.Thread):

    filename = "test.jpg"
    queue = False
    okToRun = True

    def __init__(self):
        try:
            self.cam = picamera.PiCamera()
            print "Initialized PiCamera"
        except Exception, e:
            print "Couldn't initialize camera."
            print e
            self.okToRun = False
        finally:
            super(Camera, self).__init__()

    def capture(self,filename):
        self.filename = filename
        self.queue = True

    def run(self):
        while self.okToRun:
            if self.queue:
                try:
                    self.cam.capture(config.__OUTPUT_DIR__ + str(self.filename))
                    print "Captured photo: " + config.__OUTPUT_DIR__ + str(self.filename)
                    self.queue = False
                except Exception:
                    self.queue = False
                    print "Could not take photo!"
        self.cam.close()
        print "Camera finished."

    def kill(self):
        print "Stopping camera."
        self.okToRun = False # This will call cam.close(), fool! :P



