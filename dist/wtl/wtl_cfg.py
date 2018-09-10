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

# WITSML TEST LIBRARY CONFIGURATION

# Server file
server_file_directory = ''
server_file_name = 'wtl_server'

# List of directories containing the test scripts and test suites
script_directories = []

# Output directory
result_directory = ''

# File name of file to store test results
result_filename = "witsml_result.txt"

# Log responses control
log_responses = False
log_requests = False

# Enable the schema validation for WMLS_GetFromStore responses
enable_schema_validation = True

# Result format ('xml', 'text, 'csv')
result_format = 'text'

# Flag to control stop/continue execution after a test failure
stop_on_failure = False    

 
