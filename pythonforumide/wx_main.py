# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:36:42 2011

@author: jakob, David
"""
import os
import wx
from config import config
from twisted.internet import wxreactor
wxreactor.install()

from twisted.internet import reactor
from twisted.internet.protocol import Factory, Protocol
from editor.editor import Editor
from editor.notebook import Notebook
from utils.version import get_free_port
from utils.interpreter import spawn_python

class MainFrame(wx.Frame):
    """Class with the GUI and GUI functions"""

    def __init__(self, parent, id):
        """Creates the frame, calls some construction methods."""
        wx.Frame.__init__(self, parent,
                              id, 'PF-IDE - 0.1a')

        self.conf = config.conf
        
        self.port = get_free_port()
        
        sizer= wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        panel= wx.Panel(self, style= wx.BORDER_THEME)
        sizer.Add(panel, 1, wx.EXPAND|wx.ALL, 1)
        panel_sizer= wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(panel_sizer)

        self.notebook = Notebook(panel)
        panel_sizer.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 0)        
        
        #perhaps open last edited in the future, for now just open new.
        self.notebook.new_editor_tab()
        self.spawn_menus()
        self.CreateStatusBar()
   
    def spawn_menus(self):
        """Spawns the menus and sets the bindings to keep __init__ short"""
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        menuBar.Append(fileMenu, "&File")
        fileMenu.Append(wx.ID_NEW, "New\tCtrl+N")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_OPEN, "Open\tCtrl+O") 
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_SAVE, "Save\tCtrl+S")
        fileMenu.Append(wx.ID_SAVEAS, "Save as")
        fileMenu.AppendSeparator()
        fileMenu.Append(wx.ID_CLOSE, "Close\tCtrl+W")
        fileMenu.Append(wx.ID_CLOSE_ALL, "Exit\tCtrl+Q")
        
        editMenu = wx.Menu()
        menuBar.Append(editMenu, "&Edit")
        editMenu.Append(wx.ID_UNDO, "Undo\tCtrl+Z")
        editMenu.Append(wx.ID_REDO, "Redo\tCtrl+Y")
        editMenu.AppendSeparator()
        editMenu.Append(wx.ID_CUT, "Cut\tCtrl+X")
        editMenu.Append(wx.ID_COPY, "Copy\tCtrl+C")
        editMenu.Append(wx.ID_PASTE, "Paste\tCtrl+V")
        editMenu.Append(wx.ID_DELETE, "Delete")
        editMenu.AppendSeparator()
        editMenu.Append(wx.ID_SELECTALL, "Select All\tCtrl+A")
        
        searchMenu = wx.Menu()
        searchMenu.Append(wx.ID_FIND, "Replace\tCtrl+H")
        menuBar.Append(searchMenu, "&Search")
        
        runMenu = wx.Menu()
        menuBar.Append(runMenu, "&Run")
        runMenu.Append(wx.ID_EXECUTE, "Run file\tF5")
        
        self.SetMenuBar(menuBar)
        
        tb= self.CreateToolBar(wx.TB_HORIZONTAL|wx.NO_BORDER|wx.TB_FLAT)
        tsize = (24,24)
        new_bmp =  wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        save_bmp= wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        save_as_bmp= wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE_AS, wx.ART_TOOLBAR, tsize)
        cut_bmp= wx.ArtProvider.GetBitmap(wx.ART_CUT, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)
        undo_bmp= wx.ArtProvider.GetBitmap(wx.ART_UNDO, wx.ART_TOOLBAR, tsize)
        redo_bmp= wx.ArtProvider.GetBitmap(wx.ART_REDO, wx.ART_TOOLBAR, tsize)
        tb.SetToolBitmapSize(tsize)
        tb.AddLabelTool(wx.ID_NEW, "New", new_bmp, shortHelp="New", longHelp="Create a new file")
        tb.AddLabelTool(wx.ID_OPEN, "Open", open_bmp, shortHelp="Open", longHelp="Open an exisiting file")
        tb.AddLabelTool(wx.ID_SAVE, "Save", save_bmp, shortHelp="Save", longHelp="Save the currently active file")
        tb.AddLabelTool(wx.ID_SAVEAS, "Save as", save_as_bmp, shortHelp="Save as", longHelp="Save the currently active file as something else")
        tb.AddSeparator()
        tb.AddSimpleTool(wx.ID_CUT, cut_bmp, "Cut", "Cut selected")
        tb.AddSimpleTool(wx.ID_COPY, copy_bmp, "Copy", "Copy selected")
        tb.AddSimpleTool(wx.ID_PASTE, paste_bmp, "Paste", "Paste text")
        tb.AddSeparator()
        tb.AddSimpleTool(wx.ID_UNDO, undo_bmp, "Undo", "Undo")
        tb.AddSimpleTool(wx.ID_REDO, redo_bmp, "Redo", "Redo")
        tb.Realize()
        
        self.Bind(wx.EVT_MENU, self._evt_new, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self._evt_open, id=wx.ID_OPEN)  
        self.Bind(wx.EVT_MENU, self._evt_exit, id=wx.ID_CLOSE_ALL)
        self.Bind(wx.EVT_MENU, self._evt_save, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self._evt_save_as, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self._evt_exit, id=wx.ID_CLOSE_ALL)
        self.Bind(wx.EVT_CLOSE, self._evt_exit)
        self.Bind(wx.EVT_MENU, self._evt_close_current_editor_tab, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self._evt_undo_current_editor_tab, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, self._evt_redo_current_editor_tab, id=wx.ID_REDO)
        self.Bind(wx.EVT_MENU, self._evt_cut_current_editor_tab, id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU, self._evt_copy_current_editor_tab, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self._evt_paste_current_editor_tab, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU, self._evt_clear_current_editor_tab, id=wx.ID_DELETE)
        self.Bind(wx.EVT_MENU, self._evt_selectall_current_editor_tab, id=wx.ID_SELECTALL)
        self.Bind(wx.EVT_MENU, self._evt_replace_current_editor_tab, id=wx.ID_FIND)

    def _evt_new(self, event):
        """Opens a new tab with a new editor instance"""
        self.notebook.new_editor_tab()
    
    def _evt_open(self, event):
        """Opens a new tab and ask for a file to load"""
        self.notebook.open_editor_tab()
    
    def _evt_close_current_editor_tab(self, event):
        """Closes the current editor tab"""
        self.notebook.close_active_editor()
        
    def _evt_save(self, event):
        """Saves the currently active file"""
        self.notebook.save_active_editor_tab()
        
    def _evt_save_as(self, event):
        """Save as required filename"""
        self.notebook.save_as_active_editor_tab()
    
    def _evt_undo_current_editor_tab(self, event):
        """Undo for the current editor tab"""
        self.notebook.undo_active_editor()
   
    def _evt_redo_current_editor_tab(self, event):
        """Redo for the current editor tab"""
        self.notebook.redo_active_editor()
        
    def _evt_cut_current_editor_tab(self, event):
        """Cut for the current editor tab"""
        self.notebook.cut_active_editor()
        
    def _evt_copy_current_editor_tab(self, event):
        """Copy for the current editor tab"""
        self.notebook.copy_active_editor()
    
    def _evt_paste_current_editor_tab(self, event):
        """paste for the current editor tab"""
        self.notebook.paste_active_editor()
        
    def _evt_clear_current_editor_tab(self, event):
        """Clear for the current editor tab"""
        self.notebook.clear_active_editor()
    
    def _evt_selectall_current_editor_tab(self, event):
        """Selectall for the current editor tab"""
        self.notebook.selectall_active_editor()
        
    def _evt_replace_current_editor_tab(self, event):
        """Replace for the current editor tab"""
        self.notebook.replace_active_editor()
        
    def _evt_exit(self, event):
        dial = wx.MessageDialog(None,'Do you really want to exit?',
                        'Exit Python IDE',
                        wx.YES_NO | wx.ICON_QUESTION)
        # TODO: we also need to work in a way of detecting if a file
        # has changed since last save/load, and if so prompt the user
        # to save before exit.

#        f = open("CONFIG", "w")
#        f.write("%s\n%s\n" % (self.GetSize()[0], self.GetSize()[1]))
#        f.close()

        if dial.ShowModal() == wx.ID_YES:
            self.Destroy()

    def get_file(self, prompt, style):
        """Abstracted method to prompt the user for a file path.
        Returns a 2-tuple consisting of directory path and file name."""
        dlg = wx.FileDialog(self, prompt, '.', '', '*.*', style)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
        else:
            # so maybe add error handling here.
            raise RuntimeError("I guess something has gone wrong with the dialog")
        dlg.Destroy()
        return dirname, filename

class ListenProtocol(Protocol):
    def connectionMade(self):
        print "Got connection!!!!"
        
    def connectionLost(self, reason):
        print "Connection closed."

class ListenFactory(Factory):
    protocol = ListenProtocol

if __name__=='__main__':
    app = wx.PySimpleApp(False)
    frame = MainFrame(parent=None, id=-1)
    print frame.port
    frame.Show()
    reactor.registerWxApp(app)
    reactor.listenTCP(frame.port, ListenFactory())
    reactor.spawnProcess(*spawn_python())
    #frame.Maximize() #Left commented to stop it getting on my nerves.
    reactor.run()
