#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify that the server truncates data such that no data is returned outside of the truncation interval using maxDataNodes for a time log.",
     reference =  "6.6.4.3  Special Handling for Growing Data-objects",
     reference_text = "For a point index, a server MUST eliminate the data-nodes from the truncation-end such that no eliminated node will have a node-index that is at or within the range of a selected-node. ",
     functionality_required =   ["WMLS_GetFromStore:log",
                                 "WMLS_GetFromStore:log:maxDataNodes<100000000"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup required for this test.')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

# Use SQ-010 (Get Header for one Growing Data-object) for the log. 
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                      <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <log uidWell="$server_w3_uid$" uidWellbore="$server_w3_wb1_uid$" uid="$server_w3_wb1_log3_uid$">                       
                                        </log>
                                      </logs>
                                  """,
                                  OptionsIn={'returnElements':'header-only'})  
check_ReturnValue_Success()

# Save start and end indexes
set('start_index', get_XMLout_Element_String('startDateTimeIndex'))
set('end_index', get_XMLout_Element_String('endDateTimeIndex'))

# Use SQ-015 (Get Log) to obtain all data for the log.
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                      <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <log uidWell="$server_w3_uid$" uidWellbore="$server_w3_wb1_uid$" uid="$server_w3_wb1_log3_uid$">                       
                                        </log>
                                      </logs>
                                  """,
                                  OptionsIn={'returnElements':'all'})  
check_ReturnValue_Value(2)
partial_success('Return code +2 received')

ret_startIdx = get_XMLout_Element_String('startDateTimeIndex')
check_timestamp_Equals(ret_startIdx, get('start_index'))
partial_success('startDateTimeIndex matches in the two queries')

ret_endIdx = get_XMLout_Element_String('endDateTimeIndex')
check_timestamp_Lessthan(ret_endIdx, get('end_index'))
partial_success('endDateTimeIndex in second query is earlier than endDateIndex in first query')
                
if (get_capability(CAP_GET_LOG_maxDataNodes) < get_logData_NumberOfNodes_Int()):
    fail("Server returned more nodes than maxDataNodes")
partial_success("Server did not return more nodes than maxDataNodes")

partial_success('Server truncated data correctly')

log('Script procedure end')

success()
