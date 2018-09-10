#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify that Server returns all data-nodes when no structural-range value is specified.",
     reference =  "6.6.4.3 Special Handling for Growing Data-objects",
     reference_text = "Determining Selected-nodes: If a client does not specify a structural-range value, then the server MUST include all data-nodes as selected-nodes.",
     functionality_required =   ["WMLS_GetFromStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed for this test.')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

# Use Standard Query #10 (Get Header for one Growing Data-object) for the depth-log
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                      <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <log uidWell="$server_w2_uid$" uidWellbore="$server_w2_wb1_uid$" uid="$server_w2_wb1_log1_uid$">                         
                                        </log>
                                      </logs>
                                  """,
                                  OptionsIn={'returnElements':'header-only'})  
check_ReturnValue_Success()
check_XMLout_ElementIncluded('startIndex')
check_XMLout_ElementIncluded('endIndex')

# store first query's start and end index
set('first_startIndex', get_XMLout_Element_String('startIndex'))
log_variable('first_startIndex')
set('first_endIndex', get_XMLout_Element_String('endIndex'))
log_variable('first_endIndex')

# Use Standard Query #15 (Get Log) for request
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                      <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <log uidWell="$server_w2_uid$" uidWellbore="$server_w2_wb1_uid$" uid="$server_w2_wb1_log1_uid$">                         
                                        </log>
                                      </logs>
                                  """,
                                  OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()
check_XMLout_ElementIncluded('startIndex')
check_XMLout_ElementIncluded('endIndex')

# compare first and second query's indexes
check_XMLout_ElementValue('startIndex', get('first_startIndex'))
check_XMLout_ElementValue('endIndex', get('first_endIndex'))
partial_success('SQ-010 and SQ-015 indexes match')

# compare index values in the data with the startIndex and endIndex elements
check_logData_IndexValue(0,get('first_startIndex'))
check_logData_IndexValue(get_logData_NumberOfNodes_Int()-1,get('first_endIndex'))
partial_success('SQ-015 logData indexes are consistent with startIndex and endIndex')


log('Script procedure end')
success()
