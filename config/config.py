# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 21:01:15 2011
@author: Jakob
@reviewer: David
"""

try:
    import yaml #Pretty config file :D
    has_yaml = True
except ImportError:
    import ConfigParser #Ugly config file :(
    has_yaml = False

class _BeautifulConfig(object):
    """This is the config object if we can import yaml."""
    def __init__(self):
        """Load the yaml config from file, 
        if this fails write an empty new one."""
        try:
            self.config = yaml.load(open('config.yaml'))
            self.file = open('config.yaml','w')
        except IOError:
            #Raise a config warning error here?
            self.config = {}
            self.file = open('config.yaml', 'w')
    
    def set_config(self, option, value):
        """Set an option to a value inside the config, does not write."""
        self.config[option] = value
        
    def get_config(self, option):
        """Gets the option from the config, if the option is not there
        returns None"""
        return self.config.get(option, None)
        
    def save(self):
        """Writes the config as yaml out to the config file."""
        yaml.dump(self.config, self.file)

class _UglyConfig(object):
    """This is the config object created if we can't use YAML and have to
    rely on ConfigParser."""
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        try:
            self.config.read('config.cfg')
        except IOError:
            pass #Raise a config warning error here?
            self.config.add_section('ide')
        self.file = open('config.cfg','w')

    def set_option(self, option, value):
        """Set the value to the option inside the default section."""
        self.config.set('ide',option, value)
        
    def get_option(self, option):
        """Return the values to the option given, or return None"""
        try:
            return self.config.get('ide', option)
        except ConfigParser.NoOptionError:
            return None
            
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