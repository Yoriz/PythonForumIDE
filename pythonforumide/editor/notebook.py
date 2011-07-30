# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:36:42 2011

@author: jakob, David
"""

import os
import wx
import wx.aui as aui
from editor import Editor

class Notebook(aui.AuiNotebook):
    def __init__(self, *args, **kwargs):
        super(Notebook, self).__init__(*args, **kwargs)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self._evt_page_closed)
        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self._evt_page_changed)
        self._active_editor_page= None
        self._active_tab_index= None

    def _evt_page_changed(self, event):
        """sets the currently active page index and editor page"""
        self._active_tab_index= event.Selection
        self._active_editor_page= self.GetPage(self._active_tab_index)
        
    def _evt_page_closed(self, event):
        """Sets currently active page to none and renames the untitled pages"""
        event.Skip()
        self._active_editor_page= None
        wx.CallAfter(self.name_untitled_pages)
        
    def new_editor_tab(self, page_name= ""):
        """Opens a new editor tab"""
        editor= Editor(self) 
        self.AddPage(editor, page_name)
        self._active_editor_page= editor
        self.name_untitled_pages()
        wx.CallAfter(self.SetSelection, self.GetPageCount()-1)
        return editor
        
    def open_editor_tab(self):
        """Loads a slected file into a new editor tab"""
        dirname, filename= self.GetGrandParent().get_file('Open a file', wx.OPEN)
        if dirname and filename:
            editor= self.new_editor_tab(filename)
            path = os.path.join(dirname, filename)
            editor.load_file(path)
        
    def save_active_editor_tab(self):
        """Saves the currently active editor file"""
        if self._active_editor_page.filepath:
            self._active_editor_page.save_file()
        else:
            self.save_as_active_editor_tab()
            
    def save_as_active_editor_tab(self):
        """Save as for the currently active editor file"""
        dirname, filename = self.GetGrandParent().get_file('Save file as', wx.SAVE)
        if dirname and filename:
            path = os.path.join(dirname, filename)
            if path:
                if self._active_editor_page.save_file_as(path):
                    self.set_active_tab_text(filename)
                    self._active_editor_page.filepath = path
            
    def set_active_tab_text(self, text):
        """Rename the currently active tab text"""
        if self._active_tab_index> -1:
            self.SetPageText(self._active_tab_index, text)
        
    def name_untitled_pages(self):
        """Renumbers the untitled pages"""
        empty_page_no= 1
        for page_no in xrange(self.GetPageCount()):
            page_text= self.GetPageText(page_no)
            if "Untitled" in page_text or not page_text:
                page= self.GetPage(page_no)
                self.SetPageText(page_no, "Untitled%s.py" % (empty_page_no))
                empty_page_no+= 1
                
    
    def close_active_editor(self):
        """Closes the currently active editor tab"""
        self.DeletePage(self._active_tab_index)
        wx.CallAfter(self.name_untitled_pages)
        
    def undo_active_editor(self):
        """Undo changes in active editor"""
        self._active_editor_page.on_undo()
        
    def redo_active_editor(self):
        """Redo changes in active editor"""
        self._active_editor_page.on_redo()
        
    def cut_active_editor(self):
        """Cut changes in active editor"""
        self._active_editor_page.on_cut()
        
    def copy_active_editor(self):
        """Copy changes in active editor"""
        self._active_editor_page.on_copy()
        
    def paste_active_editor(self):
        """Paste changes in active editor"""
        self._active_editor_page.on_paste()
    
    def clear_active_editor(self):
        """Paste changes in active editor"""
        self._active_editor_page.on_clear()
        
    def selectall_active_editor(self):
        """Sslectall changes in active editor"""
        self._active_editor_page.on_select_all()
        
    def replace_active_editor(self):
        """Replace changes in active editor"""
        self._active_editor_page.on_replace()

            
        
        
        
