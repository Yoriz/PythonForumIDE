# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 20:27:12 2011
@author: Jakob
@reviewer: David
"""
import platform
import socket
import sys

def is_windows():
    """Tries to identify if we are on a windows machine."""
    if 'Windows' in platform.uname():
        return True
    else:
        return False
    
def get_ip():
    """Try and return the local private IP that this computer is using."""
    return socket.gethostbyname(socket.getfqdn())
    
def get_python_exe():
    """Return the location of the python executable."""
    return sys.executable
    
def get_free_port():
    """By opening port 0 the OS will give us a random port between
    1024 to 65535, we then close down the socket and return the number"""
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port