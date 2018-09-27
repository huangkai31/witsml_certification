#! /usr/bin/env python
#  
# Copyright 2014
# 
# Third Party Software
# Teytech Inc. Version 1.0
#
# Energistics 
# The following Energistics (c) products were used in the creation of this work: 
# 
# •             WITSML Data Schema Specifications, Version 1.4.1.1 
# 
# All rights in the WITSML™ Standard, the PRODML™ Standard, and the RESQML™ Standard, or
# any portion thereof, which remain in the Standards DevKit shall remain with Energistics
# or its suppliers and shall remain subject to the terms of the Product License Agreement
# available at http://www.energistics.org/product-license-agreement. 
# 
# Apache
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. 
# 
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. 
# 
# See the License for the specific language governing permissions and limitations under the
# License.
# 
# All rights reserved. 
# 
#
from wtl.witsml import *
import wtl.globals
import create_large_objects

test(
     purpose = "Load certification data set",
     reference =  "",
     reference_text = "",
    )

##########################################################################
# This script loads the certification data set to the server to be tested #
##########################################################################

# server_w1_uid
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid='Energistics-well-0001'/>                         
                                     </wells>
                                  """)  
check_ReturnValue_Success()

if (get_XMLout_NumberOfObjects_Int() == 1):
    WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                         <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                           <well uid="Energistics-well-0001"/>
                                         </wells>
                                         """, OptionsIn={"cascadedDelete":"true"})  
    check_ReturnValue_Success()

WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <well uid="Energistics-well-0001">
                                         <name>Energistics Certification Well 1</name>
                                         <numGovt>Energistics-numGovt-11111</numGovt>
                                         <dTimLicense>2001-05-15T13:20:00Z</dTimLicense>
                                         <field>Big Field</field>
                                         <country>US</country>
                                         <state>TX</state>
                                         <county>Montgomery</county>
                                         <region>Region Name</region>
                                         <district>District Name</district>
                                         <block>Block Name</block>
                                         <timeZone>-06:00</timeZone>
                                         <operator>Operating Company</operator>
                                         <operatorDiv>Division Name</operatorDiv>
                                         <pcInterest uom="%">65</pcInterest>
                                         <numAPI>Energistics-numAPI-11111</numAPI>
                                         <statusWell>drilling</statusWell>
                                         <purposeWell>exploration</purposeWell>
                                         <dTimSpud>2001-05-31T08:15:00Z</dTimSpud>
                                         <dTimPa>2001-07-15T15:30:00Z</dTimPa>
                                         <wellDatum uid="KB">
                                             <name>Kelly Bushing</name>
                                             <code>KB</code>
                                             <elevation uom="ft">78.5</elevation>
                                         </wellDatum>
                                         <wellCRS uid="proj1">
                                             <name>ED50 / UTM Zone 31N</name>
                                             <mapProjection>
                                                 <nameCRS namingSystem="epsg">ED50 / UTM Zone 31N</nameCRS>
                                                 <NADType>unknown</NADType>
                                             </mapProjection>
                                         </wellCRS>
                                         <wellCRS uid="geog1">
                                            <name>ED50</name>
                                            <geographic>
                                                <nameCRS namingSystem="epsg">ED50</nameCRS>
                                            </geographic>
                                         </wellCRS>
                                      </well>
                                   </wells>""")  
check_ReturnValue_Success()
partial_success("Added server_w1_uid successfully")

# server_w1_wb1_uid
WMLS_AddToStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <wellbore uidWell="Energistics-well-0001" uid="Energistics-w1-wellbore-0001">
                                         <nameWell>Energistics Certification Well 1</nameWell>
                                         <name>Energistics Certification Well 1 Wellbore 1</name>
                                      </wellbore>
                                   </wellbores>""")  
check_ReturnValue_Success()
partial_success("Added server_w1_wb1_uid successfully")

