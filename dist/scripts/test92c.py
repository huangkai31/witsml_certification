#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the Server supports SQ-012 (Get Data for Growing Data-object) for Log",
     reference =  "6.6.7 Standard Query Templates",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required = ["WMLS_GetFromStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed for this test.')

#############
# TEST BODY #
#############

log('Script procedure start')

# Use SQ-012 (Get Data for Growing Data-object) for the Log. OptionsIn='returnElements=data-only'
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                    <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$"
                                                  uid="$server_w1_wb1_log1_uid$"/>
                                    </logs>""",
                                 OptionsIn={'returnElements':'data-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)     

# The query returns the log with  one logData elements and no header.
check_XMLout_ElementAttributesAndChildren('log',
                                          ['log[uidWell]', 'log[uidWellbore]', 'log[uid]', 'logData'],
                                          match='at-most')
partial_success("Only logData is included in each log")

# Each logData contains mnemonicList unitList and data
check_XMLout_ElementAttributesAndChildren('logData',
                                          ['mnemonicList', 'unitList', 'data'],
                                          match='exact')
partial_success("Correct elements included for logData")


log('Script procedure end')

success();    


