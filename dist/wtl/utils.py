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
import re
import pytz
import dateutil.parser

# Application imports
import wtl.config
import wtl.globals
import wtl.testlog
import wtl.script

#******************************************************************************
#
# Constant definitions
#

SEC_PER_DAY = 86400
SEC_PER_HR = 3600
SEC_PER_MIN = 60
ISO_DATE_TIME_FMT = "%Y-%m-%dT%H:%M:%S"

#******************************************************************************
#
# Local functions
#

def utils_error(s):
    """
    Log an error
    
    Parameters:
      s:  Error string to be logged
      
    Return:
      Nothing
    """

    wtl.testlog.wtl_log("  ***-> UTILS ERROR: %s" %s, force=True)


#******************************************************************************
#
# Utility functions
#

def get_variable_value(variable_name):
    """
    Utility function to retrieve a variables value.
    The variable name is first searched in the server file. If it does not
    exist, the variable is searched in the running script's variables 
    
    Parameters:
      variable_name:  String containing the variable's name
      
    Return:
      A string with the variable's value, or 'None' if variable does not exist
    """
      
    value = None

    # Look at the server variables first
    try:
        exec('value=sys.modules["%s"].%s' %(wtl.config.server_file_name,
                                            variable_name))
    except:
        pass
    if (value != None):
        return value
    
    # Now look into the current script's variables
    try:
        value = wtl.script.Script.get_current_script().get_variable(variable_name)
    except:
        pass
    if (value != None):
        return value

    # Finally try in the global variables
    value = wtl.globals.get(variable_name)
    
    return value

def log_variable_value(variable_name, label = ''):
    """
    Utility function to retrieve a variables value and log it.
    The variable name is first searched in the server file. If it does not
    exist, the variable is searched in the running script's variables 
    
    Parameters:
      variable_name:   String containing the variable's name
      label:           (Optional) Text to use for the log. If not given the 
                       variable name is used        
      
    Return:
      Nothing
      
    Examples:
      When variable 'x' has the value '123'
          log_variable_value('x', 'my variable') will log "my_variable = 123"
          log_variable_value('x')                will log "Variable 'x' = 123"
    """
    value = get_variable_value(variable_name)
    if label:
        wtl.testlog.wtl_log("%s = %s" %(label, value)) 
    else:
        wtl.testlog.wtl_log("Variable '%s' = %s" %(variable_name, value)) 


def set_variable_value(variable, value):

    """
    Utility function to set variables value.
    The variable is set in the running script's variables. If it already exists
    it is overwritten 
    
    Parameters:
      variable_name:  String containing the variable's name
      value:          String containing the variable's value
      
    Return:
      Nothing
    """

    wtl.script.Script.get_current_script().set_variable(variable, value) 
    
def find_construct(s, delimiter_char, escape_char):
    """
    Utility function to break a given string into substrings broken by 
    text segments delimited by a special character

    Parameters:
      s:                String to be processed
      delimiter_char:   Character used for delimiter
      escape char:      Character used to escape the special delimiter in
                        the string 
      
    Return:
      A list of substrings. Each entry in the list is of the form:
        a) If it does not contain the delimiter:
            ('None', ofsset_of_first_character, offset_of_last_character
        b) If it does contain the delimiter:
            (text_within delimiter, ofsset_of_first_delimiter, offset_of_last_delimiter)
      If there is an error in the string, 'None is returned'
      
    Examples:
      find_construct("abc$123$d$4$efgh~$ijk", '$', '~') 
         will return [(None, 0, 2), ('123', 3, 7), (None, 8, 8), ('4', 9, 11), (None, 12, 20)]
         
      find_construct("1234567890", '$', '~') 
         will return [(None, 0, 9)]
    """
    
    entries = []
    index = 0
    start = s.find(delimiter_char, index)
    while (start != -1):
        if ((start != 0) and (s[start-1] == escape_char)):
            # Special character escaped
            start = s.find(delimiter_char, start + 1)
        else:
            # Start construct found 
            end = s.find(delimiter_char,start+1)
            if (end == -1):
                utils_error("Mismatched %s in string" %(delimiter_char))
                return None
            
            if (start > index):
                entries.append((None, index, start-1))
                
            name = s[start+1:end]
            if (not name):
                utils_error("Bad delimited name in string. Empty string not allowed")
                return None
                    
            entries.append((name, start, end))
                
            index = end + 1
            start = s.find(delimiter_char, index)

    if (index < len(s)):
        entries.append((None, index, len(s)-1))
        
    return entries
                
