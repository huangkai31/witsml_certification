#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the Server supports SQ-012 (Get Data for Growing Data-object) for Mudlog",
     reference =  "6.6.7 Standard Query Templates",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required = ["WMLS_GetFromStore:mudLog"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed for this test.')

#############
# TEST BODY #
#############

log('Script procedure start')

# Use SQ-012 (Get Data for Growing Data-object) for the Modlog. OptionsIn='returnElements=data-only'
WMLS_GetFromStore(WMLTYPEIN_MUDLOG, """<?xml version="1.0" encoding="utf-8"?>
                                       <mudLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <mudLog uidWell="$server_w3_uid$" uidWellbore="$server_w3_wb1_uid$"
                                                 uid="$server_w3_wb1_mudlog1_uid$"/>
                                       </mudLogs>""",
                                    OptionsIn={'returnElements':'data-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)     

# The query returns the mudLog with  one or more geologyInterval elements and one or more parameter elements and no header.
check_XMLout_ElementAttributesAndChildren('mudLog',
                                          ['mudLog[uidWell]', 'mudLog[uidWellbore]', 'mudLog[uid]', 'geologyInterval', 'parameter'],
                                          match='at-most')
partial_success("Only geologyInterval and parameter are included in each mudLog")

# Each mdTop, mdBottom contains all mandatory attributes for geologyInterval and parameter elements
check_XMLout_ElementAttributesAndChildren('mdTop', ['mdTop[uom]' ],
                                          match='at-least')
check_XMLout_ElementAttributesAndChildren('mdBottom', ['mdBottom[uom]' ],
                                          match='at-least')

# Each geologyInterval contains all mandatory properties.
check_XMLout_ElementAttributesAndChildren('geologyInterval',
                                          ['geologyInterval[uid]', 'typeLithology', 'mdTop', 'mdBottom'],
                                          match='at-least')
partial_success("All mandatory elements and attributes included for all geologyInterval")

# Each parameter contains all mandatory properties.
check_XMLout_ElementAttributesAndChildren('parameter',
                                          ['parameter[uid]', 'type', 'mdTop', 'mdBottom'],
                                          match='at-least')
partial_success("All mandatory elements and attributes included for all parameter")

log('Script procedure end')

success();    


