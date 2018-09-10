#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server supports SQ-016 - What has changed since a specified time ( log )",
     reference =  "6.6.5.17",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required =   ["WMLS_AddToStore:log" , 
                                 "WMLS_DeleteFromStore:log",
                                 "WMLS_UpdateInStore:log",
                                 "WMLS_GetFromStore:changeLog" ],
     data_schemas = ["1.4.1.0", "1.4.1.1"],         
                                 
    )
##############
## SETUP     #
##############

log('Setup start')

# use a wellbore already added by the load_data_set
set("wellUid", "$server_w1_uid$")
set("wellboreUid", "$server_w1_wb1_uid$")
# get wellbore object
WMLS_GetFromStore(WMLTYPEIN_WELLBORE,"""
                  <wellbores xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                        <wellbore uidWell='$wellUid$' uid='$wellboreUid$'/>
                  </wellbores>
                  """,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
set("well_name", get_XMLout_Element_String("wellbores/wellbore/nameWell"))
set("wellbore_name", get_XMLout_Element_String("wellbores/wellbore/name"))

partial_success("WMLS_GetFromStore succeeded wellbore")

log('Setup end')

#############
# TEST BODY #
#############  
log('Script procedure start')

set("log_name", "Energistics Certification Log Test94d")

WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$wellUid$" uidWellbore="$wellboreUid$">
                                         <nameWell>$well_name$</nameWell>
                                         <nameWellbore>$wellbore_name$</nameWellbore>
                                         <name>$log_name$</name>
                                         <indexType>date time</indexType>
                                         <startDateTimeIndex>2012-07-26T15:17:20Z</startDateTimeIndex>
                                         <endDateTimeIndex>2012-07-26T15:17:50Z</endDateTimeIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>TIME</indexCurve>
                                         <logCurveInfo uid='TIME'>
                                           <mnemonic>TIME</mnemonic>
                                           <unit>unitless</unit>
                                           <typeLogData>date time</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='ROP2'>
                                           <mnemonic>ROP2</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>TIME,ROP2</mnemonicList>
                                           <unitList>unitless,m/h</unitList>
                                           <data>2012-07-26T15:17:20Z,0</data>
                                           <data>2012-07-26T15:17:30Z,1</data>
                                           <data>2012-07-26T15:17:40Z,2</data>
                                           <data>2012-07-26T15:17:50Z,3</data>
                                         </logData>
                                      </log>
                                   </logs>""")  
    
check_ReturnValue_Success()
partial_success("WMLS_AddToStore succeeded log")

set('logUid', get_SuppMsgOut_uid_String())
log_variable('logUid')
new_object_created(WMLTYPEIN_LOG, "$logUid$", uidWell="$wellUid$", uidWellbore="$wellboreUid$")

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

#find added log's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log"]/lastChangeType', 'add') 
partial_success("log changeLog with only Add in lastChangeType succeed ")

# get add dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log" and lastChangeType="add"]/commonData/dTimLastChange')
partial_success("log changeLog with only add has dTimLastChange succeed ")
addDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log" and lastChangeType="add"]/commonData/dTimLastChange')
set('dTim', addDTim)


# 3 Update the log
WMLS_UpdateInStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <log uidWell="$wellUid$" uidWellbore="$wellboreUid$" uid="$logUid$">
                                            <serviceCompany>Halliburton</serviceCompany>
                                      </log>
                                   </logs>
                                """)  
check_ReturnValue_Success()
partial_success("UpdateInStore log succeeded ")

#4 ChangeLog for log is update
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

#find update log's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log"]/lastChangeType', 'update') 
partial_success("log changeLog with only update in lastChangeType succeed ")

# get update dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log" and lastChangeType="update"]/commonData/dTimLastChange')
partial_success("log changeLog with only update has dTimLastChange succeed ")
updateDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log" and lastChangeType="update"]/commonData/dTimLastChange')

check_timestamp_Greaterthan(updateDTim, get('dTim'))
partial_success("log changeLog with only update dTimLastChange > changeLog with Update succeed ")
set('dTim', updateDTim)

#5 Delete log
WMLS_DeleteFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <log uidWell="$wellUid$" uidWellbore="$wellboreUid$" uid="$logUid$">
                                      </log>
                                   </logs>
                                """)  
check_ReturnValue_Success()
partial_success("DeleteFromStore log succeeded ")

#6 ChangeLog for log in Delete
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

#find update log's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log"]/lastChangeType', 'delete') 
partial_success("log changeLog with only delete in lastChangeType succeed ")

# get delete dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log" and lastChangeType="delete"]/commonData/dTimLastChange')
partial_success("log changeLog with only delete has dTimLastChange succeed ")
deleteDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$logUid$" and objectType="log" and lastChangeType="delete"]/commonData/dTimLastChange')


check_timestamp_Greaterthan(deleteDTim, get('dTim'))
partial_success("log changeLog with only delete dTimLastChange > changeLog with update succeed ")



log('Script procedure end')

success()
