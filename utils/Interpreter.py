# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:05:42 2011

@author: jakob
"""

class Interpreter(object):
    def run(self, code_object, g = None, l = None):
        if (g is None) or (l is None):
            exec code_object

class IPythonInterpreter(Interpreter):
    pass

class BPythonInterpreter(Interpreter):
    pass