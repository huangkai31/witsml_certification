#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server's growingTimeoutPeriod for Logs.",
     reference =  "9.3.2.1  Logic for Setting objectGrowing Flags",
     reference_text = "If a server receives no data to append to a growing data-object in that data-objects growingTimeoutPeriod, then the server MUST set objectGrowing = false (indicating to clients that the data-object is not actively being updated)",
     functionality_required = ["WMLS_GetFromStore:log",
                               "WMLS_UpdateInStore:log",
                               "WMLS_AddToStore:log"],
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

#Create a new log with 1 row and 2 curves of data.  
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">      
                                         <nameWell>Energistics Certification Well 1</nameWell>
                                         <nameWellbore>Energistics Certification Well 1 Wellbore 1</nameWellbore>
                                         <name>Energistics Certification Well 1 Wellbore 1 Log 78</name>
                                         <indexType>measured depth</indexType>
                                         <startIndex uom="m">0</startIndex>
                                         <endIndex uom="m">0</endIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP78</indexCurve>
                                         <logCurveInfo uid='BDEP78'>
                                           <mnemonic>BDEP78</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE178'>
                                           <mnemonic>CURVE178</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>BDEP78,CURVE178</mnemonicList>
                                           <unitList>m,m/h</unitList>
                                           <data>0,0</data>
                                         </logData>
                                         </log>
                                     </logs>
                                  """)
#AddToStore is successful
check_ReturnValue_Success()

#get uid
set('server_w1_wb1_test78_log1_uid', get_SuppMsgOut_uid_String())
log_variable('server_w1_wb1_test78_log1_uid')
new_object_created(WMLTYPEIN_LOG, "$server_w1_wb1_test78_log1_uid$", uidWellbore="$server_w1_wb1_uid$", uidWell="$server_w1_uid$")

#Use SQ-015 (Get Log) for the log to get objectGrowing.
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid="$server_w1_wb1_test78_log1_uid$" />
                     </logs>
                  """ ,OptionsIn={'returnElements':'header-only'} )
check_ReturnValue_Success()

#In the first GetFromStore query, confirm objectGrowing = false.
check_XMLout_ElementValue("objectGrowing","false")
partial_success("ObjectGrowing stays false when a new log is added")

#Add new row to a curve in the log with index value greater than original to force server to set objectGrowing=true.
WMLS_UpdateInStore(WMLTYPEIN_LOG,
"""<?xml version="1.0" encoding="UTF-8"?>
<logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
    <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_test78_log1_uid$">
        <logData>
            <mnemonicList>BDEP78,CURVE178</mnemonicList> 
            <unitList>m,m/h</unitList> 
            <data>1,1</data> 
        </logData>
    </log>
</logs>""")
#UpdateInStore for new rows is successful.
check_ReturnValue_Success()

#Wait for changeDetectionPeriod + 1 second.
pause_for_changeDetectionPeriod()
pause(1)

#Use SQ-015 (Get Log) for the log to get objectGrowing.
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid="$server_w1_wb1_test78_log1_uid$" />
                     </logs>
                  """ ,OptionsIn={'returnElements':'header-only'} )
check_ReturnValue_Success()

#In the second GetFromStore query, confirm objectGrowing = true.
check_XMLout_ElementValue("objectGrowing","true")
partial_success("ObjectGrowing is set to true when new row is added to a curve with index value greater than original")

#Wait growingTimeoutPeriod + 1 second.
pause_for_growingTimeoutPeriod("log")
pause(1)

#Use SQ-015 (Get Log) for the log to get objectGrowing.
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid="$server_w1_wb1_test78_log1_uid$" />
                     </logs>
                  """ ,OptionsIn={'returnElements':'header-only'} )
check_ReturnValue_Success()

#In the third GetFromStore query, confirm objectGrowing = false.
check_XMLout_ElementValue("objectGrowing","false")
partial_success("ObjectGrowing returns to false after growingTimeoutPeriod has elapsed.")

partial_success("The server supports growingTimeoutPeriod for Logs.")
log('Script procedure end')

success()
