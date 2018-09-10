#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server sets maxRequestLatestValues correctly.",
     reference =  "4.2.4.1 capServer Attributes and Elements",
     reference_text = "Required. Minimum = 1",
     functionality_required = ["WMLS_GetFromStore:log"],
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

WMLS_GetCap(OptionsIn={'dataVersion':get('server_schema_version')})
check_ReturnValue_Success()

check_CapabilitiesOut_ElementIncluded("maxRequestLatestValues")
partial_success("maxRequestLatestValues is included in response.");

check_CapabilitiesOut_ElementValue_Greaterthan('maxRequestLatestValues', 0)
partial_success("maxRequestLatestValues is greater or equal to 1");

log('Script procedure end')

success();    


