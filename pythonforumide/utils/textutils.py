# -*- coding: utf-8 -*-
"""
Functions for parsing and manipulating pieces of text.

@author: bunburya
"""

def split_comments(line):
    """Takes a string containing a line of python code.
    Returns a 2-tuple, containing the code part and the comment.
    If the line contains no comment, the second element is
    an empty string."""
    from tokenize import generate_tokens, COMMENT
    from StringIO import StringIO

    g = generate_tokens(StringIO(line).readline)
    for toknum, tokval, posn, _, _ in g:
        if toknum == COMMENT:
            return (line[:posn[1]], line[posn[1]+1:])
    return (line, '')
