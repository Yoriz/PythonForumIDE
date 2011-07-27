"""
@author: Jakob, David, bunburya
@reviewer: Somelauw
"""

#YES DIRT HACK GET OVER IT. Dont remove it might go before it goes into master
import sys
sys.path.append('..')

from utils.textutils import split_comments
import wx.stc as stc
import wx
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

        self.filename = ''
        self.directory = '.'
        self.filepath = ''
        self.indent_level = 0        
          
        self.SetGenerics()        
        self.SetMargins()        
        self.SetStyles()
        self.SetBindings()

    def SetBindings(self):
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
    
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
        """This is different from the other Set methods thathttp://paste.pocoo.org/show/446107/ are called in the 
        __init__ this one is for the highlighting and syntax of the langauge,
        this will eventually be callable with different langauge styles. 
        For the moment, leave the lang kwarg in. """
        
        #INDICATOR STYLES FOR ERRORS (self.errorMark)
        self.IndicatorSetStyle(2, stc.STC_INDIC_SQUIGGLE)
        self.IndicatorSetForeground(2, wx.RED)
        self.StyleSetSpec(stc.STC_P_DEFAULT, "face:%(mono)s,size:%(size)d" % faces)

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
            
    def SmartIndent(self):     
        last_line_no = self.GetCurrentLine()
        last_line = split_comments(self.GetLine(last_line_no))[0]
        self.NewLine()
        indent_level = self.GetLineIndentation(last_line_no) // 4
        
        if last_line.endswith(':'):
            indent_level += 1

        indent = "    " * indent_level
        self.AddText(indent)
        
    def OnKeyDown(self, event):
        key = event.GetKeyCode()
        control = event.ControlDown()
        alt = event.AltDown()
        if key == wx.WXK_RETURN and not control and not alt:
            self.SmartIndent()
        else:
            event.Skip()

    def on_undo(self, event):
        """Checks if can Undo and if yes undoes"""
        if self.CanUndo() == 1:
            self.Undo()
        
    def on_redo(self, event):
        """Checks if can Redo and if yes redoes"""
        if self.CanRedo() == 1:
            self.Redo()

    def on_cut(self, event):
        """Cuts selected text"""
        self.Cut()
        
    def on_copy(self, event):
        """Copies selected text"""
        self.Copy()
        
    def on_paste(self, event):
        """Pastes selected text"""
        self.Paste()
        
    def on_clear(self, event):
        """Deletes selected text"""
        self.Clear()

    def on_select_all(self, event):
        """Selects all the text, this function is not necessary but makes it cleaner"""
        self.SelectAll()

    def get_file(self, prompt, style):
        """Abstracted method to prompt the user for a file path.
        Returns a 2-tuple consisting of directory path and file name."""
        dlg = wx.FileDialog(self, prompt, self.directory, '', '*.*', style)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
        else:
            # so maybe add error handling here.
            raise RuntimeError("I guess something has gone wrong with the dialog")
        dlg.Destroy()
        return dirname, filename
        
    def save_file(self):
        if self.filepath:
            self.SaveFile(self.filepath)
        else:
            self.save_file_as()
            
    def save_file_as(self):
        dirname, filename = self.get_file('Save file as', wx.SAVE)
        self.filename = filename
        path = os.path.join(dirname, filename)
        if path:
            self.SaveFile(path)
            
    def open_file(self):
        """Open file, sets the text of Editor to the contents of that file."""
        dirname, filename = self.get_file('Open a file', wx.OPEN)
        path = os.path.join(dirname, filename)
        if path:
            self.pathname = path
            self.LoadFile(path)
            
    def on_close(self, event):
        """Closes current tab"""

        # TODO: we also need to work in a way of detecting if a file
        # has changed since last save/load, and if so prompt the user
        # to save before exit.
        # There should really be an editor instance method

        self.GetParent().DeletePage(self.GetParent().GetSelection())
