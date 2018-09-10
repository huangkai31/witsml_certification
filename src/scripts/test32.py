#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Data Test - Compare newly added to retrieved Trajectory",
     reference =  "",
     reference_text = "",
     functionality_required =   ["WMLS_GetFromStore:trajectory",
                                 "WMLS_AddToStore:trajectory" ],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Setup start')

log("Retrieving well/wellbore name")
# get dataset well 1
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <wellbore uidWell="$server_w1_uid$" uid="$server_w1_wb1_uid$">
                                     </wellbore>
                                   </wellbores>
                                """, OptionsIn={'returnElements':'id-only'}) 
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
set('well_name', get_XMLout_Element_String('nameWell'))
set("wellbore_name", get_XMLout_Element_String('name'))
partial_success("retrieved well/wellbore name")

#############
# TEST BODY #
#############

# 1. Load the object

log('Script procedure start')
set("trajectory_name","Energistics Certification Trajectory Test32")

set('trajectory_xml',"""
<trajectorys xmlns="http://www.witsml.org/schemas/1series" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" version="$server_schema_version$">
    <trajectory uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">
        <nameWell>$well_name$</nameWell>
        <nameWellbore>$wellbore_name$</nameWellbore>
        <name>$trajectory_name$</name>
        <objectGrowing>false</objectGrowing>
        <dTimTrajStart>2001-10-21T08:15:00.000Z</dTimTrajStart>
        <dTimTrajEnd>2001-10-21T08:25:00.000Z</dTimTrajEnd>
        <mdMn uom="ft">0</mdMn>
        <mdMx uom="ft">1</mdMx>
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
        <trajectoryStation uid="1">
            <dTimStn>2001-10-21T08:15:00.000Z</dTimStn>
            <typeTrajStation>tie in point</typeTrajStation>
            <typeSurveyTool>magnetic MWD</typeSurveyTool>
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
            <gravTotalUncert uom="m/s2">0</gravTotalUncert>
            <dipAngleUncert uom="dega">0</dipAngleUncert>
            <magTotalUncert uom="nT">0</magTotalUncert>
            <gravAccelCorUsed>false</gravAccelCorUsed>
            <magXAxialCorUsed>false</magXAxialCorUsed>
            <sagCorUsed>false</sagCorUsed>
            <magDrlstrCorUsed>false</magDrlstrCorUsed>
            <infieldRefCorUsed>true</infieldRefCorUsed>
            <interpolatedInfieldRefCorUsed>false</interpolatedInfieldRefCorUsed>
            <inHoleRefCorUsed>true</inHoleRefCorUsed>
            <axialMagInterferenceCorUsed>false</axialMagInterferenceCorUsed>
            <cosagCorUsed>false</cosagCorUsed>
            <MSACorUsed>false</MSACorUsed>
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
                <easting uom="m">427710.69</easting>
                <northing uom="m">6625015.54</northing>
            </location>
        </trajectoryStation>
        <trajectoryStation uid="2">
            <dTimStn>2001-10-21T08:25:00.000Z</dTimStn>
            <typeTrajStation>tie in point</typeTrajStation>
            <typeSurveyTool>magnetic MWD</typeSurveyTool>
            <md uom="ft">1</md>
            <tvd uom="ft">10</tvd>
            <incl uom="dega">20</incl>
            <azi uom="dega">247.3</azi>
            <mtf uom="dega">247.3</mtf>
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
            <gravTotalUncert uom="m/s2">0</gravTotalUncert>
            <dipAngleUncert uom="dega">0</dipAngleUncert>
            <magTotalUncert uom="nT">0</magTotalUncert>
            <gravAccelCorUsed>false</gravAccelCorUsed>
            <magXAxialCorUsed>false</magXAxialCorUsed>
            <sagCorUsed>false</sagCorUsed>
            <magDrlstrCorUsed>false</magDrlstrCorUsed>
            <infieldRefCorUsed>true</infieldRefCorUsed>
            <interpolatedInfieldRefCorUsed>false</interpolatedInfieldRefCorUsed>
            <inHoleRefCorUsed>true</inHoleRefCorUsed>
            <axialMagInterferenceCorUsed>false</axialMagInterferenceCorUsed>
            <cosagCorUsed>false</cosagCorUsed>
            <MSACorUsed>false</MSACorUsed>
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
                <easting uom="m">427710.69</easting>
                <northing uom="m">6625015.54</northing>
            </location>
        </trajectoryStation>
        <commonData>
            <itemState>plan</itemState>
            <comments>These are the comments associated with the trajectory data object.</comments>
        </commonData>
    </trajectory>
</trajectorys>""")  


WMLS_AddToStore(WMLTYPEIN_TRAJECTORY, "$trajectory_xml$")  
check_ReturnValue_Success()
partial_success("WMLS_AddToStore succeeded trajectory")
set('uid', get_SuppMsgOut_uid_String())
log_variable('uid')
new_object_created(WMLTYPEIN_TRAJECTORY, "$uid$", uidWell="$server_w1_uid$", uidWellbore="$server_w1_wb1_uid$")

# 2. Get the object

WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="utf-8"?>
                                   <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <trajectory uid="$uid$" uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$"/>
                                   </trajectorys>
                                """, OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
partial_success("WMLS_GetFromStore succeeded trajectory")


# 3. Check the received object against the loaded object

check_XMLout_XMLNormalizedString(WMLTYPEIN_TRAJECTORY, "$trajectory_xml$")
partial_success("Object retrieved matches object loaded")


log('Script procedure end')

success()
