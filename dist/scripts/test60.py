#! /usr/bin/env python
from wtl.witsml import *

import wtl.utils;
import datetime;

test(
     purpose = "Verify the server supports SQ-018 - What changes have been made in a log or multiple logs since a specified time",
     reference =  "6.6.7",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required =   ["WMLS_AddToStore:log" , 
                                 "WMLS_GetFromStore:log",
                                 "WMLS_DeleteFromStore:log",
                                 "WMLS_UpdateInStore:log",
                                 "WMLS_GetFromStore:changeLog" ]    
                                 
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


# server_w1_wb1_log1_uid - depth log
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">
                                         <nameWell>$well_name$</nameWell>
                                         <nameWellbore>$wellbore_name$</nameWellbore>
                                         <name>Energistics Certification Wellbore Test60</name>
                                         <indexType>measured depth</indexType>
                                         <startIndex uom="m">0</startIndex>
                                         <endIndex uom="m">4</endIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP</indexCurve>
                                         <logCurveInfo uid='BDEP'>
                                           <mnemonic>BDEP</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE1'>
                                           <mnemonic>CURVE1</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE2'>
                                           <mnemonic>CURVE2</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE3'>
                                           <mnemonic>CURVE3</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>BDEP,CURVE1,CURVE2,CURVE3</mnemonicList>
                                           <unitList>m, m/h, m/h, m/h</unitList>
                                           <data>0,0,0,0</data>
                                           <data>1,1,1,1</data>
                                           <data>2,2,2,2</data>
                                           <data>4,4,4,4</data>
                                         </logData>
                                      </log>
                                   </logs>""")  
check_ReturnValue_Success()
set('log_uid', get_SuppMsgOut_uid_String())
log_variable('log_uid')

#Call UpdateInStore to add a single datapoint to a curve to the existing curve rang
WMLS_UpdateInStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$log_uid$">
                                         <logData>
                                           <mnemonicList>BDEP,CURVE1</mnemonicList>
                                           <unitList>m, m/h</unitList>
                                           <data>3,3</data>
                                         </logData>
                                      </log>
                                   </logs>
                                """)  
check_ReturnValue_Success()

#Call DeleteFrom Store to delete a datapoint in a curve
WMLS_DeleteFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <log  uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$log_uid$">
                                         <startIndex uom="m">2</startIndex>
                                         <endIndex uom="m">2</endIndex>
                                         <logCurveInfo>
                                           <mnemonic>CURVE2</mnemonic>
                                         </logCurveInfo>
                                      </log>
                                   </logs>
                                """)  
check_ReturnValue_Success()


#Call UpdateInStore to delete a datapoint in a curve
WMLS_UpdateInStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <log  uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$log_uid$">
                                         <logData>
                                           <mnemonicList>BDEP,CURVE3</mnemonicList>
                                           <unitList>m, m/h</unitList>
                                           <data>1,1</data>
                                           <data>4,4</data>
                                         </logData>
                                      </log>
                                   </logs>
                                """)  
check_ReturnValue_Success()

#Get what time it was 10 minutes ago.
set ("tml", timestamp_subtract_seconds(now(),600))

WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                                <changeLog 
                                                            uidWell="$server_w1_uid$" 
                                                            uidWellbore="$server_w1_wb1_uid$" 
                                                            uidObject="$log_uid$">
                                                    <changeHistory>                                                          
                                                        <dTimChange>$tml$</dTimChange> 
                                                        <changeType>update</changeType>
                                                    </changeHistory>
                                                </changeLog>
                                        </changeLogs>
                                    """, OptionsIn = { 'returnElements':'all' })  

check_ReturnValue_Success()

check_XMLout_ElementValue('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="BDEP,CURVE1"]/changeType', 'update')
check_XMLout_ElementValue('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="BDEP,CURVE3"]/changeType', 'update')
check_XMLout_ElementValue('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="BDEP,CURVE1"]/startIndex', '3')
check_XMLout_ElementValue('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="BDEP,CURVE1"]/endIndex', '3')
check_XMLout_ElementValue('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="CURVE2"]/startIndex', '2')
check_XMLout_ElementValue('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="CURVE2"]/endIndex', '2')
check_XMLout_ElementValue('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="BDEP,CURVE3"]/startIndex', '1')
check_XMLout_ElementValue('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="BDEP,CURVE3"]/endIndex', '4')
check_timestamp_Lessthan(get("tml"), get_XMLout_Element_String('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="BDEP,CURVE1"]/dTimChange'))
check_timestamp_Lessthan(get("tml"), get_XMLout_Element_String('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="CURVE2"]/dTimChange'))
check_timestamp_Lessthan(get("tml"), get_XMLout_Element_String('/changeLogs/changeLog[@uidWell="$server_w1_uid$" and @uidWellbore="$server_w1_wb1_uid$" and @uidObject="$log_uid$"]/changeHistory[mnemonics="BDEP,CURVE3"]/dTimChange'))
partial_success('Received change history entry for well')


log('Script procedure end')
success()
