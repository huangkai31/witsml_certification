#******************************************************************************
# Copyright (c) 2011 Pason Systems Corp.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#******************************************************************************

##############################################################################
#                                                                            #
# NOTE:                                                                      #
# This is a temporary module built to implement a very simple logging system #
# It should be eventually replaced by the Python built in logging support    #
#                                                                            #
##############################################################################

# System imports
import time
import os
import logging as log_library

# Application imports
import wtl.config

#
#Logging variables
#
logging = True      # Turn on and off logging
log_file = None     # Log file handle  

def init():
    """ Open and initialize the log file """

    global log_file
    if (not log_file):
        now = time.localtime()
        log_file_name = os.path.join(wtl.config.result_directory,"log_%s.txt" %(time.strftime("%Y%m%d%H%M%S", now)))
        log_file = open(log_file_name,"w")
        log_file.write("WITSML Test Library log file. Started %s\n\n" %time.strftime("%Y-%m-%d at %H:%M:%S", now))

        # Enable logging of SOAP messages 
        soap_log_file_name = log_file_name.replace('.txt', '_soap.txt')
        log_library.basicConfig(level=log_library.INFO, filename=soap_log_file_name)
        # Set Suds logging level to debug, outputs the SOAP messages.
        log_library.getLogger('suds.client').setLevel(log_library.DEBUG)
 
def end_log_file():
    """ Close the log file """

    global log_file
    log_file.close()
    log_file = None

def logging_off():
    """ Turn logging off """

    global logging
    logging = False

def logging_on():
    """ Turn logging on """

    global logging
    logging = True
    
def wtl_log(log_string, force=False, no_new_line=False, prefix=''):
    """
    Log internal message from WTL library
    
    Parameters:
      log_string:  Message to log
      force:       Force the message to be logged independent of the 'logging'
                   variable state
      no_new_line: Flag to prevent a new line to be added at the end of the
                   message
    """
    
    global log_file
    if (force or logging):
        if (no_new_line):
            print prefix+log_string,
            if log_file:
                log_file.write(prefix+log_string)
        else:
            print prefix+log_string
            if log_file:
                log_file.write(prefix+log_string+'\n')

def wtl_log_server_response(label, response):
    """
    Log server responses if enabled

    Parameters:
      label:     Label to add to the log
      response:  Server response to log
        """        
    if ((response is not None) and wtl.config.log_responses):
        wtl_log(str(response), prefix='[' + label + ']\n')    
     
def wtl_log_server_query(labelWitsmlType, wmlTypeIn, labelQuery, query, labelOptionsIn, optionsIn, labelCapsIn, capsIn):
    """
    Log server queries if enabled

    Parameters:
      labelWitsmlType: Label to add to the log
      wmlTypeIn:  Server witsml data type to log      
      labelQuery:     Label to add to the log
      query:  Server query to log  
      labelOptionsIn:     Label to add to the log
      optionsIn:  Server query to log  
      labelCapsIn:     Label to add to the log
      capsIn:  Server capsIn to log                    
        """
    if ( wtl.config.log_requests ):
        if (wmlTypeIn is not None):
            wtl_log(str(wmlTypeIn), prefix='\n[' + labelWitsmlType + ']\n')                  
        if (optionsIn is not None):
            wtl_log(str(optionsIn), prefix='\n[' + labelOptionsIn + ']\n')           
        if (query is not None):
            wtl_log(str(query), prefix='[' + labelQuery + ']\n') 
        if (capsIn is not None):
            wtl_log(str(capsIn), prefix='[' + labelCapsIn + ']\n')           
        
def log(log_string, force=False, no_new_line=False, prefix=''):
    """
    Log test primitive. Uses the internal log function and prepends the "#"
    character to the message to identify the script log messages in the log
    file
    
    Parameters:
      log_string:  Message to log
      force:       Force the message to be logged independent of the 'logging'
                   variable state
      no_new_line: Flag to prevent a new line to be added at the end of the
                   message
    """

    wtl_log(log_string, force=force, no_new_line=no_new_line, prefix="# %s" %(prefix))
