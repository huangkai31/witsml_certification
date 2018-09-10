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

# Application imports
import wtl.config as config
import wtl.testlog as testlog
import wtl.response as response
import wtl.control_prim as control_prim 
import wtl.store_prim as store_prim
import wtl.time_prim as time_prim
import wtl.script as script 
import wtl.utils as utils
import wtl.results as results
import wtl.globals
import unitDict.unitDictUtility as unitDictUtility 

exec("import %s" %(config.server_file_name))
    

###############################################################################
#                                                                             #
#                                WTL INITIALIZATION                           #
#                                                                             #
###############################################################################

def wtl_init():
    # Start logging
    testlog.init()

    # Initialize the STORE interface 
    store_prim.WITSMLServer.init()
    
    # Initialize the script execution
    script.Script.init()
    
wtl_init()


###############################################################################
#                                                                             #
#                                CONSTANT DEFINITIONS                         #
#                                                                             #
###############################################################################


# Key Return Values
# See WITSML STORE Application Program Interface (API) v1.4.1 - Appendix A
RETURNVALUE_FUNCTION_COMPLETED_SUCCESSFULLY    = 1 
RETURNVALUE_PARTIAL_SUCCESS                    = 2


# Default values for object selection query
# See WITSML STORE Application Program Interface (API) v1.4.1 - Appendix B 
DEF_Boolen                                = '0'
DEF_string                                = 'abc'
DEF_date                                  = '1900-01-01'
DEF_dateTime                              = '1900-01-01T00:00:00.000Z'
DEF_timeZone                              = 'Z'
DEF_number                                = '1'
DEF_calendarYear                          = '1000'
DEF_iadcBearingWearCode                   = 'E'
DEF_geodeticZoneString                    = '60N'
DEF_sectionNumber                         = '36'
DEF_publicLandSurveySystemQuarterTownship = 'NE'
DEF_publicLandSurveySystemQuarterSection  = 'NE'


# WMLtypeIn
# See WITSML STORE Application Program Interface (API) v1.4.1 - Appendix C
WMLTYPEIN_ATTACHMENT = 'attachment'
WMLTYPEIN_BHARUN = 'bhaRun'
WMLTYPEIN_CEMENTJOB = 'cementJob'
WMLTYPEIN_CHANGELOG = 'changeLog'
WMLTYPEIN_CONVCORE = 'convCore'
WMLTYPEIN_COORDINATEREFERENCESYSTEM = 'coordinateReferenceSystem'
WMLTYPEIN_DRILLREPORT = 'drillReport'
WMLTYPEIN_FLUIDSREPORT = 'fluidsReport'
WMLTYPEIN_FORMATIONMARKER = 'formationMarker'
WMLTYPEIN_LOG = 'log'
WMLTYPEIN_MESSAGE = 'message'
WMLTYPEIN_MUDLOG = 'mudLog'
WMLTYPEIN_OBJECTGROUP = 'objectGroup'
WMLTYPEIN_OPSREPORT = 'opsReport'
WMLTYPEIN_RIG = 'rig'
WMLTYPEIN_RISK = 'risk'
WMLTYPEIN_SIDEWALLCORE = 'sidewallCore'
WMLTYPEIN_STIMJOB = 'stimJob'
WMLTYPEIN_SURVEYPROGRAM = 'surveyProgram'
WMLTYPEIN_TARGET = 'target'
WMLTYPEIN_TOOLERRORMODEL = 'toolErrorModel'
WMLTYPEIN_TOOLERRORTERSET = 'toolErrorTermSet'
WMLTYPEIN_TRAJECTORY = 'trajectory'
WMLTYPEIN_TUBULAR = 'tubular'
WMLTYPEIN_WBGEOMETRY = 'wbGeometry'
WMLTYPEIN_WELL = 'well'
WMLTYPEIN_WELLBORE = 'wellbore'


