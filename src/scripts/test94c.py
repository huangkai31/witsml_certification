#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server supports SQ-016 - What has changed since a specified time ( trajectory )",
     reference =  "6.6.5.17",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required =   ["WMLS_AddToStore:trajectory" , 
                                 "WMLS_DeleteFromStore:trajectory",
                                 "WMLS_UpdateInStore:trajectory",
                                 "WMLS_GetFromStore:changeLog" ],
     data_schemas = ["1.4.1.0", "1.4.1.1"],         
                                 
    )
##############
## SETUP     #
##############

log('Setup start')

# use a wellbore already added by the load_data_set
set("wellUid", "$server_w1_uid$")
set("wellboreUid", "$server_w1_wb1_uid$")
# get wellbore object
WMLS_GetFromStore(WMLTYPEIN_WELLBORE,"""
                  <wellbores xmlns='http://www.witsml.org/schemas/1series' version='$server_schema_version$'>
                        <wellbore uidWell='$wellUid$' uid='$wellboreUid$'/>
                  </wellbores>
                  """,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
set("well_name", get_XMLout_Element_String("wellbores/wellbore/nameWell"))
set("wellbore_name", get_XMLout_Element_String("wellbores/wellbore/name"))

partial_success("WMLS_GetFromStore succeeded wellbore")

log('Setup end')

#############
# TEST BODY #
#############  
log('Script procedure start')

set("trajectory_name", "Energistics Certification Trajectory Test94c")

WMLS_AddToStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
    <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
        <trajectory uidWell="$wellUid$" uidWellbore="$wellboreUid$">
            <nameWell>$well_name$</nameWell>
            <nameWellbore>$wellbore_name$</nameWellbore>
            <name>$trajectory_name$</name>
            <dTimTrajStart>2001-10-21T08:15:00.000Z</dTimTrajStart>
            <dTimTrajEnd>2001-11-03T16:30:00.000Z</dTimTrajEnd>
            <mdMn uom="ft">0</mdMn>
            <mdMx uom="ft">14089.3</mdMx>
            <serviceCompany>Anadrill</serviceCompany>
            <magDeclUsed uom="dega">-4.038</magDeclUsed>
            <gridCorUsed uom="dega">0.99961</gridCorUsed>
            <aziVertSect uom="dega">82.700</aziVertSect>
            <dispNsVertSectOrig uom="ft">0</dispNsVertSectOrig>
            <dispEwVertSectOrig uom="ft">0</dispEwVertSectOrig>
            <definitive>false</definitive>
            <memory>true</memory>
            <finalTraj>true</finalTraj>
            <aziRef>grid north</aziRef>
            <trajectoryStation uid="34ht5">
                <dTimStn>2001-10-21T08:15:00.000Z</dTimStn>
                <typeTrajStation>tie in point</typeTrajStation>
                <md uom="ft">0</md>
                <tvd uom="ft">0</tvd>
                <incl uom="dega">0</incl>
                <azi uom="dega">47.3</azi>
                <mtf uom="dega">47.3</mtf>
                <gtf uom="dega">0</gtf>
                <dispNs uom="ft">0</dispNs>
                <dispEw uom="ft">0</dispEw>
                <vertSect uom="ft">0</vertSect>
                <dls uom="dega/ft">0</dls>
                <rateTurn uom="dega/ft">0</rateTurn>
                <rateBuild uom="dega/ft">0</rateBuild>
                <mdDelta uom="ft">0</mdDelta>
                <tvdDelta uom="ft">0</tvdDelta>
                <modelToolError>good gyro</modelToolError>
                <gravTotalUncert uom="ft/s2">0</gravTotalUncert>
                <dipAngleUncert uom="dega">0</dipAngleUncert>
                <magTotalUncert uom="nT">0</magTotalUncert>
                <gravAccelCorUsed>false</gravAccelCorUsed>
                <magXAxialCorUsed>false</magXAxialCorUsed>
                <sagCorUsed>false</sagCorUsed>
                <magDrlstrCorUsed>false</magDrlstrCorUsed>
                <statusTrajStation>position</statusTrajStation>
                <rawData>
                    <gravAxialRaw uom="ft/s2">0.116</gravAxialRaw>
                    <gravTran1Raw uom="ft/s2">-0.168</gravTran1Raw>
                    <gravTran2Raw uom="ft/s2">-1654</gravTran2Raw>
                    <magAxialRaw uom="nT">22.77</magAxialRaw>
                    <magTran1Raw uom="nT">22.5</magTran1Raw>
                    <magTran2Raw uom="nT">27.05</magTran2Raw>
                </rawData>
                <corUsed>
                    <gravAxialAccelCor uom="ft/s2">0.11</gravAxialAccelCor>
                    <gravTran1AccelCor uom="ft/s2">0.14</gravTran1AccelCor>
                    <gravTran2AccelCor uom="ft/s2">0.13</gravTran2AccelCor>
                    <magAxialDrlstrCor uom="nT">0.17</magAxialDrlstrCor>
                    <magTran1DrlstrCor uom="nT">0.16</magTran1DrlstrCor>
                    <magTran2DrlstrCor uom="nT">0.24</magTran2DrlstrCor>
                    <sagIncCor uom="dega">0</sagIncCor>
                    <sagAziCor uom="dega">0</sagAziCor>
                    <stnMagDeclUsed uom="dega">-4.038</stnMagDeclUsed>
                    <stnGridCorUsed uom="dega">-0.4917</stnGridCorUsed>
                    <dirSensorOffset uom="ft">48.3</dirSensorOffset>
                </corUsed>
                <valid>
                    <magTotalFieldCalc uom="nT">51.19</magTotalFieldCalc>
                    <magDipAngleCalc uom="dega">41.5</magDipAngleCalc>
                    <gravTotalFieldCalc uom="ft/s2">0.999</gravTotalFieldCalc>
                </valid>
                <matrixCov>
                    <varianceNN uom="ft2">0.005236</varianceNN>
                    <varianceNE uom="ft2">0.005236</varianceNE>
                    <varianceNVert uom="ft2">2.356194</varianceNVert>
                    <varianceEE uom="ft2">0.005236</varianceEE>
                    <varianceEVert uom="ft2">0.005236</varianceEVert>
                    <varianceVertVert uom="ft2">0.785398</varianceVertVert>
                    <biasN uom="ft">0</biasN>
                    <biasE uom="ft">0</biasE>
                    <biasVert uom="ft">0</biasVert>
                </matrixCov>
                <location uid="loc-1">
                    <wellCRS uidRef="geog1">ED50</wellCRS>
                    <latitude uom="dega">59.755300</latitude>
                    <longitude uom="dega">1.71347417</longitude>
                </location>
                <location uid="loc-2">
                    <wellCRS uidRef="proj1">ED50 / UTM Zone 31N</wellCRS>
                    <easting uom="ft">427710.69</easting>
                    <northing uom="ft">6625015.54</northing>
                </location>
            </trajectoryStation>
            <commonData>
                <itemState>plan</itemState>
                <comments>These are the comments associated with the trajectory data object.</comments>
            </commonData>
        </trajectory>
    </trajectorys>
    """)
    
check_ReturnValue_Success()
partial_success("WMLS_AddToStore succeeded trajectory")

set('trajectoryUid', get_SuppMsgOut_uid_String())
log_variable('trajectoryUid')
new_object_created(WMLTYPEIN_TRAJECTORY, "$trajectoryUid$", uidWell="$wellUid$", uidWellbore="$wellboreUid$")

# 2. Get ChangeLogs
#get time for 1 hour ago.
set('dTim', timestamp_subtract_seconds(now(), 3600))
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                                <changeLog> 
                                                    <commonData>
                                                        <dTimLastChange>$dTim$</dTimLastChange>
                                                    </commonData>
                                                </changeLog>
                                        </changeLogs>
                                    """, OptionsIn = { 'returnElements':'latest-change-only' })  

