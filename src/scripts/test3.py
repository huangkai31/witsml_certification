#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server supports apiVers 1.4.1",
     reference =  "4.2.4.1  capServer Attributes and Elements",
     reference_text = "apiVers Specifies the API Version that the server supports, which is associated with the Data Schema Version provided in the dataVersion element of the WMSL_GetCap Function. This API Version MUST match one of the API Versions associated with the API Schema Version used (For definitions and information about versions, see Section 3.5, page 11).",
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

# Ensure the apiVers = "1.4.1" in the returned CapabilitiesOut string
check_CapabilitiesOut_AttributeValue('capServer','apiVers','1.4.1')
partial_success("correct apiVers returned")

success()

