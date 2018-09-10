#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server sets dTimCreation when adding a new object",
     reference =  "9.3.1 dTimCreation Element",
     reference_text = "When a data-object or sub-node is added in a server, the server MUST set the dTimCreation to the time when the operation was detected",
     functionality_required =   ["WMLS_GetFromStore:well",
                                 "WMLS_AddToStore:well"],
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

#Get what time it was 10 minutes ago.
set ("tml", timestamp_subtract_seconds(now(),600))

# Call AddToStore to add a Well to the server.
WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <well>
                                         <name>Energistics Certification Well Test67</name>
                                      </well>
                                   </wells>""")
check_ReturnValue_Success()
set("uid", get_SuppMsgOut_uid_String())
log_variable('uid')

# Use SQ-003 (Get details for a Well) with the returned uid.
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <well uid="$uid$"/>
                                   </wells>
                                """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success();
check_XMLout_NumberOfObjects(1);

# Verify the server has set dTimCreation within 10 minute of when the add was sent.
check_timestamp_Lessthan(get("tml"), get_XMLout_Element_String('dTimCreation'))
partial_success('dTimCreation set within the last 10 minutes')

log('Script procedure end')
success()