# Test Script result codes
NONE = script.SCRIPT_RESULT_NONE
PASS = script.SCRIPT_RESULT_PASS 
FAIL = script.SCRIPT_RESULT_FAIL
INCONCLUSIVE = script.SCRIPT_RESULT_INCONCLUSIVE

# Capabilities
CAP_name = wtl.capability.CAP_name 
CAP_vendor = wtl.capability.CAP_vendor
CAP_version = wtl.capability.CAP_version
CAP_changeDetectionPeriod = wtl.capability.CAP_changeDetectionPeriod
CAP_cascadedDelete = wtl.capability.CAP_cascadedDelete
CAP_compressionMethod = wtl.capability.CAP_compressionMethod
CAP_GET_LOG_maxDataNodes = wtl.capability.CAP_GET_LOG_maxDataNodes
CAP_ADD_LOG_maxDataNodes = wtl.capability.CAP_ADD_LOG_maxDataNodes
CAP_UPDATE_LOG_maxDataNodes = wtl.capability.CAP_UPDATE_LOG_maxDataNodes
CAP_GET_TRAJECTORY_maxDataNodes = wtl.capability.CAP_GET_TRAJECTORY_maxDataNodes
CAP_ADD_TRAJECTORY_maxDataNodes = wtl.capability.CAP_ADD_TRAJECTORY_maxDataNodes
CAP_UPDATE_TRAJECTORY_maxDataNodes = wtl.capability.CAP_UPDATE_TRAJECTORY_maxDataNodes
CAP_GET_LOG_maxDataPoints = wtl.capability.CAP_GET_LOG_maxDataPoints
CAP_ADD_LOG_maxDataPoints = wtl.capability.CAP_ADD_LOG_maxDataPoints
CAP_UPDATE_LOG_maxDataPoints = wtl.capability.CAP_UPDATE_LOG_maxDataPoints
CAP_GET_TRAJECTORY_maxDataPoints = wtl.capability.CAP_GET_TRAJECTORY_maxDataPoints
CAP_ADD_TRAJECTORY_maxDataPoints = wtl.capability.CAP_ADD_TRAJECTORY_maxDataPoints
CAP_UPDATE_TRAJECTORY_maxDataPoints = wtl.capability.CAP_UPDATE_TRAJECTORY_maxDataPoints
CAP_LOG_growingTimeoutPeriod = wtl.capability.CAP_LOG_growingTimeoutPeriod 
CAP_TRAJECTORY_growingTimeoutPeriod = wtl.capability.CAP_TRAJECTORY_growingTimeoutPeriod
CAP_MUDLOG_growingTimeoutPeriod = wtl.capability.CAP_MUDLOG_growingTimeoutPeriod
CAP_OBJECTGROUP_growingTimeoutPeriod = wtl.capability.CAP_OBJECTGROUP_growingTimeoutPeriod

###############################################################################
#                                                                             #
#                                   TEST PRIMITIVES                           #
#                                                                             #
###############################################################################



##################################
#                                #
#  Test Definition Primitives    #
#                                #
##################################

def test(purpose, reference, reference_text, functionality_required = [] , data_schemas=[], parameters=[]):
    global script
    global utils    

    current_script = script.Script.get_current_script()

    if (current_script == script.Script.get_initial_script()):
        # Test Script run independently, not from a 'run' command
        testlog.wtl_log("! SCRIPT '%s' started\n" %(os.path.splitext(os.path.basename(sys.argv[0]))[0]), force=True)
        # Get parameters
        for arg in sys.argv[1:]:
            param = arg.split('=')
            if ((len(param) == 2) and param[1]):
                variable = param[0]
                if ((param[1][0] == '$') and (param[1][-1] == '$')):
                    value = value = utils.get_variable_value(param[1][1:-1])
                else:            
                    value = param[1]
                current_script.set_variable(variable, value)
                
    # set script information            
    current_script.set_info(purpose, reference, reference_text, parameters, functionality_required, data_schemas)

    # check if script's requirements are met
    if (not current_script.areMinimumRequirementsMet()):
        current_script.skip(current_script.getRequirementsMetString());

