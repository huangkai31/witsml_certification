#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify objectGrowing functionality for delete behaviour for Logs.",
     reference =  "Expected behavior",
     reference_text = "ObjectGrowing should not change to true for certain changes to the log",
     functionality_required = ["WMLS_GetFromStore:log",
                               "WMLS_AddToStore:log",
                               "WMLS_DeleteFromStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Setup start')

log("Retrieving well and wellbore name")
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <wellbore uidWell="$server_w1_uid$" uid="$server_w1_wb1_uid$"/>
                                     </wellbores>
                                  """, OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success();
set('well_name', get_XMLout_Element_String('nameWell'))
set('wellbore_name', get_XMLout_Element_String('name'))

log('Setup end')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

#Create a new log with 2 rows and 3 curves of data.
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">      
                                         <nameWell>$well_name$</nameWell>
                                         <nameWellbore>$wellbore_name$</nameWellbore>
                                         <name>Energistics Certification Well 1 Wellbore 1 Log 79</name>
                                         <indexType>measured depth</indexType>
                                         <startIndex uom="m">0.5</startIndex>
                                         <endIndex uom="m">2</endIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP79</indexCurve>
                                         <logCurveInfo uid='BDEP79'>
                                           <mnemonic>BDEP79</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>double</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE179'>
                                           <mnemonic>CURVE179</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE479'>
                                           <mnemonic>CURVE479</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>BDEP79,CURVE179,CURVE479</mnemonicList>
                                           <unitList>m,m/h,m/h</unitList>
                                           <data>0.5,0,1</data>
                                           <data>2,2,3</data>
                                         </logData>
                                         </log>
                                     </logs>
                                  """)
#AddToStore is successful
check_ReturnValue_Success()
set('server_w1_wb1_test79b_log1_uid', get_SuppMsgOut_uid_String())
new_object_created(WMLTYPEIN_LOG, "$server_w1_wb1_test79b_log1_uid$", uidWellbore="$server_w1_wb1_uid$", uidWell="$server_w1_uid$")

#Wait for changeDetectionPeriod + 1 second.
pause_for_changeDetectionPeriod()
pause(1)

#Use SQ-015 (Get Log) for the log.
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$'  uid="$server_w1_wb1_test79b_log1_uid$" />
                     </logs>
                  """ ,OptionsIn={'returnElements':'all'} )
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

#Confirm objectGrowing = false
check_XMLout_ElementValue("objectGrowing","false")
partial_success("ObjectGrowing stays false when adding a new log")

#Delete a curve from the log.
WMLS_DeleteFromStore(WMLTYPEIN_LOG,
"""<?xml version="1.0" encoding="UTF-8"?>
<logs xmlns="http://www.witsml.org/schemas/1series" version="1.4.1.1">
    <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_test79b_log1_uid$">
        <logCurveInfo uid='CURVE179'>
            <mnemonic>CURVE179</mnemonic>
        </logCurveInfo>
    </log>
</logs>""")  
#DeleteFromStore is successful
check_ReturnValue_Success()

#Wait for changeDetectionPeriod + 1 second.
pause_for_changeDetectionPeriod()
pause(1)

#Use SQ-015 (Get Log) for the log.
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$'  uid="$server_w1_wb1_test79b_log1_uid$" />
                     </logs>
                  """ ,OptionsIn={'returnElements':'all'} )
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

#Confirm objectGrowing = false
check_XMLout_ElementValue("objectGrowing","false")
partial_success("ObjectGrowing stays false when deleting a curve of an existing log")

#Delete a row from the log.
WMLS_DeleteFromStore(WMLTYPEIN_LOG,
"""<?xml version="1.0" encoding="UTF-8"?>
<logs xmlns="http://www.witsml.org/schemas/1series" version="1.4.1.1">
    <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_test79b_log1_uid$">
        <startIndex uom="m">0.5</startIndex>
        <endIndex uom="m">0.5</endIndex>
    </log>
</logs>""")  
#DeleteFromStore is successful
check_ReturnValue_Success()

#Wait for changeDetectionPeriod + 1 second.
pause_for_changeDetectionPeriod()
pause(1)

#Use SQ-015 (Get Log) for the log.
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$'  uid="$server_w1_wb1_test79b_log1_uid$" />
                     </logs>
                  """ ,OptionsIn={'returnElements':'all'} )
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

#Confirm objectGrowing = false
check_XMLout_ElementValue("objectGrowing","false")
partial_success("ObjectGrowing stays false when deleting a row from a log")

partial_success("Delete behavior for ObjectGrowing functionality for logs has been verified")
log('Script procedure end')

success()
