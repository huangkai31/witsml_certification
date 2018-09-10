from wtl.witsml import *



test(
     purpose = "Verify that UpdateInStore block-clearing action does not occur",
     reference =  "6.7.4.6",
     reference_text = "When an update request is received by a server, the server does not clear the referenced channels based on the header's startIndex (or startDateTimeIndex) and endIndex (or endDateTimeIndex) values, if supplied. Instead, the server MUST use the implicit indices within the logData section to clear only the range specified for each channel. That range is bracketed by the earliest and latest value of each channel in the update request",
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

##################################################################################
##ADD a log with two curves and 3 indexes                                       ##
##################################################################################
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">
                                         <nameWell>$well_name$</nameWell>
                                         <nameWellbore>$wellbore_name$</nameWellbore>
                                         <name>Energistics Certification Wellbore Test72</name>
                                         <indexType>measured depth</indexType>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP</indexCurve>
                                         <logCurveInfo uid='BDEP'>
                                           <mnemonic>BDEP</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CHANNELA'>
                                           <mnemonic>CHANNELA</mnemonic>
                                           <unit>unitless</unit>
                                           <typeLogData>int</typeLogData>
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
                                           <data>1001,,12</data>
                                           <data>1002,3,</data>
                                         </logData>
                                      </log>
                                   </logs>
                                """)  

check_ReturnValue_Success();
partial_success("Add to store succeeded")

set('uid', get_SuppMsgOut_uid_String())
log_variable('uid')
new_object_created(WMLTYPEIN_LOG, "$uid$", uidWellbore="$server_w1_wb1_uid$", uidWell="$server_w1_uid$")




##################################################################################
## Update the log                                                               ##
##################################################################################
WMLS_UpdateInStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$uid$">
                                         <logData>
                                           <mnemonicList>BDEP,CHANNELA,CHANNELB</mnemonicList>
                                           <unitList>m,unitless,unitless</unitList>
                                           <data>1002,,13</data>
                                           <data>1003,4,14</data>
                                           </logData>
                                      </log>
                                   </logs>
                                """)
check_ReturnValue_Success()

######################################################################################
##Check to see if the value of CHANNELA at index 1002 is not cleared by the update  ##
######################################################################################


WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$uid$"/>
                                   </logs>
                                """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

# Verify that the value for CHANNELA at 1002 is not deleted
check_logData_DataValue(2,'CHANNELA',3,error_margin=1)
partial_success("Clearing range for curve is based on curve data received in update")

log('Script procedure end')

success()
