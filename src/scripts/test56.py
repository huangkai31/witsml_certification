#! /usr/bin/env python
from wtl.witsml import *



test(
     purpose = "Verify server creates uid for AddToStore when uid not specified .",
     reference =  "6.4.4",
     reference_text = "If the client does not define the uid value for the data-object in the XMLin file, the server MUST create one and (if no errors occur) return the created uid value to the client in SuppMsgOut",
     functionality_required =   ["WMLS_AddToStore:well" , 
                                 "WMLS_GetFromStore:well" ],    
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

WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <well>
                                       <name>Energistics Certification Well Test56</name>
                                     </well>
                                   </wells>
                                """)  

check_ReturnValue_Success()
partial_success("AddToStore succeeded")

set('uid', get_SuppMsgOut_uid_String())
partial_success("Server generate uid for new well")

WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <well uid="$uid$">
                                     </well>
                                   </wells>
                                """, OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('well', 'uid', '$uid$')
partial_success('One well returned and uid is ok')

log('Script procedure end')
success()
