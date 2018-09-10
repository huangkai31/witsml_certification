#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify objectGrowing functionality for append behaviour for trajectories.",
     reference =  "9.3.2.1 Logic for Setting objectGrowing Flags",
     reference_text = "When an append occurs for a growing data-object and objectGrowing = false, then the server sets objectGrowing = true. If a server receives no data to append to a growing data-object in that data-objects growingTimeoutPeriod, then the server MUST set objectGrowing = false indicating to clients that the data-object is not actively being updated.",
     functionality_required = ["WMLS_GetFromStore:trajectory",
                               "WMLS_AddToStore:trajectory",
                               "WMLS_UpdateInStore:trajectory"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Setup start')

log("Retrieving well and wellbore name")
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <wellbore uidWell="$server_w1_uid$" uid="$server_w1_wb1_uid$"/>
                                     </wellbores>
                                  """, OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success();
set('well_name', get_XMLout_Element_String('nameWell'))
set('wellbore_name', get_XMLout_Element_String('name'))

log('Setup end')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

set ("server_w1_wb1_test80_trajstn1_uid", "test80trajstn1")
set ("server_w1_wb1_test80_trajstn2_uid", "test80trajstn2")

#Create a new trajectory with 1 trajectoryStation.
WMLS_AddToStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
<trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
    <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">
        <nameWell>$well_name$</nameWell>
        <nameWellbore>$wellbore_name$</nameWellbore>
        <name>Energistics Certification Well 1 Wellbore 1 Trajectory 80</name>
        <dTimTrajStart>2001-10-21T08:15:00.000Z</dTimTrajStart>
        <dTimTrajEnd>2001-11-03T16:30:00.000Z</dTimTrajEnd>
        <mdMn uom="ft">0</mdMn>
        <mdMx uom="ft">14089.3</mdMx>
        <trajectoryStation uid="$server_w1_wb1_test80_trajstn1_uid$">
            <dTimStn>2001-10-21T08:15:00.000Z</dTimStn>
            <typeTrajStation>tie in point</typeTrajStation>
            <md uom="ft">0</md>
            <tvd uom="ft">0</tvd>
        </trajectoryStation>
    </trajectory>
</trajectorys>
""")

#AddToStore is successful
check_ReturnValue_Success()
set('server_w1_wb1_test80_trajectory1_uid', get_SuppMsgOut_uid_String())
new_object_created(WMLTYPEIN_TRAJECTORY, "$server_w1_wb1_test80_trajectory1_uid$", uidWellbore="$server_w1_wb1_uid$", uidWell="$server_w1_uid$")

#Wait for changeDetectionPeriod + 1 second.
pause_for_changeDetectionPeriod()
pause(1)

#Use SQ-009 (Get Details for a Specific Data-object) for the trajectory object.
WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY,
                  """<trajectorys xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                        <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_test80_trajectory1_uid$" />
                    </trajectorys>
                  """ ,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()


#In the first GetFromStore query, confirm objectGrowing = false.
check_XMLout_ElementValue("objectGrowing","false")
partial_success("ObjectGrowing stays false when adding a new trajectory with a trajectoryStation")

#Update a trajectoryStation.
WMLS_UpdateInStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
<trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
    <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_test80_trajectory1_uid$">
        <trajectoryStation uid="$server_w1_wb1_test80_trajstn1_uid$">
            <dTimStn>2001-10-21T08:15:00.000Z</dTimStn>
            <typeTrajStation>tie in point</typeTrajStation>
            <md uom="ft">0</md>
            <tvd uom="ft">100</tvd>
        </trajectoryStation>
    </trajectory>
</trajectorys>""")

#UpdateInStore is successful
check_ReturnValue_Success()

#Wait for changeDetectionPeriod + 1 second.
pause_for_changeDetectionPeriod()
pause(1)

#Use SQ-009 (Get Details for a Specific Data-object) for the trajectory object.
WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY,
                  """<trajectorys xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                        <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_test80_trajectory1_uid$" />
                    </trajectorys>
                  """ ,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()

#In the second GetFromStore query, confirm objectGrowing = false.
check_XMLout_ElementValue("objectGrowing","false")
partial_success("ObjectGrowing stays false when updating a trajectory station")

#Add a trajectoryStation to the trajectory.
WMLS_UpdateInStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
<trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
    <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_test80_trajectory1_uid$">
        <trajectoryStation uid="$server_w1_wb1_test80_trajstn2_uid$">
            <dTimStn>2001-10-21T08:15:00.000Z</dTimStn>
            <typeTrajStation>tie in point</typeTrajStation>
            <md uom="ft">100</md>
            <tvd uom="ft">200</tvd>
        </trajectoryStation>
    </trajectory>
</trajectorys>""")

#UpdateInStore is successful
check_ReturnValue_Success()

#Wait for changeDetectionPeriod + 1 second.
pause_for_changeDetectionPeriod()
pause(1)

#Use SQ-009 (Get Details for a Specific Data-object) for the trajectory object.
WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY,
                  """<trajectorys xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                        <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$" uid="$server_w1_wb1_test80_trajectory1_uid$" />
                    </trajectorys>
                  """ ,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()

#In the third GetFromStore query, confirm objectGrowing = true.
check_XMLout_ElementValue("objectGrowing","true")
partial_success("ObjectGrowing turns true when adding a new trajectory station")

partial_success("ObjectGrowing functionality for append behaviour of trajectories has been verified.")
log('Script procedure end')

success()