# server_w1_wb1_log1_uid - depth log
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="Energistics-well-0001" uidWellbore="Energistics-w1-wellbore-0001" uid="Energistics-w1-wb1-log-0001">
                                         <nameWell>Energistics Certification Well 1</nameWell>
                                         <nameWellbore>Energistics Certification Well 1 Wellbore 1</nameWellbore>
                                         <name>Energistics Certification Well 1 Wellbore 1 Log 1</name>
                                         <indexType>measured depth</indexType>
                                         <startIndex uom="m">0</startIndex>
                                         <endIndex uom="m">4</endIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP</indexCurve>
                                         <logCurveInfo uid='BDEP'>
                                           <mnemonic>BDEP</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>double</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE1'>
                                           <mnemonic>CURVE1</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE2'>
                                           <mnemonic>CURVE2</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE3'>
                                           <mnemonic>CURVE3</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>BDEP,CURVE1,CURVE2,CURVE3</mnemonicList>
                                           <unitList>m, m/h, m/h, m/h</unitList>
                                           <data>0,0,0,0</data>
                                           <data>1,1,1,1</data>
                                           <data>2,2,2,2</data>
                                           <data>3,3,3,3</data>
                                           <data>4,4,4,4</data>
                                         </logData>
                                      </log>
                                   </logs>""")  
check_ReturnValue_Success()
partial_success("Added server_w1_wb1_log1_uid successfully")

# make server_w1_wb1_log1_uid growing
#todo

# server_w1_wb1_log2_uid - time log
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="Energistics-well-0001" uidWellbore="Energistics-w1-wellbore-0001" uid="Energistics-w1-wb1-log-0002">
                                         <nameWell>Energistics Certification Well 1</nameWell>
                                         <nameWellbore>Energistics Certification Well 1 Wellbore 1</nameWellbore>
                                         <name>Energistics Certification Well 1 Wellbore 1 Log 2</name>
                                         <indexType>date time</indexType>
                                         <startDateTimeIndex>2012-07-26T15:17:20Z</startDateTimeIndex>
                                         <endDateTimeIndex>2012-07-26T15:17:50Z</endDateTimeIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>TIME</indexCurve>
                                         <logCurveInfo uid='TIME'>
                                           <mnemonic>TIME</mnemonic>
                                           <unit>unitless</unit>
                                           <typeLogData>date time</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='ROP'>
                                           <mnemonic>ROP</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>TIME,ROP</mnemonicList>
                                           <unitList>unitless,m/h</unitList>
                                           <data>2012-07-26T15:17:20Z,0</data>
                                           <data>2012-07-26T15:17:30Z,1</data>
                                           <data>2012-07-26T15:17:40Z,2</data>
                                           <data>2012-07-26T15:17:50Z,3</data>
                                         </logData>
                                      </log>
                                   </logs>""")  
check_ReturnValue_Success()
partial_success("Added server_w1_wb1_log2_uid successfully")

# server_w1_wb1_traj1_uid
if (wtl.globals.is_function_object_supported('WMLS_AddToStore' , WMLTYPEIN_TRAJECTORY) == True):
    WMLS_AddToStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
    <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
        <trajectory uidWell="Energistics-well-0001" uidWellbore="Energistics-w1-wellbore-0001" uid="Energistics-w1-wb1-trajectory-0001">
            <nameWell>Energistics Certification Well 1</nameWell>
            <nameWellbore>Energistics Certification Well 1 Wellbore 1</nameWellbore>
            <name>Energistics Certification Well 1 Wellbore 1 Trajectory 1</name>
            <dTimTrajStart>2001-10-21T08:15:00.000Z</dTimTrajStart>
            <dTimTrajEnd>2001-10-21T08:25:00.000Z</dTimTrajEnd>
            <mdMn uom="ft">0</mdMn>
            <mdMx uom="ft">14089.3</mdMx>
            <serviceCompany>Anadrill</serviceCompany>
            <magDeclUsed uom="dega">-4.038</magDeclUsed>
            <gridCorUsed uom="dega">0.99961</gridCorUsed>
            <aziVertSect uom="dega">82.700</aziVertSect>
            <dispNsVertSectOrig uom="ft">0</dispNsVertSectOrig>
            <dispEwVertSectOrig uom="ft">0</dispEwVertSectOrig>
            <definitive>true</definitive>
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
                <gravTotalUncert uom="m/s2">0</gravTotalUncert>
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
                    <easting uom="m">427710.69</easting>
                    <northing uom="m">6625015.54</northing>
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
    
    partial_success("Added server_w1_wb1_traj1_uid successfully")

