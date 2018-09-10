#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify a server supports data-object selection for a well using numGovt",
     reference =  "4.1.3",
     reference_text = "A server MAY only support a subset of elements and attributes for data-object selection. However, if a server supports a data-object, then it MUST support all the data-object selection items specified for that data-object in Chapter 7, page 18",
     functionality_required =   ["WMLS_GetFromStore:well"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Script setup start')

# Get the well 1 numGovt needed for the script 
log("Retrieving well 1 'numGovt'")
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well uid="$server_w1_uid$">
                                           <numGovt/>
                                         </well>
                                     </wells>
                                  """)  
check_ReturnValue_Success()								  
check_XMLout_ElementIncluded('numGovt')
set('well_1_numGovt', get_XMLout_Element_String('numGovt'))
log_variable('well_1_numGovt', label='Well 1 numGovt' )

log('Script setup end')
log('')

#############
# TEST BODY #
#############

# Use Standard Query #1 (Get ID of all Wells) including the numGovt with the first well's numGovt
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <well>                         
                                           <numGovt>$well_1_numGovt$</numGovt>
                                       </well>                         
                                     </wells>
                                  """,
                                  OptionsIn={'returnElements':'id-only'})  
check_ReturnValue_Success()

# Verify the query returns one well with the specified numGovt
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('well','uid', "$server_w1_uid$")
check_XMLout_ElementValue('numGovt','$well_1_numGovt$')
partial_success("Selection by 'numGovt' succeeded")

success()