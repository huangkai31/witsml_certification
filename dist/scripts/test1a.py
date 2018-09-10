#! /usr/bin/env python
from wtl.witsml import *
import datetime
import time

test(
     purpose = "Verify a server supports the following data-object selection items for a well: uid, name, dTimLastChange",
     reference =  "4.1.3",
     reference_text = "A server MAY only support a subset of elements and attributes for data-object selection. However, if a server supports a data-object, then it MUST support all the data-object selection items specified for that data-object in Chapter 7, page 18",
     functionality_required =   ["WMLS_GetFromStore:well"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########


log('Script setup start')

log("Retrieving well 1 'name' and 'dTimLastChange'")
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well uid="$server_w1_uid$">
                                           <name/>
                                           <commonData>
                                             <dTimLastChange/>
                                           </commonData>
                                         </well>
                                     </wells>
                                  """)  
check_XMLout_ElementIncluded('name')
set('well_1_name', get_XMLout_Element_String('name'))
log_variable('well_1_name', label='Well 1 name' )

check_XMLout_ElementIncluded('dTimLastChange')
set('well_1_dTimLastChange', get_XMLout_Element_String('dTimLastChange'))

log('Script setup end')
log('')

#############
# TEST BODY #
#############

# Use Standard Query #1 (Get ID of all Wells) including the uid of first well.
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well uid='$server_w1_uid$'/>                         
                                     </wells>
                                  """,
                                  OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()

# Verify the first query returns one well with the specified uid
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('well','uid', "$server_w1_uid$")
partial_success("Selection by 'uid' succeeded")


# Use Standard Query #1 (Get ID of all Wells) including the name element with the first well's name.
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well>                         
                                           <name>$well_1_name$</name>
                                       </well>                         
                                     </wells>
                                  """,
                                  OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()

# Verify the second query returns one well with the specified name
check_XMLout_NumberOfObjects(1) 
    
# Verify that a well was retrieved with the correct name
check_XMLout_ElementValue('name', '$well_1_name$')   
partial_success("Selection by 'name' succeeded")

# Use SQ-001 (Get ID of all Wells) including a  dTimLastChange between the dTimLastChange of the two wells.
# For simplicity we use well 1's dTimLastChange which should not be included in the response.
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well>
                                        <commonData>
                                         <dTimLastChange>$well_1_dTimLastChange$</dTimLastChange>
                                        </commonData>
                                       </well>                         
                                     </wells>
                                  """,
                                  OptionsIn={'returnElements':'id-only'})  
    
check_ReturnValue_Success()
if ( get_XMLout_NumberOfObjects_Int() < 1):
    fail("SQ-001 by dTimLastChange did not return any results")
    
partial_success("Selection by 'dTimLastChange' succeeded")
    
# confirm well 2 is included in results
check_XMLout_ElementIncluded("/wells/well[@uid='$server_w2_uid$']")
partial_success("Newer well included in results of query by dTimLastChange")

#confirm well 1 is not included in results
check_XMLout_ElementNotIncluded("/wells/well[@uid='$server_w1_uid$']")
partial_success("Older well not included in results of query by dTimLastChange")

success()