# server_w1_wb1_traj2_uid
if (wtl.globals.is_function_object_supported('WMLS_AddToStore' , WMLTYPEIN_TRAJECTORY) == True):
    WMLS_AddToStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
    <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
        <trajectory uidWell="Energistics-well-0001" uidWellbore="Energistics-w1-wellbore-0001" uid="Energistics-w1-wb1-trajectory-0002">
            <nameWell>Energistics Certification Well 1</nameWell>
            <nameWellbore>Energistics Certification Well 1 Wellbore 1</nameWellbore>
            <name>Energistics Certification Well 1 Wellbore 1 Trajectory 2</name>
            <dTimTrajStart>2001-10-21T08:15:00.000Z</dTimTrajStart>
            <dTimTrajEnd>2001-10-21T08:25:00.000Z</dTimTrajEnd>
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
                <gravTotalUncert uom="m/s2">0</gravTotalUncert>
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
                    <easting uom="m">427710.69</easting>
                    <northing uom="m">6625015.54</northing>
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
    partial_success("Added server_w1_wb1_traj2_uid successfully")

# server_w1_wb2_uid
WMLS_AddToStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <wellbore uidWell="Energistics-well-0001" uid="Energistics-w1-wellbore-0002">
                                         <nameWell>Energistics Certification Well 1</nameWell>
                                         <name>Energistics Certification Wellbore 2</name>
                                      </wellbore>
                                   </wellbores>""")  
check_ReturnValue_Success()
partial_success("Added server_w1_wb2_uid successfully")

# server_w2_uid
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid='Energistics-well-0002'/>                         
                                     </wells>
                                  """)  
check_ReturnValue_Success()

if (get_XMLout_NumberOfObjects_Int() == 1):
    WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                         <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                           <well uid="Energistics-well-0002"/>
                                         </wells>
                                         """,OptionsIn={"cascadedDelete":"true"})  
    check_ReturnValue_Success()

WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <well uid="Energistics-well-0002">
                                         <name>Energistics Certification Well 2</name>
                                         <numGovt>Energistics-numGovt-22222</numGovt>
                                         <dTimLicense>2001-05-15T13:20:00Z</dTimLicense>
                                         <field>Big Field</field>
                                         <country>US</country>
                                         <state>TX</state>
                                         <county>Montgomery</county>
                                         <region>Region Name</region>
                                         <district>District Name</district>
                                         <block>Block Name</block>
                                         <timeZone>-06:00</timeZone>
                                         <operator>Operating Company</operator>
                                         <operatorDiv>Division Name</operatorDiv>
                                         <pcInterest uom="%">65</pcInterest>
                                         <numAPI>Energistics-numAPI-22222</numAPI>
                                         <statusWell>drilling</statusWell>
                                         <purposeWell>exploration</purposeWell>
                                         <dTimSpud>2001-05-31T08:15:00Z</dTimSpud>
                                         <dTimPa>2001-07-15T15:30:00Z</dTimPa>
                                      </well>
                                   </wells>""")  
check_ReturnValue_Success()
partial_success("Added server_w2_uid successfully")

# server_w2_wb1_uid
WMLS_AddToStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <wellbore uidWell="Energistics-well-0002" uid="Energistics-w2-wellbore-0001">
                                         <nameWell>Energistics Certification Well 2</nameWell>
                                         <name>Energistics Certification Well 2 Wellbore 1</name>
                                      </wellbore>
                                   </wellbores>""")  
check_ReturnValue_Success()
partial_success("Added server_w1_wb1_uid successfully")

# server_w2_wb1_log1_uid - depth log
WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="Energistics-well-0002" uidWellbore="Energistics-w2-wellbore-0001" uid="Energistics-w2-wb1-log-0001">
                                         <nameWell>Energistics Certification Well 2</nameWell>
                                         <nameWellbore>Energistics Certification Well 2 Wellbore 1</nameWellbore>
                                         <name>Energistics Certification Well 2 Wellbore 1 Log 1</name>
                                         <indexType>measured depth</indexType>
                                         <startIndex uom="m">0</startIndex>
                                         <endIndex uom="m">4</endIndex>
                                         <direction>increasing</direction>
                                         <indexCurve>BDEP</indexCurve>
                                         <logCurveInfo uid='BDEP'>
                                           <mnemonic>BDEP</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE1'>
                                           <mnemonic>CURVE1</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE2'>
                                           <mnemonic>CURVE2</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logCurveInfo uid='CURVE3'>
                                           <mnemonic>CURVE3</mnemonic>
                                           <unit>m/h</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                         <logData>
                                           <mnemonicList>BDEP,CURVE1,CURVE2,CURVE3</mnemonicList>
                                           <unitList>m, m/h, m/h, m/h</unitList>
                                           <data>0,0,0,0</data>
                                           <data>1,1,1,1</data>
                                           <data>2,2,2,2</data>
                                           <data>3,3,3,3</data>
                                           <data>4,4,4,4</data>
                                         </logData>
                                      </log>
                                   </logs>""")  
