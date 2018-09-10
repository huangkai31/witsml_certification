#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server supports SQ-017 – What has been added to the server since a specified time",
     reference =  "6.6.7  Standard Query Templates",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required =   ["WMLS_GetFromStore:well",
                                 "WMLS_GetFromStore:wellbore",
                                 "WMLS_GetFromStore:changeLog",
                                 "WMLS_AddToStore:well",
                                 "WMLS_AddToStore:wellbore"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

# Call AddToStore to add a Well and Wellbore object to the server.

WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <well>
                                         <name>Energistics Certification Well Test59</name>
                                      </well>
                                   </wells>""")
check_ReturnValue_Success()
set('well_uid', get_SuppMsgOut_uid_String())
log_variable('well_uid')

WMLS_AddToStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <wellbore uidWell="$well_uid$">
                                        <nameWell>Energistics Certification Well Test59</nameWell>
                                        <name>Energistics Certification Wellbore Test59</name>
                                      </wellbore>
                                   </wellbores>
                                   """)
check_ReturnValue_Success()
set('wellbore_uid', get_SuppMsgOut_uid_String())
log_variable('wellbore_uid')

#Get what time it was 10 minutes ago.
set ("tml", timestamp_subtract_seconds(now(),600))

#Use SQ-017 with a dTimLastChange of NOW()-10 minutes to get the objects added the last 10 minutes.
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <changeLog>
                                            <changeHistory>
                                                <dTimChange>$tml$</dTimChange>
                                                <changeType>add</changeType>
                                            </changeHistory>
                                        </changeLog>
                                    </changeLogs>
                                  """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$well_uid$"]/changeHistory/changeType', 'add')
check_timestamp_Lessthan(get("tml"), get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$well_uid$"]/changeHistory/dTimChange'))
partial_success('Received change history entry for well')
                
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$wellbore_uid$" and @uidWell="$well_uid$"]/changeHistory/changeType', 'add')
check_timestamp_Lessthan(get("tml"), get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$wellbore_uid$" and @uidWell="$well_uid$"]/changeHistory/dTimChange'))
partial_success('Received change history entry for wellbore')

partial_success("Server supports SQ-017 What has been added to the server since a specified time")
log('Script procedure end')


success()