check_ReturnValue_Success()
partial_success("GetFromStore changeLogs after Add succeeded ")

#check to see that the return is valid
check_XMLout_ValidWriteSchema()
partial_success("changeLogs returned are write schema valid ")

#check to see that no changeHistory's exist
check_XMLout_ElementNotIncluded('/changeLogs/changeLog/changeHistory')
partial_success("No changeHistory in changeLogs exist, succeed ")

#find added trajectory's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory"]/lastChangeType', 'add') 
partial_success("trajectory changeLog with only Add in lastChangeType succeed ")

# get add dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory" and lastChangeType="add"]/commonData/dTimLastChange')
partial_success("trajectory changeLog with only add has dTimLastChange succeed ")
addDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory" and lastChangeType="add"]/commonData/dTimLastChange')
set('dTim', addDTim)

# 3 Update the trajectory
WMLS_UpdateInStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="utf-8"?>
                                   <trajectorys xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <trajectory uidWell="$wellUid$" uidWellbore="$wellboreUid$" uid="$trajectoryUid$">
                                            <serviceCompany>Halliburton</serviceCompany>
                                      </trajectory>
                                   </trajectorys>
                                """)  
check_ReturnValue_Success()
partial_success("UpdateInStore trajectory succeeded ")

#4 ChangeLog for trajectory is update
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                                <changeLog> 
                                                    <commonData>
                                                        <dTimLastChange>$dTim$</dTimLastChange>
                                                    </commonData>
                                                </changeLog>
                                        </changeLogs>
                                    """, OptionsIn = { 'returnElements':'latest-change-only' })  