check_ReturnValue_Success()
partial_success("Added server_w2_wb1_log1_uid successfully")


##########
# well 3
##########

# server_w3_uid
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid='Energistics-well-0003'/>                         
                                     </wells>
                                  """)  
check_ReturnValue_Success()

if (get_XMLout_NumberOfObjects_Int() == 1):
    WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                         <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                           <well uid="Energistics-well-0003"/>
                                         </wells>
                                         """,OptionsIn={"cascadedDelete":"true"})  
    check_ReturnValue_Success()

WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <well uid="Energistics-well-0003">
                                         <name>Energistics Certification Well 3</name>
                                         <numGovt>Energistics-numGovt-22222</numGovt>
                                         <dTimLicense>2001-05-15T13:20:00Z</dTimLicense>
                                         <field>Big Field</field>
                                         <country>US</country>
                                         <state>TX</state>
                                         <county>Montgomery</county>
                                         <region>Region Name</region>
                                         <district>District Name</district>
                                         <block>Block Name</block>
                                         <timeZone>-06:00</timeZone>
                                         <operator>Operating Company</operator>
                                         <operatorDiv>Division Name</operatorDiv>
                                         <pcInterest uom="%">65</pcInterest>
                                         <numAPI>Energistics-numAPI-22222</numAPI>
                                         <statusWell>drilling</statusWell>
                                         <purposeWell>exploration</purposeWell>
                                         <dTimSpud>2001-05-31T08:15:00Z</dTimSpud>
                                         <dTimPa>2001-07-15T15:30:00Z</dTimPa>
                                      </well>
                                   </wells>""")  
check_ReturnValue_Success()
partial_success("Added server_w3_uid successfully")

# server_w3_wb1_uid
WMLS_AddToStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <wellbore uidWell="Energistics-well-0003" uid="Energistics-w3-wellbore-0001">
                                         <nameWell>Energistics Certification Well 3</nameWell>
                                         <name>Energistics Certification Well 3 Wellbore 1</name>
                                      </wellbore>
                                   </wellbores>""")  
check_ReturnValue_Success()
partial_success("Added server_w3_wb1_uid successfully")

