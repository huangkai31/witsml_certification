#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server supports SQ-016 - What has changed since a specified time ( wellbore )",
     reference =  "6.6.5.17",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required =   ["WMLS_AddToStore:wellbore" , 
                                 "WMLS_DeleteFromStore:wellbore",
                                 "WMLS_UpdateInStore:wellbore",
                                 "WMLS_GetFromStore:changeLog" ],
     data_schemas = ["1.4.1.0", "1.4.1.1"],         
                                 
    )
##############
## SETUP     #
##############

log('Setup start')

# use a well already added by the load_data_set
set("wellUid", "$server_w1_uid$")
# get well object
WMLS_GetFromStore(WMLTYPEIN_WELL,"""
                  <wells xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                        <well uid='$wellUid$'/>
                  </wells>
                  """,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
set("well_name", get_XMLout_Element_String("wells/well/name"))

partial_success("WMLS_GetFromStore succeeded well")

log('Setup end')

#############
# TEST BODY #
#############  
log('Script procedure start')

set("wellbore_name", "Energistics Certification Wellbore Test94b")

WMLS_AddToStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                       <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                          <wellbore uidWell="$wellUid$">
                                            <nameWell>$well_name$</nameWell>
                                            <name>$wellbore_name$</name>
                                          </wellbore>
                                       </wellbores>
                                       """)
check_ReturnValue_Success()
partial_success("WMLS_AddToStore succeeded wellbore")

set('wellboreUid', get_SuppMsgOut_uid_String())
log_variable('wellboreUid')
new_object_created(WMLTYPEIN_WELLBORE, "$wellboreUid$", uidWell="$wellUid$")

# 2. Get ChangeLogs
#get time for 1 hour ago.
set('dTim', timestamp_subtract_seconds(now(), 3600))
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                                <changeLog> 
                                                    <commonData>
                                                        <dTimLastChange>$dTim$</dTimLastChange>
                                                    </commonData>
                                                </changeLog>
                                        </changeLogs>
                                    """, OptionsIn = { 'returnElements':'latest-change-only' })  

check_ReturnValue_Success()
partial_success("GetFromStore changeLogs after Add succeeded ")

#check to see that the return is valid
check_XMLout_ValidWriteSchema()
partial_success("changeLogs returned are write schema valid ")

#check to see that no changeHistory's exist
check_XMLout_ElementNotIncluded('/changeLogs/changeLog/changeHistory')
partial_success("No changeHistory in changeLogs exist, succeed ")

#find added wellbore's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore"]/lastChangeType', 'add') 
partial_success("wellbore changeLog with only Add in lastChangeType succeed ")

# get add dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore" and lastChangeType="add"]/commonData/dTimLastChange')
partial_success("wellbore changeLog with only add has dTimLastChange succeed ")
addDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore" and lastChangeType="add"]/commonData/dTimLastChange')
set('dTim', addDTim)


# 3 Update the Wellbore
WMLS_UpdateInStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <wellbore uidWell="$wellUid$" uid="$wellboreUid$">
                                            <number>1234-0987</number>
                                      </wellbore>
                                   </wellbores>
                                """)  
check_ReturnValue_Success()
partial_success("UpdateInStore wellbore succeeded ")

#4 ChangeLog for wellbore is update
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                                <changeLog> 
                                                    <commonData>
                                                        <dTimLastChange>$dTim$</dTimLastChange>
                                                    </commonData>
                                                </changeLog>
                                        </changeLogs>
                                    """, OptionsIn = { 'returnElements':'latest-change-only' })  

check_ReturnValue_Success()
partial_success("GetFromStore changeLogs after Update succeeded ")

#check to see that the return is valid
check_XMLout_ValidWriteSchema()
partial_success("changeLogs returned are write schema valid ")

#check to see that no changeHistory's exist
check_XMLout_ElementNotIncluded('/changeLogs/changeLog/changeHistory')
partial_success("No changeHistory in changeLogs exist, succeed ")

#find update wellbore's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore"]/lastChangeType', 'update') 
partial_success("wellbore changeLog with only update in lastChangeType succeed ")

# get update dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore" and lastChangeType="update"]/commonData/dTimLastChange')
partial_success("wellbore changeLog with only update has dTimLastChange succeed ")
updateDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore" and lastChangeType="update"]/commonData/dTimLastChange')

check_timestamp_Greaterthan(updateDTim, get('dTim'))
partial_success("wellbore changeLog with only update dTimLastChange > changeLog with Update succeed ")
set('dTim', updateDTim)

#5 Delete Wellbore
WMLS_DeleteFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <wellbore uidWell="$wellUid$" uid="$wellboreUid$">
                                      </wellbore>
                                   </wellbores>
                                """)  
check_ReturnValue_Success()
partial_success("DeleteFromStore wellbore succeeded ")

#6 ChangeLog for wellbore in Delete
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                                <changeLog> 
                                                    <commonData>
                                                        <dTimLastChange>$dTim$</dTimLastChange>
                                                    </commonData>
                                                </changeLog>
                                        </changeLogs>
                                    """, OptionsIn = { 'returnElements':'latest-change-only' })  

check_ReturnValue_Success()
partial_success("GetFromStore changeLogs after Delete succeeded ")

#check to see that the return is valid
check_XMLout_ValidWriteSchema()
partial_success("changeLogs returned are write schema valid ")

#check to see that no changeHistory's exist
check_XMLout_ElementNotIncluded('/changeLogs/changeLog/changeHistory')
partial_success("No changeHistory in changeLogs exist, succeed ")

#find update wellbore's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore"]/lastChangeType', 'delete') 
partial_success("wellbore changeLog with only delete in lastChangeType succeed ")

# get delete dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore" and lastChangeType="delete"]/commonData/dTimLastChange')
partial_success("wellbore changeLog with only delete has dTimLastChange succeed ")
deleteDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$wellboreUid$" and objectType="wellbore" and lastChangeType="delete"]/commonData/dTimLastChange')

check_timestamp_Greaterthan(deleteDTim, get('dTim'))
partial_success("wellbore changeLog with only delete dTimLastChange > changeLog with update succeed ")



log('Script procedure end')

success()
