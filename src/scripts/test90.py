#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the Server supports SQ-004 (Get ID of all Wellbores)",
     reference =  "6.6.7  Standard Query Templates",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required =   ["WMLS_GetFromStore:wellbore"],
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

# Use GetFromStore using SQ-004 (Get ID of all Wellbores ) 
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0"?>
                                         <wellbores version="$server_schema_version$" xmlns="http://www.witsml.org/schemas/1series">
                                           <wellbore/>
                                         </wellbores>""",
                                      OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()


# Confirm that the three prerequisite wellbores are contained in the results of the query.
check_XMLout_ElementIncluded('wellbore[@uid="$server_w1_wb1_uid$" and @uidWell="$server_w1_uid$"]')
check_XMLout_ElementIncluded('wellbore[@uid="$server_w1_wb2_uid$" and @uidWell="$server_w1_uid$"]')
check_XMLout_ElementIncluded('wellbore[@uid="$server_w2_wb1_uid$" and @uidWell="$server_w2_uid$"]')
partial_success("Expected wellbores in the data model received")

# Verify that each wellbore returned contains the following and only the following:
# - uidWell
# - uid
# - nameWell
# - name
check_XMLout_ElementAttributesAndChildren('wellbore',
                                          ['wellbore[uidWell]', 'wellbore[uid]', 'name', 'nameWell'],
                                          match='exact')
partial_success("Only expected attributes and elements received for each wellbore")


log('Script procedure end')

success();
