# -*- coding: utf-8 -*-
"""
utils module from GeoDataKit package

This module implement common utility class and functions that can be used in 
the different other modules.

List of avaiblable objects:
     - get_kargs(): for accessing arguments passed as **kargs in functions

Created on Thu Dec 15 09:54:15 2022

@author: glaurent
"""

def get_kargs(key, default, **kargs):
    """Reads a parameter from kargs dict (**kargs)
    
    Arguments can be passed to functions as keyword arguments, e.g.,
        function(argument1=value)
    It access the value of the argument given its key, if not found 
    or if kargs is None, it returns the default value.
    
    Parameters
    ----------
    key: str
        The key (string) giving the name of the argument 
        to be found in kargs
    default: any
        The value to be returned if the argument is not in the kargs.
        If there is no default value, None should be given.
    kargs: dict()
        The keyword arguments passed as **kargs
    
    Returns
    -------
    The selected argument if valid, else the default value (e.g.,
     if the key is not available in kargs)
    """
    return default if key not in kargs.keys() else kargs[key]

