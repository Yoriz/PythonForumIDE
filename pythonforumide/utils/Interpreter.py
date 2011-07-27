# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:05:42 2011

@author: jakob
"""
from twisted.internet.protocol import ProcessProtocol
from twisted.internet import reactor

class PythonProcessProtocol(ProcessProtocol):
    def __init__(self, text):
        self.text = text
        
    def connectionMade(self):
        self.transport.write(self.text)
        self.transport.closeStdin()