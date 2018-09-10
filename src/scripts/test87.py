from wtl.witsml import *



test(
     purpose = "Verify server creates welldatum attribute called 'code' and deletes the same.",
     reference =  "6.5.4.1",
     reference_text = "To delete an attribute, the client specifies an empty attribute and the server MUST delete that attribute",
     functionality_required =   ["WMLS_AddToStore:well" ,
                                 "WMLS_GetFromStore:well",
                                 "WMLS_DeleteFromStore:well"],
     data_schemas = ["1.4.1.0", "1.4.1.1"],
    )

#########
# SETUP #
#########

log('No setup is needed for this test.')
log('')

#############
# TEST BODY #
#############

log('Script procedure start')
set('datumcodeValue',"Test No87 datumCode")
##################################################################################
##ADD the well with the attribute "code" in the element <datumName> under <well>##
##################################################################################
WMLS_AddToStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <well>
                                         <name>Energistics Certification Well Test87</name>
                                         <timeZone>-06:00</timeZone>
                                         <wellDatum uid="welldatum">
                                            <name>Test No87 Name</name>
                                            <datumName namingSystem="wellNamingSystem" code='$datumcodeValue$'>Test No87 datumName</datumName>
                                        </wellDatum>       
                                      </well>
                                    </wells>
                                """)

check_ReturnValue_Success()
partial_success("Add to store succeeded")
set('uid', get_SuppMsgOut_uid_String())
new_object_created(WMLTYPEIN_WELL, "$uid$", uidWell="$uid$")

##################################################################################
##Check to see if the attribute 'code' is added                                 ##
##################################################################################


WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <well uid="$uid$">
                                     </well>
                                   </wells>
                                """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeValue('wells/well/wellDatum/datumName', 'code', "$datumcodeValue$")
partial_success('One well returned and wells/well/wellDatum/datumName[@code] is ok')

##################################################################################
##Delete the 'code' attribute by passing empty string in the attribute value    ##
##################################################################################


WMLS_DeleteFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                            <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                               <well uid="$uid$">
                                                 <wellDatum uid="welldatum">
                                                    <datumName code=""></datumName>
                                                 </wellDatum>
                                               </well>
                                            </wells>
                                         """)
check_ReturnValue_Success()

##################################################################################
##Check to see if the "code" attribute is deleted                               ##
##################################################################################


WMLS_GetFromStore(WMLTYPEIN_WELL, """<?xml version="1.0" encoding="utf-8"?>
                                   <wells xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                     <well uid="$uid$">
                                     </well>
                                   </wells>
                                """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)
check_XMLout_AttributeNotIncluded('/wells/well/wellDatum/datumName','code')
partial_success('wells/well/wellDatum/datumName[@code] is deleted');

log('Script procedure end')

success()
