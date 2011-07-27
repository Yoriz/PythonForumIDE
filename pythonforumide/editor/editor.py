"""
@author: Jakob, David, bunburya
@reviewer: Somelauw
"""

## Do not include pythonforumide in import path, as this breaks imports.
#from utils.Interpreter import Interpreter
from utils.textutils import split_comments
from output import OutputFrame
import wx
import wx.stc as stc
import wx.aui as aui
import os
import code

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
        self.faces = None #will be a config object
        self.filename = ''
        self.indent_level = 0        
        self.SetGenerics()        
        self.SetMargins()        
        self.SetStyles()
        self.SetBindings()
        self.filepath = ''

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

    def run(self, event):
        #interpreter = Interpreter()
        interpreter = code.InteractiveInterpreter()
        text = self.GetText()        
        if not isinstance(text, unicode):
            text.encode("utf-8")
        if not self.filename:
            self.filename = "<script>"
        result, error = interpreter.runsource(text, self.filename, 'exec')
        out = OutputFrame(parent=None, id=-1)
        out.Show()
        out.output.SetText(result.read())
        
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

class MainFrame(wx.Frame):
    """Class with the GUI and GUI functions"""
    def __init__(self, parent, id):
        """Creates the frame, calls some construction methods."""
        wx.Frame.__init__(self, parent,
                              id, 'PF-IDE - *', size=(660,590))
        self.title = "PF-IDE - %s"
        
        self.notebook = aui.AuiNotebook(self)
        self.editor = Editor(self)
        self.notebook.AddPage(self.editor, "Untitled")
        
        self.spawn_menus()
    
    @property
    def dirname(self):
        return os.path.dirname(self.editor.filepath)

    def get_file(self, prompt, style):
        """Abstracted method to prompt the user for a file path.
        Returns a 2-tuple consisting of directory path and file name."""
        dlg = wx.FileDialog(self, prompt, self.dirname, '', '*.*', style)
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetDirectory()
            filename = dlg.GetFilename()
        else:
            # I guess this means something has gone wrong with the dialog,
            # so maybe add error handling here.
            pass
        dlg.Destroy()
        return dirname, filename
       
    def on_new(self, event):
        """Opens a new tab with a new editor instance"""
        #We need to figure out a way of having several editors, perhaps a list
        self.notebook.AddPage(self.editor, "Untitled")

    def open_file(self):
        """Open file, sets the text of Editor to the contents of that file."""
        dirname, filename = self.get_file('Open a file', wx.OPEN)
        path = os.path.join(dirname, filename)
        if path:
            self.pathname = path
            self.editor.LoadFile(path)
            self.SetTitle(self.title % filename)
    
    def save_file(self):
        if self.editor.filepath:
            self.editor.SaveFile(self.editor.filepath)
        else:
            self.save_file_as(self)
        
    def save_file_as(self):
        dirname, filename = self.get_file('Save file as', wx.SAVE)
        path = os.path.join(dirname, filename)
        if path:
            self.editor.filepath = path
            self.editor.SaveFile(path)
            self.SetTitle(self.title % filename)

    def exit(self):
        """Prompt user then quit."""
        dial = wx.MessageDialog(None,'Do you really want to exit?',
                                'Exit Python IDE',
                                wx.YES_NO | wx.ICON_QUESTION)
        # TODO: we also need to work in a way of detecting if a file
        # has changed since last save/load, and if so prompt the user
        # to save before exit.

        if dial.ShowModal() == wx.ID_YES:
            self.Destroy()
    
    def on_open(self, event):
        self.open_file()
    def on_save(self, event):
        self.save_file()
    def on_save_as(self, event):
        self.save_file_as()
    def on_exit(self, event):
        self.exit()

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
        
        #File Menu
        self.Bind(wx.EVT_MENU, self.on_new, id=new_id)
        self.Bind(wx.EVT_MENU, self.on_open, id=open_id)  
        self.Bind(wx.EVT_MENU, self.on_exit, id=exit_id)
        self.Bind(wx.EVT_MENU, self.on_save, id=save_id)
        self.Bind(wx.EVT_MENU, self.on_save_as, id=save_as_id)
        
        #Edit Menu
        self.Bind(wx.EVT_MENU, self.editor.on_undo, id=undo_id)
        self.Bind(wx.EVT_MENU, self.editor.on_redo, id=redo_id)
        self.Bind(wx.EVT_MENU, self.editor.on_cut, id=cut_id)
        self.Bind(wx.EVT_MENU, self.editor.on_copy, id=copy_id)
        self.Bind(wx.EVT_MENU, self.editor.on_paste, id=paste_id)
        self.Bind(wx.EVT_MENU, self.editor.on_clear, id=clear_id)
        self.Bind(wx.EVT_MENU, self.editor.on_select_all, id=select_all_id)
        
        #Run Menu
        self.Bind(wx.EVT_MENU, self.editor.run, id=run_id)

if __name__=='__main__':
    app = wx.PySimpleApp()
    frame = MainFrame(parent=None, id=-1)
    frame.Show()
    #frame.Maximize() #Left commented to stop it getting on my nerves.
    app.MainLoop()
