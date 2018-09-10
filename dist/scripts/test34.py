#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Data Test - Compare newly added to retrieved MudLog",
     reference =  "",
     reference_text = "",
     functionality_required =   ["WMLS_GetFromStore:mudLog",
                                 "WMLS_AddToStore:mudLog" ],
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

log('Script procedure start')

# 1. Load the object

set("mudLog_name","Energistics Certification MudLog Test34")

set('mudLog_xml',"""
<mudLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
    <mudLog uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$">
        <nameWell>$well_name$</nameWell>
        <nameWellbore>$wellbore_name$</nameWellbore>
        <name>$mudLog_name$</name>
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
            <wobAv uom="klbf">6</wobAv>
            <tqAv uom="kft.lbf">600</tqAv>
            <rpmAv uom="rpm">120</rpmAv>
            <wtMudAv uom="lbm/galUS">10.5</wtMudAv>
            <ecdTdAv uom="lbm/galUS">10.6</ecdTdAv>
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
                <wtMudIn uom="lbm/galUS">10.5</wtMudIn>
                <wtMudOut uom="lbm/galUS">10.5</wtMudOut>
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
            <densBulk uom="g/cm3">1.56</densBulk>
            <densShale uom="g/cm3">1.65</densShale>
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
        <commonData>
            <dTimCreation>2011-09-14T19:26:42.129Z</dTimCreation>
            <dTimLastChange>2011-09-15T16:15:33.591Z</dTimLastChange>
            <itemState>actual</itemState>
            <defaultDatum uidRef="KB">Kelly Bushing</defaultDatum>
        </commonData>
    </mudLog>
</mudLogs>""")  

WMLS_AddToStore(WMLTYPEIN_MUDLOG, "$mudLog_xml$")  
check_ReturnValue_Success()
partial_success("WMLS_AddToStore succeeded mudLog")
set('uid', get_SuppMsgOut_uid_String())
log_variable('uid')
new_object_created(WMLTYPEIN_MUDLOG, "$uid$", uidWell="$server_w1_uid$", uidWellbore="$server_w1_wb1_uid$")

# 2. Get the object

WMLS_GetFromStore(WMLTYPEIN_MUDLOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <mudLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <mudLog uid="$uid$" uidWell="$server_w1_uid$" uidWellbore="$server_w1_wb1_uid$"/>
                                   </mudLogs>
                                """, OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
partial_success("WMLS_GetFromStore succeeded mudLog")


# 3. Check the received object against the loaded object

check_XMLout_XMLNormalizedString(WMLTYPEIN_MUDLOG, "$mudLog_xml$")
partial_success("Object retrieved matches object loaded")


log('Script procedure end')

success()
