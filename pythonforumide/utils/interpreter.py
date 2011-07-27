# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:05:42 2011

@author: jakob
"""
import sys
sys.path.append('..')

from twisted.internet.protocol import ProcessProtocol
from utils.version import get_python_exe

class PythonProcessProtocol(ProcessProtocol):       
    def __init__(self, frame):
        self.frame = frame
        
    def connectionMade(self):
        print "subprocess open.!"
        self.transport.write("2+2")
        
    def outReceived(self, data):
        print "Got stdout."
    
    def errRecieved(self, data):
        print "Got stderr!"

def spawn_python():
    return [PythonProcessProtocol(), get_python_exe(), ["python"]]
