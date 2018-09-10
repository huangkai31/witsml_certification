#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify that minIndex/maxIndex values are being set to the MATHEMATICAL min/max index for a decreasing log.",
     reference =  "Expected behavior",
     reference_text = "",
     functionality_required = ["WMLS_GetFromStore:log",
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

# Add a new decreasing log with 2 curves including the index curve, and 2 rows of data for those curves.
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
<logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
  <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">   
    <nameWell>$well_name$</nameWell>
    <nameWellbore>$wellbore_name$</nameWellbore>
    <name>Energistics Certification Well 1 Wellbore 1 Log 89</name>
    <indexType>measured depth</indexType>
    <startIndex uom="ft">998.3</startIndex>
    <endIndex uom="ft">997.3</endIndex>
    <direction>decreasing</direction>
    <indexCurve>Depth</indexCurve>
    <logCurveInfo uid='Depth'>                                         
      <mnemonic>Depth</mnemonic>
      <unit>ft</unit>
      <nullValue>-999.25</nullValue>
      <minIndex uom="ft">997.3</minIndex>
      <maxIndex uom="ft">998.3</maxIndex>
      <curveDescription>measured depth index</curveDescription>
      <typeLogData>double</typeLogData>
    </logCurveInfo>
    <logCurveInfo uid='ChannelA'>
      <mnemonic>ChannelA</mnemonic>
      <unit>psi</unit>
      <minIndex uom="ft">997.3</minIndex>
      <maxIndex uom="ft">998.3</maxIndex>
      <typeLogData>double</typeLogData>
    </logCurveInfo>
    <logData>
      <mnemonicList>Depth,ChannelA</mnemonicList>
      <unitList>ft,psi</unitList>
      <data>998.3,11</data>
      <data>997.3,16</data>
    </logData>
  </log>
</logs>
""")

#AddToStore is successful
check_ReturnValue_Success()
set ("server_w1_wb1_test89_log1_uid",get_SuppMsgOut_uid_String())
log_variable("server_w1_wb1_test89_log1_uid")
new_object_created(WMLTYPEIN_LOG, "$server_w1_wb1_test89_log1_uid$", uidWellbore="$server_w1_wb1_uid$", uidWell="$server_w1_uid$")
partial_success("AddToStore is successful.")

#Get the log using SQ-015 (Get Log)
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version="$server_schema_version$">
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid='$server_w1_wb1_test89_log1_uid$'>
                         </log>                      
                       </logs>
                  """ ,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
partial_success("GetFromStore is successful.")

#confirm log is decreasing
check_XMLout_ElementValue("direction", "decreasing")
partial_success("Log is decreasing.")

log_verify_check_log_header_and_data()
partial_success("minIndex/maxIndex values are being set to the MATHEMATICAL min/max index for a decreasing log.")

log('Script end')
success()
