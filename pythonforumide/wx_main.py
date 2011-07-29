# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:36:42 2011

@author: jakob, David
"""
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

        # Load configuration
        config_file = config.config_file("default")
        conf = config.load_config(config_file)

        # Set defaults
        conf.set_default("indent", 4)
        conf.set_default("usetab", 0) #0 means false
        self.conf = conf
        self.conf.save()
        
        self.port = get_free_port()        
        
        self.notebook = Notebook(self)
        self.untitled_index = 1

        #perhaps open last edited in the future, for now just open new.
        self.add_editor("untitled.py")
               
        #self.notebook.GetRowCount()
        self.current_editor = self.notebook.editors[self.notebook.GetSelection()]
        self.spawn_menus()
        self.CreateStatusBar()

    def add_editor(self, filename):
        """Open an new empty editor instance in a new tab"""
        editor = Editor(self.notebook)
        editor.filename = filename

        # Pass along config file
        editor.conf = self.conf

        self.untitled_index += 1

        self.notebook.editors[self.notebook.GetPageCount()] = editor        
        self.notebook.AddPage(editor, editor.filename)
        
    def on_new(self, event):
        """Opens a new tab with a new editor instance"""
        self.add_editor("untitled%s.py" % self.untitled_index)

    def on_open(self, event):
        editor = Editor(self.notebook)
        self.notebook.InsertPage(0, editor, editor.filename)
        editor.open_file()

        # Pass along config file
        editor.conf = self.conf

        self.notebook.SetSelection(0)
        self.notebook.SetPageText(0, editor.filename)
        self.current_editor = self.notebook.editors[0]
   
    def on_save(self, event):
        self.current_editor.save_file()
        self.notebook.SetPageText(self.notebook.GetSelection(), self.current_editor.filename)

    def on_save_as(self, event):
        self.current_editor.save_file_as()
        self.notebook.SetPageText(self.notebook.GetSelection(), self.current_editor.filename)
    
    def on_exit(self, event):
        dial = wx.MessageDialog(None,'Do you really want to exit?',
                        'Exit Python IDE',
                        wx.YES_NO | wx.ICON_QUESTION)
        # TODO: we also need to work in a way of detecting if a file
        # has changed since last save/load, and if so prompt the user
        # to save before exit.

        f = open("CONFIG", "w")
        f.write("%s\n%s\n" % (self.GetSize()[0], self.GetSize()[1]))
        f.close()

        if dial.ShowModal() == wx.ID_YES:
            self.Destroy()

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
        
        self.Bind(wx.EVT_MENU, self.on_new, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, self.on_open, id=wx.ID_OPEN)  
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_CLOSE_ALL)
        self.Bind(wx.EVT_MENU, self.on_save, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, self.on_save_as, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, self.on_exit, id=wx.ID_CLOSE_ALL)
        self.Bind(wx.EVT_CLOSE, self.on_exit)
        self.Bind(wx.EVT_MENU, self.current_editor.on_close, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.current_editor.on_undo, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, self.current_editor.on_redo, id=wx.ID_REDO)
        self.Bind(wx.EVT_MENU, self.current_editor.on_cut, id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU, self.current_editor.on_copy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self.current_editor.on_paste, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU, self.current_editor.on_clear, id=wx.ID_DELETE)
        self.Bind(wx.EVT_MENU, self.current_editor.on_select_all, id=wx.ID_SELECTALL)
        self.Bind(wx.EVT_MENU, self.current_editor.on_replace, id=wx.ID_FIND)

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
