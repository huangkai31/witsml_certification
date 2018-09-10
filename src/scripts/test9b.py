#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server adjusts header information to match the range of a selected subset of data for a time log.",
     reference =  "6.6.4.3 Special Handling for Growing Data-objects",
     reference_text = "The server MUST return requested header data that represents the range of selected-nodes in the results.",
     functionality_required =   ["WMLS_GetFromStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed for this test.')

#############
# TEST BODY #
#############

log('Script test procedure start')

#Use SQ-015 to retrieve the entire log (don't care about truncations)
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_log2_uid$">      
                                         </log>
                                     </logs>
                                  """,
                                  OptionsIn={'returnElements':'all'})    

check_ReturnValue_Success()

#confirm log's content is valid
log_verify_check_log_header_and_data()
partial_success("Server returned a log whose content is consistent")

# Set start and end indexes to smaller range than log 
# Pre-req states that there are a minimum of 4 rows of data
set('req_startIndex',get_logData_IndexValue_String(1))
set('req_endIndex', get_logData_IndexValue_String(2))

#Use SQ-015 with startIndex and endIndex specified
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                         <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                             <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_log2_uid$">
                                               <startDateTimeIndex>$req_startIndex$</startDateTimeIndex>
                                               <endDateTimeIndex>$req_endIndex$</endDateTimeIndex>                 
                                             </log>
                                         </logs>
                                  """,
                                  OptionsIn={'returnElements':'all'})    

check_ReturnValue_Success()

#confirm number of expected rows of data
check_logData_NumberOfNodes(2)

#confirm start/end indexes match request
check_timestamp_Equals(get_logData_IndexValue_String(0), get('req_startIndex'))
check_timestamp_Equals(get_logData_IndexValue_String(1), get('req_endIndex'))
partial_success("Server returned a subset of log data rows as expected.")    

#confirm log's content is valid
log_verify_check_log_header_and_data()
partial_success("Server returned a log whose content is consistent")

log('Script test procedure end')
success()

