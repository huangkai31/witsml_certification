#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server supports 1.4.1.x in the WMLS_GetVersion function.",
     reference =  "4.2.3",
     reference_text = "To determine which Data Schema Versions (and therefore which API Versions) that the server supports, a client should use the WMLS_GetVersion function (page 47). After the client receives the server response, the client MUST [else error -467] then pass an API Version that the server supports.",
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed for this test.')

#############
# TEST BODY #
#############


# Call WMLS_GetVersion.
WMLS_GetVersion()

# Check that "1.4.1.x" exists in the returned string (where x is a number from 0-9)
check_ReturnValue_String('.*1\.4\.1\.[0-9].*', enable_regex=True)

partial_success("'1.4.1.x' exists in the returned string")
success()

