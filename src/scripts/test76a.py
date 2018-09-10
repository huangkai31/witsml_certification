#! /usr/bin/env python
from wtl.witsml import *



test(
     purpose = "Verify the server supports requestLatestValues behavior for an increasing time log",
     reference =  "6.6.2.1",
     reference_text = "DEFAULT: normal log behavior. A server MUST support this option. If specified, return the latest n values from each curve in a log data-object. ",
     functionality_required =   ["WMLS_GetFromStore:log" ],    
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

#############
# TEST BODY #
#############

log('Script procedure start')

log("Retrieving log")
# Use SQ-015 (Get Log) specifying OptionsIn = requestLatestValues = 1
WMLS_GetFromStore(WMLTYPEIN_LOG,
                  """<logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                           <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_log2_uid$">
                           </log>
                     </logs>"""
                  ,OptionsIn={'returnElements':'all', 'requestLatestValues':'1'})

check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

partial_success("GetFromStore (requestLatestValues = 1) returned successfully. ")

# validate log 
log_verify_check_requestLatestValue_header_and_data(numberOfExpectedValues=1)

partial_success("log_verify_check_requestLatestValue_header_and_data returned successfully. ")

mnemonicList = get_XMLout_Mnemonics_List()
  
# get order list of maxDateTimeIndex(s)
listMaxIndexRequestLatestValue = get_XMLout_RecurringElementViaKey_List("logCurveInfo", mnemonicList, "mnemonic", "maxDateTimeIndex")
   
# Use SQ-010 (Get Log Header) 
WMLS_GetFromStore(WMLTYPEIN_LOG, 
                  """<logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                           <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_log2_uid$">
                           </log>
                     </logs>"""
                    ,OptionsIn={'returnElements':'header-only'} )
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

partial_success("GetFromStore header-only returned successfully. ")

log_verify_check_log_header_only()

partial_success("log_verify_check_log_header_only returned successfully. ")

listMaxIndexHeader = get_XMLout_RecurringElementViaKey_List("logCurveInfo", mnemonicList, "mnemonic", "maxDateTimeIndex")

if listMaxIndexRequestLatestValue != listMaxIndexHeader:
    fail("Server returned an incorrect maxDateTimeIndex for each curve between queries")


partial_success('Server returned the correct maxDateTimeIndex for each curve between queries')

log('Script procedure end')

success()