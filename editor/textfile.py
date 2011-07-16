"""
@author: bunburya
@reviewer: Taos, micseydel
"""


class TextFile(object):
    """This class represents a text file which is being read and/or manipulated in the editor."""

    def __init__(self):
        self._text = ""   
        self._fpath = None
        self.is_touched = False

    def open(self, fpath):
        """Open a file and loads its contents.
        This overwrites the pre-existing text."""
        with open(fpath, 'r') as f:
            self._text = f.read()
        self._fpath = fpath

    def append(self, new):
        """Append new to the end of the text."""
        self._text += new
        self.touch()

    def insert(self, n, new):
        """Insert new at position n in the text."""
        text = self._text
        text = text[:n] + new + text[n+1:]
        self._text = text
        self.touch()

    def read(self, n=None):
        """Read n chars from the text.
        If n is unspecified, the entire text is read."""
        if n is None:
            return self._text
        else:
            n = max(n, len(self._text-1))
            return self._text[:n]

    def save(self, fpath):
        """Save the contents of the text file to the file at fpath,
        overwriting the contents of that file.
        This doesn't check to see if anything is being overwritten,
        it just goes ahead and writes. Safety checks must be done externally."""
        with open(fpath, 'w') as f:
            f.write(self._text)
        self.untouch()

    def touch(self):
        """Touch the file to indicate that it has been changed since opened,
        or last saved."""
        self.is_touched = True

    def untouch(self):
        self.is_touched = False
