# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 17:22:44 2011

@author: jakob
"""
import wx
from editor.editor import MainFrame

if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = MainFrame(parent=None, id=-1)
    frame.Show()
    #frame.Maximize() #Left commented to stop it getting on my nerves.
    app.MainLoop()