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
import os
from lxml import etree

# Application imports
import wtl.script
import wtl.testlog
import wtl.config
import wtl.globals

def get_server_info_string():
    """
    Generate a string for printing, that contains the server information stored
    in the WTL library configuration that was obtained during the initial 
    connection to the WITSML server through WMLS_GetVersion and WMLS_GetCap
    calls
    
    Parameters:
      Nothing
      
    Return:
      String containing all the WITSML server information
    """
    
    info = ""
    
    # Add the server schema versions supported
    versions = ["Server schema versions supported:"]
    schema_versions = wtl.globals.get(wtl.globals.GBL_SERVER_SCHEMA_VERSIONS)
    if (schema_versions):
        for version in schema_versions:
            versions.append("    %s" %(version))
    else:
        versions.append("    <unknown>")
    info += '\n'.join(versions)
    info += "\n\n"

    # Add the server capabilities
    info += str(wtl.globals.get(wtl.globals.GBL_SERVER_CAPABILITIES))
    
    return info

def write_server_info(output_file):
    """
    Write the server information to the file provided
    
    Parameters:
      output_file: File where to write the information
      
    Return:
      Nothing
    """
    
    output_file.write(get_server_info_string())
    

def write_script_results(output_file, script_list, indent):
    """
    Write the results for all the scripts in the file provided.
    This function is called recursively to travers the script tree generated
    during execution in which scripts are children of the script that runs
    them
    
    Parameters:
      output_file: File where to write the information
      script_list: List of scripts at a certain level of the script tree
      indent: Indent to use based on the lever of the script tree
      
    Return:
      Nothing
    """
    
    for current_script in script_list:
        if (current_script != wtl.script.Script.get_initial_script()):
            if (current_script.running_time()):
                rtime = "%.2f sec" %(current_script.running_time())
            else:
                rtime = "---"
            output_file.write("%sScript:%-20s     %10s  (Duration:%s)\n" %(" " * indent * 4, current_script.name, current_script.test_result, rtime))
            for partial in current_script.partial_sucesses:
                output_file.write("%sPartial Pass:  %s\n" %(" " * ((indent * 4)+2), partial))
            if (current_script.skip_string):
                output_file.write("%sSkipped:       %s\n" %(" " * ((indent * 4)+2), current_script.skip_string))
            elif (current_script.fail_string):
                output_file.write("%sFail:          %s\n" %(" " * ((indent * 4)+2), current_script.fail_string))
                 
        write_script_results(output_file, current_script.sub_scripts, indent+1)

def produce_and_reset_results():
    """
    Generate the results obtained in the execution, including the known server
    information, the result for each script file and the summary of tests
    passed and failed.
    Results are stored in the file provided in the WTL configuration 
    Results are then reset
    
    Parameters:
      Nothing
      
    Return:
      Nothing
    """

    result_file = os.path.join(wtl.config.result_directory,wtl.config.result_filename)
    output_file = open(result_file,"w")
    
    write_server_info(output_file)
             
    output_file.write("Results Summary\n")
    output_file.write("---------------\n\n")

    write_script_results(output_file, [wtl.script.Script.get_initial_script()], 0)

    output_file.write("\nTotals\n")
    output_file.write("------\n\n")
    output_file.write("Run         %5d\n" %(wtl.script.Script.fail_number + wtl.script.Script.pass_number))
    output_file.write("  Pass      %5d\n" %(wtl.script.Script.pass_number))
    output_file.write("  Fail      %5d\n" %(wtl.script.Script.fail_number))
    output_file.write("Skipped     %5d\n" %(wtl.script.Script.skip_number))
      
    output_file.close()
    
    wtl.script.Script.reset_statistics()