def replace_conditional_statements(s):
    """
    Utility function to replace the ^condition?str1:str2^ constructs in a
    string. The condition is evaluated and the construct is replaced by str1 if
    the condition is True or by str2 if the condition is False
    The character '~' is used as escape character to be able to include the special
    character '^' in the string

    Parameters:
      s:                String to be processed
      
    Return:
      A new string with the construct replacements done or an empty string if
      there is an error in the string
      
    Examples:
      replace_conditional_statements("aaaaa^1==1?ttttt:ffffff^bbbbb") 
         will return 'aaaaatttttbbbbb'

      replace_conditional_statements("a~^aaaa^1==2?ttttt:ffffff^bbbbb") 
         will return 'a~^aaaaffffffbbbbb'   
    """

    construct_list = find_construct(s, '^', '~')
    if (construct_list == None):
        utils_error("Error processing string for condition") 
        return ""
        
    new_string = ''
    for segment in construct_list:
        if (segment[0] == None):
            # Not a condition
            new_string += s[segment[1]:segment[2]+1]  
        else:
            # Condition
            index = segment[0].find('?')
            if (index > 0):
                cond = segment[0][:index]
                index2 = segment[0].find(':', index+1)
                if (index2 > index+1):
                    str1 = segment[0][index+1:index2]
                    str2 = segment[0][index2+1:]
                    exec("if (%s): str2 = '%s'" %(cond, str1))
                    new_string += str2
                    continue
            utils_error('Cannot process condition %s' %(segment[0]))
            return ""

    return new_string

def replace_file_contents(s):
    """
    Replace #filename# constructs in a string with the contents of the
    corresponding file
    
    Parameters:
      s:  String to be processed
      
    Return:
      The string with the file inserted or an empty string if there is an error
      in the string
    """
        
    construct_list = find_construct(s, '#', '~')
    if (construct_list == None):
        utils_error("Error processing string for files") 
        return ""
        
    new_string = ''
    for segment in construct_list:
        if (segment[0] == None):
            # Not a file
            new_string += s[segment[1]:segment[2]+1]  
        else:
            # File
            infile = open(segment[0],"r")
            if (infile):
                content = infile.read()
                if content:
                    new_string += content
                else:
                    utils_error('Cannot read file %s' %(segment[0]))
                    return ""
            else:
                utils_error('Cannot open file %s' %(segment[0]))
                return ""

    return new_string

def replace_variables(s):
    """
    Replace $var$ constructs in a string with the value of the variable var
    
    Parameters:
      s:  String to be processed
      
    Return:
      The string with the variables replaced or an empty string if there is an
      error in the string
    """
    
    construct_list = find_construct(s, '$', '~')
    if (construct_list == None):
        utils_error("Error processing string for variables") 
        return ""
        
    new_string = ''
    for segment in construct_list:
        if (segment[0] == None):
            # Not a variable
            new_string += s[segment[1]:segment[2]+1]  
        else:
            # Variable
            var_value = get_variable_value(segment[0])
            if var_value:
                new_string += str(var_value)
            else:
                utils_error('Variable %s does not exist' %(segment[0]))
                return ""

    return new_string
        
def replace_escaped_values(s):
    """
    Un-escape characters with the special escape character '~' in a string
        
    Parameters:
      s:  String to be processed
      
    Return:
      The string without the escape characters or an empty string if there is an
      error in the string
      
    Example:
      replace_escpaed_values("123~$456~~789")
         will return '123$456~789' 
    """

    # Replace escaped values
    start = 0
    index = s.find('~',start)
    while (index != -1):
        s = s[:index] +  s[index+1:]
        start = index + 1
        index = s.find('~',start)
            
    return s

