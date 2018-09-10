#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the Server supports SQ-013 (Get Restricted Data Subset)",
     reference =  "6.6.7 Standard Query Templates",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required = ["WMLS_GetFromStore:trajectory"],
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

# Use SQ-013 (Get Restricted Data Subset) for the Trajectory. OptionsIn='station-location-only'
WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
                                           <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                             <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$"
                                                         uid="$server_w1_wb1_traj1_uid$"/>
                                           </trajectorys>""",
                                        OptionsIn={'returnElements':'station-location-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)     

# The query returns the trajectory with  one or more trajectoryStation elements and no header.
check_XMLout_ElementAttributesAndChildren('trajectory',
                                          ['trajectory[uidWell]', 'trajectory[uidWellbore]', 'trajectory[uid]', 'trajectoryStation'],
                                          match='at-most')

# confirm one or more trajectoryStation elements
check_XMLout_ElementIncluded('trajectoryStation')
partial_success("Only trajectoryStation are included in each trajectory")

# Each trajectoryStation contains all mandatory properties.
check_XMLout_ElementAttributesAndChildren('trajectoryStation',
                                          ['trajectoryStation[uid]', 'typeTrajStation', 'md'],
                                          match='at-least')
check_XMLout_ElementAttributesAndChildren('md', ['md[uom]' ],
                                          match='at-least')
partial_success("All mandatory elements and attributes included for all trajectoryStation")

# Each trajectoryStation does not contain anything except the allowed elements for station-location-only.
check_XMLout_ElementAttributesAndChildren('trajectoryStation',
                                          ['trajectoryStation[uid]', 'dTimStn', 'typeTrajStation', 'md', 'tvd', 'incl', 'azi', 'location'],
                                          match='at-most')
partial_success("Only station-location-only elements returned in each trajectoryStation")


log('Script procedure end')

success();    


