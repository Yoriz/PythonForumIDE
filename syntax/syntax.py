# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 16:45:41 2011

@author: jakob
"""

class Styler(object):
    def __init__(self, language='python', configobj):
        self.language = language
        self.config = configobj