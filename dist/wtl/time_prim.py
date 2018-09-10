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
import datetime
import pytz

# Application imports
import wtl.script
import wtl.utils
import wtl.testlog


def time_primitive_fail(fail_message):
    """
    Make the script fail
    
    Parameters:
      fail message:  String indicating the fail reason
      
    Return:
      Nothing
    """
    
    wtl.script.Script.get_current_script().fail(fail_message)

def log_time_action(action):
    """ Log a time primitive action """

    wtl.testlog.wtl_log("  ' %s..." %action)

def log_time_result(result):
    """ Log a time primitive result """

    wtl.testlog.wtl_log("  ' ... %s" %result)

def log_time_info(info):
    """ Log a time primitive info message """

    wtl.testlog.wtl_log("  '     %s" %info)

def get_current_datetime_string():
    """
    Primitive function to return the current datetime as an ISO 8601 string.
    
    Parameters:
      none
      
    Return:
      ISO 8601 formatted date time string of the current date and time.      
    """
    return wtl.utils.datetime_to_iso(datetime.datetime.now(pytz.utc))

def check_timestamp_equals(timestamp_lhs, timestamp_rhs):
    """
    Primitive function to compare two timestamp strings for equality
    
    Parameters:
      timestamp_lhs: a timestamp string to compare for equality.
      timestamp_rhs: a timestamp string to compare for equality.
      
    Return:
      'True' if the timestamps represent the same time (taking into account formatting and timezone)
      Raise an exception otherwise      
    """
    
    log_time_action("Checking: {} == {}".format(timestamp_lhs, timestamp_rhs))
        
    dtlhs = wtl.utils.iso_to_utc(timestamp_lhs, True)
    dtrhs = wtl.utils.iso_to_utc(timestamp_rhs, True)
    if (dtlhs == dtrhs):
        log_time_result("OK")
        return True
    
    log_time_result("Not Ok")
    log_time_info("Timestamp {} != {}".format(timestamp_lhs, timestamp_rhs))
    time_primitive_fail("Timestamp comparison failed")

def check_timestamp_lessthan(timestamp_lhs, timestamp_rhs):
    """
    Primitive function to compare two timestamp strings such that lhs < rhs
    
    Parameters:
      timestamp_lhs: left hand side timestamp string to compare for <.
      timestamp_rhs: right hand side timestamp string to compare.
      
    Return:
      'True' if timestamp_lhs < timestamp_rhs
      Raise an exception otherwise     
    """
    
    log_time_action("Checking: {} < {}".format(timestamp_lhs, timestamp_rhs))
        
    dtlhs = wtl.utils.iso_to_utc(timestamp_lhs, True)
    dtrhs = wtl.utils.iso_to_utc(timestamp_rhs, True)   
    if (dtlhs < dtrhs):
        log_time_result("OK")
        return True
    
    log_time_result("Not Ok")
    log_time_info("Timestamp {} >= {}".format(timestamp_lhs, timestamp_rhs))
    time_primitive_fail("Timestamp comparison failed")

def check_timestamp_lessthan_equalto(timestamp_lhs, timestamp_rhs):
    """
    Primitive function to compare two timestamp strings such that lhs <= rhs
    
    Parameters:
      timestamp_lhs: left hand side timestamp string to compare for <=.
      timestamp_rhs: right hand side timestamp string to compare.
      
    Return:
      'True' if timestamp_lhs <= timestamp_rhs
      Raise an exception otherwise           
    """
    
    log_time_action("Checking: {} <= {}".format(timestamp_lhs, timestamp_rhs))
        
    dtlhs = wtl.utils.iso_to_utc(timestamp_lhs, True)
    dtrhs = wtl.utils.iso_to_utc(timestamp_rhs, True)
    if (dtlhs <= dtrhs):
        log_time_result("OK")
        return True
    
    log_time_result("Not Ok")
    log_time_info("Timestamp % > %".format(timestamp_lhs, timestamp_rhs))
    time_primitive_fail("Timestamp comparison failed")

def check_timestamp_greaterthan(timestamp_lhs, timestamp_rhs):
    """
    Primitive function to compare two timestamp strings such that lhs > rhs
    
    Parameters:
      timestamp_lhs: left hand side timestamp string to compare for >.
      timestamp_rhs: right hand side timestamp string to compare.
      
    Return:
      'True' if timestamp_lhs > timestamp_rhs
      Raise an exception otherwise            
    """
    
    log_time_action("Checking: {} > {}".format(timestamp_lhs, timestamp_rhs))
        
    dtlhs = wtl.utils.iso_to_utc(timestamp_lhs, True)
    dtrhs = wtl.utils.iso_to_utc(timestamp_rhs, True)
    if (dtlhs > dtrhs):
        log_time_result("OK")
        return True
    
    log_time_result("Not Ok")
    log_time_info("Timestamp % <= %".format(timestamp_lhs, timestamp_rhs))
    time_primitive_fail("Timestamp comparison failed")

def check_timestamp_greaterthan_equalto(timestamp_lhs, timestamp_rhs):
    """
    Primitive function to compare two timestamp strings such that lhs >= rhs
    
    Parameters:
      timestamp_lhs: left hand side timestamp string to compare for >=.
      timestamp_rhs: right hand side timestamp string to compare.
      
    Return:
      'True' if timestamp_lhs >= timestamp_rhs
      Raise an exception otherwise            
    """
    
    log_time_action("Checking: {} >= {}".format(timestamp_lhs, timestamp_rhs))
        
    dtlhs = wtl.utils.iso_to_utc(timestamp_lhs, True)
    dtrhs = wtl.utils.iso_to_utc(timestamp_rhs, True)   
    if (dtlhs >= dtrhs):
        log_time_result("OK")
        return True
    
    log_time_result("Not Ok")
    log_time_info("Timestamp % < %".format(timestamp_lhs, timestamp_rhs))
    time_primitive_fail("Timestamp comparison failed")

def add_seconds_to_timestamp(timestamp_str, seconds):
    """
    Primitive function to add seconds to a timestamp string
    and return a timestamp ISO 8601 string with the result of the addition (in UTC)
    
    Parameters:
      timestamp_str: timestamp string to add to.
      seconds: number of seconds to add.
      
    Return:
      ISO 8601 string consisting of result of addition.      
    """
    
    dt = wtl.utils.iso_to_utc(timestamp_str, False)
    dt_result = dt + datetime.timedelta(0,seconds)
    return wtl.utils.datetime_to_iso(dt_result, False)
    
def subtract_seconds_to_timestamp(timestamp_str, seconds):
    """
    Primitive function to subtract seconds from a timestamp string
    and return a timestamp ISO 8601 string with the result of the addition (in UTC)
    
    Parameters:
      timestamp_str: timestamp string to subtract from.
      seconds: number of seconds to subtract.
      
    Return:
      ISO 8601 string consisting of result of addition.      
    """
    
    dt = wtl.utils.iso_to_utc(timestamp_str, False)
    dt_result = dt - datetime.timedelta(0,seconds)
    return wtl.utils.datetime_to_iso(dt_result, False)
