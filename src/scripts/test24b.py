#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify that Server returns all data-nodes when no structural-range value is specified for a subset of curves.",
     reference =  "6.6.4.3 Special Handling for Growing Data-objects",
     reference_text = "Determining Selected-nodes: If a client does not specify a structural-range value, then the server MUST include all data-nodes as selected-nodes.",
     functionality_required =   ["WMLS_GetFromStore:log"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup required for this test.')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

# Obtain the minIndex and maxIndex for the non-Index curve
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                      <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <log uidWell="$server_w2_uid$" uidWellbore="$server_w2_wb1_uid$" uid="$server_w2_wb1_log1_uid$">                       
                                        </log>
                                      </logs>
                                  """,
                                  OptionsIn={'returnElements':'header-only'})  
check_ReturnValue_Success()

# get the min and max index for the non-index curve
set('firstMinIndex',get_XMLout_Element_String('/logs/log/logCurveInfo[mnemonic="$server_w2_wb1_log1_mnemonic_1$"]/minIndex'))
log_variable('firstMinIndex')
set('firstMaxIndex',get_XMLout_Element_String('/logs/log/logCurveInfo[mnemonic="$server_w2_wb1_log1_mnemonic_1$"]/maxIndex'))
log_variable('firstMaxIndex')

# Use Standard Query #15 (Get Log) for request
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                      <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <log uidWell="$server_w2_uid$" uidWellbore="$server_w2_wb1_uid$" uid="$server_w2_wb1_log1_uid$">
                                          <logData>
                                            <mnemonicList>$server_w2_wb1_log1_index_mnemonic$,$server_w2_wb1_log1_mnemonic_1$</mnemonicList> 
                                          </logData>                          
                                        </log>
                                      </logs>
                                  """,
                                  OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()


if (get('firstMinIndex') <> get_XMLout_Element_String('/logs/log/logCurveInfo[mnemonic="$server_w2_wb1_log1_mnemonic_1$"]/minIndex')):
    fail('minIndex is different from both queries')
if (get('firstMaxIndex') <> get_XMLout_Element_String('/logs/log/logCurveInfo[mnemonic="$server_w2_wb1_log1_mnemonic_1$"]/maxIndex')):
    fail('maxIndex is different from both queries')
partial_success('minIndex and maxIndex match from both queries')    

# compare first and last index values in second response with minIndex and maxIndex
check_logData_IndexValue(0,get('firstMinIndex'))
check_logData_IndexValue(get_logData_NumberOfNodes_Int()-1,get('firstMaxIndex'))
partial_success('SQ-015 logData indexes are consistent with SQ-010 minIndex and maxIndex')

log('Script procedure end')
success()
