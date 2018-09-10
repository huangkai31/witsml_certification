#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server supports the item ObjectGrowing.",
     reference =  "7.2 For Specific Data-objects",
     reference_text = "If a server declares support for log then the server MUST support the item: objectGrowing",
     functionality_required = ["WMLS_GetFromStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup required')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

#Send SQ-008 (Get ID of all Instances of a Data-object in a Wellbore) for a log with objectGrowing set to true
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$'>
                             <objectGrowing>true</objectGrowing>
                         </log>                      
                     </logs>
                  """ ,OptionsIn={'returnElements':'id-only'} )
check_ReturnValue_Success()
check_XMLout_ElementIncluded('/logs/log[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uid="$server_w1_wb1_log1_uid$"]/name')
check_XMLout_ElementNotIncluded('/logs/log[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uid="$server_w1_wb1_log2_uid$"]/name')

partial_success("Server supports the item ObjectGrowing and returns only logs that are growing")

log('Script procedure end')
success()