def test_suite(description):
    global script
    global utils

    testlog.wtl_log("\nTEST SUITE started: ~~~~~%s~~~~~\n" %(description), force=True)



#############################
#                           #
#  WITSML Store Primitives  #
#                           #
#############################

WMLS_AddToStore = store_prim.WITSMLServer.add_to_store
WMLS_DeleteFromStore = store_prim.WITSMLServer.delete_from_store
WMLS_GetBaseMsg = store_prim.WITSMLServer.get_base_msg
WMLS_GetCap = store_prim.WITSMLServer.get_cap
WMLS_GetFromStore = store_prim.WITSMLServer.get_from_store
WMLS_GetVersion = store_prim.WITSMLServer.get_version
WMLS_UpdateInStore = store_prim.WITSMLServer.update_in_store


#######################
#                     #
#  Verify Primitives  #
#                     #
#######################

check_ReturnValue_Success = store_prim.WITSMLServer.result.check_success
check_ReturnValue_Failure = store_prim.WITSMLServer.result.check_failure
check_ReturnValue_Value = store_prim.WITSMLServer.result.check_value
check_ReturnValue_String = store_prim.WITSMLServer.result.check_string
check_ReturnValue_Contains = store_prim.WITSMLServer.result.check_value_contains

check_SuppMsgOut_Contains = store_prim.WITSMLServer.supp_msg_out.check_value_contains

check_CapabilitiesOut_String = store_prim.WITSMLServer.capabilities_out.check_string
check_CapabilitiesOut_XMLString = store_prim.WITSMLServer.capabilities_out.check_xml_string
check_CapabilitiesOut_ElementIncluded = store_prim.WITSMLServer.capabilities_out.check_element_included
check_CapabilitiesOut_ElementNotIncluded = store_prim.WITSMLServer.capabilities_out.check_element_not_included
check_CapabilitiesOut_ElementValue = store_prim.WITSMLServer.capabilities_out.check_element_value
check_CapabilitiesOut_ElementValue_Greaterthan = store_prim.WITSMLServer.capabilities_out.check_element_value_greaterthan
check_CapabilitiesOut_ElementValue_Lessthan = store_prim.WITSMLServer.capabilities_out.check_element_value_lessthan
check_CapabilitiesOut_RecurringElementValue = store_prim.WITSMLServer.capabilities_out.check_recurring_element_value
check_CapabilitiesOut_RecurringElementValueContains = store_prim.WITSMLServer.capabilities_out.check_recurring_element_value_contains
check_CapabilitiesOut_ElementValueContains = store_prim.WITSMLServer.capabilities_out.check_element_value_contains
check_CapabilitiesOut_AttributeIncluded = store_prim.WITSMLServer.capabilities_out.check_attribute_included
check_CapabilitiesOut_AttributeNotIncluded = store_prim.WITSMLServer.capabilities_out.check_attribute_not_included
check_CapabilitiesOut_AttributeValue = store_prim.WITSMLServer.capabilities_out.check_attribute_value
check_CapabilitiesOut_AttributeValueIsContained = store_prim.WITSMLServer.capabilities_out.check_attribute_value_is_contained

