# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 02:23:08 2011

@author: jakob
"""

import wx
import wx.stc as stc

class Output(stc.StyledTextCtrl):
    def __init__(self, parent):
        super(Output, self).__init__(parent)
        
class OutputFrame(wx.Frame):
    """Class with the GUI and GUI functions"""
    def __init__(self, parent,id):
        """Creates the frame, calls some construction methods."""
        wx.Frame.__init__(self, parent,
                              id, 'Python - *', size=(660,590))
        self.output = Output(self)