check_ReturnValue_Success()
partial_success("GetFromStore changeLogs after Update succeeded ")

#check to see that the return is valid
check_XMLout_ValidWriteSchema()
partial_success("changeLogs returned are write schema valid ")

#check to see that no changeHistory's exist
check_XMLout_ElementNotIncluded('/changeLogs/changeLog/changeHistory')
partial_success("No changeHistory in changeLogs exist, succeed ")

#find update trajectory's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory"]/lastChangeType', 'update') 
partial_success("trajectory changeLog with only update in lastChangeType succeed ")

# get update dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory" and lastChangeType="update"]/commonData/dTimLastChange')
partial_success("trajectory changeLog with only update has dTimLastChange succeed ")
updateDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory" and lastChangeType="update"]/commonData/dTimLastChange')

check_timestamp_Greaterthan(updateDTim, get('dTim'))
partial_success("trajectory changeLog with only update dTimLastChange > changeLog with Update succeed ")
set('dTim', updateDTim)

#5 Delete Trajectory
WMLS_DeleteFromStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="utf-8"?>
                                   <trajectorys xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <trajectory uidWell="$wellUid$" uidWellbore="$wellboreUid$" uid="$trajectoryUid$">
                                      </trajectory>
                                   </trajectorys>
                                """)  
check_ReturnValue_Success()
partial_success("DeleteFromStore trajectory succeeded ")

#6 ChangeLog for trajectory in Delete
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<changeLogs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                                <changeLog> 
                                                    <commonData>
                                                        <dTimLastChange>$dTim$</dTimLastChange>
                                                    </commonData>
                                                </changeLog>
                                        </changeLogs>
                                    """, OptionsIn = { 'returnElements':'latest-change-only' })  

check_ReturnValue_Success()
partial_success("GetFromStore changeLogs after Delete succeeded ")

#check to see that the return is valid
check_XMLout_ValidWriteSchema()
partial_success("changeLogs returned are write schema valid ")

#check to see that no changeHistory's exist
check_XMLout_ElementNotIncluded('/changeLogs/changeLog/changeHistory')
partial_success("No changeHistory in changeLogs exist, succeed ")

#find update trajectory's lastChangeType
check_XMLout_ElementValue('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory"]/lastChangeType', 'delete') 
partial_success("trajectory changeLog with only delete in lastChangeType succeed ")

# get delete dTimLastChange
check_XMLout_ElementIncluded('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory" and lastChangeType="delete"]/commonData/dTimLastChange')
partial_success("trajectory changeLog with only delete has dTimLastChange succeed ")
deleteDTim = get_XMLout_Element_String('/changeLogs/changeLog[@uidObject="$trajectoryUid$" and objectType="trajectory" and lastChangeType="delete"]/commonData/dTimLastChange')

check_timestamp_Greaterthan(deleteDTim, get('dTim'))
partial_success("trajectory changeLog with only delete dTimLastChange > changeLog with update succeed ")



log('Script procedure end')

success()
