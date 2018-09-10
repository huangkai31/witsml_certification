#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server ignores attempts to change dTimCreation",
     reference =  "9.3 Change Mechanisms",
     reference_text = "The server MUST ignore any attempt by a client to change dTimCreation Element",
     functionality_required =   ["WMLS_GetFromStore:well",
                                 "WMLS_UpdateInStore:well"],
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

##Use SQ-003 (Get details for a Well) to obtain the well.
WMLS_GetFromStore(WMLTYPEIN_WELL,"""
                  <wells xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                        <well uid='$server_w1_uid$'/>
                  </wells>
                  """,OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()
set ("dTim", get_XMLout_Element_String("dTimCreation"))

##Use UpdateInStore to update the well object's dTimCreation to 5 seconds greater than the original.
set('st', timestamp_add_seconds(get('dTim'), 5))
WMLS_UpdateInStore(WMLTYPEIN_WELL, """<wells xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                                        <well uid='$server_w1_uid$'>
                                            <commonData>
                                                <dTimCreation>$st$</dTimCreation>
                                            </commonData>
                                        </well>
                                      </wells>
                                   """)  
##Check UpdateInStore returns success.
check_ReturnValue_Success()

##Use SQ-003 (Get details for a Well) to obtain the well.
WMLS_GetFromStore(WMLTYPEIN_WELL,"""
                  <wells xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                        <well uid='$server_w1_uid$'/>
                  </wells>
                  """,OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()

##Verify the dTimCreation has not changed between the two standard queries.
check_XMLout_ElementValue("dTimCreation","$dTim$")

partial_success("Server ignored attempt to change dTimCreation.")
log('Script test procedure end')
success()
