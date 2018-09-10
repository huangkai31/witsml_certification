#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Data Test - Compare newly added to retrieved Wellbore",
     reference =  "",
     reference_text = "",
     functionality_required =   ["WMLS_GetFromStore:wellbore",
                                 "WMLS_AddToStore:wellbore" ],
     data_schemas = ["1.4.1.0",  "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Setup start')

log("Retrieving well name")

# get dataset well 1
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <well uid="$server_w1_uid$">
                                     </well>
                                   </wells>
                                """, OptionsIn={'returnElements':'id-only'}) 
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
set('well_name', get_XMLout_Element_String('name'))
partial_success("retrieved well name")

#############
# TEST BODY #
#############

log('Script procedure start')

set("wellbore_name", "Energistics Certification Wellbore Test27")
set('wellbore_xml', """<wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
<wellbore uidWell="$server_w1_uid$">
        <nameWell>$well_name$</nameWell>
        <name>$wellbore_name$</name>
        <number>1234-0987</number>
        <suffixAPI>02</suffixAPI>
        <numGovt>Govt001</numGovt>
        <statusWellbore>active</statusWellbore>
        <isActive>true</isActive>
        <purposeWellbore>exploration</purposeWellbore>
        <typeWellbore>initial</typeWellbore>
        <shape>horizontal</shape>
        <dTimKickoff>2001-03-15T13:20:00.000Z</dTimKickoff>
        <achievedTD>true</achievedTD>
        <md uom="ft">0</md>
        <tvd uom="ft">0</tvd>
        <mdBit uom="ft" datum="KB">0</mdBit>
        <tvdBit uom="ft" datum="KB">0</tvdBit>
        <mdKickoff uom="ft">0</mdKickoff>
        <tvdKickoff uom="ft">0</tvdKickoff>
        <mdPlanned uom="ft">15800</mdPlanned>
        <tvdPlanned uom="ft">12567</tvdPlanned>
        <mdSubSeaPlanned uom="ft">12800</mdSubSeaPlanned>
        <tvdSubSeaPlanned uom="ft">9567</tvdSubSeaPlanned>
        <dayTarget uom="d">128</dayTarget>
        <commonData>
            <sourceName>wellboreSourceName</sourceName>
            <dTimCreation>2001-04-30T08:15:00.000Z</dTimCreation>
            <dTimLastChange>2001-05-31T08:15:00.000Z</dTimLastChange>
            <itemState>plan</itemState>
            <serviceCategory>string</serviceCategory>
            <comments>These are the comments associated with the Wellbore data object.</comments>
            <acquisitionTimeZone dTim="2001-04-30T08:15:00.000Z">Z</acquisitionTimeZone>
            <defaultDatum uidRef="KB">Kelly Bushing</defaultDatum>
            <privateGroupOnly>false</privateGroupOnly>
        </commonData>
    </wellbore>
</wellbores>""")
  

# 1. Load the object

log("Adding wellbore")

WMLS_AddToStore(WMLTYPEIN_WELLBORE, "$wellbore_xml$")  
check_ReturnValue_Success()
partial_success("WMLS_AddToStore succeeded wellbore")

set('uid', get_SuppMsgOut_uid_String())
log_variable('uid')
new_object_created(WMLTYPEIN_WELLBORE, "$uid$", uidWell="$server_w1_uid$")

# 2. Get the object

WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                   <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <wellbore uid="$uid$" uidWell="$server_w1_uid$"/>
                                   </wellbores>
                                """, OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
partial_success("WMLS_GetFromStore succeeded")


# 3. Check the received object against the loaded object

check_XMLout_XMLNormalizedString(WMLTYPEIN_WELLBORE, "$wellbore_xml$")
partial_success("Object retrieved matches object loaded")


log('Script procedure end')

success()
