#! /usr/bin/env python
from wtl.witsml import *



test(
     purpose = "Verify the server supports requestLatestValues behaviour for sparse logs",
     reference =  "6.6.2.1",
     reference_text = "DEFAULT: normal log behavior. A server MUST support this option. If specified, return the latest n values from each curve in a log data-object. ",
     functionality_required =   ["WMLS_AddToStore:log" , 
                                 "WMLS_GetFromStore:log" ],    
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


WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">
                                         <nameWell>$well_name$</nameWell>
                                         <nameWellbore>$wellbore_name$</nameWellbore>
                                         <name>Energistics Certification Well 1 Wellbore 1 Log Test76b</name>
                                         <indexType>measured depth</indexType>
                                         <startIndex uom="m">0</startIndex>
                                         <endIndex uom="m">4</endIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP</indexCurve>
                                         <logCurveInfo uid='BDEP'>
                                           <mnemonic>BDEP</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>double</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE1'>
                                           <mnemonic>CURVE1</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>double</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE2'>
                                           <mnemonic>CURVE2</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>double</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE3'>
                                           <mnemonic>CURVE3</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>double</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>BDEP,CURVE1,CURVE2,CURVE3</mnemonicList>
                                           <unitList>m, m/h, m/h, m/h</unitList>
                                           <data>0,0.1,0.2,0.3</data>
                                           <data>1,1,1.2,</data>
                                           <data>2,2.1,,2.3</data>
                                           <data>3,3.1,,1</data>
                                           <data>4,,,4.3</data>
                                         </logData>
                                      </log>
                                   </logs>
                                """)  

check_ReturnValue_Success()
partial_success("Add to store succeeded")

set('uid', get_SuppMsgOut_uid_String())
log_variable('uid')
new_object_created(WMLTYPEIN_LOG, "$uid$", uidWellbore="$server_w1_wb1_uid$", uidWell="$server_w1_uid$")

# Use SQ-015 (Get Log) specifying OptionsIn = requestLatestValues = 1 for  the curve
WMLS_GetFromStore(WMLTYPEIN_LOG, 
					"""<logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                         <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$uid$"/>
				       </logs>
					""" ,OptionsIn={'requestLatestValues':'1','returnElements':'data-only'} )
check_ReturnValue_Success()

check_logData_DataValue(0,'CURVE2',1.2,error_margin=1)
check_logData_DataValue(1,'CURVE1',3.1,error_margin=1)
check_logData_DataValue(2,'CURVE3',4.3,error_margin=1)
partial_success('Server returned the latest values for each curve')

check_logData_NumberOfNodes(3)
check_logData_DataValue(0,'CURVE1','')
check_logData_DataValue(0,'CURVE3','')
check_logData_DataValue(1,'CURVE2','')
check_logData_DataValue(1,'CURVE3','')
check_logData_DataValue(2,'CURVE1','')
check_logData_DataValue(2,'CURVE2','')
partial_success("Server returned one value for each curve")

log('Script procedure end')

success()
