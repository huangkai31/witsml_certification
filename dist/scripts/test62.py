#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server defines a growingTimeoutPeriod for the log object",
     reference =  "4.2.4.1 capServer Attributes and Elements",
     reference_text = "growingTimeoutPeriod:  Defines the maximum number of seconds that a server will consider a growing data-object to be growing when no data is being appended to the object. A separate time is defined for each growing data-object type. If data is not appended within the specified time, the server sets the objectGrowing flag for the data-object to 'false'. A server MUST define a value for each supported growing data-object type.",
     data_schemas = ["1.4.1.0", "1.4.1.1"],
     functionality_required =   ['WMLS_GetFromStore:log'],
    )

#########
# SETUP #
#########
           
log('No setup is needed for this test.')
log('')

#############
# TEST BODY #
#############

log('Script start')

#Call GetCap
WMLS_GetCap(OptionsIn={'dataVersion':get('server_schema_version')})
check_ReturnValue_Success()

#Check the growingTimeoutPeriod is defined in the GetCap response for log
check_CapabilitiesOut_ElementIncluded("/capServers/capServer/growingTimeoutPeriod[@dataObject='log']")

partial_success("growingTimeoutPeriod is defined in the GetCap response for log")
log('Script end')
success()
