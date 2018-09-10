#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify that the GetFromStore optionsIn id-only is supported for a Trajectory",
     reference =  "6.6.2.1 OptionsIn Keywords",
     reference_text = "A server MUST support subject to rights-management constraints - a request for only the identity uid name parentage-pointers and parentage names. For all of a particular data-object type e.g., trajectory that have a particular parent wellbore and well.",
     functionality_required =   ["WMLS_GetFromStore:trajectory"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed for this test.')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

#Call SQ-008 (Get ID of all Instances of a Data-object in a Wellbore) for Trajectories passing the uid of a Trajectory.
WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
                                     <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_traj1_uid$" /> 
                                     </trajectorys>
                                  """,OptionsIn={'returnElements':'id-only'})
check_ReturnValue_Success()

##Ensure the returned trajectory contains the following:
## a uidWell matching the Well’s uid element.
## a uidWellbore matching the Wellbore’s uid element.
## a uid matching the Trajectory uid
## the well's name 'uidWell'
## the wellbores's name 'uidWellbore'
## the trajectory's name 'uid'
##No other elements are returned. 
check_XMLout_OnlyIncluded( ['trajectorys', 'trajectorys[version]','trajectory', 'trajectory[uidWell]' , 'trajectory[uidWellbore]', 'trajectory[uid]','nameWell', 'nameWellbore', 'name' ] )
check_XMLout_AttributeValue("trajectory","uidWell", "$server_w1_uid$")
check_XMLout_AttributeValue("trajectory","uidWellbore","$server_w1_wb1_uid$")
check_XMLout_AttributeValue('trajectory','uid', '$server_w1_wb1_traj1_uid$') 

partial_success("GetFromStore optionsIn id-only is supported for a Trajectory")
log('Script procedure end')
success()
