#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server supports data-object selection for a well using numAPI",
     reference =  "4.1.3",
     reference_text = "A server MAY only support a subset of elements and attributes for data-object selection. However, if a server supports a data-object, then it MUST support all the data-object selection items specified for that data-object in Chapter 7, page 18",
     functionality_required =   ["WMLS_GetFromStore:well"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Script setup start')

# Get the well 1 numAPI needed for the script 
log("Retrieving well 1 'numAPI'")
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well uid="$server_w1_uid$">
                                           <numAPI/>
                                         </well>
                                     </wells>
                                  """)
check_ReturnValue_Success()								  
check_XMLout_ElementIncluded('numAPI')
set('well_1_numAPI', get_XMLout_Element_String('numAPI'))
log_variable('well_1_numAPI', label='Well 1 numAPI' )

log('Script setup end')
log('')

#############
# TEST BODY #
#############

# Use Standard Query #1 (Get ID of all Wells) including the numAPI with the first well's numAPI
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well>                         
                                           <numAPI>$well_1_numAPI$</numAPI>
                                       </well>                         
                                     </wells>
                                  """,
                                  OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()

# Verify the query returns one well with the specified numAPI.
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('well','uid', "$server_w1_uid$")
check_XMLout_ElementValue('numAPI','$well_1_numAPI$')
partial_success("Selection by 'numAPI' succeeded")

success()
