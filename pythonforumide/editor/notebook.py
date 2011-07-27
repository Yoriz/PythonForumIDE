# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:36:42 2011

@author: jakob
"""

import wx.aui as aui
from editor import Editor

class Notebook(aui.AuiNotebook):
    def __init__(self, *args, **kwargs):
        super(Notebook, self).__init__(*args, **kwargs)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.on_tab_closed)
        self.editors = {}
        
    def on_tab_closed(self, event):
        """When a tab is closed remove every editor instance from self.editors
        that is actually a wrapper for the deleted C++ object."""
        ghosts = []
        for key, instance in self.editors.iteritems():
            if not isinstance(instance, Editor):
                ghosts.append(key)
        for ghost in ghosts:
            del self.editors[ghost]
        