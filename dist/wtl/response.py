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
from lxml import etree
import re
import os
import sys

# Application imports
import wtl.testlog
import wtl.control_prim
import wtl.utils
import wtl.config
from sets import Set 
from functools import wraps
from wsvt.SchemaValidator import WITSMLSchemaValidator;
import wcmp.witsml_obj_compare

#******************************************************************************
#
# Local Functions
#
def remove_spaces_from_xml_string(s):
    """
    Remove extra blank text from an XML string
    
    Paramaters:
      s: String to be processed
      
    Return:
      String after removing blank spaces
    """

    parser = etree.XMLParser(remove_blank_text=True)
    root = etree.XML(s, parser)
    return etree.tostring(root)

def response_fail(fail_message):
    """
    Execute a control fail primitive when a response check fails
    
    Parameters:
      fail message:  String indicating the fail reason
      
    Return:
      Nothing
    """
    
    wtl.control_prim.fail(fail_message)

def log_response_message(action):
    """ Log a response message """

    wtl.testlog.wtl_log("  > %s" %action)

def log_response_action(action):
    """ Log a response action """

    wtl.testlog.wtl_log("  > %s..." %action, no_new_line=True)

def log_response_result(result):
    """ Log the result of a response action """

    wtl.testlog.wtl_log(result)

def objectLoop(function_to_decorate):
    @wraps(function_to_decorate)
    def loopbjectControl(*args, **kwargs):
        """
        Decorator function that calls the original function for every object
        if the parameter check='all_objects' is provided
        Otherwise calls the original function once as usual
        
        Parameters:
          Parameters for the original function call
        
        Return:
          Nothing
        """
        if 'check' in kwargs:
            if (kwargs['check'] == 'all_objects'):
                del kwargs['check']
                # Create a list of objects
                num_objects = args[0].get_number_of_objects()
                if (num_objects):
                    for i in range(num_objects):                
                        log_response_message("Checking object %d..." %(i+1))
                        function_to_decorate(*args, _object_index=i+1, **kwargs)
        else:
            function_to_decorate(*args, **kwargs)                
                   
    return loopbjectControl
    
