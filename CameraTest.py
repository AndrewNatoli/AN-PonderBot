__author__ = 'andrew'

"""
A little HTTP server program to help me pick where I want to place Ponder's camera
"""

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
from time import sleep
from camera import *

PORT_NUMBER = 8080

class myHandler(BaseHTTPRequestHandler):

    #Handler for the GET requests
    def do_GET(self):
        try:
            if self.path=="/":
                self.path="/camera_test.html"
                mimetype='text/html'

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True

            if sendReply:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()

            if self.path == "/camera_test.html":
                #Capture a test photo
                camera.capture("camera_test.jpg")
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

try:
    camera = ""
    camera = Camera()
    camera.start()
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ' , PORT_NUMBER

    #Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    camera.kill()
    server.socket.close()