def process_string(s):
    """
    Process special constructs inside a string in the given order 

        $variable_name$          The construct is replaced with the variable contents at runtime
                                 Example: 
                                         Variable 'x' has value 'abc' 
                                         "The value of x is $x$"   ->   The value of x is abc

        ^condition?str1:str2^    The construct is replaced with str1 if the condition is true or with str2 otherwise
                                 Example:
                                         "^1==2?This:That^"   ->   That
                                         
        #filename#               The construct is replaced with the contents of the file specified
                                 Example:
                                         "#file.xml#" -> contents of file.xml 
                                                                                      
        $variable_name$          The construct is replaced with the variable contents at runtime
                                 Example: 
                                         Variable 'x' has value 'abc' 
                                         "The value of x is $x$"   ->   The value of x is abc

        ~<char>                  The construct is replaced with the character specified after the '~'.
                                 This is used to escape the special characters: $ # ^
                                 Example:
                                         "~$~~"   ->    $~
    Parameters:
      s:  String to be processed
      
    Return:
      The string processed or an empty string if there is an error in the string
    """
        
    # First replace variables so variables can be used in conditional constructs and filenames 
    s = replace_variables(s)
    
    # Now process conditional constructs
    s = replace_conditional_statements(s)
    
    # Next replace text from files
    s = replace_file_contents(s)

    # One more variable replacement for text read from files 
    s = replace_variables(s)

    # Finally replace escaped values
    s = replace_escaped_values(s)
        
    return s

def compare_strings_regex_and_var(expected_string, received_string):
    """
    Compare two strings with the following 2 special processing rules
        1. Use regular expressions in expected string
        2. When a string delimited by the character '&' is found in the
           expected string, match the string before and the string after and 
           save the string in between to the variable specified between the '&'
           delimiters 
    Parameters:
      expected_string:  String to be compared against, containing regular
                        expressions and '&' constructs
      received_string:  String to be compared
      
    Return:
      'True' if the strings match, or 'False' otherwise
      
    Examples:
      '*123*' will match "aaaa123' and 'xxx123yyyyy'
      '123&name&456' will match '123abc456' and set variable 'name' to 'abc'  
    """
            
    # Parse receive variables
    match_list = find_construct(expected_string, '&', '~')
    
    start = 0
    index = 0
    while (index < len(match_list)):
        if ((index == 0) and (match_list[0][0] == None)):
            # Straight match
            match = re.match(expected_string[match_list[0][1]:match_list[0][2]+1],received_string[start:])
            if (not match):
                return False
            start = match.end()
            index = 1
        else:
            # Variable
            if (index == (len(match_list) - 1)):
                # Variable at the end of the string
                set_variable_value(match_list[index][0], received_string[start:])
                start = len(received_string)
                index = index + 1
            else: 
                # need to match next segment to see where the variable text ends
                match = re.search(expected_string[match_list[index+1][1]:match_list[index+1][2]+1],received_string[start:])
                if (not match):
                    return False
                set_variable_value(match_list[index][0], received_string[start:start + match.start()])                
                start = start + match.end()
                index = index + 2

    if (start != len(received_string)):
        return False
    
    return True
    
def compare_strings(expected_string, received_string, enable_regex=False):
    """
    Compare two strings depending on the flag enable_regex
    If enable_regex is True, use the compare_strings_regex_and_var function. 
    Otherwise do a straight string comparison  
    Parameters:
      expected_string:  String to be compared against. Maybe containing regular
                        expressions and '&' constructs if enable_regex=True
      received_string:  String to be compared
      enable_regex:     Flag (True or False) to indicate the type of comparison to be used
      
    Return:
      'True' if the strings match, or 'False' otherwise    
    """
    
    if (enable_regex):
        return compare_strings_regex_and_var(expected_string, received_string) 

    return (expected_string == received_string)
 
