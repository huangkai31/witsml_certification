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
import traceback
from lxml import etree
from lxml import objectify

# Application imports
import wtl.globals

#******************************************************************************
#
# Capabilities
#
CAP_name = 'name' 
CAP_vendor = 'vendor'
CAP_version = 'version'
CAP_changeDetectionPeriod = 'changeDetectionPeriod'
CAP_cascadedDelete = 'cascadedDelete'
CAP_compressionMethod = 'compressionMethod'
CAP_GET_LOG_maxDataNodes = 'WMLS_GetFromStore:log:maxDataNodes'
CAP_ADD_LOG_maxDataNodes = 'WMLS_AddToStore:log:maxDataNodes'
CAP_UPDATE_LOG_maxDataNodes = 'WMLS_UpdateInStore:log:maxDataNodes'
CAP_GET_TRAJECTORY_maxDataNodes = 'WMLS_GetFromStore:trajectory:maxDataNodes'
CAP_ADD_TRAJECTORY_maxDataNodes = 'WMLS_AddToStore:trajectory:maxDataNodes'
CAP_UPDATE_TRAJECTORY_maxDataNodes = 'WMLS_UpdateInStore:trajectory:maxDataNodes'
CAP_GET_LOG_maxDataPoints = 'WMLS_GetFromStore:log:maxDataPoints'
CAP_ADD_LOG_maxDataPoints = 'WMLS_AddToStore:log:maxDataPoints'
CAP_UPDATE_LOG_maxDataPoints = 'WMLS_UpdateInStore:log:maxDataPoints'
CAP_GET_TRAJECTORY_maxDataPoints = 'WMLS_GetFromStore:trajectory:maxDataPoints'
CAP_ADD_TRAJECTORY_maxDataPoints = 'WMLS_AddToStore:trajectory:maxDataPoints'
CAP_UPDATE_TRAJECTORY_maxDataPoints = 'WMLS_UpdateInStore:trajectory:maxDataPoints'
CAP_LOG_growingTimeoutPeriod = 'log-growingTimeoutPeriod'
CAP_TRAJECTORY_growingTimeoutPeriod = 'trajectory-growingTimeoutPeriod'
CAP_MUDLOG_growingTimeoutPeriod = 'mudLog-growingTimeoutPeriod'
CAP_OBJECTGROUP_growingTimeoutPeriod = 'objectGroup-growingTimeoutPeriod'

CAP_EQUALITY_SEPARATORS = ['=','<','>']      

#******************************************************************************
#
# WITSML Capabilities Structure
#
class WITSMLStoreCapabilities:
    
    def __init__(self, schema_version_str, capabilities_xml_str):
        """
        Parse the server capabilities and save them.
        Capabilities are saved in global variables so they can be accesses by variable constructs in the code
        """
        self.schema_version = schema_version_str;
        self.tree = None;
        ###
        try:
            self.tree = objectify.fromstring(capabilities_xml_str) 
        except:
            # Failed to parse XML Capabilities: Capabilities is not a well-formed XML 
            etype, value, tb = sys.exc_info();
            error = ''.join(traceback.format_exception(etype, value, tb, 10));
            return;
        ###
        try:
            if ( 'schemaVersion' in self.tree.capServer[0].__dict__):
                if (self.tree.capServer[0].schemaVersion != self.schema_version):
                    # Bad schemaVersion in server capabilities object
                    return;
                 
            """ Getting generic info from capabilities """
            for element in [CAP_name, CAP_vendor, CAP_version, CAP_changeDetectionPeriod, CAP_cascadedDelete, CAP_compressionMethod]:
                if (element in self.tree.capServer[0].__dict__):
                    wtl.globals.set_capability(element, self.tree.capServer[0][element])

            """ Updating server functionality list from  """
            for cap_iter in self.tree.capServer:
                """ Iterating over capServer nodes """ 

                """ Getting growingTimeoutPeriod information """
                if 'growingTimeoutPeriod' in cap_iter.__dict__:
                    for growing_iter in cap_iter.growingTimeoutPeriod:
                        """ Iterating over growingTimeoutPeriod=n nodes """ 
                        wtl.globals.set_growingTimeoutPeriod(growing_iter.attrib["dataObject"], int(growing_iter.text.strip()))

                """ Getting function support information """
                if 'function' in cap_iter.__dict__:
                    for func_iter in cap_iter.function:
                        """ Iterating over function nodes """ 
                        if 'dataObject' in func_iter.__dict__:
                            for dataObject_iter in func_iter.dataObject:
                                """ Iterating over dataObject nodes to get objects that are supported by this functionality """
                                wtl.globals.set_function_object_supported(func_iter.attrib["name"], dataObject_iter.text.strip())
                                if ('maxDataNodes' in dataObject_iter.attrib.keys()):
                                    wtl.globals.set_maxDataNodes(func_iter.attrib["name"],
                                                                  dataObject_iter.text.strip(),
                                                                  dataObject_iter.attrib['maxDataNodes'])
                                if ('maxDataPoints' in dataObject_iter.attrib.keys()):
                                    wtl.globals.set_maxDataPoints(func_iter.attrib["name"],
                                                                  dataObject_iter.text.strip(),
                                                                  dataObject_iter.attrib['maxDataPoints'])
        except:
            # Failed to parse XML Capabilities
            etype, value, tb = sys.exc_info();
            error = ''.join(traceback.format_exception(etype, value, tb, 10));
        
    def isSatisfyFollowingRequrements(self, required_item):
         """
          This method is checking if server capabilities satisfy required functionality
         """
         
         # check through equality separators to determine if capabilities satisfies the requirements
         for separator in CAP_EQUALITY_SEPARATORS:
             
             if required_item.find(separator) != -1:
                 requires_item_split = required_item.split(separator)
                 
                 # check invalid number of separators
                 if (len(requires_item_split) != 2):
                     return False
                 
                 else:
                     lhs = wtl.globals.get_capability(requires_item_split[0])
                     
                     # equality case
                     if (separator == '='):
                         
                         # if no lhs, test does not meet criteria
                         if (lhs is None):
                             return False
                         
                         lhs = str(lhs)
                         rhs = str(requires_item_split[1])
                         return (lhs == rhs)
                         
                     # handle > case    
                     elif(separator == ">"):
                         
                         # if no LHS and we are testing for >, assume that this is satisfied 
                         # i.e. this is true for maxDataNodes and maxDataPoints
                         if (lhs is None):
                             return True
                         
                         lhs = int(lhs)
                         rhs = int(requires_item_split[1])
                         return (lhs > rhs)
                     
                      # handle < case    
                     else:
                         
                        # if no lhs, test does not meet criteria
                         if (lhs is None):
                             return False
                         
                         lhs = int(lhs)
                         rhs = int(requires_item_split[1])
                         return (lhs < rhs)
                             
         # check globals if required item does not contain a separator 
         if (wtl.globals.get_capability(required_item)):
             return(True)
        
         # otherwise return false
         return(False)
         
     
    def __str__(self):
         """
         This method generates a readable version of the server capabilities
         """
         capabilities = "Server capabilities for schema version %s:\n\n" %(self.schema_version)
         if (self.tree is not None):
              capabilities += etree.tostring(self.tree, pretty_print=True)
         capabilities += "\n\n"
         
         return capabilities         
