#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify that Server properly deletes a curve",
     reference =  "Expected behavior",
     reference_text = "",
     functionality_required = ["WMLS_GetFromStore:log",
                               "WMLS_UpdateInStore:log",
                               "WMLS_AddToStore:log"],
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

#Use AddToStore, creating a log object with two curves with non-null data. 
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">      
                                         <nameWell>$well_name$</nameWell>
                                         <nameWellbore>$wellbore_name$</nameWellbore>
                                         <name>Energistics Certification Well 1 Wellbore 1 Log 88</name>
                                         <indexType>measured depth</indexType>
                                         <startIndex uom="m">100</startIndex>
                                         <endIndex uom="m">300</endIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP88</indexCurve>
                                         <logCurveInfo uid='BDEP88'>                                         
                                           <mnemonic>BDEP88</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE188'>
                                           <mnemonic>CURVE188</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE288'>
                                           <mnemonic>CURVE288</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>BDEP88,CURVE188,CURVE288</mnemonicList>
                                           <unitList>m,m/h,m/h</unitList>
                                           <data>100,10,40</data>
                                           <data>200,20,50</data>
                                           <data>300,30,60</data>
                                         </logData>
                                       </log>
                                     </logs>
                                  """)

#AddToStore is successful
check_ReturnValue_Success()

set('server_w1_wb1_test88_log1_uid', get_SuppMsgOut_uid_String())
log_variable('server_w1_wb1_test88_log1_uid')
new_object_created(WMLTYPEIN_LOG, "$server_w1_wb1_test88_log1_uid$", uidWellbore="$server_w1_wb1_uid$", uidWell="$server_w1_uid$")

#Use SQ-015 (Get Log)
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid="$server_w1_wb1_test88_log1_uid$" />
                     </logs>
                  """ ,OptionsIn={'returnElements':'all'} )
check_ReturnValue_Success()

check_XMLout_RecurringElementValue('logs/log/logCurveInfo/mnemonic', ['CURVE188','CURVE288','BDEP88'])
partial_success("GetFromStore contains a log with all the expected curves.")

#Use DeleteFromStore specifying a curve mnemonic to be deleted
WMLS_DeleteFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid="$server_w1_wb1_test88_log1_uid$">
                              <logCurveInfo uid='CURVE188'>
                                  <mnemonic>CURVE188</mnemonic>
                              </logCurveInfo>
                         </log>
                     </logs>
                  """)
check_ReturnValue_Success()

#Use SQ-015 (Get Log) to obtain the log data
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid="$server_w1_wb1_test88_log1_uid$" />
                     </logs>
                  """ ,OptionsIn={'returnElements':'all'} )
check_ReturnValue_Success()

check_XMLout_RecurringElementValue('logs/log/logCurveInfo/mnemonic', ['BDEP88','CURVE288'])
partial_success("GetFromStore contains a log without deleted curve.")

#Check the log integrity
log_verify_check_log_header_and_data()

partial_success("The server supports proper deletion of a curve.")
log('Script procedure end')
success()
