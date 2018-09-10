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
#

#******************************************************************************
#
# Global variables
#
GBL_SERVER_SCHEMA_VERSIONS = 'schema_version_supported_by_server'
GBL_SERVER_CAPABILITIES = 'capabilities_from_server'  

#******************************************************************************
#
# Local constants
#
CAP_PREFIX = 'cap_' 

#******************************************************************************
#
# Dictionary to store global variables
#
variables = {}

def reset():
    global variables
    variables = {
                 GBL_SERVER_SCHEMA_VERSIONS:[],
                 GBL_SERVER_CAPABILITIES:None,
                 CAP_PREFIX + 'cascadedDelete':False,
                 CAP_PREFIX + 'compressionMethod':'none',
                 }
    
def set(var, value):
    variables[var] = value

def set_capability(cap, value):
    set(CAP_PREFIX + cap, value)

def set_function_object_supported(func, obj):
    set_capability(func + ':' + obj , True)
    
def set_maxDataNodes(func, obj, value):
    set_capability(func + ':' + obj + ':' + 'maxDataNodes', value)
    
def set_maxDataPoints(func, obj, value):
    set_capability(func + ':' + obj + ':' + 'maxDataPoints', value)
    
def set_growingTimeoutPeriod(obj, value):
    set_capability(obj + '-' + 'growingTimeoutPeriod', value)
    
def get(var): 
    return variables.get(var)

def get_capability(cap): 
    return get(CAP_PREFIX + cap)

def is_function_object_supported(func, obj):
    if (get_capability(func + ':' + obj ) == True):
        return True
    return False

def get_maxDataNodes(func, obj):
    return get_capability(func + ':' + obj + ':' + 'maxDataNodes')

def get_maxDataPoints(func, obj):
    return  get_capability(func + ':' + obj + ':' + 'maxDataPoints')

def get_growingTimeoutPeriod(obj):
    return  get_capability(obj + '-' + 'growingTimeoutPeriod')

# initialize upon import
reset()