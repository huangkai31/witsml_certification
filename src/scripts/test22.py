#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify that server handles cascadedDelete",
     reference =  "6.5.2  WMLS_DeleteFromStore - Parameters",
     reference_text = "OptionsIn - cascadedDelete:  If the client specifies a value of 'true', when a server deletes a data-object, the server MUST delete all data-objects whose identity depends on that data-object.",
     functionality_required =   ["WMLS_GetFromStore:well",
                                 "WMLS_GetFromStore:wellbore",
                                 "WMLS_GetFromStore:log",
                                 "WMLS_AddToStore:well",
                                 "WMLS_AddToStore:wellbore",
                                 "WMLS_AddToStore:log",
                                 "WMLS_DeleteFromStore:well",
                                 "cascadedDelete=True"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

# setup for well
set('wellUid', 'Certification-Test-Well-22')
set('wellboreUid', 'Certification-Test-Wellbore-22')
set('logUid', 'Certification-Test-Log-22')
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid='$wellUid$'/>                         
                                     </wells>
                                  """)
check_ReturnValue_Success()
  
if (get_XMLout_NumberOfObjects_Int() == 0):
    WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                       <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                          <well uid="$wellUid$">
                                             <name>Certification-Test-Well-22 name</name>
                                          </well>
                                       </wells>""")
    check_ReturnValue_Success()
    log('Successfully added well')

# setup for wellbore
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <wellbore uidWell="$wellUid$" uid='$wellboreUid$'/>                         
                                     </wellbores>
                                  """)
check_ReturnValue_Success()
  
if (get_XMLout_NumberOfObjects_Int() == 0):
    WMLS_AddToStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                       <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                          <wellbore uidWell="Certification-Test-Well-22" uid="$wellboreUid$">
                                            <nameWell>Energistics Certification Well Test22</nameWell>
                                            <name>Energistics Certification Wellbore Test22</name>
                                          </wellbore>
                                       </wellbores>
                                       """)
    check_ReturnValue_Success()
    log('Successfully added wellbore')

# setup for log
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <log uidWell='$wellUid$' uidWellbore="$wellboreUid$" uid="$logUid$"/> 
                                     </logs>
                                  """)
check_ReturnValue_Success()
  
if (get_XMLout_NumberOfObjects_Int() == 0):
    WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
    <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
        <log uidWell="$wellUid$" uidWellbore="$wellboreUid$" uid="$logUid$">
            <nameWell>Energistics Certification Well Test22</nameWell>
            <nameWellbore>Energistics Certification Wellbore Test22</nameWellbore>
            <name>Energistics Certification Log Test22</name>
            <indexType>measured depth</indexType>
            <startIndex uom="m">499</startIndex>
            <endIndex uom="m">500.01</endIndex>
            <indexCurve>Mdepth</indexCurve>
            <logCurveInfo uid="lci-Test22">
                <mnemonic>Mdepth</mnemonic>
                <unit>m</unit>
                <typeLogData>double</typeLogData>
            </logCurveInfo>
        </log>
    </logs>""")
    check_ReturnValue_Success()
    log('Successfully added log')

#############
# TEST BODY #
#############

log('Script procedure start')

#Call deleteFromStore on the specified well setting optionsIn = "cascadedDelete=true".
WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="$wellUid$"/>
                                     </wells>
                                     """,OptionsIn={'cascadedDelete':'true'})  
check_ReturnValue_Success()
partial_success("DeleteFromStore with cascadedDelete succeeded.")

#Call SQ-002 (Get ID for a well) for the Well.
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid='$wellUid$'/>                         
                                     </wells>
                                  """,OptionsIn={'returnElements':'id-only'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(0)
partial_success("Well has been cascadeDeleted")

#Call SQ-005 (Get ID for all Wellbores in Well) for the Wellbore.
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <wellbore uidWell="$wellUid$" />                         
                                     </wellbores>
                                  """,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(0)
partial_success("Wellbore has been cascadeDeleted")

#Call SQ-008 (Get ID of all Instances of a Data-object in a Wellbore) for the Log.
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <log uidWell='$wellUid$' uidWellbore="$wellboreUid$" /> 
                                     </logs>
                                  """,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(0)
partial_success("Log has been cascadeDeleted")

log('Script procedure end')

success()
