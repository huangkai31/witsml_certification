#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the changeLog lastChangeType and lastChangeInfo matches the changeHistory",
     reference =  "9.3.4.1 changeLog Elements Attributes",
     reference_text = " The values of lastChangeType and lastChangeInfo MUST match the changeType and changeInfo elements of the last entry that was added to the changeHistory.",
     functionality_required =   ["WMLS_GetFromStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

#Query the changeLog to obtain a changeLog entry.
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                            <changeLog uidWell="$server_w3_uid$" uidWellbore="$server_w3_wb1_uid$" uidObject='$server_w3_wb1_log1_uid$'>
                                                <objectType>log</objectType> 
                                            </changeLog>
                                          </changeLogs>
                                  """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()

set("dTimLatest", get_XMLout_LatestdTimChange_String())
set("changeType", get_XMLout_Element_String("changeHistory[dTimChange='$dTimLatest$']/changeType"))
set("changeInfo", get_XMLout_Element_String("changeHistory[dTimChange='$dTimLatest$']/changeInfo"))


#Verify the lastChangeType matches the latest entry in the changeHistory.changeType.    
check_XMLout_ElementValue("lastChangeType","$changeType$")
partial_success ("Latest changeType matches latest entry in changeHistory")

#Verify the lastChangeInfo matches the latest entry in changeHistory.changeInfo
if (get('changeInfo') is not None):
    check_XMLout_ElementValue("lastChangeInfo","$changeInfo$")
else:
    check_XMLout_ElementNotIncluded("lastChangeInfo")
partial_success ("Latest changeInfo matches latest entry in changeHistory")

partial_success("LastChangeType and lastChangeInfo match latest changeType and changeInfo in changeHistory")
log('Script procedure end')
success()
