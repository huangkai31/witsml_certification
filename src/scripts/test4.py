#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server supports WMLS_GetCap",
     reference =  "4.2.4.1  capServer Attributes and Elements",
     reference_text = "All WITSML servers MUST support WMLS_GetVersion and WMLS_GetCap function, so they need not be listed.",
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########
    
log('No setup is needed for this test.')

#############
# TEST BODY #
#############

# Call WMLS_GetCap with OptionsIn set to "dataVersion=1.4.1.x" (where x is a number from 0-9)
WMLS_GetCap(OptionsIn={'dataVersion':get('server_schema_version')})
check_ReturnValue_Success()

# Ensure the GetCap returns a capServer with the version attribute of "1.4.1"
check_CapabilitiesOut_AttributeValue('capServers','version','1.4.1')
check_CapabilitiesOut_ElementValue('schemaVersion','$server_schema_version$')
partial_success("correct version returned")

success()