#******************************************************************************
#
# Measure the elapse time of a server api 
#
#
class ElapseTimeInSecondsValue:
    """ Elapse Time of a Server API """

    def __init__(self, value=None):
        """
        Initialization of the elapse time 
        
        Parameters:
          value:  Value to be used for the elapse time 
        """

        self.set(value)

    def clear(self):
        """ Remove the stored value """
         
        self.value = None

    def set(self, value, log=None):
        """ Set the elapse time """
        
        self.value = value

        # Output responses to log
        if log is not None and wtl.config.log_responses:
            wtl.testlog.wtl_log_server_response(log, self.value)            

    def get(self):
        """ Return the elapse time in seconds"""
        return self.value
        
    def check_value_is_set(self):
        """
        Utility function to check value is set before doing other actions
        This will cause the script to stop
        """

        if (self.value == None):
            log_response_message("Cannot verify value because it is not set")
            response_fail("Cannot check Result")

    def check_value_less_than(self, expected_value):
        """
        Check the stored value is less than the expected value
        
        Parameters:
          expected_value: Return value to compare against.
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()
        
        actual_elapse_time = self.value;
        if ( actual_elapse_time > expected_value ):
            log_response_result("Not Ok")
            log_response_message("Elapse Time: %f\n > Expected: %f" % (actual_elapse_time, expected_value))
            response_fail("Fail: Actual Time exceeds Expected.")
        else:                 
            log_response_result("Elapse time Ok")
                
#******************************************************************************
#
# Return value from WITSML server that is not a XML documents 
# This class is used for the Return Value and SuppMsgOut
#
class ReturnValue:
    """ Return value container for non XML return values """

    def __init__(self, value=None):
        """
        Initialization of the returned value 
        
        Parameters:
          value:  Value to be used for the return value 
        """

        self.set(value)

    def clear(self):
        """ Remove the stored value """
         
        self.value = None

    def set(self, value, log=None):
        """ Set the return value """
        
        self.value = value

        # Output responses to log
        if log is not None:
            wtl.testlog.wtl_log_server_response(log, self.value)

    def get(self):
        """ Return the stored value """
        return self.value
        
    def check_value_is_set(self):
        """
        Utility function to check value is set before doing other actions
        This will cause the script to stop
        """

        if (self.value == None):
            log_response_message("Cannot verify value because it is not set")
            response_fail("Cannot check Result")

    def get_first_word(self):
        """ 
        Return all the characters up to the first space
        If value is empty, fail

        Return:
          All the characters up to the first space
          Fail control primitive is called if no string is set
        """

        if (not self.value):
            log_response_message("Value does not contain anything or is not set")
            response_fail("Cannot get uid")
        else:    
            index = self.value.find(' ')
            if (index == -1):
                return self.value
        
            return self.value[0:index]
        
    def check_value(self, expected_value, enable_regex=False):
        """
        Check the stored value matches the expected value
        
        Parameters:
          expected_value: Return value to compare against.
                          This string can contain variable substitutions ($...$),
                          file substitutions (#...#) and  conditional substitutions
                          (^...?...:...^)
          enable_regex:   Flag to enable regex comparison
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()
            
        processed_value_string = wtl.utils.process_string(str(expected_value))
        log_response_action("verifying return value is equal to '%s'" %(processed_value_string))
        value_str = str(self.value)
        if (wtl.utils.compare_strings(processed_value_string, value_str, enable_regex)):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: %s\n    Received: %s" % (processed_value_string, value_str))
            response_fail("Bad value received")

    def check_string(self, expected_string, enable_regex=False):
        """
        Check the stored value matches the expected string
        
        Parameters:
          expected_string: String to compare against.
                           This string can contain variable substitutions ($...$),
                           file substitutions (#...#) and  conditional substitutions
                           (^...?...:...^)
          enable_regex:   Flag to enable regex comparison
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value(expected_string, enable_regex)
        
    def check_value_contains(self, expected_substring):
        """
        Check the stored value contains the expected substring
        
        Parameters:
          expected_substring: String segment to search in the value
          					  This string can contain variable substitutions ($...$),
                              file substitutions (#...#) and  conditional substitutions
                              (^...?...:...^)
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()
            
        processed_substring = wtl.utils.process_string(expected_substring)
        log_response_action("verifying return value contains '%s'" %(processed_substring))
        value_str = str(self.value)
        if (value_str.find(processed_substring) == -1):
            log_response_result("Not Ok")
            log_response_message("Expected substring: %s\n    Received: %s" % (processed_substring, value_str))
            response_fail("Bad value received")
        else:
            log_response_result("Ok")    

    def check_success(self):
        """
        Check the return value indicates success (i.e. is positive)
              
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()
            
        log_response_action("verifying return value is success")
        if (type(self.value) is int):
            if (self.value < 0):
                log_response_result("Not Ok")
                log_response_message("Expected: value greater than 0\n    Received: %s" % (self.value))
                response_fail("Bad value received")
            else:
                log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Value cannot be checked for success because it is not integer")
            response_fail("Bad value received")

    def check_failure(self):
        """
        Check the return value indicates error (i.e. is negative)
              
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()
            
        log_response_action("verifying return value is failure")
        if (type(self.value) is int):
            if (self.value > 0):
                log_response_result("Not Ok")
                log_response_message("Expected: value less than 0\n    Received: %s" % (self.value))
                response_fail("Bad value received")
            else:
                log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Value cannot be checked for failure because it is not integer")
            response_fail("Bad value received")
            
#******************************************************************************
#
# Return value from WITSML server that is an XML document 
# This class is used for the XMLout and CapabilitiesOut
#
class XMLValue:
    """ Return value container for an XML return values """

    def __init__(self, value=None):
        """
        Initialization of the returned value 
        
        Parameters:
          value:  Value to be used for the return value 
        """

        self.set(value)

    def clear(self):
        """ Remove the stored value """

        self.original_value = None
        self.value = None
        self.log_data = None
        self.mnemonics_list = []
        self.units_list = []
        self.indexCurve_list = []

    def _remove_encoding(self, s):
        """ Remove the encoding from an XML document """ 
        
        first_line = s.lstrip().splitlines()[0]
        match_str = re.search(r'\<?xml .*encoding=.*\?\>', first_line)
        if not match_str:
            return s
        else:
            replace_str = re.sub("""encoding=["'].*["']""", '', match_str.group(0))
            return s.replace(match_str.group(0), replace_str, 1)
            
    def _remove_default_namespace(self, s):
        """ Remove the defult namespace  """ 
        
        match_str = re.search(r'xmlns=".*?"', s)
        if not match_str:
            return s
        else:
            return s.replace(match_str.group(0), "", 1)
    
    def set(self, value, log=None):
        """
        Store the XML document in a string and a XML tree.
        If applicable, also store the logData element
        """

        self.root = None
        self.mnemonics_list = []
        self.units_list = []
        self.indexCurve_list = []

        self.object_name = ""
        self.version = ""

        co = value
        if co:
            co = self._remove_encoding(co) # do not pass the encoding to library, as we do not want to stop if it is incorrect
            self.original_value = co
            co = self._remove_default_namespace(co)
            try:
                parser = etree.XMLParser(remove_blank_text=True)
                self.root = etree.XML(co, parser)
                co =  etree.tostring(self.root)
            except:
                # Something wrong with XML
                log_response_message("XML value is incorrect")
                self.clear()
                return
            
            self.object_name = self.root.tag[:-1]
            self.version = self.root.get('version')

        self.value = co
        
        # Output responses to log
        if ((log is not None) and co):
            wtl.testlog.wtl_log_server_response(log, etree.tostring(self.root, pretty_print=True))
        
        # Set the log data if applicable
        if self.get_element("logData"):
            self.log_data = self.get_log_data()
            
        # prime mnemonics, units and index curve list    
        self.mnemonics_list = self.get_mnemonics_list()
        self.units_list = self.get_units_list()
        self.indexCurve_list = self.get_index_curve_list()

    def get(self):
        """ Return the stored value """

        return self.value

    def get_original_value(self):
        """ Return the initial value used to set the variable """

        return self.original_value

    def get_version(self):
        """ Return the data schema version extracted from the XML document """

        return self.version
    
    def get_object_name(self):
        """ Return the object name extracted from the XML document """

        return self.object_name
    
    def get_element(self, xpath_string, _object_index=None):
        """
        Get the elements from the XML tree with the corresponding xpath.
        A list of all elements matching in the document with the tag is returned
        
        Parameters:
          xpath_string: Element name or element's xpath without namespace
          _object_index: (Optional) Index of the object in the XML document to use
                         as root for the search instead of the documents main element
                         If this is provided, xpath_string must not start with '/'
                         (e.g. an absolutepath is not alloed) and if the object name is included
                         in the path it should not have a predicate
                         Examples, if _object_index is not None
                            xpath_string='/logs/log/name'       -> bad
                            xpath_string='//name'               -> bad
                            xpath_string='log[@uid='123']/name' -> bad
                            xpath_string='logs/log/name'        -> ok
                            xpath_string='name'                 -> ok
                            xpath_string='log/name' -           -> ok                       
        Return:
          A list of elements if found, otherwise 'None'
        """

        if ((self.value == None) or (not xpath_string)):
            return None
               
        if(xpath_string[0] <> '/'):
            if (_object_index is not None):
                # Add indexed object to XPath
                path = xpath_string.split('/')
                found = False
                for i in range(len(path)):
                    if (path[i] == self.object_name):
                        path[i] = path[i] + '[' + str(_object_index) + ']'
                        found = True
                        break
                xpath_string = '/'.join(path)
                if (not found):
                    xpath_string = self.object_name + '[' + str(_object_index) + ']//' + xpath_string                  
            
            xpath_string = "//" + xpath_string
                
        return self.root.xpath(xpath_string)

    def get_element_text_value(self, tag, _object_index=None):
        """
        Get the text of the element from the XML tree with the corresponding
        tag.
        The first element in the document with the tag is returned
        
        Parameters:
          tag:     The element's tag
        
        Return:
          The element's text if found, otherwise 'None'
        """

        tag = wtl.utils.process_string(tag)

        element = self.get_element(tag, _object_index)
        if (element):
            return element[0].text
        return None

    def get_element_boolean_value(self, tag, _object_index=None):
        """
        Get the Boolean value of the element from the XML tree with the
        corresponding tag.
        The first element in the document with the tag is returned
        
        Parameters:
          tag:     The element's tag
        
        Return:
          'True' or 'False' if element is found, otherwise 'None'
        """

        tag = wtl.utils.process_string(tag)

        element = self.get_element(tag, _object_index)
        if (element):
            if element[0].text in ['true', '1']:
                return True
            elif element[0].text in ['false', '0']:
                return False
            else:
                return None
        return None
    
    
    def get_recurring_element_list_via_key(self, tag, keyList, keyTag, desiredTag):
        """
        Get a list of the the text of all the recurring elements from the XML
        tree with the corresponding tag, keyTag and desiredTag.
        The first recurring element list in the document with the tag is
        returned
        
        Parameters:
          tag       : The element's tag
          keyList   : The list of key values that will determine the order of the returned desired values
          keyTag    : The key that represents the keyList
          desiredTag: The column name that will determine the values returned
          
        Return:
          A list with the text of all elements with the tag if found,
          otherwise 'None'
          If a key value does not have a corresponding value in the source, its value will be None.
          
         Examples, 
            if you desired to get all of the minIndex(s) of a logCurveInfo based on the mnemonic then
               the tag = "logCurveInfo"
               keyList = the list of mnemonics
               keyTag = 'mnemonic'
               desiredTag = 'minIndex'
        """   
             
        desiredKeyValues = []
        for keyValue in keyList:
             desiredTagValue = self.get_element_text_value("{0}[{1}='{2}']/{3}".format(tag,keyTag,keyValue,desiredTag))
             desiredKeyValues.append(desiredTagValue)
        return desiredKeyValues    
    
    def get_recurring_element_list(self, tag, _object_index=None):
        """
        Get a list of the text of all the recurring elements from the XML
        tree with the corresponding tag.
        The first recurring element list in the document with the tag is
        returned
        
        Parameters:
          tag:     The element's tag
        
        Return:
          A list with the text of all elements with the tag if found,
          otherwise 'None'
        """
        
        tag = wtl.utils.process_string(tag)

        elements = []
        element = self.get_element(tag, _object_index)
        if (element is not None):
            for child in element:
                elements.append(child.text) 
        
        return elements
    
    def get_number_of_objects(self):
        """
        Get the number of objects in the XML tree
        
        Parameters:
          None
        
        Return:
          The number of objects returned if there is a value exists,
          otherwise 'None'
        """
        if (self.value == None):
            return None
        
        obj = self.get_element(self.get_object_name())
        if obj:
            return len(obj)
            
        return 0

    def get_latest_dTimChange(self):
        """
        Get the dTimChange of the changeHistory element with the latest dTimChange
                
        Parameters:
          None
        
        Return:
          The latest dTimChange, otherwise 'None'
        """

        latest = None
        elements = self.get_element('changeHistory/dTimChange')
        if (elements):
            for element in elements:
                if ((latest is None) or (wtl.utils.iso_to_utc(element.text) > wtl.utils.iso_to_utc(latest))):
                    latest = element.text

        return latest             
        
    def check_value_is_set(self):
        """
        Utility function to check value is set before doing other actions
        This will cause the script to stop
        """

        if (self.value == None):
            log_response_message("Cannot verify value because it is not set")
            response_fail("Cannot check Result")

    def check_string(self, expected_xml_string, enable_regex=False):           
        """
        Check the stored value contains the substring
        
        Parameters:
          expected_xml_string: String segment to determine as present in value
                               expected_xml_string cannot contain regex if enable_regex is False 
                               expected_xml_string can contain variable substitutions ($...$),
                               file substitutions (#...#) and  conditional substitutions
                               (^...?...:...^)
          enable_regex:   Flag to enable regex comparison
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        processed_expected_xml_string = wtl.utils.process_string(expected_xml_string)
        if (not processed_expected_xml_string):
            response_fail("Bad expected string in check primitive")
     
        log_response_action("verifying value against '%s'" %(processed_expected_xml_string))
    
        if (wtl.utils.compare_strings(processed_expected_xml_string, self.value, enable_regex)):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: %s\n    Received: %s" % (processed_expected_xml_string, self.value))
            response_fail("Bad value received")
         
    def check_string_does_not_contain(self, unexpected_substring):
        """
        Check the stored value does not contain the substring
        
        Parameters:
          unexpected_substring: String segment to determine as not present in value
          unexpected_substring cannot contain regex 
          unexpected_substring can contain variable substitutions ($...$),
            file substitutions (#...#) and  conditional substitutions
            (^...?...:...^)
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()
            
        processed_substring = wtl.utils.process_string(unexpected_substring)
        log_response_action("verifying value does NOT contain '%s'" %(processed_substring))
                
        if (self.value.find(processed_substring) != -1):
            log_response_result("Not Ok")
            log_response_message("Did Not Expect Substring: %s\n    Received: %s" % (processed_substring, self.value))
            response_fail("Bad value received")
        else:
            log_response_result("Ok")        
            

    def check_xml_string(self, expected_xml_string, enable_regex=False):
        """
        Check the stored value contains the expected string
        
        Parameters:
          expected_xml_string: XML string segment to determine as present in value
                               expected_xml_string cannot contain regex if enable_regex is False 
                               expected_xml_string can contain variable substitutions ($...$),
                               file substitutions (#...#) and  conditional substitutions
                               (^...?...:...^)
          enable_regex:   Flag to enable regex comparison
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()
            
        processed_expected_xml_string = wtl.utils.process_string(expected_xml_string)
        if (not processed_expected_xml_string):
            response_fail("Bad expected sting in check primitive")

        processed_expected_xml_string = remove_spaces_from_xml_string(processed_expected_xml_string)
        log_response_action("verifying value value against '%s'" %(processed_expected_xml_string))
    
        if (wtl.utils.compare_strings(processed_expected_xml_string, self.value, enable_regex)):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: %s\n    Received: %s" % (processed_expected_xml_string, self.value))
            response_fail("Bad value received")

    def check_xml_normalized_string(self, object, expected_xml_string, diff_only=True):
        """
        Check the returned object from GetFromStore matches the expected_xml_string
        
        Parameters:
          object: String name of the object ( i.e. well, wellbore )
          expected_xml_string: representation of the object to compare with
          diff_only: if true, log text differences, false will log html differences
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """        
        self.check_value_is_set()
            
        processed_object = wtl.utils.process_string(object)
        processed_expected_xml_string = wtl.utils.process_string(expected_xml_string)
        if (not processed_expected_xml_string):
            response_fail("Bad expected sting in check primitive")
 
        log_response_action("verifying normalized value value against object sent")
        
        result, report = wcmp.witsml_obj_compare.compareWITSMLObject(self.version, processed_object , processed_expected_xml_string, self.value, diff_only)
        
        log_response_message(report)

        if (result):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_result("Differences: " + report)
            log_response_message("Expected: %s\n    Received: %s" % (processed_expected_xml_string, self.value))
            response_fail("Bad value received")

    @objectLoop
    def check_element_included(self, tag, _object_index=None):
        """
        Check the stored value contains the expected element
        
        Parameters:
          tag:     The element's tag
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()

        tag = wtl.utils.process_string(tag)

        log_response_action("verifying element '%s' is included" %(tag))
        if (self.get_element(tag, _object_index)):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            response_fail("Missing expected element")
               
    @objectLoop
    def check_element_not_included(self, tag, _object_index=None):
        """
        Check the stored value does not contain the expected element
        
        Parameters:
          tag:     The element's tag
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        self.check_value_is_set()

        tag = wtl.utils.process_string(tag)

        log_response_action("verifying element '%s' is not included" %(tag))
        if (self.get_element(tag, _object_index)):
            log_response_result("Not Ok")
            response_fail("Received unexpected element")
        else:
            log_response_result("Ok")

    @objectLoop
    def check_element_value(self, tag, expected_value, enable_regex=False, _object_index=None):
        """
        Check the stored value matches the expected value
        
        Parameters: 
          tag:            The element's tag
          expected_value: Value to be compared against
          enable_regex:   Flag to enable regex comparison
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        tag = wtl.utils.process_string(tag)

        processed_value_string = wtl.utils.process_string(str(expected_value))
        log_response_action("verifying <%s> value is equal to '%s'" %(tag,processed_value_string))
        element = self.get_element(tag, _object_index)
        if (element):
            value_str = element[0].text 
            if (wtl.utils.compare_strings(processed_value_string, value_str, enable_regex)):
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Expected: %s\n    Received: %s" % (processed_value_string, value_str))
                response_fail("Bad element value received")
        else:
            log_response_result("Not Ok")
            response_fail("Missing expected element")

    @objectLoop
    def check_element_value_greaterthan(self, tag, value, _object_index=None):
        """
        Check the stored value is greater than the provided value
        Float comparison is used
        
        Parameters: 
          tag:   The element's tag
          value: Int or float number to be compared against
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        tag = wtl.utils.process_string(tag)

        value = float(value)
        element = self.get_element(tag, _object_index)
        log_response_action("verifying <%s> value is greater than '%f'" %(tag, value))
        if (element):
            element_float_value = float(element[0].text) 
            if (element_float_value > value):
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Expected: greater than %f\n    Received: %f" % (value, element_float_value))
                response_fail("Bad element value received")
        else:
            log_response_result("Not Ok")
            response_fail("Missing expected element")

    @objectLoop
    def check_element_value_lessthan(self, tag, value, _object_index=None):
        """
        Check the stored value is less than the provided value
        Float comparison is used
        
        Parameters: 
          tag:   The element's tag
          value: Int or float number to be compared against
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        tag = wtl.utils.process_string(tag)

        value = float(value)
        element = self.get_element(tag, _object_index)
        log_response_action("verifying <%s> value is less than '%f'" %(tag, value))
        if (element):
            element_float_value = float(element[0].text) 
            if (element_float_value < value):
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Expected: less than %f\n    Received: %f" % (value, element_float_value))
                response_fail("Bad element value received")
        else:
            log_response_result("Not Ok")
            response_fail("Missing expected element")

    @objectLoop
    def check_recurring_element_value_contains(self, tag, expected_value_list, enable_regex=False, _object_index=None):
        """
        Check the recurring elements in the XPath tag contain the provided value list
        
        Parameters: 
          tag:                 The element's tag
          expected_value_list: list of values
          enable_regex:   Flag to enable regex comparison
                  
        Example:
          check_recurring_element_value_contains('logs/log/logCurveInfo/mnemonic', ['DEPTH', 'GR', 'CALI', 'RHOB'])
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """          
        self.check_value_is_set()

        tag = wtl.utils.process_string(tag)

        element = self.get_element(tag, _object_index)

        for expected_value in expected_value_list:
            processed_value_string = wtl.utils.process_string(str(expected_value))
            log_response_action("verifying one of <%s> values is equal to '%s'" %(tag,processed_value_string))
            if (element):
                found = False
                for instance in element[:]:
                    value_str = instance.text 
                    if (wtl.utils.compare_strings(processed_value_string, value_str, enable_regex)):
                        log_response_result("Ok")
                        found = True
                        element.remove(instance)
                        break
                if (not found):
                    log_response_result("Not Ok")
                    log_response_message("Expected: %s not received" % (processed_value_string))
                    response_fail("Bad recurring element value received")
            else:
                log_response_result("Not Ok")
                response_fail("Missing expected recurring element")

    @objectLoop
    def check_recurring_element_value(self, tag, expected_value_list, enable_regex=False, _object_index=None):
        """
        Check the recurring elements in the XPath tag match the provided value list
        
        Parameters: 
          tag:                 The element's tag
          expected_value_list: list of names
          enable_regex:   Flag to enable regex comparison
        
          
        Example:
          check_recurring_element_value('logs/log/logCurveInfo/mnemonic', ['DEPTH', 'GR', 'CALI', 'RHOB'])

        Return:
          Nothing. Fail control primitive is called if check fails
        """        
        
        tag = wtl.utils.process_string(tag)
       
        # Check all element in the list are included
        self.check_recurring_element_value_contains(tag, expected_value_list, enable_regex, _object_index)
        
        #Check that that is all elements
        log_response_action("verifying there are no more <%s> values not in the provided list" %tag)
        element_list = self.get_recurring_element_list(tag, _object_index)
        if (len(expected_value_list) == len(element_list)):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: %s" %(str(expected_value_list)))
            log_response_message("Received: %s" %(str(element_list)))
            response_fail("Mismatch in expected recurring elements.")
 
    @objectLoop
    def check_element_value_contains(self, tag, expected_substring, _object_index=None):
        """
        Check the tag value contains the expected substring
        
        Parameters: 
          tag:                The element's tag
          expected_substring: String to search in the tag value
          expected_substring cannot contain regex 
          expected_substring can contain variable substitutions ($...$),
            file substitutions (#...#) and  conditional substitutions
            (^...?...:...^)
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """        

        self.check_value_is_set()

        tag = wtl.utils.process_string(tag)

        processed_substring = wtl.utils.process_string(expected_substring)
        log_response_action("verifying <%s> value contains to '%s'" %(tag,processed_substring))
        element = self.get_element(tag, _object_index)
        if (element):
            value_str = element[0].text 
            if (value_str.find(processed_substring) == -1):
                log_response_result("Not Ok")
                log_response_message("Expected substring: %s\n    Received: %s" % (processed_substring, value_str))
                response_fail("Bad element value received")
            else:
                log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            response_fail("Missing expected element")

    def get_attribute(self, tag, attribute, _object_index=None):
        """
        Get the value of the given attribute in the given tag
        The first element with the tag is used
        
        Parameters:
          tag:       The element's tag
          attribute: The attribute's name
        
        Return:
          The attribute's value if found, otherwise 'None'
        """

        tag = wtl.utils.process_string(tag)

        element = self.get_element(tag, _object_index)
        if (element):
            return element[0].get(attribute)

        return None

    def get_log_data(self):
        """
        Retrieve the logData as a list of rows of data.
        Each row is a list of strings corresponding to the data values.
        
        Parameters:
          none
        
        Return:
          A list of logData rows
        """
        log_data = []
        num_points = 0
        
        element = self.get_element('logData')
        if not element:
            return None
        
        else:
            # Get the data first
            data = self.get_element('data')
            if (data == None):
                return None
            for row in data:
                new_data =(row.text.split(','))
                if (not num_points):
                    num_points = len(new_data)                                   
                else:
                    if  (num_points != len(new_data)):
                        # A column with different number of points -> bad
                        log_response_message("logData does not have equal width rows.")
                        return None
                log_data.append(new_data)
            
        return log_data
        
    def get_mnemonics_list(self):
        """
        Build a list of mnemonics from the mnemonicList attribute delimited by ","
        
        Parameters:
          none
        
        Return:
          A list of mnemonic strings.  An empty list if no mnemonics
        """
        
        if (not self.mnemonics_list):
            mnemonic_list = [];
            mnemonic_list_element = self.get_element('mnemonicList')
            
            if (mnemonic_list_element and mnemonic_list_element[0].text):
                mnemonic_list = mnemonic_list_element[0].text.split(',')
                    
            else:
                # handle case where we don't have mnemonicList:  Use logCurveInfo instead
                # note: this is for WITSML 1.3.1.1 handling
                curves = self.get_element('logCurveInfo')
                                   
                if (curves is not None):
                    mnemonic_list = [''] * len(curves)
                    
                    for curve in curves:
                        column = curve.find("columnIndex")
                        if (column is not None):
                            column_number = int(column.text) - 1
                            mnemonic = curve.find("mnemonic")
                            if (mnemonic is not None):
                                mnemonic_list[column_number] = mnemonic.text
            
            # store the mnemonics list                      
            self.mnemonics_list = mnemonic_list
            
        return self.mnemonics_list;
    
    
    def get_units_list(self):
        """
        Retrieve a unit list from the unitsList attribute delimited by ","
        
        Parameters:
          none
        
        Return:
          A list of unit strings.  An empty list if no units
        """
        
        if (not self.units_list):
        
            unit_list = [];
            unit_list_element = self.get_element('unitList')
            
            if (unit_list_element and unit_list_element[0].text):
                unit_list = unit_list_element[0].text.split(',')
            
            else:
                # handle case where we don't have unitList:  Use logCurveInfo instead
                curves = self.get_element('logCurveInfo')
                                
                if (curves is not None):
                    unit_list = [''] * len(curves)
                    
                    for curve in curves:
                        column = curve.find("columnIndex")
                        if (column is not None):
                            column_number = int(column.text) - 1
                            unit = curve.find("unit")
                            if (unit is not None):
                                unit_list[column_number] = unit.text
                            
            self.units_list = unit_list                
                            
        return self.units_list;
            
    def get_index_curve_list(self):
        """
        Retrieve a list of booleans representing whether each curve stored in 
        the log_data structure is the index curve or not.  True represents
        the index curve, False if not an index curve.  
        
        Note: this is mostly useful for 1.3.1.1 support.
        
        Parameters:
          none
        
        Return:
          A list of booleans.  An empty list if no curves
        """
        
        if (not self.indexCurve_list):
            index_list = [];
            
            # populate size of index_list
            mnemonic_list = self.get_mnemonics_list()
            index_list = [False] * len(mnemonic_list)
            
            # Mark the index curve column
            column_index = None
            index_curve = self.get_element('indexCurve')
            if (index_curve):
                # If 1.3.1.1 schema try to find the columnIndex attribute
                column_index = index_curve[0].get('columnIndex')
                
                if (column_index):
                    index_list[int(column_index)-1] = True
                    
                # If 1.4.1.x and after check if the index is in the data. If so the column is the first one
                if (mnemonic_list and (mnemonic_list[0] == index_curve[0].text)):
                    index_list[0] = True
            self.indexCurve_list = index_list
                
        return self.indexCurve_list
    
        
    def get_log_data_index_value(self, n):
        """
        Return the index value of the nth row of the log data
        
        Parameters:
          n: The row number of the value
          
        Return:
          The index value if found, otherwise 'None'
        """
        if (self.log_data == None):
            return None
        elif (n < len(self.log_data)):
            index_list = self.get_index_curve_list()
            for index in range(len(index_list)):
                if (index_list[index]):
                    return self.log_data[n][index]
        return None
        
    def get_log_data_data_value(self, n, mnemonic):
        """
        Return the value of the nth row of the log data for the given mnemonic curve
        
        Parameters:
          n       : The row number of the value
          mnemonic: String representing the logCurve 
          
        Return:
          The value if found, otherwise 'None'
        """
        if (self.log_data == None):
            return None
        elif (n < len(self.log_data)):
            mnemonics_list = self.get_mnemonics_list()
            
            for index in range(len(mnemonics_list)):
                if (mnemonics_list[index] == mnemonic):
                    return self.log_data[n][index]
        return None
        
    def get_log_curve_array_length(self, mnemonic):
        """
        Determine the array length of the desired curve
        Needs the logCurveInfo in the log header 
        
        Parameters:
          mnemonic
        
        Return:
          Array length or if the logCurveInfo section is not defined, a return of 1
        """        
        wtl.utils.set_variable_value('array_length_mnemonic', mnemonic)
        axisCountList = self.get_recurring_element_list("logs/log/logCurveInfo[mnemonic='$array_length_mnemonic$']/axisDefinition/count")
        if ( axisCountList is not None and len(axisCountList) > 0):
            total=1
            for x in axisCountList:
                total = total * int(x)
            return total
        else:
            return 1        
        
    def get_log_data_number_of_nodes(self):
        """
        Return the number of logData rows
        
        Parameters:
          None
          
        Return:
          The number of logData rows
        """
        if (self.log_data):
            return len(self.log_data)
        
        return 0
        
    def get_log_data_number_of_points(self):
        """
        Return the number of logData rows multiplied by the number of curves
        
        Parameters:
          None
          
        Return:
          The number of logData rows multiplied by the number of curves
        """
        index_curves = self.get_index_curve_list()
        if (self.log_data):
            return (len(self.log_data)) * (len(index_curves))
        
        return 0

    def check_log_data_index_value(self, n, value, error_margin=0):
        """
        Compare the value against the index of the nth row of the log data
        
        Parameters:
          n           : The row number with the value being checked
          value       : Value to compare against
                        This string can contain variable substitutions ($...$),
                        file substitutions (#...#) and  conditional substitutions
                        (^...?...:...^)
          error_margin: Acceptable percent deviation from the value 
          
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        actual_value = self.get_log_data_index_value(n)
        if actual_value is None:
            log_response_action("verifying index %d" %(n))
            log_response_result("Not Ok")
            log_response_message("No index %d received" % (n))
            response_fail("Bad index value received: %d"% (n))
        elif (error_margin):
            log_response_action("verifying index: %d is equal to %s (+/-%.0f" %(n, value, error_margin) +'%)')
            try:
                min_val = float(actual_value) * (100 - error_margin) /100
                max_val = float(actual_value) * (100 + error_margin) /100
            except:
                #if error margin is provided the values must be able to be converted to float
                log_response_result("Not Ok")
                log_response_message("Cannot convert index value %d to float" % (n))
                response_fail("Bad index value received: %d"% (n))
                return
            if ((float(value) >= min_val) and (float(value) <= max_val)):
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Expected: %s (+/-%.0f" % (value, error_margin) + '%' + ")\n    Received: %s" % (actual_value))
                response_fail("Bad index value received: %d"% (n))
        else:
            log_response_action("verifying index: %d is equal to %s" %(n, value))
            if (value == actual_value):
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Expected: %s\n    Received: %s" % (value, actual_value))
                response_fail("Bad index value received: %d"% (n))
        
    def check_log_data_data_value(self, n, mnemonic, value, error_margin=0):
        """
        Compare the value against the nth row of the log data for the given mnemonic curve
        
        Parameters:
          n           : The row number with the value being checked
          mnemonic    : String representing the logCurve 
          value       : Value to compare against
                        This string can contain variable substitutions ($...$),
                        file substitutions (#...#) and  conditional substitutions
                        (^...?...:...^)
           error_margin: Acceptable percent deviation from the value 
          
        Return:
          Nothing. Fail control primitive is called if check fails
        
        """        
        self.check_value_is_set()

        actual_value = self.get_log_data_data_value(n, mnemonic)
        if actual_value is None:
            log_response_action("verifying value %d of '%s'" %(n, mnemonic))
            log_response_result("Not Ok")
            log_response_message("No value %d for '%s' received" % (n, mnemonic))
            response_fail("Bad %d data value received for %s"% (n, mnemonic))            
        elif (error_margin):
            log_response_action("verifying value %d of '%s' is equal to %s (+/-%.0f" %(n, mnemonic, value, error_margin) +'%)')
            try:
                min_val = float(actual_value) * (100 - error_margin) /100
                max_val = float(actual_value) * (100 + error_margin) /100
            except:
                #if error margin is provided the values must be able to be converted to float
                log_response_result("Not Ok")
                log_response_message("Cannot convert data value %d for '%s' to float" % (n, mnemonic))
                response_fail("Bad %d data value received for %s"% (n, mnemonic))
                return
            if ((float(value) >= min_val) and (float(value) <= max_val)):
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Expected: %s (+/-%.0f" % (value, error_margin) + '%' + ")\n    Received: %s" % (actual_value))
                response_fail("Bad %d data value received for %s"% (n, mnemonic))
        else:
            log_response_action("verifying value %d of '%s' is equal to %s" %(n, mnemonic, value))
            if (value == actual_value):
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Expected: %s\n    Received: %s" % (value, actual_value))
                response_fail("Bad %d data value received for %s"% (n, mnemonic))
        
    def check_log_data_all(self, array, mnemonics_list, index_error_margin=0, error_margin=0):
        """
        Check all the data values received in the logData
        
        Parameters:
          data_array: Array with all the data values to check against. The array is formatted as follows
                       [(value00, value01, value02,...value0n),
                        (value10, value11, value12,...value1n),
                        ...
                        (valuem0, valuem1, valuem2,...valuemn)]
                       Notes:
                       - Index data has to be in the first column
                       - No null values can be in the data
                       - Index can be datatime or a floating point number
                       - Data values can be only floating point numbers

          mnemonics_list:  Mnemonic list for the array provided
          
          index_error_margin (optional): Error margin to apply to the index comparison
                                         Must be set to zero or not included for index datatime
                                         Must be set to non-zero for depth index

          error_margin (optional): Error margin to apply to the data value comparison Must be non-zero

        Return:
            None
            Script will fail if comparison fails
        """
                
        self.check_value_is_set()

        if (len(array) != self.get_log_data_number_of_nodes()):
            log_response_action("verifying number of nodes in logData")
            log_response_result("Not Ok")
            log_response_message("Expected %d nodes" % (len(array)))
            log_response_message("Received %d nodes" % (self.get_log_data_number_of_nodes()))
            response_fail("Unexpected number of nodes in logData")
            return
        
        if ((len(array)*len(array[0])) != self.get_log_data_number_of_points()):
            log_response_action("verifying number of points in logData")
            log_response_result("Not Ok")
            log_response_message("Expected %d points" % (len(array)*len(array[0])))
            log_response_message("Received %d points" % (self.get_log_data_number_of_points()))
            response_fail("Unexpected number of node=s in logData")
            return
             
        if (len(array[0]) != len(mnemonics_list)):
            log_response_action("verifying length of mnemonic list")
            log_response_result("Not Ok")
            log_response_message("Expected %d entries" % (len(array[0])))
            log_response_message("Received %d entries" % (len(mnemonics_list)))
            response_fail("Unexpected number of mnemonics provided")
            return
             
        log_response_message("verifying all logData values:")
        for index in range(len(array)):
            self.check_log_data_index_value(index, array[index][0], index_error_margin)
            for value_index in range(len(array[index]) - 1):            
                self.check_log_data_data_value(index, mnemonics_list[value_index+1], array[index][value_index+1], error_margin)

    def check_log_data_number_of_nodes(self, n):
        """
        Check n against the number of logData rows returned
        
        Parameters:
          n : The number of logData rows expected
          
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        log_response_action("verifying <logData> has %d data nodes" %(n))
        num_nodes = self.get_log_data_number_of_nodes()
        if (n == num_nodes):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: %d\n    Received: %d" % (n, num_nodes))
            response_fail("Bad number of data nodes received")
        
    def check_log_data_number_of_points(self, n):
        """
        Check n against the number of logData rows multiplied by the number of curves returned
        
        Parameters:
          n : The number of logData rows multiplied by the number of curves expected
          
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        log_response_action("verifying <logData> has %d data points" %(n))
        num_points = self.get_log_data_number_of_points()
        if (n == num_points):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: %d\n    Received: %d" % (n, num_points))
            response_fail("Bad number of data points received")
        

    @objectLoop
    def check_attribute_included(self, tag, attribute, _object_index=None):
        """
        Check the stored value contains the expected attribute in the tag
        
        Parameters:
          tag:       The attribute's tag
          attribute: The name of the attribute being checked if included
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        log_response_action("verifying element '%s' has attribute '%s'" %(tag, attribute))
        if (self.get_attribute(tag, attribute, _object_index) != None):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            response_fail("Missing expected attribute")

    @objectLoop
    def check_attribute_not_included(self, tag, attribute, _object_index=None):
        """
        Check the stored value does not contain the expected attribute in the tag
        
        Parameters:
          tag:       The attribute's tag
          attribute: The name of the attribute being checked if not included
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        log_response_action("verifying element '%s' does not have attribute '%s'" %(tag, attribute))
        if (self.get_attribute(tag, attribute, _object_index) != None):
            log_response_result("Not Ok")
            response_fail("Received unexpected attribute")
        else:
            log_response_result("Ok")

    @objectLoop
    def check_attribute_value(self, tag, attribute, expected_value, enable_regex=False, _object_index=None):
        """
        Check the stored value contains the expected attribute in the tag
        
        Parameters:
          tag:            The attribute's tag
          attribute:      The attribute whose value is being checked
          expected_value: The value that the attribute is expected to have
          enable_regex:   Flag to enable regex comparison
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        processed_value_string = wtl.utils.process_string(str(expected_value))
        log_response_action("verifying '%s' attribute of <%s> has value equal to %s" %(attribute, tag, processed_value_string))
        value_str = self.get_attribute(tag, attribute, _object_index)
        if (value_str != None):
            if (wtl.utils.compare_strings(processed_value_string, value_str, enable_regex)):
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Expected: %s\n    Received: %s" % (processed_value_string, value_str))
                response_fail("Bad attribute value received")
        else:
            log_response_result("Not Ok")
            response_fail("Missing expected attribute")

    @objectLoop
    def check_attribute_value_is_contained(self, tag, attribute, expected_superstring, _object_index=None):
        """
        Check the stored value contains the expected string in the attribute
        
        Parameters:
          tag:                  The attribute's tag
          attribute:            The attribute whose value is being checked
          expected_superstring: The value that the attribute is expected to contain
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        processed_value_string = wtl.utils.process_string(str(expected_superstring))
        log_response_action("verifying '%s' attribute of <%s> is included in '%s'" %(attribute, tag, processed_value_string))
        value_str = self.get_attribute(tag, attribute, _object_index)
        if (value_str != None):
            if value_str in processed_value_string:
                log_response_result("Ok")
            else:
                log_response_result("Not Ok")
                log_response_message("Container string: %s\n    Received: %s" % (processed_value_string, value_str))
                response_fail("Bad attribute value received")
        else:
            log_response_result("Not Ok")
            response_fail("Missing expected attribute")

    def check_number_of_objects(self, num):
        """
        Check the number of objects matches the number provided
        
        Parameters: 
          num: Expected number of objects 
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        log_response_action("verifying objects received is equal to %d" %(num))
        if (self.get_number_of_objects() == num):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: %d\n    Received: %d" % (num, self.get_number_of_objects()))
            response_fail("Wrong number of objects received")

    def check_number_of_objects_greaterthan(self, num):
        """
        Check the number of objects is greater than the number provided
        
        Parameters: 
          num: Number to be compared against 
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        log_response_action("verifying objects received is greater than %d" %(num))
        if (self.get_number_of_objects() > num):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: greater than %d\n    Received: %d" % (num, self.get_number_of_objects()))
            response_fail("Wrong number of objects received")

    def check_number_of_objects_lessthan(self, num):
        """
        Check the number of objects is less than the number provided
        
        Parameters: 
          num: Number to be compared against 
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        self.check_value_is_set()

        log_response_action("verifying objects received is less than %d" %(num))
        if (self.get_number_of_objects() < num):
            log_response_result("Ok")
        else:
            log_response_result("Not Ok")
            log_response_message("Expected: less than %d\n    Received: %d" % (num, self.get_number_of_objects()))
            response_fail("Wrong number of objects received")

    def build_elements_list(self):
        """ 
        Build list representing nodes and attributes in form of xxx[zzz]
        
        Parameters:
          root_node - root node
        
        Return:
          list of elements, and attributes 
        """
        root_node = etree.fromstring(self.value);
        #root_node = self.root;
        rez_list = [];
        for node in root_node.getiterator():
                rez_list.append( str(node.xpath('local-name()')) );
                for attrib_i in node.attrib:
                    if (attrib_i.find("{") == -1):
                        rez_list.append( str(node.xpath('local-name()'))+"["+attrib_i+"]" );
        return rez_list;
    
    def build_attribute_and_child_elements_list(self, node):
        """ 
        Utility function to build a list of the provided node's attribute names
        in the form node[attribute] and the node's child element tags.
        Only a single child element is included for recurring child elements
        E.g. for <node attrib1='a1' attrib2='a2'>
                  <childelement1 attrib3='a3'>elem1-a</childelement1>
                  <childelement1 attrib4='a4'>elem1-b</childelement1>
                  <childelement2>
                     <grandchildelement3/>
                  </childelement2>
                 </node> 
        The list returned is
          ['node[attrib1]' , 'node[attrib2]', 'childelement1', 'childelement2']
        Note:
           - recurring child elements are included only once in the list
           - grandchildren elements are not included
           - Only node attributes are included
           
        Parameters:
          node - node for which the attributes and child elements are listed
        
        Return:
          list of attributes and child elements of the given node 
        """
             
        rez_list = [];
        
        if (node is None):
            return rez_list
            
        for attrib_i in node.attrib:
            if (attrib_i.find("{") == -1):
                rez_list.append( str(node.xpath('local-name()'))+"["+attrib_i+"]" );
        for child in node:
            if (child.tag not in rez_list):
                rez_list.append(child.tag);

        return rez_list
    
    def check_element_attribute_and_children_list(self, xpath_string, expected_list, match='exact', enable_regex=False,):
        """
        This function will find all elements matching the given xpath and check their
        list of attributes and child elements against the list provided based on the match parameter type.
          match='exact'     - All the attributes and child element tags in the expected list
                              are contained in all matching elements.
                              No additional attributes or child elements in the matching elements
          match='at-least'  - All the attributes and child element tags in the expected list
                              are contained in all matching elements.
                              Additional attributes or child elements may exist in the matching elements
          match='at-most'   - The attributes and child element tags in the expected list
                              may be contained in all matching elements.
                              No additional attributes or child elements in the matching elements
        
        Parameters:
          xpath_string:  Element name or element's xpath without namespace
          expected_list: The list of expected attribute names and child element tags expected
                         Attributes are given in the form elementName[attributeName]
                         Example ['wellbore[uid]', 'wellbore[uidWell]', 'name', 'nameWell']
          match:         Match type. One of 'exact', 'at-least' or 'at-most'
          enable_regex:  Flag to enable regex comparison
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """

        log_response_message("verifying attributes and child elements of '%s'. Match=%s" %(xpath_string, match))
        element = self.get_element(xpath_string)        
        if (element is None):
            log_response_result("Not Ok")
            response_fail("Did not receive any %s" %(xpath_string))
            return False
            
        for i in range(len(element)):
            log_response_message("verifying instance %d" %(i+1))
            attrib_childelement_list = self.build_attribute_and_child_elements_list(element[i]) 
            
            copy_list = attrib_childelement_list[:]
            for expected_value in expected_list:
                processed_value_string = wtl.utils.process_string(str(expected_value))
                log_response_action("  verifying '%s' was received" %(processed_value_string))
                found = False
                for value_str in copy_list[:]:                  
                    if (wtl.utils.compare_strings(processed_value_string, value_str, enable_regex)):
                        log_response_result("Received")
                        found = True
                        copy_list.remove(value_str) 
                        break
                if (not found):
                    log_response_result("Not received")
                    if (match != 'at-most'):
                        # The value must be there
                        log_response_message("Expected: %s not received in node instance %d" % (processed_value_string, i+1))
                        response_fail("Missing attribute or child element expected")
                        return False

            log_response_action("verifying if there are additional values received")
            if (len(copy_list) == 0):
                log_response_result("No additional received")
            else:
                log_response_result("Additional received")
                if (match != 'at-least'):                
                    log_response_message("Expected: %s" %(str(expected_list)))
                    log_response_message("Received: %s" %(attrib_childelement_list))
                    response_fail("Received additonal attribute or child element not expected")
          
    def check_only_included(self,elements):
        """
		Check the stored value contains only the provided element[attribute] list
       
        Parameters:
          elements: The element[attribute] list to match against
                    Elements set in form [ 'elm[attr]', 'elm[attr]' ]
                    Example: ['trajectorys', 'trajectorys[version]','trajectory', 'trajectory[uidWell]' , 'trajectory[uidWellbore]', 'trajectory[uid]','nameWell', 'nameWellbore', 'name' ]
        
        Return:
          Nothing. Fail control primitive is called if check fails

        """
        log_response_action("verifying that only items are included in XML " + str(elements) + " ...");
        available = self.build_elements_list();
        for element_iter in elements:
            found = False;
            for available_iter in available:
                if (available_iter == element_iter):
                    found = True;
                    available.remove(available_iter);
                    break;
            if (not found):
                log_response_result("Not Ok")
                log_response_message("Expected item : '" + element_iter + "' is not found in XML") ;
                response_fail("Received unexpected element/attribute")
        if (len(available) == 0):
            log_response_result("OK");
            return True
        else:
            log_response_result("Not Ok")
            log_response_message("Did not receive the following: " + str(available));
            response_fail("Wrong number of elements/attributes received")
            
    def check_valid_witsml_versions(self, version_str):
        """
        Check that string consists of WITSML versions in order from oldest to newest
        Does basic checking on WITSML version string, but does not validate string against actual 
          versions of the specification (i.e. does not check for 1.3.1, 1.4.1.1 explicitly)
             
        Parameters:
          version_str: String of version numbers being validated
        
        Return:
          Nothing. Fail control primitive is called if check fails
        """
        
        version_list = version_str.split(',')
        
        # check for empty version string
        if len(version_list) == 0:
            response_fail("Empty version string")
            return False
        
        #check for illegal spacing in string
        for version_iter in version_list:
            if (version_iter.strip() != version_iter):
                response_fail("Version string contains illegal space")
                return False
        
        # make copy of version list
        sorted_version_list = list(version_list)
        
        try:
            # sort version list 
            sorted_version_list.sort(key = lambda s: map(int,s.split('.')))
            
            # if list of 1, and sort was okay the formatting is okay
            if len(version_list) == 1:
                return True
            
            # check if list order remains unchanged (then it is in order)
            if sorted_version_list[:-1] == version_list[:-1]:
                return True
            
        except ValueError:
            response_fail("Invalid version formatting contained in list: " + version_str)
            return False
        
        # handle fall through, valid formatting, but out of order
        response_fail("Invalid version formatting contained in list: " + version_str)
        return False   

    def check_valid_write_schema(self):        
        """
        Check that the object specified validates against the specified version's write schema.
             
        Return:
          True if object validates against write schema version
          False if object does not validate against write schema version. Fail control primitive is called if check fails
        """
        processed_version_string = self.get_version()
        processed_object_string =  self.get_object_name()
        
        document = self.get_original_value()
        if (wtl.config.WITSML_files_directory == ''):
            files_path = sys.modules['wsvt'].__path__[0]
        else:
            files_path = wtl.config.WITSML_files_directory
        validator = WITSMLSchemaValidator(os.path.join(files_path,'schemas'))
        is_valid, message =  validator.validateXMLAgainstWriteSchema(processed_version_string, processed_object_string, document)
        
        if (is_valid):
            return True
        else:
            response_fail(message)
            return False
                