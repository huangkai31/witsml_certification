#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify server supports objectGrowing for trajectory object selection.",
     reference =  "7.2 for specific data-objects",
     reference_text = "objectGrowing:  In addition to the above items that a server MUST support for all data-objects, a server MUST support the following items for specific data-objects. If a server declares support for the specified data-object type, then the server MUST support the listed items for that data-object. For elements with a uom attribute, the server MUST also support the uom attribute.",
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

#Send SQ-008 (Get ID of all Instances of a Data-object in a Wellbore) for a trajectory with objectGrowing set to true
WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY,
                  """<trajectorys xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                         <trajectory uidWell='$server_w1_uid$' uidWellbore='$server_w1_wb1_uid$'>
							<objectGrowing>true</objectGrowing>
						 </trajectory>
                     </trajectorys>
                  """ ,OptionsIn={'returnElements':'id-only'} )
check_ReturnValue_Success()

# Verify server returns trajectories with objectGrowing = true.
check_XMLout_ElementIncluded('/trajectorys/trajectory[@uid="$server_w1_wb1_traj1_uid$"]')
partial_success("Server returned growing trajectory")
check_XMLout_ElementNotIncluded('/trajectorys/trajectory[@uid="$server_w1_wb1_traj2_uid$"]')
partial_success("Server did not return non-growing trajectory")

success()
