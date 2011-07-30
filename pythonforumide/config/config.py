# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 21:01:15 2011
@author: Jakob, Somelauw
@reviewer: David, SomeLauw
"""

from __future__ import print_function
import os.path

try:
    import yaml #Pretty config file :D
    has_yaml = True
except ImportError:
    import ConfigParser #Ugly config file :(
    has_yaml = False

def config_file(profile):
    """Returns the name of the configuration file. It does not guarantee existence.
    Side effect: Tells the user if can't load the configuration file if it is not supported.
    """

    # We will need some fuzzy logic to accomplish this
    (profile, ext) = os.path.splitext(profile)
    yaml_exists = os.path.exists(profile + ".yaml")
    cfg_exists = os.path.exists(profile + ".cfg")

    # If no extension could be found, guess what configuration type is likely to be preferred
    if not ext:
        if yaml_exists or (has_yaml and not cfg_exists):
            ext = ".yaml"
        else:
            ext = ".cfg"

    # We can't load yaml if it doesn't exist
    if ext == ".yaml" and not has_yaml:
        print("yaml configuration could not be loaded because python-yaml is not installed.")
        ext = ".cfg"

    return profile + ext

def load_config(configfile):
    """Loads a config file"""
    (profile, ext) = os.path.splitext(configfile)
    if ext == ".yaml":
        return _BeautifulConfig(profile)
    else:
        return _UglyConfig(profile)

class _BeautifulConfig(object):
    """This is the config object if we can import yaml."""
    def __init__(self, profile):
        """Load the yaml config from file, 
        if this fails write an empty new one."""
        filename = profile + ".yaml"

        try:
            self.config = yaml.load(open(filename))
        except IOError:
            #Raise a config warning error here?
            self.config = {}

        self.file = open(filename,'w')
    
    def __setitem__(self, option, value):
        """Set an option to a value inside the config, does not write."""
        self.config[option] = value
        
    def __getitem__(self, option):
        """Gets the option from the config, if the option is not there
        returns None"""
        return self.config.get(option, None)

    def set_default(self, option, value):
        self.config.set_default(option, value)

    def save(self):
        """Writes the config as yaml out to the config file."""
        yaml.dump(self.config, self.file)

class _UglyConfig(object):
    """This is the config object created if we can't use YAML and have to
    rely on ConfigParser."""
    def __init__(self, profile):
        filename = profile + ".cfg"

        self.config = ConfigParser.ConfigParser()
        try:
            self.config.read(filename)
        except IOError: # <<< Exception will never be trown (RTFM, noob!)
            pass #Raise a config warning error here?
            self.config.add_section('ide')

        if not self.config.has_section('ide'):
            self.config.add_section('ide')

        self.file = open(filename,'w')

    def __setitem__(self, option, value):
        """Set the value to the option inside the default section."""
        self.config.set('ide',option, value)
        
    def __getitem__(self, option):
        """Return the values to the option given, or return None"""
        try:
            return self.config.get('ide', option)
        except ConfigParser.NoOptionError:
            return None

    def set_default(self, option, value):
        if not self.config.has_option('ide', option):
            self[option] = value
            
    def save(self):
        """Write config to file."""
        self.config.write(self.file)


#If we have yaml then the ConfigObject will point to the cooler config object
if has_yaml:
    Config = _BeautifulConfig
else: # Otherwise we point to the ugly one
    Config = _UglyConfig
#This way the importers use the config the same way, same api but under the 
#hood they are different.

# Load configuration
config_file = config_file("default")
conf = load_config(config_file)

# Set defaults
conf.set_default("indent", 4)
conf.set_default("usetab", 0) #0 means false

conf.save()