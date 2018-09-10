#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server ignores attempts to change objectGrowing.",
     reference =  "9.3 Change Mechanisms",
     reference_text = "The server MUST ignore any attempt by a client to change objectGrowing Element",
     functionality_required =   ["WMLS_GetFromStore:log",
                                 "WMLS_UpdateInStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed for this test')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

#Use UpdateInStore to update the log object, setting objectGrowing = true.
WMLS_UpdateInStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid='$server_w1_wb1_log2_uid$'>
                             <objectGrowing>true</objectGrowing>
                         </log>
                     </logs>
                  """)
check_ReturnValue_Success()

#Use SQ-011 (Get Header for all Growing Data-objects in a Wellbore) to obtain objectGrowing.
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid='$server_w1_wb1_log2_uid$'>
                         </log>                      
                     </logs>
                  """ ,OptionsIn={'returnElements':'header-only'})
check_ReturnValue_Success()

#Check that the GetFromStore query returns objectGrowing = false"
check_XMLout_ElementValue("objectGrowing","false")

partial_success("The server ignores attempts to change objectGrowing.")
log('Script procedure end')
success()
