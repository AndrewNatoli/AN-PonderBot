import os
import config
import threading

class CLI(threading.Thread):

    okToRun = True # Keeps the thread alive
    input = ""

    def __init__(self):
        super(CLI, self).__init__()
        print "Initialized command line interface. Call start() to active."

    def run(self):
        while self.okToRun:
            try:
                #Get some input and convert it to lowercase....
                self.input = str(raw_input("PonderBot " + str(config.__VERSION__) + ": ")).lower()
                if self.input != "":
                    words = self.input.split()

                    if words[0] == "shutdown":
                        print "Stopping the robot."
                        self.okToRun = False
                    else:
                        print "Unknown command, " + str(words[0])

            except Exception, e:
                print "Error in CLI Thread"
                print e
                self.okToRun = False


    def kill(self):
        self.okToRun = False

