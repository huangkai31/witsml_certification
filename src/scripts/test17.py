#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server returns the supported data schema versions in order from oldest to newest.",
     reference =  "4.2.3.1  capClient Attributes and Elements",
     reference_text = "schemaVersion Defines all of the Data Schema Version(s) (for definition, see Section 3.5.1, page 11) that the client supports. The values MUST [else error -473] match the version attribute used in the plural data-objects. The default is '1.4.1.0'. The value is a comma separated list of values without spaces. The client MUST [else error -404] order the list oldest to newest Data Schema Versions supported. This ordering is required so that newer Data Schema Versions will not confuse older servers.",
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

#Call GetVersion to retrieve the list of supported versions.
WMLS_GetVersion()

#Verify that a string is returned with a set of Schema Versions separated by commas ordered from oldest to newest. 
check_Version(get_ReturnValue()) 

partial_success("Data schema versions are returned in order from oldest to newest.")
log('Script procedure end')
success()
