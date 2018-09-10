#! /usr/bin/env python
from wtl.witsml import *

test(purpose = "Verify the Server supports SQ-011 (Get Header for all Growing Data-objects in a Wellbore) for a trajectory",
     reference =  "6.6.7 Standard Query Templates",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required = ["WMLS_GetFromStore:trajectory"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],)

#########
# SETUP #
#########

log('Script procedure start')


WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
                                     <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <trajectory 
                                                     uidWell="$server_w1_uid$" 
                                                     uidWellbore="$server_w1_wb1_uid$">
                                         </trajectory>
                                         
                                     </trajectorys>
                                  """,
                                  OptionsIn={'returnElements':'header-only'})  
check_ReturnValue_Success()

check_XMLout_NumberOfObjects_Greaterthan(0)     
partial_success("trajectory objects received");

check_XMLout_ElementIncluded("nameWell", check='all_objects')
check_XMLout_ElementIncluded("nameWellbore", check='all_objects')
check_XMLout_ElementIncluded("name", check='all_objects')
partial_success("All required elements are included");

check_XMLout_ElementNotIncluded("trajectoryStation")
partial_success("trajectoryStation is not included");

log('Script procedure end')

success();    