check_XMLout_String = store_prim.WITSMLServer.xml_out.check_string
check_XMLout_DoesNotContain = store_prim.WITSMLServer.xml_out.check_string_does_not_contain
check_XMLout_XMLString = store_prim.WITSMLServer.xml_out.check_xml_string
check_XMLout_XMLNormalizedString = store_prim.WITSMLServer.xml_out.check_xml_normalized_string
check_XMLout_ElementIncluded = store_prim.WITSMLServer.xml_out.check_element_included
check_XMLout_ElementNotIncluded = store_prim.WITSMLServer.xml_out.check_element_not_included
check_XMLout_ElementValue = store_prim.WITSMLServer.xml_out.check_element_value
check_XMLout_ElementValue_Greaterthan = store_prim.WITSMLServer.xml_out.check_element_value_greaterthan
check_XMLout_ElementValue_Lessthan = store_prim.WITSMLServer.xml_out.check_element_value_lessthan
check_XMLout_RecurringElementValue = store_prim.WITSMLServer.xml_out.check_recurring_element_value
check_XMLout_RecurringElementValueContains = store_prim.WITSMLServer.xml_out.check_recurring_element_value_contains
check_XMLout_ElementValueContains = store_prim.WITSMLServer.xml_out.check_element_value_contains
check_XMLout_AttributeIncluded = store_prim.WITSMLServer.xml_out.check_attribute_included
check_XMLout_AttributeNotIncluded = store_prim.WITSMLServer.xml_out.check_attribute_not_included
check_XMLout_AttributeValue = store_prim.WITSMLServer.xml_out.check_attribute_value
check_XMLout_AttributeValueIsContained = store_prim.WITSMLServer.xml_out.check_attribute_value_is_contained
check_XMLout_NumberOfObjects = store_prim.WITSMLServer.xml_out.check_number_of_objects
check_XMLout_NumberOfObjects_Greaterthan = store_prim.WITSMLServer.xml_out.check_number_of_objects_greaterthan
check_XMLout_NumberOfObjects_Lessthan = store_prim.WITSMLServer.xml_out.check_number_of_objects_lessthan
check_XMLout_OnlyIncluded = store_prim.WITSMLServer.xml_out.check_only_included
check_XMLout_ValidWriteSchema = store_prim.WITSMLServer.xml_out.check_valid_write_schema
check_XMLout_ElementAttributesAndChildren = store_prim.WITSMLServer.xml_out.check_element_attribute_and_children_list

check_Version = store_prim.WITSMLServer.xml_out.check_valid_witsml_versions

check_logData_IndexValue = store_prim.WITSMLServer.xml_out.check_log_data_index_value
check_logData_DataValue = store_prim.WITSMLServer.xml_out.check_log_data_data_value
check_logData_AllData = store_prim.WITSMLServer.xml_out.check_log_data_all
check_logData_NumberOfNodes = store_prim.WITSMLServer.xml_out.check_log_data_number_of_nodes
check_logData_NumberOfPoints = store_prim.WITSMLServer.xml_out.check_log_data_number_of_points

check_ElapseTimeInSeconds_Lessthan = store_prim.WITSMLServer.elapse_time_in_seconds.check_value_less_than
#######################
#                     #
#  Parse Primitives   #
#                     #
#######################
get_ReturnValue = store_prim.WITSMLServer.result.get

get_SuppMsgOut_String = store_prim.WITSMLServer.supp_msg_out.get
get_SuppMsgOut_uid_String = store_prim.WITSMLServer.supp_msg_out.get_first_word

get_CapabilitiesOut_Element_String = store_prim.WITSMLServer.capabilities_out.get_element_text_value
get_CapabilitiesOut_RecurringElement_List = store_prim.WITSMLServer.capabilities_out.get_recurring_element_list
get_CapabilitiesOut_RecurringElementViaKey_List = store_prim.WITSMLServer.capabilities_out.get_recurring_element_list_via_key

get_XMLout_Element_String = store_prim.WITSMLServer.xml_out.get_element_text_value
get_XMLout_Attribute_String = store_prim.WITSMLServer.xml_out.get_attribute
get_XMLout_RecurringElement_List = store_prim.WITSMLServer.xml_out.get_recurring_element_list
get_XMLout_RecurringElementViaKey_List = store_prim.WITSMLServer.xml_out.get_recurring_element_list_via_key
get_XMLout_NumberOfObjects_Int = store_prim.WITSMLServer.xml_out.get_number_of_objects
get_XMLout_Mnemonics_List = store_prim.WITSMLServer.xml_out.get_mnemonics_list
get_XMLout_Units_List = store_prim.WITSMLServer.xml_out.get_units_list
get_XMLout_LatestdTimChange_String = store_prim.WITSMLServer.xml_out.get_latest_dTimChange

