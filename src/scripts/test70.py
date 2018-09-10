#! /usr/bin/env python
from wtl.witsml import *

test(
     purpose = "Verify changeLog entries populates nameWell, nameWellbore, nameObject, uidWell, uidWellbore,uidObject",
     reference = "9.3.4.1",
     reference_text = "The value for this element/attribute MUST match the value of . . . in the changed data-object",
     functionality_required =   ["WMLS_GetFromStore:log",
                                 "WMLS_GetFromStore:changeLog"],
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

# Use SQ-008 (Get ID of all Instances of a Data-object in a Wellbore) to obtain the log's nameWell, nameWellbore.
WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <log uidWell="$server_w3_uid$" uidWellbore='$server_w3_wb1_uid$' uid='$server_w3_wb1_log1_uid$'/>      
                                     </logs>
                                  """, OptionsIn={'returnElements':'id-only'})
check_ReturnValue_Success()                               
set('nameWell', get_XMLout_Element_String('nameWell'))
set('nameWellbore', get_XMLout_Element_String('nameWellbore'))
set('name', get_XMLout_Element_String('name'))


# Use SQ-018 (What changes have been made in a log/mudLog or multiple logs/mudlogs since a specified time)
# specifying a dTimLastChange and dTimChange of Jan 1, 1970 and the uidObject equal to the log's uid.
WMLS_GetFromStore(WMLTYPEIN_CHANGELOG, """<?xml version="1.0" encoding="UTF-8"?>
                                          <changeLogs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <changeLog uidWell="$server_w3_uid$" uidWellbore = "$server_w3_wb1_uid$" uidObject="$server_w3_wb1_log1_uid$">
                                                <objectType>log</objectType>
                                                <changeHistory>
                                                    <dTimChange>1970-01-01T00:00:01Z</dTimChange>
                                                </changeHistory>
                                                <commonData>
                                                    <dTimLastChange>1970-01-01T00:00:01Z</dTimLastChange>
                                                </commonData>
                                            </changeLog>
                                          </changeLogs>
                                       """,OptionsIn={'returnElements':'all'})
check_ReturnValue_Success()
check_XMLout_NumberOfObjects(1)

# Verify the changeLog nameWell matches the log’s nameWell
check_XMLout_ElementValue('/changeLogs/changeLog/nameWell', get('nameWell'))
partial_success('nameWell in changeLog is correct')
                
# Verify the changeLog nameWellbore matches the log’s nameWellbore
check_XMLout_ElementValue('/changeLogs/changeLog/nameWellbore', get('nameWellbore'))
partial_success('nameWellbore in changeLog is correct')

# Verify the changeLog nameObject matches the log’s name.
check_XMLout_ElementValue('/changeLogs/changeLog/nameObject', get('name'))
partial_success('nameObject in changeLog is correct')

# Verify the changeLog uidWell matches the log’s well uid.
check_XMLout_AttributeValue('changeLog', 'uidWell', get('server_w3_uid'))
partial_success('uidWell in changeLog is correct')

# Verify the changeLog uidWellbore matches the log’s wellbore uid.
check_XMLout_AttributeValue('changeLog', 'uidWellbore', get('server_w3_wb1_uid'))
partial_success('uidWellbore in changeLog is correct')

# Verify the changeLog uidObject matches the logs' uid.
check_XMLout_AttributeValue('changeLog', 'uidObject', get('server_w3_wb1_log1_uid'))
partial_success('uidObject in changeLog is correct')


log('Script procedure end')

success()
