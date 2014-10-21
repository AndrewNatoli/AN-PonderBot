import os
import config
import threading

class CLI(threading.Thread):

    okToRun = True # Keeps the thread alive
    input = ""
    stack = []

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
                    elif words[0] == "photo" or words[0] == "capture":
                        if len(words) > 1:
                            words[0] = "capture"
                            self.stack.append(words)
                        else:
                            print "Missing second argument: filename."

                   # Start the robot
                    elif words[0] == "go" or words[0] == "start":
                        words[0] = "start"
                        self.stack.append(words)

                    # Stop the Robot
                    elif words[0] == "stop":
                        self.stack.append(words)

                    else:
                        print "Unknown command, " + str(words[0])

            except Exception, e:
                print "Error in CLI Thread"
                print e
                self.okToRun = False


    def kill(self):
        self.okToRun = False