def encode_options_in(options_in):
    """
    Utility function to encode the options in provided as a dictionary into the
    proper WITSML format
    
    Parameters:
      options_in:  A Python dictionary containing a list of option_in:value
      
    Return:
      The encoded string or an empty strign if the parameters provided are
      invalid (i.e. not a proper dictionary)
      
    Example:
      encode_options_in({'returnElements':'id-only','maxReturnNodes':'100'})
         will return 'maxReturnNodes=100;returnElements=id-only'
    """
    encoded_options = []
    
    try:
        for option in options_in.keys():
            encoded_options.append('%s=%s' %(option, options_in[option]))
    except:
        pass
        
    return ';'.join(encoded_options)


def iso_to_utc(iso_str, interpretInTimezone=False):
    """
    Method to parse an ISO 8601 string and return a datetime in UTC.

    Arguments: iso_str - A string formatted in the ISO 8601 standard.
               interpretInTimezone - A flag to force us to assume that the provided
                                     datetime string is UTC if no timezone info is
                                     provided as part of the datetime string
    Returns: python datetime in UTC
    """
    return iso_to_localized(iso_str, 'UTC', interpretInTimezone)
        
        
def iso_to_localized(iso_str, timezone_name, interpretInTimezone=False):
    """
    Method to parse an ISO 8601 string and return a datetime in the given timezone.

    Arguments: iso_str - A string formatted in the ISO 8601 standard.
               timezone_name - A timezone string, ie. "Canada/Mountain"
               interpretInTimezone - A flag to force us to assume that the provided
                       datetime string is in the given timezone if no timezone
                       info is provided as part of the datetime string
    Returns: python datetime in the given timezone
    """
    date_time = dateutil.parser.parse(iso_str)
    if not timezone_name:
        timezone_name = 'UTC'
    try:
        dt = date_time.astimezone(pytz.timezone(timezone_name))
    except ValueError, ve:
        if interpretInTimezone:
            dt = pytz.timezone(timezone_name).localize(date_time)
        else:
            raise
        
    return dt        

def datetime_to_iso(date_time, preserve_timezone=True):
    """
    Method to convert a timezone aware datetime to an ISO 8601 string. This 
    method does not support sub-second resolution by design.

    Arguments: date_time - python datetime with valid tzinfo
               preserve_timezone - if true, renders the datetime in its 
                                   current timezone, and prints the offset
                                   from UTC. Otherwise, converts to UTC
                                   and then indicates no offset with a 'Z' as
                                   per the ISO8601 standard.
    Returns: ISO 8601 formatted date time string.
    """

    if date_time.utcoffset() is None:
        raise ValueError("Datetime must have timezone info set")

    if preserve_timezone:
        offset = date_time.utcoffset()
        offset_absolute = abs(offset)
        offset_dir = "+" if offset == offset_absolute else "-"
        hours_off, sec_off = divmod(offset_absolute.seconds, SEC_PER_HR)
        min_off, _ = divmod(sec_off, SEC_PER_MIN)
        offset_str = "%s%02i:%02i" %(offset_dir, hours_off, min_off)
    else:
        date_time = date_time.astimezone(pytz.utc)
        offset_str = "Z"

    iso_str = date_time.strftime(ISO_DATE_TIME_FMT) + offset_str
    return iso_str

def new_object(object_type, uid, uidWellbore="", uidWell=""):
    """
    logs the addition of objects to the server so they can be cleaned up. For now, just print.
        
    Parameters:
      object_type : The WITSML object type. Eg: WMLTYPEIN_LOG
      uid         : The new object's unique identifier
      uidwellbore : If object is a child of a wellbore, the wellbore's unique identifier
      uidWell     : If object is a child of a well, the well's unique identifier
          
    Return:
      Nothing.
    """
    wtl.testlog.wtl_log('ADDED OBJECT ' + object_type + ': uid=' + process_string(uid) + " ", force=True,  no_new_line=True)
    if uidWellbore:
        wtl.testlog.wtl_log('uidWellbore=' + process_string(uidWellbore) + " ", force=True,  no_new_line=True)
    if uidWell:
        wtl.testlog.wtl_log('uidWell=' + process_string(uidWell) + " ", force=True,  no_new_line=True)
    wtl.testlog.wtl_log(' ', force=True)
