#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server supports SQ-018 - What changes have been made in a mudLog or multiple mudLogs since a specified time",
     reference =  "6.6.5",
     reference_text = "All WITSML servers that support the function MUST support these queries",
     functionality_required =   ['WMLS_GetFromStore:changeLog',
                                 'WMLS_GetFromStore:mudLog',
                                 'WMLS_GetFromStore:wellbore',
                                 'WMLS_AddToStore:mudLog',
                                 'WMLS_UpdateInStore:mudLog',
                                 'WMLS_DeleteFromStore:mudLog'],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########
           
log('Setup start')

log("Retrieving well and wellbore name")
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <wellbore uidWell="$server_w3_uid$" uid="$server_w3_wb1_uid$"/>
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

log('Script start')

#Call AddToStore to create a new mudLog
WMLS_AddToStore(WMLTYPEIN_MUDLOG, """<?xml version="1.0" encoding="UTF-8"?>
                                    <mudLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <mudLog uidWell="$server_w3_uid$" uidWellbore="$server_w3_wb1_uid$">
                                            <nameWell>$well_name$</nameWell>
                                            <nameWellbore>$wellbore_name$</nameWellbore>
                                            <name>Energistics Certification Mudlog Test61</name>
                                            <objectGrowing>true</objectGrowing>
                                            <dTim>2011-09-15T15:30:00.402Z</dTim>
                                            <mudLogCompany>Mud log company</mudLogCompany>
                                            <mudLogEngineers>Mud log Engineers</mudLogEngineers>
                                            <startMd uom="ft">8990</startMd>
                                            <endMd uom="ft">9420</endMd>
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
check_ReturnValue_Success()
set('mudLog_uid', get_SuppMsgOut_uid_String())
log_variable('mudLog_uid')
new_object_created(WMLTYPEIN_MUDLOG, "$mudLog_uid$", uidWell="$server_w3_uid$", uidWellbore="$server_w3_wb1_uid$")

# Call GetfromStore to retrieve the dTimLastChange of the mudLog object. 
WMLS_GetFromStore(WMLTYPEIN_MUDLOG, """<?xml version="1.0" encoding="utf-8"?>
                                    <mudLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <mudLog uidWell="$server_w3_uid$" uidWellbore="$server_w3_wb1_uid$" uid="$mudLog_uid$">
                                          <commonData>
                                            <dTimLastChange/>
                                          </commonData>
                                        </mudLog>
                                    </mudLogs>""")  
check_ReturnValue_Success()
set('tml', get_XMLout_Element_String('dTimLastChange'))

# Pause for at least one second to make sure the update time is different that the dTimLastChange
pause(1)

# Call UpdateInStore to update a single geologyInterval without doing an append. 
WMLS_UpdateInStore(WMLTYPEIN_MUDLOG,"""<?xml version="1.0" encoding="UTF-8"?>
                                    <mudLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <mudLog uidWell="$server_w3_uid$" uidWellbore="$server_w3_wb1_uid$" uid="$mudLog_uid$">
                                            <geologyInterval uid="00001">
                                                <mdTop uom="ft">8000</mdTop> 
                                                <mdBottom uom="ft">9000</mdBottom>
                                            </geologyInterval>
                                        </mudLog>
                                    </mudLogs>""")  
check_ReturnValue_Success()

# Call DeleteFromStore to delete a single geologyInterval. 
WMLS_DeleteFromStore(WMLTYPEIN_MUDLOG,"""<?xml version="1.0" encoding="UTF-8"?>
                                    <mudLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                        <mudLog uidWell="$server_w3_uid$" uidWellbore="$server_w3_wb1_uid$" uid="$mudLog_uid$">
                                            <geologyInterval uid="00001"/>
                                        </mudLog>
                                    </mudLogs>""")  
check_ReturnValue_Success()

# Now we have to make sure the changes are detected by the server
pause_for_changeDetectionPeriod()

# Use SQ-018 with a dTimLastChange and dTimChange of the mudLog from the first GetFromStore query.
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<?xml version="1.0" encoding="UTF-8"?>
                                          <changeLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                            <changeLog uidObject="$mudLog_uid$" uidWellbore="$server_w3_wb1_uid$" uidWell="$server_w3_uid$">
                                                <objectType>mudLog</objectType>
                                                <changeHistory>
                                                    <dTimChange>$tml$</dTimChange>
                                                </changeHistory>
                                                <commonData>
                                                    <dTimLastChange>$tml$</dTimLastChange>
                                                </commonData>
                                            </changeLog>
                                          </changeLogs>
                                       """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

# Verify that the response contains a ChangeLog object for the corresponding mudLog with only
# two changeHistory entries with changeType = 'update' and dTimChange is greater than the provided dTimChange
check_XMLout_AttributeValue('changeLog', 'uidWell','$server_w3_uid$')
check_XMLout_AttributeValue('changeLog', 'uidWellbore','$server_w3_wb1_uid$')
check_XMLout_AttributeValue('changeLog', 'uidObject','$mudLog_uid$')
partial_success('The correct changeLog object received')

check_XMLout_RecurringElementValue('changeType', ['update', 'update'])
partial_success("Two 'update' changeHistory entries received")

times = get_XMLout_RecurringElement_List('dTimChange')   
check_timestamp_Greaterthan(times[0], get('tml'))
partial_success('dTimChange of first changeHistory entry is correct')
check_timestamp_Greaterthan(times[1], get('tml'))  
partial_success('dTimChange of second changeHistory entry is correct')

log('Script procedure end')

success()
