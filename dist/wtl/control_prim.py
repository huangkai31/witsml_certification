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

# System imports
import sys
import time

# Application imports
import wtl.script
import wtl.testlog
import wtl.config
import wtl.results
import wtl.capability
import wtl.globals

def end(code):
    """
    Terminate execution of tests and exit
    
    Parameters:
      code: Exit code to use when terminating program execution
    """
    
    sys.exit(code)
    
def test(purpose, reference, reference_text, parameters=[]):
    """
    Set the Test Script information

    Parameters:
      purpose:        The reason for the test script
      reference:      Pointer to the corresponding part in the specification
      reference_text: Corresponding text from the specification
      paramater_list: A list of tuples containing script parameters
                      in the form (param_name, description)
      
    Return:
      Nothing
    """

    wtl.script.Script.get_current_script().set_info(purpose, reference, reference_text, parameters)
    
def run(script_name, **kwargs):
    """
    Execute the provided script with the given parameters.
    This primitive is meant to be used within a Test Suite. Test Scripts 
    should use the 'run_script' command
    Even if the script to be run fails, the Test Suite continues execution

    Parameters:
      script name: Script to be run
      kwargs:      Dictionary with optional script parameters
      
    Return:
      Nothing
    """
    current_script = wtl.script.Script.get_current_script()
    new_script = wtl.script.Script(script_name)
    current_script.add_sub_script(new_script)
    new_script.run(**kwargs)

def run_script(script_name, **kwargs):
    """
    Execute the provided script with the given parameters.
    This primitive is meant to be used within a Test Script. Test Suites 
    should use the 'run' command
    If the script to be run fails, the current running script fails

    Parameters:
      script name: Script to be run
      kwargs:      Dictionary with optional script parameters
      
    Return:
      Nothing
    """
    
    current_script = wtl.script.Script.get_current_script()
    new_script = wtl.script.Script(script_name)
    current_script.add_sub_script(new_script)
    new_script.run(**kwargs)
    if (wtl.script.Script.last_test_result() != wtl.script.SCRIPT_RESULT_PASS):
        fail("Child script failed")
            
def fail(fail_string):
    """
    Stop execution of the running script. The script failed
    Depending on the WTL configuration end running the scripts 
    
    Parameters:
      fail_string: Reason for failure
      
    Return:
      Nothing
    """
    
    wtl.script.Script.get_current_script().fail(fail_string)
        
def partial_success(success_string):
    """
    Record a partial success in the running script

    Parameters:
      success_string: The check that was successful 
      
    Return:
      Nothing
    """

    wtl.script.Script.get_current_script().partial_success(success_string)

def success():
    """
    Stop execution of the running script. The script was successful
    
    Parameters:
      Nothing 
      
    Return:
      Nothing
    """    
    
    wtl.script.Script.get_current_script().success()

def stop():
    """
    Stop execution of the running script
    
    Parameters:
      Nothing 
      
    Return:
      Nothing
    """
    wtl.script.Script.get_current_script().stop()

def error(error_text):
    """
    Log the error text provided and fail the running script
    
    Parameters:
      error_text: Error condition 
      
    Return:
      Nothing
    """

    wtl.testlog.wtl_log('Error: %s' %(error_text), force=True)
    fail("Script failed due to error")

def get_last_test_result():
    """
    Return the result of the last script run
    
    Return:
      One of '', 'Pass', 'Fail' or  'Inconclusive'
    """
    return wtl.script.Script.last_test_result()

def pause(seconds):
    """
    Pause the script execution for the specified number of seconds

    Parameters:
      seconds: Number of seconds to stop execution
     
    Return:
      Nothing
    """

    wtl.testlog.wtl_log('...pausing for %d seconds...' %(seconds),
                        force=True, no_new_line=True)
    time.sleep(seconds)
    wtl.testlog.wtl_log('Done', force=True)

def pause_changeDetectionPeriod():
    """
    Pause the script execution for the length of the server's 
    changeDetectionPeriod

    Parameters:
      None
     
    Return:
      Nothing
    """

    seconds = wtl.globals.get_capability(wtl.capability.CAP_changeDetectionPeriod)
    if (seconds is None):
        wtl.testlog.wtl_log('Cannot pause for changeDetectionPeriod because it is not set',
                        force=True)
        return
    
    wtl.testlog.wtl_log('Pausing for changeDetectionPeriod: ',
                        force=True, no_new_line=True)
    pause(seconds)
    
def pause_growingTimeoutPeriod(data_object):
    """
    Pause the script execution for the length of the server's 
    growingTimeoutPeriod for the provide object

    Parameters:
      data_object:  Object to use to obtain the growingTimeoutPeriod 
     
    Return:
      Nothing
    """

    seconds = wtl.globals.get_growingTimeoutPeriod(data_object)
    if (seconds is None):
        wtl.testlog.wtl_log('Cannot pause for growingTimeoutPeriod for %s because it is not set'%(data_object),
                        force=True)
        return
    
    wtl.testlog.wtl_log("Pausing for %s's growingTimeoutPeriod: "%(data_object),
                        force=True, no_new_line=True)
    pause(seconds)
