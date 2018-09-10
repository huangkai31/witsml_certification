#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server recognizes a request with an empty column-identifier value in the column-description is interpreted as a request for header information for all columns.",
     reference =  "6.6.4.3  Special Handling for Growing Data-objects",
     reference_text = "For Systematically Growing Data Objects: If a client specifies an empty column-identifier value in the column-description, then the server MUST interpret it as a request for header information for all columns.",
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

# Use SQ-010 (Get Header for one Growing Data-object) for the log.
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                      <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <log uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_log1_uid$">                  
                                        </log>
                                      </logs>
                                  """,
                                  OptionsIn={'returnElements':'header-only'})  
check_ReturnValue_Success()

# compare expected list of curves from acutal list of curves.
check_XMLout_RecurringElementValue('logs/log/logCurveInfo/mnemonic', get('server_w1_wb1_log1_curves'))

partial_success("Server returned the expected log Curve mnemonics.")

log('Script procedure end')

success()
