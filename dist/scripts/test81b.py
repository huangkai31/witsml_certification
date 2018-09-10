#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify that boundary conditions for UIDs are handled by the server",
     reference =  "typ_baseType.xsd",
     reference_text = '<xsd:pattern  value="[^ ]*"/>',
     functionality_required =   ['WMLS_GetFromStore:well',
                                 'WMLS_GetFromStore:wellbore',
                                 'WMLS_GetFromStore:log',
                                 'WMLS_DeleteFromStore:well',
                                 'WMLS_DeleteFromStore:wellbore',
                                 'WMLS_DeleteFromStore:log',
                                 'WMLS_AddToStore:well',
                                 'WMLS_AddToStore:wellbore',
                                 'WMLS_AddToStore:log'],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Test Setup Start')
              
set('uidWell',    'a')
set('uidWellbore','b')
set('uidLog',     'c')
set('nameWell',     'Certification-Test-81-well')
set('nameWellbore', 'Certification-Test-81-wellbore')
set('nameLog',      'Certification-Test-81-log')

# Remove objects if they exist
WMLS_DeleteFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <log uidWell="$uidWell$" uidWellbore="$uidWellbore$" uid="$uidLog$"/>
                                     </logs>
                                     """ )

WMLS_DeleteFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="utf-8"?>
                                     <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <wellbore uidWell="$uidWell$" uid="$uidWellbore$"/>
                                     </wellbores>
                                     """ )

WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="$uidWell$"/>
                                     </wells>
                                     """ )
    
log('Test Setup End')

#############
# TEST BODY #
#############

log('Script procedure start')

# Send WMLS_AddToStore to create a well, a wellbore for the well and a log for the wellbore
# using uids that have the minimum length allowed 
WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                    <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <well uid="$uidWell$">
                                        <name>$nameWell$</name>
                                      </well>
                                    </wells>""" )  
check_ReturnValue_Success()
partial_success("Add to store succeeded for well with minimum size uid")
new_object_created(WMLTYPEIN_WELL, "$uidWell$")

WMLS_AddToStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                       <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                          <wellbore uidWell="$uidWell$" uid="$uidWellbore$">
                                            <nameWell>$nameWell$</nameWell>
                                            <name>$nameWellbore$</name>
                                          </wellbore>
                                       </wellbores>
                                       """)
check_ReturnValue_Success()
partial_success("Add to store succeeded for wellbore with minimum size uid")
new_object_created(WMLTYPEIN_LOG, "$uidWellbore$", uidWell="$uidWell$")

WMLS_AddToStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$uidWell$" uidWellbore="$uidWellbore$" uid="$uidLog$">
                                         <nameWell>$nameWell$</nameWell>
                                         <nameWellbore>$nameWellbore$</nameWellbore>
                                         <name>$nameLog$</name>
                                         <indexType>measured depth</indexType>
                                         <indexCurve>BDEP</indexCurve>
                                         <logCurveInfo uid='BDEP'>
                                           <mnemonic>BDEP</mnemonic>
                                           <unit>m</unit>
                                           <typeLogData>int</typeLogData>
                                         </logCurveInfo>
                                      </log>
                                   </logs>""")  
check_ReturnValue_Success()
partial_success("Add to store succeeded for log with minimum size uid")
new_object_created(WMLTYPEIN_LOG, "$uidLog$", uidWellbore="$uidWellbore$", uidWell="$uidWell$")

# Use SQ-002 to retrieve the well created
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="$uidWell$"/>                         
                                     </wells>
                                  """ ,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('well','uid', "$uidWell$")
partial_success("Minimum uid length supported for well")

# Use SQ-005 to retrieve the wellbore created
WMLS_GetFromStore(WMLTYPEIN_WELLBORE, """<?xml version="1.0" encoding="UTF-8"?>
                                         <wellbores xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                           <wellbore uidWell="$uidWell$"/>                         
                                         </wellbores>
                                  """ ,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('wellbore','uidWell', "$uidWell$")
check_XMLout_AttributeValue('wellbore','uid', "$uidWellbore$")
partial_success("Minimum uid length supported for wellbore")

# Use SQ-008 to retrieve the log created
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                    <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <log uidWell="$uidWell$" uidWellbore="$uidWellbore$"/>                         
                                    </logs>
                                  """ ,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('log','uidWell', "$uidWell$")
check_XMLout_AttributeValue('log','uidWellbore', "$uidWellbore$")
check_XMLout_AttributeValue('log','uid', "$uidLog$")
partial_success("Minimum uid length supported for log")

log('Script procedure end')

success()
