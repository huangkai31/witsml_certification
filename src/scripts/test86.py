#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the Server properly deletes an object.",
     reference =  "Expected behavior",
     reference_text = "",
     functionality_required = ["WMLS_AddToStore:well",
                               "WMLS_GetFromStore:well",
                               "WMLS_DeleteFromStore:well"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup needed for this test.')
log ('')

#############
# TEST BODY #
#############

log('Script procedure start')

#1) Add a well with an empty uid.
WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                    <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <well>
                                        <name>Energistics Certification Well Test86</name>
                                      </well>
                                    </wells>""" )  
check_ReturnValue_Success()
set("suppUid",get_SuppMsgOut_uid_String())
log_variable('suppUid')
new_object_created(WMLTYPEIN_WELL, uid="$suppUid$")
partial_success("AddToStore succeeds and a uid is returned in SuppMsgOut")

#2) Send SQ-002 (Get ID of a Well) using the uid returned in SuppMsgOut
WMLS_GetFromStore(WMLTYPEIN_WELL, """<wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <well uid="$suppUid$" />
                                     </wells>""", OptionsIn={'returnElements':'id-only'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1);
check_XMLout_AttributeValue('well','uid', "$suppUid$")
partial_success("The first GetFromStore returns success and returns the expected well.")



#3) Delete the well using the uid returned in SuppMsgOut
WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="$suppUid$"/>                         
                                     </wells>""")
check_ReturnValue_Success()
partial_success("DeleteFromStore was successful.")

#4) GetFromStore using SQ-002 (Get ID of a Well) with the uid.
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="$suppUid$"/>                         
                                     </wells>
                                  """ ,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(0)
partial_success("The second GetFromStore request returns success and returns no wells.")

partial_success("Server properly deletes an object")
log('Script procedure end')
success()
