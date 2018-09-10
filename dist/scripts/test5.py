#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server supports case-insensitive comparisons.",
     reference =  "6.1.5 Case Sensitivity",
     reference_text = "When performing a query against a stored data item (including uids), a WITSML server MUST perform case-insensitive comparisons.",
     functionality_required =   ["WMLS_GetFromStore:well"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Script setup start')

# Get the well 1 name 
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well uid="$server_w1_uid$">
                                           <name/>
                                         </well>
                                     </wells>
                                  """)  
check_XMLout_ElementIncluded('name')
set('name', get_XMLout_Element_String('name'))

#Get lowercase and uppercase versions of the name
set('name_lower',get('name').lower())
set('name_upper',get('name').upper())

log('Script setup end')
log('')

#############
# TEST BODY #
#############

#Verify server returns 1 well that matches provided name in lower case
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well>
                                             <name>$name_lower$</name>
                                         </well>
                                     </wells>
                                  """ ,OptionsIn={'returnElements':'id-only'})  

check_ReturnValue_Success()
check_XMLout_ElementValue('name','$name$')
check_XMLout_NumberOfObjects(1)

#Verify server returns 1 well that matches provided name in upper case
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well>
                                             <name>$name_upper$</name>
                                         </well>
                                     </wells>
                                  """ ,OptionsIn={'returnElements':'id-only'})  

check_ReturnValue_Success()
check_XMLout_ElementValue('name','$name$')
check_XMLout_NumberOfObjects(1)

partial_success("Server supports case-insensitive comparisons")

success()
