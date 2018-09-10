#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server preserves uid case",
     reference =  "6.4.4.1 Case",
     reference_text = "The server MUST store upper or lowercase string data values present in the XMLin string exactly as supplied, 'preserving their case.' For subsequent invocations of WMLS_GetFromStore, the server MUST return the string data values in their originally supplied case",
     functionality_required =   ["WMLS_GetFromStore:well",
                                 "WMLS_AddToStore:well",
                                 "WMLS_DeleteFromStore:well" ],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Test Setup')

set('welluid','certification-Test-21')
set('welluidChangeCase','Certification-Test-21')

# Cleanup well with uid = certification-Test-21 
WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="$welluid$"/>
                                     </wells>
                                     """ )
    
log('Test Setup End')


#############
# TEST BODY #
#############

log('Script procedure start')

#Send an AddToStore request to create a new Well object with a mixedcase uid 'certification-Test-21'
WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                    <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                      <well uid="$welluid$">
                                        <name>$welluid$ name</name>
                                      </well>
                                    </wells>""" )  
check_ReturnValue_Success()

#Use Standard Query #2 (Get ID of a well) with well.uid = 'Certification-Test-21'
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="$welluidChangeCase$"/>                         
                                     </wells>
                                  """ ,OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()

# Verify the first query returns one well with the specified uid
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('well','uid', "$welluid$")

partial_success("Server preserves uid case for AddToStore")
log('Script procedure end')

############
# CLEANUP  #
############

log('Test Cleanup Start')

# Cleanup well with uid = certification-Test-21 
WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid="$welluid$"/>
                                     </wells>
                                     """ )
    
log('Test Cleanup End')


success()
