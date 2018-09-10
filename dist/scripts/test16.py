#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server returns the 1.4.1.x data schema version in the plural data object",
     reference =  "4.1.1.1",
     reference_text = "The server MUST return the version attribute in the plural object defining the Data Schema Version",
     functionality_required =   ["WMLS_GetFromStore:well"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

# No setup required

#############
# TEST BODY #
#############

#Well query
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid='$server_w1_uid$'/>                         
                                     </wells>
                                  """,
                                  OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()

# Verify that server returns the same data schema version in plural object as the one received in the request
check_XMLout_AttributeValue('wells','version', "$server_schema_version$")
partial_success("Received correct Schema Version")

success()
