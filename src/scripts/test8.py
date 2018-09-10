#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Check the server supports requesting data subset for a point index object",
     reference =  "6.6.4.3  Special Handling for Growing Data-objects",
     reference_text = "Determining Selected-nodes:  For a point index (see schema), the server MUST include as selected-nodes those data nodes where the node-index is greater than or equal to the minimum range value AND less than or equal to the maximum range value.",
     functionality_required = ["WMLS_GetFromStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

#Get mnemonic list and choose 2 curves (including the index curve)
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version="$server_schema_version$">
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid='$server_w1_wb1_log1_uid$'>
                         </log>                      
                       </logs>
                  """ ,OptionsIn={'returnElements':'data-only'})
check_ReturnValue_Success()

mnemonics = get_XMLout_Mnemonics_List()
set("indx", mnemonics[0])
set("ndx1", mnemonics[1])
set("mn", get("indx") + "," + get("ndx1"))

#############
# TEST BODY #
#############

log('Script procedure start')

#Use Standard Query #14 (Get Log Data Subset) requesting 2 curves (including the index curve) and not specifying a startIndex or endIndex
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version="$server_schema_version$">
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid='$server_w1_wb1_log1_uid$'>
                         <logData>
                             <mnemonicList>$mn$</mnemonicList>
                         </logData>
                         </log>                      
                       </logs>
                  """ ,OptionsIn={'returnElements':'data-only'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

#Get index value from rows 2 and 3 (to essentially truncate the log)
set("valueFrst",get_logData_DataValue_String(1, get('indx')))
set("valueLast",get_logData_DataValue_String(2, get('indx')))
 
#Get uom for index curve
set('idxUom', get_XMLout_Units_List()[0])

#Use SQ-014 (Get Log Data Subset) requesting a subset of the data (specify startIndex and endIndex) for the same 2 curves (including the index curve)
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns='http://www.witsml.org/schemas/1series' version="$server_schema_version$">
                         <log uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$' uid='$server_w1_wb1_log1_uid$'>
                         <startIndex uom="$idxUom$">$valueFrst$</startIndex>
                         <endIndex uom="$idxUom$">$valueLast$</endIndex>
                         <logData>
                             <mnemonicList>$mn$</mnemonicList>
                         </logData>
                         </log>                      
                       </logs>
                  """ ,OptionsIn={'returnElements':'data-only'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

#Confirm expected truncation
check_logData_DataValue(0,get('indx'),get('valueFrst'))
check_logData_DataValue(1,get('indx'),get('valueLast'))
partial_success("Server supports requesting data subset for a point index object")

log('Script end')
success()