# server_w3_wb1_mudlog1_uid
if (wtl.globals.is_function_object_supported('WMLS_AddToStore' , WMLTYPEIN_MUDLOG) == True):
    WMLS_AddToStore(WMLTYPEIN_MUDLOG, """<?xml version="1.0" encoding="utf-8"?>
                                    <mudLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <mudLog uidWell="Energistics-well-0003" uidWellbore="Energistics-w3-wellbore-0001" uid="Energistics-w3-wb1-mudlog-0001">
                                            <nameWell>Energistics Certification Well 3</nameWell>
                                            <nameWellbore>Energistics Certification Well 3 Wellbore 1</nameWellbore>
                                            <name>Energistics Certifications Well 3 Mudlog 1</name>
                                            <objectGrowing>true</objectGrowing>
                                            <dTim>2011-09-15T15:30:00.402Z</dTim>
                                            <mudLogCompany>Mud log company</mudLogCompany>
                                            <mudLogEngineers>Mud log Engineers</mudLogEngineers>
                                            <startMd uom="ft">8990</startMd>
                                            <endMd uom="ft">9420</endMd>
                                            <parameter uid="00001">
                                                <type>midnight depth date</type>
                                                <mdTop uom="ft">8920.19</mdTop>
                                                <mdBottom uom="ft">8920.19</mdBottom>
                                                <text>2011/09/15</text>
                                                <commonTime>
                                                    <dTimCreation>2011-09-15T00:00:00.000Z</dTimCreation>
                                                    <dTimLastChange>2011-09-15T00:00:00.000Z</dTimLastChange>
                                                </commonTime>
                                            </parameter>
                                            <parameter uid="00002">
                                                <type>core interval comment</type>
                                                <mdTop uom="ft">9010</mdTop>
                                                <mdBottom uom="ft">9070</mdBottom>
                                                <text>Core 3. Core 8 1/2 inches from 9010 MD to 9070 MD, recovered 98%</text>
                                                <commonTime>
                                                    <dTimCreation>2011-09-15T03:14:27.166Z</dTimCreation>
                                                    <dTimLastChange>2011-09-15T03:14:27.166Z</dTimLastChange>
                                                </commonTime>
                                            </parameter>
                                            <parameter uid="00003">
                                                <type>overpull on connection</type>
                                                <mdTop uom="ft">9195.42</mdTop>
                                                <mdBottom uom="ft">9195.42</mdBottom>
                                                <force uom="klbf">50</force>
                                                <text>50 Klb o/p on connection</text>
                                                <commonTime>
                                                    <dTimCreation>2011-09-15T04:37:51.819Z</dTimCreation>
                                                    <dTimLastChange>2011-09-15T04:37:51.819Z</dTimLastChange>
                                                </commonTime>
                                            </parameter>
                                            <geologyInterval uid="00001">
                                                <typeLithology>cuttings</typeLithology>
                                                <mdTop uom="ft">8990</mdTop>
                                                <mdBottom uom="ft">9420</mdBottom>
                                                <dTim>2011-09-15T02:45:36.381Z</dTim>
                                                <tvdTop uom="ft">7236.72</tvdTop>
                                                <tvdBase uom="ft">7680.39</tvdBase>
                                                <ropAv uom="ft/h">12</ropAv>
                                                <ropMn uom="ft/h">10</ropMn>
                                                <ropMx uom="ft/h">15</ropMx>
                                                <wobAv uom="lbf">6</wobAv>
                                                <tqAv uom="lbf.ft">600</tqAv>
                                                <rpmAv uom="rpm">120</rpmAv>
                                                <wtMudAv uom="lbm/ft3">10.5</wtMudAv>
                                                <ecdTdAv uom="lbm/ft3">10.6</ecdTdAv>
                                                <dxcAv>0.95</dxcAv>
                                                <lithology uid="00001">
                                                    <type>sandstone</type>
                                                    <description>Sandstone: vf-f, clr-frost, mod srt, gd vis por</description>
                                                    <color>frosted</color>
                                                    <texture>friable</texture>
                                                    <hardness>moderately hard</hardness>
                                                    <sizeGrain>fine sand</sizeGrain>
                                                    <roundness>well rounded</roundness>
                                                    <sorting>well sorted</sorting>
                                                    <matrixCement>calcite</matrixCement>
                                                    <porosityVisible>moderate</porosityVisible>
                                                    <permeability>fairly permeable</permeability>
                                                    <densShale uom="g/cm3">2.6</densShale>
                                                    <qualifier uid="00001">
                                                        <type>pyrite</type>
                                                        <abundance uom="%">10</abundance>
                                                        <description>lg crystals</description>
                                                    </qualifier>
                                                </lithology>
                                                <show>
                                                    <showRat>good</showRat>
                                                    <stainColor>brown</stainColor>
                                                    <stainDistr>even</stainDistr>
                                                    <stainPc uom="%">50</stainPc>
                                                    <natFlorColor>White</natFlorColor>
                                                    <natFlorPc uom="%">25</natFlorPc>
                                                    <natFlorLevel>faint</natFlorLevel>
                                                    <natFlorDesc>Nat Flor Desc</natFlorDesc>
                                                    <cutColor>white</cutColor>
                                                    <cutSpeed>fast</cutSpeed>
                                                    <cutStrength>strong</cutStrength>
                                                    <cutForm>streaming</cutForm>
                                                    <cutLevel>bright</cutLevel>
                                                    <cutFlorColor>bright white</cutFlorColor>
                                                    <cutFlorSpeed>instantaneous</cutFlorSpeed>
                                                    <cutFlorStrength>strong</cutFlorStrength>
                                                    <cutFlorForm>blooming</cutFlorForm>
                                                    <cutFlorLevel>bright</cutFlorLevel>
                                                    <residueColor>brown</residueColor>
                                                    <showDesc>Show Desc</showDesc>
                                                    <impregnatedLitho>Impregnated Litho</impregnatedLitho>
                                                    <odor>petrol</odor>
                                                </show>
                                                <chromatograph>
                                                    <dTim>2011-09-15T04:34:25.270Z</dTim>
                                                    <mdTop uom="ft">9210.41</mdTop>
                                                    <mdBottom uom="ft">9291.93</mdBottom>
                                                    <wtMudIn uom="lbm/ft3">10.5</wtMudIn>
                                                    <wtMudOut uom="lbm/ft3">10.5</wtMudOut>
                                                    <chromType>Flame Ion Detect</chromType>
                                                    <eTimChromCycle uom="s">30</eTimChromCycle>
                                                    <chromIntRpt>2011-09-15T04:29:33.579Z</chromIntRpt>
                                                    <methAv uom="ppm">600</methAv>
                                                    <methMn uom="ppm">500</methMn>
                                                    <methMx uom="ppm">700</methMx>
                                                    <ethAv uom="ppm">120</ethAv>
                                                    <ethMn uom="ppm">100</ethMn>
                                                    <ethMx uom="ppm">130</ethMx>
                                                    <propAv uom="ppm">45</propAv>
                                                    <propMn uom="ppm">40</propMn>
                                                    <propMx uom="ppm">70</propMx>
                                                    <ibutAv uom="ppm">10</ibutAv>
                                                    <ibutMn uom="ppm">5</ibutMn>
                                                    <ibutMx uom="ppm">15</ibutMx>
                                                    <nbutAv uom="ppm">10</nbutAv>
                                                    <nbutMn uom="ppm">10</nbutMn>
                                                    <nbutMx uom="ppm">10</nbutMx>
                                                    <ipentAv uom="ppm">1</ipentAv>
                                                    <ipentMn uom="ppm">1</ipentMn>
                                                    <ipentMx uom="ppm">1</ipentMx>
                                                    <npentAv uom="ppm">1</npentAv>
                                                    <npentMn uom="ppm">.099</npentMn>
                                                    <npentMx uom="ppm">.099</npentMx>
                                                    <epentAv uom="ppm">.099</epentAv>
                                                    <epentMn uom="ppm">.099</epentMn>
                                                    <epentMx uom="ppm">.099</epentMx>
                                                    <ihexAv uom="ppm">.099</ihexAv>
                                                    <ihexMn uom="ppm">.099</ihexMn>
                                                    <ihexMx uom="ppm">.099</ihexMx>
                                                    <nhexAv uom="ppm">.099</nhexAv>
                                                    <nhexMn uom="ppm">.099</nhexMn>
                                                    <nhexMx uom="ppm">.099</nhexMx>
                                                    <co2Av uom="ppm">.099</co2Av>
                                                    <co2Mn uom="ppm">.099</co2Mn>
                                                    <co2Mx uom="ppm">.099</co2Mx>
                                                    <h2sAv uom="ppm">0</h2sAv>
                                                    <h2sMn uom="ppm">0</h2sMn>
                                                    <h2sMx uom="ppm">0</h2sMx>
                                                    <acetylene uom="ppm">.099</acetylene>
                                                </chromatograph>
                                                <mudGas>
                                                    <gasAv uom="%">1.24</gasAv>
                                                    <gasPeak uom="%">1.4</gasPeak>
                                                    <gasPeakType>connection gas</gasPeakType>
                                                    <gasBackgnd uom="%">1</gasBackgnd>
                                                    <gasConAv uom="%">1.2</gasConAv>
                                                    <gasConMx uom="%">1.3</gasConMx>
                                                    <gasTrip uom="%">2.4</gasTrip>
                                                </mudGas>
                                                <densBulk uom="lbm/ft3">1.56</densBulk>
                                                <densShale uom="lbm/ft3">1.65</densShale>
                                                <calcite uom="%">6</calcite>
                                                <dolomite uom="%">1</dolomite>
                                                <cec uom="meq/g">.099</cec>
                                                <calcStab uom="%">.099</calcStab>
                                                <lithostratigraphic kind="formation">Rotliegende</lithostratigraphic>
                                                <chronostratigraphic kind="period">Permian</chronostratigraphic>
                                                <chronostratigraphic kind="epoch">Cisuralian</chronostratigraphic>
                                                <chronostratigraphic kind="stage">Sakmarian</chronostratigraphic>
                                                <sizeMn uom="in">.099</sizeMn>
                                                <sizeMx uom="in">.099</sizeMx>
                                                <lenPlug uom="in">.099</lenPlug>
                                                <description>Sandstone: vf-f, clr-frost, mod srt, gd vis por</description>
                                                <cuttingFluid>Chlorothene</cuttingFluid>
                                                <cleaningMethod>Agitene</cleaningMethod>
                                                <dryingMethod>Spin Dryer</dryingMethod>
                                                <commonTime>
                                                    <dTimCreation>2011-09-15T15:30:00.000Z</dTimCreation>
                                                    <dTimLastChange>2011-09-15T15:30:00.000Z</dTimLastChange>
                                                </commonTime>
                                            </geologyInterval>
                                        </mudLog>
                                    </mudLogs>""")  
    partial_success("Added server_w3_wb1_mudlog1_uid successfully")
    check_ReturnValue_Success()


