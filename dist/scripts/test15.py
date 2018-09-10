#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the requestObjectSelectionCapability behaviour for the well object.",
     reference =  "6.6.2.1  WMLS_GetFromStore - OptionsIn Keywords",
     reference_text = "requestObjectSelectionCapability:  When a client specifies this option with a value other than 'none', A client MUST NOT [else error -427] specify another option and the QueryIn parameter MUST [else error -428] be empty. The server MUST return XMLout that conforms to the derived read schema, but the returned values will be meaningless",
     functionality_required = ["WMLS_GetFromStore:well"],
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

log('Script test procedure start')

# Use Minimum Query Template with OptionsIn parameter requestObjectSelection=true
WMLS_GetFromStore(WMLTYPEIN_WELL,"""<?xml version="1.0" encoding="utf-8"?>
                 <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                     <well />
                 </wells>""",OptionsIn={'requestObjectSelectionCapability':'true'})
check_ReturnValue_Success()

#XMLOut conforms to derived read shema.
#A single well object is returned.
#At a minimum the following attributes and elements are included in the response:
# -uid
# -name
# -numGovt 
# -numAPI
# -dTimLastChange
#The values returned are not empty.

check_XMLout_NumberOfObjects(1)
partial_success("Single well was returned")

check_XMLout_AttributeIncluded('well','uid') 
partial_success('uid returned')

check_XMLout_ElementIncluded('name')
partial_success('name returned')

check_XMLout_ElementIncluded('numGovt')
partial_success('numGovt returned')

check_XMLout_ElementIncluded('numAPI')
partial_success('numAPI returned')

check_XMLout_ElementIncluded('dTimLastChange')
partial_success('dTimLastChange returned')

partial_success("Minimum attributes and elements returned for requestObjectSelectionCapability met")
log('Script test procedure end')
success()
