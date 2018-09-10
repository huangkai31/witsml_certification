#! /usr/bin/env python
from wtl.witsml import *



test(purpose = "Verify a server registers support for the changeLog object",
     reference =  "9.3.4 changeLog Object",
     reference_text = "All servers MUST register support for changeLog objects in the server's capability object for the WMLS_GetFromStore function.",
     functionality_required = [],
     data_schemas = ["1.4.1.0", "1.4.1.1"]) 


#########
# SETUP #
#########


log('Script procedure start')

WMLS_GetCap(OptionsIn={'dataVersion':get('server_schema_version')})
check_ReturnValue_Success()
check_CapabilitiesOut_ElementIncluded('/capServers/capServer/function[@name="WMLS_GetFromStore"]/dataObject[.="changeLog"]')
    
partial_success("Server does register support for ChangeLog object");
#
log('Script procedure end')

success();    
