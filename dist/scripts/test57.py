#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the Server returns the expected wellbore(s) when receiving a SQ-007  ( Get Details for all Wellbores in a Well )",
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


# get the list of wellbores for the choosen well, i.e. SQ-007
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0"?>
                                     <wellbores version="$server_schema_version$" xmlns="http://www.witsml.org/schemas/1series">
                                         <wellbore uidWell="$server_w1_uid$">
                                         </wellbore>
                                     </wellbores>
                                  """, OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()


# should have received more than one wellbore
check_XMLout_NumberOfObjects_Greaterthan(1)  

partial_success("Have more than 1 wellbore under desired well")

# check mandatory elements and attributes
check_XMLout_ElementIncluded("nameWell", check='all_objects')
check_XMLout_ElementIncluded("name", check='all_objects')

check_XMLout_AttributeIncluded('../wellbore', 'uidWell', check='all_objects')
check_XMLout_AttributeIncluded('../wellbore', 'uid', check='all_objects')

partial_success("All mandatory properties exist in all wellbores") 

check_XMLout_AttributeValue('../wellbore','uidWell', "$server_w1_uid$", check='all_objects')

partial_success("All wellbores have the correct uidWell")
     

log('Script procedure end')

success();