get_logData_IndexValue_String = store_prim.WITSMLServer.xml_out.get_log_data_index_value
get_logData_DataValue_String = store_prim.WITSMLServer.xml_out.get_log_data_data_value
get_logData_NumberOfNodes_Int = store_prim.WITSMLServer.xml_out.get_log_data_number_of_nodes
get_logData_NumberOfPoints_Int = store_prim.WITSMLServer.xml_out.get_log_data_number_of_points

get_ElapseTimeInSeconds_float = store_prim.WITSMLServer.elapse_time_in_seconds.get

#############################
#                           #
#  Capabilities Primitives  #
#                           #
#############################

get_capability = wtl.globals.get_capability
is_function_supported_for_object = wtl.globals.is_function_object_supported

#####################
#                   #
#  Time Primitives  #
#                   #
#####################

now = time_prim.get_current_datetime_string

check_timestamp_Equals = time_prim.check_timestamp_equals
check_timestamp_Lessthan = time_prim.check_timestamp_lessthan
check_timestamp_LessthanEquals = time_prim.check_timestamp_lessthan_equalto
check_timestamp_Greaterthan = time_prim.check_timestamp_greaterthan      
check_timestamp_GreaterthanEquals = time_prim.check_timestamp_greaterthan_equalto

timestamp_add_seconds = time_prim.add_seconds_to_timestamp
timestamp_subtract_seconds = time_prim.subtract_seconds_to_timestamp

#####################
#                   #
#  log verify  #
#                   #
#####################


log_verify_check_log_header_and_data = store_prim.WITSMLServer.log_verify_object.test_full_log
log_verify_check_log_header_only = store_prim.WITSMLServer.log_verify_object.test_header_only_log
log_verify_check_requestLatestValue_header_and_data = store_prim.WITSMLServer.log_verify_object.test_requestLatestValues_full_log
log_verify_check_requestLatestValue_header_and_data_max = store_prim.WITSMLServer.log_verify_object.test_requestLatestValues_full_log_max
log_verify_check_data_only = store_prim.WITSMLServer.log_verify_object.test_dataOnly_log
log_verify_check_data_only_extended = store_prim.WITSMLServer.log_verify_object.test_dataOnly_log_extended
log_verify_get_curve_info_dictionary = store_prim.WITSMLServer.log_verify_object.get_CurveInfo_Dictionary

####################
#                   #
#  unit Dictionary  #
#                   #
#####################


convert_units = unitDictUtility.convert_to_unit


##################################
#                                #
#  Execution Control Primitives  #
#                                #
##################################

# Execution Control Primitives: Test Script 
fail = control_prim.fail
partial_success = control_prim.partial_success
success = control_prim.success
stop = control_prim.stop
error = control_prim.error
run_script = control_prim.run_script
pause = control_prim.pause
pause_for_changeDetectionPeriod = control_prim.pause_changeDetectionPeriod
pause_for_growingTimeoutPeriod = control_prim.pause_growingTimeoutPeriod


# Execution Control Primitives: Test Suite 
run = control_prim.run
get_last_test_result = control_prim.get_last_test_result
end = control_prim.end
produce_and_reset_results = results.produce_and_reset_results

#######################
#                     #
#  Misc Primitives    #
#                     #
#######################

set = utils.set_variable_value
get = utils.get_variable_value
logging_on = testlog.logging_on
logging_off = testlog.logging_off
log = testlog.log
log_variable = utils.log_variable_value

def log_server_info():
    testlog.wtl_log(results.get_server_info_string())
new_object_created = utils.new_object  

start_session = store_prim.WITSMLServer.start_server_session
