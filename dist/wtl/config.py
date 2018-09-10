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
import os
     
#Default configuration
server_file_directory = '.'
server_file_name = 'default_server'
script_directories = ['.']
result_directory = '.\\results'
result_filename = "witsml_result.txt"
log_responses = True
log_requests = False
enable_schema_validation = False
result_format = 'text'
stop_on_failure = False    
WITSML_files_directory = ''
auto_start = True

# If a local configuration file exists, overwrite configuration parameters from there
local_config_file = os.path.join(os.getcwd(),'wtl_cfg.py')
if os.path.isfile(local_config_file):
    execfile(local_config_file)

#Set path to default server file directory and add it to the path 
if (not server_file_directory):
    server_file_directory = sys.modules['wtl'].__path__[0]
sys.path.insert(0,server_file_directory)

#Override the server file if the command line option -s<filename> is given
for option in sys.argv:
    if (option[:2] == '-s'):
        server_file_name = option[2:]
    elif (option == '-a'):
        auto_start = True
    elif (option == '-A'):
        auto_start = False
    elif (option == '-l'):
        log_responses = True
    elif (option == '-L'):
        log_responses = False
    elif (option == '-r'):
        log_requests = True
    elif (option == '-R'):
        log_requests = False        
    elif (option == '-v'):
        enable_schema_validation = True
    elif (option == '-V'):
        enable_schema_validation = False
    
