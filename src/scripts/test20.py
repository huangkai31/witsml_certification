#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify the server treats requests for comparison for dTimLastChange correctly.",
     reference =  "6.6.4  WMLS_GetFromStore -How it Works",
     reference_text = "For the commonData and commonTime elements dTimCreation and dTimLastChange, the server MUST treat a request for comparisons as 'greater than' NOT 'equal'. This behavior is an exception to the standard STORE behavior of 'equal' comparisons.",
     functionality_required =   ["WMLS_GetFromStore:well"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('Setup start')

#Get dTimLastChange to use in test
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well uid="$server_w1_uid$">
                                           <commonData>
                                             <dTimLastChange/>
                                           </commonData>
                                         </well>
                                     </wells>
                                  """)  
check_ReturnValue_Success()
set('tml', get_XMLout_Element_String('dTimLastChange'))  

log('Setup end')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')

#Use Standard Query #3 (Get Details for a well) setting the dTimLastChange element to dTimLastChange - 1 second of the well
set('st', timestamp_subtract_seconds(get('tml'), 1))
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well uid="$server_w1_uid$">
                                           <commonData>
                                             <dTimLastChange>$st$</dTimLastChange>
                                           </commonData>
                                         </well>
                                     </wells>
                                  """, OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
partial_success("Server did return a well with a newer dTimLastChange")


#Use Standard Query #3 (Get Details for a well) setting the dTimLastChange element to dTimLastChange of the well
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well uid="$server_w1_uid$">
                                           <commonData>
                                             <dTimLastChange>$tml$</dTimLastChange>
                                           </commonData>
                                         </well>
                                     </wells>
                                  """, OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(0)
partial_success("Server did not return a well with a matching dTimLastChange")

#Use Standard Query #3 (Get Details for a well) setting the dTimLastChange element to dTimLastChange + 1 second of the well
set('st', timestamp_add_seconds(get('tml'), 1))
WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="UTF-8"?>
                                     <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                         <well uid="$server_w1_uid$">
                                           <commonData>
                                             <dTimLastChange>$st$</dTimLastChange>
                                           </commonData>
                                         </well>
                                     </wells>
                                  """, OptionsIn={'returnElements':'all'})  
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(0)
partial_success("Server did not return a well with an older dTimLastChange")

log('Script end')
success()
