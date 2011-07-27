# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 17:36:42 2011

@author: jakob
"""
import wx
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
                              id, 'PF-IDE - 0.1a', size=(660,590))

        self.port = get_free_port()        
        
        self.notebook = Notebook(self)

        #perhaps open last edited in the future, for now just open new.
        editor = Editor(self.notebook)  
        editor.filename = "untitled.py"
        self.notebook.editors[self.notebook.GetPageCount()] = editor        
        
        for name, instance in self.notebook.editors.iteritems():
            self.notebook.AddPage(instance, instance.filename)
               
        #self.notebook.GetRowCount()
        self.current_editor = self.notebook.editors[self.notebook.GetSelection()]
        self.spawn_menus()
    
    def on_new(self, event):
        """Opens a new tab with a new editor instance"""
        editor = Editor(self.notebook)
        editor.filename = "untitled.py"

        self.notebook.editors[self.notebook.GetPageCount()] = editor        
        self.notebook.AddPage(editor, editor.filename)

    def on_open(self, event):
        self.current_editor.open_file()
    def on_save(self, event):
        self.current_editor.save_file()
        self.notebook.SetPageText(self.notebook.GetSelection(), self.current_editor.filename)
    def on_save_as(self, event):
        self.current_editor.save_file_as()
        self.notebook.SetPageText(self.notebook.GetSelection(), self.current_editor.filename)
    def on_exit(self, event):
        self.current_editor.exit()    
    def spawn_menus(self):
        """To keep the __init__ short and to aid debugging the construction
        is in seperate methods, this is one of them."""
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        new_id = wx.NewId()
        fileMenu.Append(new_id, "New\tCtrl+N")
        open_id = wx.NewId()
        fileMenu.Append(open_id, "Open\tCtrl+O") 
        save_id = wx.NewId()
        fileMenu.Append(save_id, "Save\tCtrl+S")
        save_as_id = wx.NewId()
        fileMenu.Append(save_as_id, "Save as")
        exit_id = wx.NewId()
        fileMenu.Append(exit_id, "Exit\tCtrl+Q")
        menuBar.Append(fileMenu, "&File")
        editMenu = wx.Menu()
        undo_id = wx.NewId()
        editMenu.Append(undo_id, "Undo\tCtrl+Z")
        redo_id = wx.NewId()
        editMenu.Append(redo_id, "Redo\tCtrl+Y")
        editMenu.AppendSeparator()
        cut_id = wx.NewId()
        editMenu.Append(cut_id, "Cut\tCtrl+X")
        copy_id = wx.NewId()
        editMenu.Append(copy_id, "Copy\tCtrl+C")
        paste_id = wx.NewId()
        editMenu.Append(paste_id, "Paste\tCtrl+V")
        clear_id = wx.NewId()
        editMenu.Append(clear_id, "Delete")
        editMenu.AppendSeparator()
        select_all_id = wx.NewId()
        editMenu.Append(select_all_id, "Select All\tCtrl+A")
        menuBar.Append(editMenu, "&Edit")
        runMenu = wx.Menu()
        run_id = wx.NewId()
        runMenu.Append(run_id, "Run file\tF5")
        menuBar.Append(runMenu, "&Run")
        self.SetMenuBar(menuBar)  
        self.Bind(wx.EVT_MENU, self.on_new, id=new_id)
        self.Bind(wx.EVT_MENU, self.on_open, id=open_id)  
        self.Bind(wx.EVT_MENU, self.on_exit, id=exit_id)
        self.Bind(wx.EVT_MENU, self.on_save, id=save_id)
        self.Bind(wx.EVT_MENU, self.on_save_as, id=save_as_id)
        self.Bind(wx.EVT_MENU, self.current_editor.on_undo, id=undo_id)
        self.Bind(wx.EVT_MENU, self.current_editor.on_redo, id=redo_id)
        self.Bind(wx.EVT_MENU, self.current_editor.on_cut, id=cut_id)
        self.Bind(wx.EVT_MENU, self.current_editor.on_copy, id=copy_id)
        self.Bind(wx.EVT_MENU, self.current_editor.on_paste, id=paste_id)
        self.Bind(wx.EVT_MENU, self.current_editor.on_clear, id=clear_id)
        self.Bind(wx.EVT_MENU, self.current_editor.on_select_all, id=select_all_id)

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
#    reactor.run()
