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
from os.path import exists, join
import time
import sys

# Application imports
import wtl.config
import testlog
import utils

#******************************************************************************
#
# Constant Definitions
#
INITIAL_SCRIPT = "__main__"

# Test results 
SCRIPT_RESULT_NONE = ''
SCRIPT_RESULT_PASS = 'Pass'
SCRIPT_RESULT_FAIL = 'Fail'
SCRIPT_RESULT_SKIP = 'Skip'
SCRIPT_RESULT_INCONCLUSIVE = 'Inconclusive'

  
#******************************************************************************
#
# Local Script Exception
#
class ScriptEvent(Exception):
    """ Exception raised when processing a script """

    SCRIPT_SUCCESS    =  0
    SCRIPT_FAILURE    = -1
    SCRIPT_ABORT      = -2
    SCRIPT_SKIP       = -3
      
    def __init__(self, error, msg):
        """
        Initialization for the script event
        
        error:  Error code for the error
        msg:    Explanation of the error                         
        """
        self.error = error
        self.msg = msg
        

#******************************************************************************
#
# Script Module
#
class Script:
    """ Encapsulation of a single test script instance """

    #
    # Stack of running scripts
    #
    script_stack = []

    # Script statistics
    pass_number = 0
    fail_number = 0
    skip_number = 0;
    inconclusive_number = 0
    last_result = SCRIPT_RESULT_NONE


    def __init__(self, name):
        """
        Initialization of the script information 
        
        Parameters:
          name: Script name
        """
        
        self.name = name
        self.file = "%s.py" %(self.name)
        self.purpose = ""
        self.reference =  ""
        self.reference_text = ""
        self.parameter_list = []
        self.variables = {}
        self.test_result = SCRIPT_RESULT_NONE
        self.start_time = None
        self.stop_time = None
        self.sub_scripts = []
        self.partial_sucesses = []
        self.fail_string = None 
        self.skip_string = None 
        self.functionality_required = []
        self.data_schemas_supported = []
        self.requirements_string = "Requirements not checked yet."

    def log_script_action(self, action):
        """ Log a script action """

        testlog.wtl_log("!SCRIPT '%s' %s\n" %(self.name, action), force=True)

    def log_script_info(self, info):
        """ Log script information """

        testlog.wtl_log("!%s" %(info), force=True)

    def log_script_result(self, message):
        """ Log the result of a script """

        testlog.wtl_log("!*** %s" %(message), force=True)
        
    def set_info(self, purpose, reference, reference_text, parameter_list, functionality_required, data_schemas_supported):
        """
        Set the script information
        
        Parameters:
          purpose:                The reason for the test script
          reference:              Pointer to the corresponding part in the specification
          reference_text:         Corresponding text from the specification
          paramater_list:         A list of tuples containing script parameters
                                  in the form (param_name, description)
          functionality_required: A list of functionality required by the script to execute 
                                  (i.e witsml_function:object and capability=value)
          data_schemas_supported: A list of data schemas supported by the script
        """

        self.purpose = purpose
        self.reference =  reference
        self.reference_text = reference_text
        self.parameters = parameter_list
        self.functionality_required = functionality_required
        self.data_schemas_supported = data_schemas_supported
        
        if len(self.parameters):
            self.log_script_info('  Script parameters:')
            for param in self.parameters:
                value = utils.get_variable_value(param[0])
                if (value == None):
                    self.fail("Script parameter '%s' not set" %(param[0]))
                self.log_script_info("    %s = %s" %(param[0], value))
    
    
    def getRequirementsMetString(self):
        """
        Returns the string associated with the last areRequirementsMet call.
        """
        return self.requirements_string
    
    def areMinimumRequirementsMet(self):
        """
        Checks if the script's requirements are met by the server capabilities or config.
        returns True if requirements met, False if not met.
        
        """
        
        # loop through functionality required.    
        for required_item in self.functionality_required:
            func_available = False;
        
            # if item does not contain a separator than check server capability variables
            if ((required_item.find(':') == -1) and 
                (not any(sep in required_item for sep in wtl.capability.CAP_EQUALITY_SEPARATORS))):
                
                # This item in required functionality is a server capability variable
                capability_value = utils.get_variable_value(required_item)
                if (capability_value != None): 
                    func_available = utils.get_variable_value(required_item)
            else:  
                # otherwise check globals      
                func_available = wtl.globals.get(wtl.globals.GBL_SERVER_CAPABILITIES).isSatisfyFollowingRequrements(required_item);
            
            if (not func_available):
                self.requirements_string = "Server does not satisfy server script capability requirements: " + required_item
                return False

        # get server schema version and test if server supports it
        script_suite_uses_version = utils.get_variable_value('server_schema_version') ;
        
        if (self.data_schemas_supported and (script_suite_uses_version not in self.data_schemas_supported)):
            self.requirements_string = "Script does not support the data schema %s under test" %script_suite_uses_version
            return False
            
        self.requirements_string = "Script requirements met"    
        return True
    
    def execute_file(self):
        """ Execute the commands in the script file """
        
        script_file = None
        for path in wtl.config.script_directories:
            if exists(join(path, self.file)):
                script_file = open(join(path, self.file),"r")
                break
        if (not script_file):
            self.test_result = SCRIPT_RESULT_FAIL
            self.log_script_result("FAILURE: %s" %('Cannot find file %s' %(self.file)))
            return
        file_contents = script_file.read()
        script_file.close()

        try:
            exec(file_contents)
        except ScriptEvent, e:
            pass
        except Exception, inst:
            self.test_result = SCRIPT_RESULT_FAIL
            self.log_script_result('ERROR: "%s"' %(inst))

        if (self.test_result == SCRIPT_RESULT_NONE):
            # Reached end of script with no result primitive -> Test passed             
            self.test_result = SCRIPT_RESULT_PASS
            self.log_script_result("SUCCESS")

        return
           
    def run(self, **kwargs):
        """ Start running the scripts with the given parameters """
        
        for key in kwargs:
            if ((kwargs[key][0] == '$') and (kwargs[key][-1] == '$')):
                value = utils.get_variable_value(kwargs[key][1:-1])
            else:            
                value = kwargs[key]
            self.set_variable(key, value)

        # Add script to the stack and execute it
        Script.script_stack.append(self)
        self.log_script_action("started")
        self.start_time = time.time()
        self.execute_file()
        # Determine the run time
        self.stop_time = time.time()
        self.log_script_action("run time = %.2f seconds" %(self.running_time()))
        # Save result and update statistics
        Script.last_result = self.test_result
        if (self.test_result == SCRIPT_RESULT_PASS):
            # Script completed successfully
            self.log_script_action("completed: Pass")
            Script.pass_number += 1
        elif (self.test_result == SCRIPT_RESULT_FAIL):
            # Script failed
            self.log_script_action("completed: Fail")
            Script.fail_number += 1
        elif (self.test_result == SCRIPT_RESULT_SKIP):
            # Script skipped
            self.log_script_action("completed: Skipped")
            Script.skip_number += 1;
        else:
            # Script result inconclusive
            self.log_script_action("completed: Inconclusive")
            Script.inconclusive_number += 1
        Script.script_stack.pop()

    def partial_success(self, success_string):
        """
        Capture a partial success check
        
        Parameters:
          success_string: String to log for the check condition
        """
        
        self.log_script_result("PASS : %s" %(success_string))
        self.partial_sucesses.append(success_string)
        
    def success(self):
        """
        Script has been successful
        If this is the main script, end program.
        Otherwise, indicate success and stop execution of the script
        """
        
        self.test_result = SCRIPT_RESULT_PASS
        self.log_script_result("SUCCESS")
        if (self.name == INITIAL_SCRIPT):
            sys.exit(1)
        else:
            raise ScriptEvent(ScriptEvent.SCRIPT_SUCCESS, "Success")

    def fail(self, fail_string):
        """
        Script has failed
        If this is the main script, end program.
        Otherwise, indicate failure and stop execution of the script

        Parameters:
          fail_string: String to log the condition that caused the failure
        """

        self.test_result = SCRIPT_RESULT_FAIL
        self.fail_string = fail_string 
        self.log_script_result("FAILURE: %s" %(fail_string))
        if (self.name == INITIAL_SCRIPT):
            sys.exit(-1)
        else:
            raise ScriptEvent(ScriptEvent.SCRIPT_FAILURE, fail_string)
        
    def skip(self, skip_string):
        """
        Script is skipped
        If this is the main script, end program.
        Otherwise, indicate failure and stop execution of the script

        Parameters:
          skip_string: String to log the condition that caused the skip
        """

        self.test_result = SCRIPT_RESULT_SKIP
        self.skip_string = skip_string 
        self.log_script_result("SKIPPED: %s" %(skip_string))
        if (self.name == INITIAL_SCRIPT):
            sys.exit(-1)
        else:
            raise ScriptEvent(ScriptEvent.SCRIPT_SKIP, skip_string)
            
        
    def stop(self):
        """
        Stop the script execution
        If this is the main script, end program.
        Otherwise, indicate abort condition and stop execution of the script
        """
        self.test_result = SCRIPT_RESULT_NONE
        self.log_script_result("SCRIPT ABORTED")
        if (self.name == INITIAL_SCRIPT):
            sys.exit(0)
        else:
            raise ScriptEvent(ScriptEvent.SCRIPT_ABORT, "Stop")
        
    def set_variable(self, name, value):
        """
        Set the value of a script variable. If variable already exists it 
        is overwritten
        
        Parameters:
          name:  String containing the variable name
          value: String containing the variable's value to be set
        """
         
        self.variables[name] = value

    def get_variable(self, name):
        """
        Retrieve the value of a script variable. If variable does not exist
        the 'None' value is returned
        
        Parameters:
          name:  String containing the variable name
        """
        
        value = None
        if (self.variables.has_key(name)):
            value = self.variables[name]
        return value 

    def running_time(self):
        """ Calculate the script's running time """
        
        rtime = 0 
        if (self.start_time):
            if (self.stop_time):
                rtime = self.stop_time - self.start_time
            else:
                rtime = time.time() - self.start_time
        return rtime

    def add_sub_script(self, new_script):
        """
        Save a new child script (A script 'run' within this script)
        
        Parameters:
          new_script:  Pointer to child script object
        """
        
        self.sub_scripts.append(new_script)
    
    @staticmethod
    def reset_statistics(): 
        Script.pass_number = 0
        Script.fail_number = 0
        Script.skip_number = 0;
        Script.inconclusive_number = 0
    
    @staticmethod
    def last_test_result():
        """ Return the result of the last script run """
        
        return Script.last_result

    @staticmethod
    def get_initial_script():
        """ Return the original script that was run """
    
        return Script.script_stack[0]

    @staticmethod
    def get_current_script():
        """ Return the currently running script """
    
        return Script.script_stack[-1]
    
    @staticmethod
    def init():
        """ Initialize the script stack """
        Script.script_stack.append(Script(INITIAL_SCRIPT))
