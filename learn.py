#!/usr/bin/env python

DEFAULT_GLOBAL_ERROR = 0.01

class Learn():
    """
    Learn and adjust from data an ANN corresponding to an application.
    """
    new_data = None
    """ A dictionary containing the new data to learn from."""
    appl_id = None
    """ A unique integer identifying the application and thus the ANN."""
    success = None
    """ A boolean to determine if the global error is convenient."""
    global_error =None
    """ A float between 0 and 0.5 to set the minnimum global error."""
    
    def __init__(self, new_data,appl_id, global_error =None):
        self.new_data = new_data
        self.appl_id = appl_id
        if global_error == None:
            self.global_error = DEFAULT_GLOBAL_ERROR
        else:
            self.global_error= global_error
        self.success = False
