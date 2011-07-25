"""
@author: Jakob, David
@reviewer: Somelauw
"""

import wx
import wx.stc as stc
import os

#TODO: make customisable font and sizes. Perhaps maked this named tuple?
faces = { 'times': 'Times',
              'mono' : 'Courier',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

class Editor(stc.StyledTextCtrl):
    def __init__(self, parent):
        super(Editor, self).__init__(parent)
        self.SetGenerics()        
        self.SetMargins()        
        self.SetStyles()

    def SetGenerics(self):
        """Rather than do it in the __init__ and to help debugging the styles
        and settings are split into seperate SetOptions, this sets the generic
        options like Tabwidth, expandtab and indentation guides + others."""
        self.SetLexer(stc.STC_LEX_PYTHON) #is this giving us trouble? 
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:%(mono)s,size:%(size)d" % faces) #set mono spacing here!
        self.SetTabWidth(4)
        self.SetIndentationGuides(1)
        #Indentation will only use space characters if useTabs is false
        self.SetUseTabs(False)
        
    def SetMargins(self):
        """This is specifically for the margins. Like the other Set methods it
        is only really to be called in the __init__ its here more for 
        readability purpsoses than anything else."""
        # margin 0 for breakpoints
        self.SetMarginSensitive(0, True)
        self.SetMarginType(0, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(0, 0x3)
        self.SetMarginWidth(0, 12)
        # margin 1 for current line arrow
        self.SetMarginSensitive(1, False)
        self.SetMarginMask(1, 0x4)
        # margin 2 for line numbers
        self.SetMarginType(2, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(2, 28)
     
    def SetStyles(self, lang='python'):
        """This is different from the other Set methods that are called in the 
        __init__ this one is for the highlighting and syntax of the langauge,
        this will eventually be callable with different langauge styles. 
        For the moment, leave the lang kwarg in. """
        
        #INDICATOR STYLES FOR ERRORS (self.errorMark)
        self.IndicatorSetStyle(2, stc.STC_INDIC_SQUIGGLE)
        self.IndicatorSetForeground(2, wx.RED)
        self.StyleSetSpec(stc.STC_P_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)
        self.StyleClearAll()

        # Python styles
        
        # White space
        self.StyleSetSpec(stc.STC_P_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)
        # Comment
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "face:%(mono)s,fore:#007F00,back:#E8FFE8,italic,size:%(size)d" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "face:%(mono)s,fore:#007F7F,size:%(size)d" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "face:%(mono)s,fore:#7F007F,size:%(size)d" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "face:%(mono)s,fore:#7F007F,size:%(size)d" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "face:%(mono)s,fore:#00007F,bold,size:%(size)d" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "face:%(mono)s,fore:#7F0000,size:%(size)d" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "face:%(mono)s,fore:#7F0000,size:%(size)d" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "face:%(mono)s,fore:#0000FF,bold,underline,size:%(size)d" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "face:%(mono)s,fore:#007F7F,bold,size:%(size)d" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "face:%(mono)s,bold,size:%(size)d" % faces)
        # Identifiers
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "")
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "face:%(mono)s,fore:#990000,back:#C0C0C0,italic,size:%(size)d" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "face:%(mono)s,fore:#000000,face:%(mono)s,back:#E0C0E0,eol,size:%(size)d" % faces)


class MainFrame(wx.Frame):
    """Class with the GUI and GUI functions"""
    def __init__(self, parent,id):
        """Creates the frame, calls some construction methods."""
        wx.Frame.__init__(self, parent,
                              id, 'TitleToBeChanged', size=(660,590))
        self.dirname = ''
        self.text_input = Editor(self)
        self.spawn_menus()
        
    def on_open(self, event):
        """Open file, sets the text of Editor to the contents of that file."""
        dlg = wx.FileDialog(self, "Open a file", self.dirname, 
                            "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_name=dlg.GetFilename()
            self.dir_name=dlg.GetDirectory()
            file_handle=open(os.path.join(self.dir_name, self.file_name), 'rb')
            
            self.SetTitle("%s" % self.file_name)
            self.text_input.SetText(file_handle.read())
            file_handle.close()
        dlg.Destroy()

    def on_close(self, event):
        """Prompt user then quit."""
        dial = wx.MessageDialog(None,'Do you really want to exit?',
                                'Exit Python IDE',
                                wx.YES_NO |wx.ICON_QUESTION)

        if dial.ShowModal() == wx.ID_YES:
            self.Destroy()

    def spawn_menus(self):
        """To keep the __init__ short and to aid debugging the construction
        is in seperate methods, this is one of them."""
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        
        open_selection = fileMenu.Append(wx.ID_ANY, "Open\tCtrl+O") 
        exit_selection = fileMenu.Append(wx.ID_ANY, "Exit\tCtrl+Q")
        menuBar.Append(fileMenu, "File")

        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.on_open, open_selection)  
        self.Bind(wx.EVT_MENU, self.on_close, exit_selection)
        
if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = MainFrame(parent=None, id=-1)
    frame.Show()
    #frame.Maximize() #Left commented to stop it getting on my nerves.
    app.MainLoop()
