__author__ = 'andrew'
import os
import config
import threading

class SpeechRunner (threading.Thread):

    okToRun = False
    speaking = False
    speechQueue = [] # List of items to speak

    def __init__(self):
        super(SpeechRunner, self).__init__()
        print "Starting Speech Runner"
        self.okToRun = True
        print "Raising output volume"
        os.system("amixer sset 'PCM' 90%")

    def speak(self, textToSpeak):
        self.speechQueue.append(textToSpeak)
        print "Added '" + textToSpeak + "' to speech queue"

    def run(self):
        while self.okToRun:
            if len(self.speechQueue) > 0 and not self.speaking:
                self.speaking = True
                aboutToSay = self.speechQueue.pop(0)
                print "Speaking: " + aboutToSay
                os.system(config.__VOICE__ + '"' + aboutToSay + '"')
                print "Done speaking"
                self.speaking = False
        print "SpeechRunner ended."

    def kill(self):
        print "Stopping SpeechRunner thread."
        self.okToRun = False