# cleanup for Test 21
log('Cleanup Test 21')
WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="certification-Test-21"/>
                                     </wells>
                                     """ )

##############################
# build large logs for well 3
##############################


#obtain maxDataNodes and maxDataPoints
server_maxDataNodes = {}
server_maxDataNodes['WMLS_AddToStore'] = int(wtl.globals.get_maxDataNodes('WMLS_AddToStore', 'log'))
server_maxDataNodes['WMLS_GetFromStore'] = int(wtl.globals.get_maxDataNodes('WMLS_GetFromStore', 'log'))
server_maxDataNodes['WMLS_UpdateInStore'] = int(wtl.globals.get_maxDataNodes('WMLS_UpdateInStore', 'log'))

server_maxDataPoints = {}
server_maxDataPoints['WMLS_AddToStore'] = int(wtl.globals.get_maxDataPoints('WMLS_AddToStore', 'log'))
server_maxDataPoints['WMLS_GetFromStore'] = int(wtl.globals.get_maxDataPoints('WMLS_GetFromStore', 'log'))
server_maxDataPoints['WMLS_UpdateInStore'] = int(wtl.globals.get_maxDataPoints('WMLS_UpdateInStore', 'log'))

create_large_objects.create_log_maxDataNodes("Energistics-well-0003",
         "Energistics-w3-wellbore-0001",
         "Energistics-w3-wb1-log-0001",
         "Energistics Certification Well 3",
         "Energistics Certification Well 3 Wellbore 1",
         "Energistics Certification Well 3 Wellbore 1 Log 1",
         "measured depth",
         server_maxDataNodes)
partial_success("Added server_w3_wb1_log1_uid successfully")    

create_large_objects.create_log_maxDataNodes("Energistics-well-0003",
         "Energistics-w3-wellbore-0001",
         "Energistics-w3-wb1-log-0003",
         "Energistics Certification Well 3",
         "Energistics Certification Well 3 Wellbore 1",
         "Energistics Certification Well 3 Wellbore 1 Log 3",
         "date time",
         server_maxDataNodes)
partial_success("Added server_w3_wb1_log3_uid successfully")    

create_large_objects.create_log_maxDataPoints("Energistics-well-0003",
         "Energistics-w3-wellbore-0001",
         "Energistics-w3-wb1-log-0002",
         "Energistics Certification Well 3",
         "Energistics Certification Well 3 Wellbore 1",
         "Energistics Certification Well 3 Wellbore 1 Log 2",
         "measured depth",
         server_maxDataPoints)
partial_success("Added server_w3_wb1_log2_uid successfully")    

create_large_objects.create_log_maxDataPoints("Energistics-well-0003",
         "Energistics-w3-wellbore-0001",
         "Energistics-w3-wb1-log-0004",
         "Energistics Certification Well 3",
         "Energistics Certification Well 3 Wellbore 1",
         "Energistics Certification Well 3 Wellbore 1 Log 4",
         "date time",
         server_maxDataPoints)
partial_success("Added server_w3_wb1_log4_uid successfully")   

# wait for the above changes to be detected by the server.
pause_for_changeDetectionPeriod()

success()
