#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the Server properly overwrites interior data when the update-Column range overlaps the pre-update column-range, and does not duplicate index rows",
     reference =  "6.7.4.5",
     reference_text = "If a client specifies data-nodes for existing columns, then the server MUST ignore structural-range. Rather, the server MUST evaluate each column of data separately to determine the update-column-range.",
     functionality_required =   ["WMLS_AddToStore:log" ,
                                 "WMLS_UpdateInStore:log",
                                 "WMLS_GetFromStore:log"],
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

# Add a new log with a set of curves and a set of data for those curves.
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">
                                         <nameWell>$well_name$</nameWell>
                                         <nameWellbore>$wellbore_name$</nameWellbore>
                                         <name>Energistics Certification Wellbore Test85</name>
                                         <indexType>measured depth</indexType>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP</indexCurve>
                                         <logCurveInfo uid='BDEP'>
                                           <mnemonic>BDEP</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>double</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CHANNELA'>
                                           <mnemonic>CHANNELA</mnemonic>
                                           <unit>unitless</unit>
                                           <typeLogData>float</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CHANNELB'>
                                           <mnemonic>CHANNELB</mnemonic>
                                           <unit>unitless</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>BDEP,CHANNELA,CHANNELB</mnemonicList>
                                           <unitList>m,unitless,unitless</unitList>
                                           <data>1000,1,11</data>
                                           <data>1001.1,35,12</data>
                                           <data>1002,3,82</data>
                                         </logData>
                                      </log>
                                   </logs>
                                """)  

check_ReturnValue_Success()
partial_success("Add to store succeeded")

set('uid', get_SuppMsgOut_uid_String())
log_variable('uid')
new_object_created(WMLTYPEIN_LOG, "$uid$", uidWellbore="$server_w1_wb1_uid$", uidWell="$server_w1_uid$")


# Get the log using SQ-015 (Get Log)
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$uid$"/>
                                   </logs>
                                """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
# Get index vales (in case units were converted)
index0 = float(get_logData_IndexValue_String(0))
index1 = float(get_logData_IndexValue_String(1))
index2 = float(get_logData_IndexValue_String(2))

# Update the log with the same set of curves and the same indexes, but with different data value
WMLS_UpdateInStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$uid$">
                                         <logData>
                                           <mnemonicList>BDEP,CHANNELA,CHANNELB</mnemonicList>
                                           <unitList>m,unitless,unitless</unitList>
                                           <data>1000,2.5,7</data>
                                           <data>1001.1,23.1,1</data>
                                           <data>1002,5,54</data>
                                           </logData>
                                      </log>
                                   </logs>
                                """)
check_ReturnValue_Success()

#Get the log using SQ-015 (Get Log) 
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$uid$"/>
                                   </logs>
                                """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

# Verify that the data has been updated with the new values from the Update.
# Verify that there are no duplicate indices.
data = [(index0,2.5,7),
        (index1,23.1,1),
        (index2,5,54)]
check_logData_AllData(data, ['BDEP', 'CHANNELA', 'CHANNELB'], index_error_margin=1, error_margin=1)
partial_success("Data received after the update is correct")

log('Script procedure end')

success()
