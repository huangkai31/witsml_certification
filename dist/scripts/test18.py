#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server constrains GetFromStore requests according to maxReturnNodes",
     reference =  "6.6.2.1  WMLS_GetFromStore - OptionsIn Keywords",
     reference_text = "maxReturnNodes:  A server that declares support for a growing data-object MUST support this option.",
     functionality_required = ["WMLS_GetFromStore:log",
                               "WMLS_GetFromStore:log:maxDataNodes>4"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
     )

#########
# SETUP #
#########

log('No Setup Required')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

#Use SQ-015 (Get Log) 3 times, using all curves and OptionsIn set to:
#1) maxReturnNodes = 1 
#Check server returns 1 row of data

WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns="http://www.witsml.org/schemas/1series" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="$server_schema_version$">
                           <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_log1_uid$">
                           </log>
                     </logs>"""
                  ,OptionsIn={'returnElements':'all','maxReturnNodes':'1'})
check_ReturnValue_Success()
check_logData_NumberOfNodes(1)

#2) maxReturnNodes = 3 
#Check server returns 3 rows of data

WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns="http://www.witsml.org/schemas/1series" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="$server_schema_version$">
                           <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_log1_uid$">
                           </log>
                     </logs>"""
                  ,OptionsIn={'returnElements':'all','maxReturnNodes':'3'})
check_ReturnValue_Success()
check_logData_NumberOfNodes(3)

#3) maxReturnNodes = 5 
#Check server returns 5 rows of data

WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns="http://www.witsml.org/schemas/1series" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="$server_schema_version$">
                           <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_log1_uid$">
                           </log>
                     </logs>"""
                  ,OptionsIn={'returnElements':'all','maxReturnNodes':'5'})
check_ReturnValue_Success()
check_logData_NumberOfNodes(5)

partial_success("Server constrains GetFromStore requests according to maxReturnNodes")
log('Script procedure end')
success()
