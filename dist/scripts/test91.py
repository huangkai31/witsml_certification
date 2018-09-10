#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the Server returns the expected wellbore's details when receiving a SQ-006  ( Get Details for a Wellbore )",
     reference =  "6.6.7  Standard Query Templates",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required =   ["WMLS_GetFromStore:wellbore"],
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


# get the details of a wellbore for the chosen well, i.e. SQ-006
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0"?>
                                     <wellbores version="$server_schema_version$" xmlns="http://www.witsml.org/schemas/1series">
                                         <wellbore uidWell="$server_w1_uid$" uid="$server_w1_wb1_uid$">
                                         </wellbore>
                                     </wellbores>
                                  """, OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()


# should only receive one wellbore
check_XMLout_NumberOfObjects(1)  
check_XMLout_AttributeValue('wellbore', 'uidWell', '$server_w1_uid$')
check_XMLout_AttributeValue('wellbore', 'uid', '$server_w1_wb1_uid$')
partial_success("Correct wellbore was returned")

# verify the wellbore returned matches the wellbore write-schema
check_XMLout_ValidWriteSchema()
partial_success("Wellbore validates against write schema")

log('Script procedure end')

success()
