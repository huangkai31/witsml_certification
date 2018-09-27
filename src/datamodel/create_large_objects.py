#! /usr/bin/env python
#  
# Copyright 2014
# 
# Third Party Software
# Teytech Inc. Version 1.0
#
# Energistics 
# The following Energistics (c) products were used in the creation of this work: 
# 
# •             WITSML Data Schema Specifications, Version 1.4.1.1 
# 
# All rights in the WITSML™ Standard, the PRODML™ Standard, and the RESQML™ Standard, or
# any portion thereof, which remain in the Standards DevKit shall remain with Energistics
# or its suppliers and shall remain subject to the terms of the Product License Agreement
# available at http://www.energistics.org/product-license-agreement. 
# 
# Apache
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. 
# 
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. 
# 
# See the License for the specific language governing permissions and limitations under the
# License.
# 
# All rights reserved. 
# 
#
from wtl.witsml import *

import random
import string

from lxml import etree
from lxml import objectify
from wtl.time_prim import subtract_seconds_to_timestamp,\
    add_seconds_to_timestamp


def create_log_maxDataNodes(uidWell, uidWellbore, uidLog, nameWell, nameWellbore, nameLog, indexType, maxDataNodes ):
    """
    Creates a large log of the specified indexType on the specified well/wellbore of a size larger than
    the specified maxDataNodes for WMLS_GetFromStore for the log object.
    
    Parameters:
      uidWell: uid of well to attach log to
      uidWellbore: uid of wellbore to attach log to
      uidLog: uid of log to create
      nameWell: name of well to attach log to
      nameWellbore: name of wellbore to attach log to
      nameLog: name of log to create
      indexType: indexType of log to create.  This should match the WITSML LogIndexType
          only "date time" and "measured depth" are supported
      maxDataNodes: dictionary of maxDataNodes keyed by WITSML function.

    Returns:
      True if successfully able to create the large log. False otherwise.
        """

    # set variables based on indexType
    if (indexType == "measured depth"):
        indexMnemonic = "BDEP"
        indexUnit = "m"
        indexDataType = "double"
    elif (indexType == "date time"):
        indexMnemonic = "TIME"
        indexUnit = "unitless"
        indexDataType = "date time"
    else:
        return False
    
    empty_data_template_xml = string.Template("""<?xml version="1.0" encoding="utf-8"?>
                                       <logs xmlns="http://www.witsml.org/schemas/1series" version="$ver">
                                          <log uidWell="$uidWell" uidWellbore="$uidWellbore" uid="$uid">
                                             <nameWell>$nameWell</nameWell>
                                             <nameWellbore>$nameWellbore</nameWellbore>
                                             <name>$name</name>
                                             <indexType>$indexType</indexType>
                                             <direction>increasing</direction>
                                             <indexCurve>$indexMnemonic</indexCurve>
                                             <logCurveInfo uid='$indexMnemonic'>
                                               <mnemonic>$indexMnemonic</mnemonic>
                                               <unit>$indexUnit</unit>
                                               <typeLogData>$indexDataType</typeLogData>
                                             </logCurveInfo>
                                             <logCurveInfo uid='CURVE1'>
                                               <mnemonic>CURVE1</mnemonic>
                                               <unit>m/h</unit>
                                               <typeLogData>double</typeLogData>
                                             </logCurveInfo>
                                             <logCurveInfo uid='CURVE2'>
                                               <mnemonic>CURVE2</mnemonic>
                                               <unit>m/h</unit>
                                               <typeLogData>double</typeLogData>
                                             </logCurveInfo>
                                             <logCurveInfo uid='CURVE3'>
                                               <mnemonic>CURVE3</mnemonic>
                                               <unit>m/h</unit>
                                               <typeLogData>double</typeLogData>
                                             </logCurveInfo>
                                             <logData>
                                               <mnemonicList>$indexMnemonic,CURVE1,CURVE2,CURVE3</mnemonicList>
                                               <unitList>$indexUnit, m/h, m/h, m/h</unitList>
                                             </logData>
                                          </log>
                                       </logs>""").substitute(ver = get("server_schema_version"),
                                                              uidWell = uidWell,
                                                              uidWellbore = uidWellbore,
                                                              uid = uidLog,
                                                              nameWell = nameWell,
                                                              nameWellbore = nameWellbore,
                                                              name = nameWell,
                                                              indexType = indexType,
                                                              indexMnemonic = indexMnemonic,
                                                              indexUnit = indexUnit,
                                                              indexDataType = indexDataType );
    
    # set maximum number of rows per request to lesser of UpdateInStore or AddToStore
    if (maxDataNodes['WMLS_AddToStore'] < maxDataNodes['WMLS_UpdateInStore']):
        maximum_rows_per_request = maxDataNodes['WMLS_AddToStore']
    else:
        maximum_rows_per_request = maxDataNodes['WMLS_UpdateInStore']
    
    # now divide it by 2    
    maximum_rows_per_request = maximum_rows_per_request / 2;
    
    # set a cap at 5000 row
    if (maximum_rows_per_request < 1):
        maximum_rows_per_request = 1;
    if (maximum_rows_per_request) >5000 :
        maximum_rows_per_request = 5000;
    uploaded_rows = 0;
    
    ns = "http://www.witsml.org/schemas/1series";
    EF = objectify.ElementMaker(annotate=False, namespace=ns, nsmap={None : ns})
    
    if (indexType == "measured depth"):
        curr_index = 0.0;
    else:
        curr_index = timestamp_subtract_seconds(now(), 24 * 60 * 60)
              
    first_query_flag = True;
    nodesToExceed = maxDataNodes['WMLS_GetFromStore']
    print ("uploading log that exceeds maxDataRows of " + str(nodesToExceed));
    while uploaded_rows <= nodesToExceed:
        ###
        crv1 = random.random();
        crv2 = random.random();
        crv3 = random.random();
        ###
        new_logs_xml = objectify.fromstring( empty_data_template_xml );
        for i in range(maximum_rows_per_request):
            data = EF.data( str(curr_index)+","+
                            str(crv1)+","+
                            str(crv2)+","+
                            str(crv3) );
            new_logs_xml.log.logData.append( data );
            if (indexType == "measured depth"):
                curr_index+=0.1;
            else:
                curr_index = timestamp_add_seconds(curr_index,1)
            ###
        update_query = etree.tostring( new_logs_xml , pretty_print = True );
        if (first_query_flag):
            print "Adding to store new log..."
            #print update_query;
            WMLS_AddToStore(WMLTYPEIN_LOG,  update_query );
        else:
            print "Appending data to log..."
            WMLS_UpdateInStore(WMLTYPEIN_LOG,  update_query );
        check_ReturnValue_Success();
        uploaded_rows+=maximum_rows_per_request;
        first_query_flag = False;
        print "uploaded so far : "+str(uploaded_rows)+" rows";
        
    return True

def create_log_maxDataPoints(uidWell, uidWellbore, uidLog, nameWell, nameWellbore, nameLog, indexType, maxDataPoints ):
    """
    Creates a large log of the specified indexType on the specified well/wellbore of a size larger than
    the specified maxDataPoints for WMLS_GetFromStore:log
    
    Parameters:
      uidWell: uid of well to attach log to
      uidWellbore: uid of wellbore to attach log to
      uidLog: uid of log to create
      nameWell: name of well to attach log to
      nameWellbore: name of wellbore to attach log to
      nameLog: name of log to create
      indexType: indexType of log to create.  This should match the WITSML LogIndexType
          only "date time" and "measured depth" are supported
      maxDataPoints: dictionary of maxDataPoints keyed by WITSML function..

    Returns:
      True if successfully able to create the large log. False otherwise.
    """
   
    # set variables based on log indexType
    if (indexType == "measured depth"):
        indexMnemonic = "DEPTH"
        indexUnit = "m"
        indexDataType = "double"
    elif (indexType == "date time"):
        indexMnemonic = "TIME"
        indexUnit = "unitless"
        indexDataType = "date time"
    else:
        return False
    
    
     # set maximum number of rows per request to lesser of UpdateInStore or AddToStore
    if (maxDataPoints['WMLS_AddToStore'] < maxDataPoints['WMLS_UpdateInStore']):
        maximum_rows_per_request = maxDataPoints['WMLS_AddToStore']
    else:
        maximum_rows_per_request = maxDataPoints['WMLS_UpdateInStore']
    
    maxPointsToExceed = maxDataPoints['WMLS_GetFromStore']  
    print ("uploading log that exceeds maxDataPoints of " + str(maxPointsToExceed));
    
    # set number of curves to write (capped at 500)
    curve_count =  maxPointsToExceed / 1000;
    if (curve_count < 1):
        curve_count = 1
    if (curve_count > 500):
        curve_count = 500
        
    row_count = maxPointsToExceed / curve_count;
    curves = [];
    depth_index_curve_name = indexMnemonic
    rows_per_request = row_count / 10
    uploaded_points = 0;
        
    ### generating curve names
    for i in range(curve_count):
        number_as_str = str(i);
        while len(number_as_str) < 4:
            number_as_str = "0"+number_as_str;
        curves.append( "CURVE_"+number_as_str );
    
    current_row_index = 0;
    uploaded_nodes = 0;
    
    if ( indexType == "measured depth"):
        virtual_index = 0.0;
    else:
        virtual_index = subtract_seconds_to_timestamp(now(), 24*60*60)
    
    first_upload = True;
    while 1:
        if (uploaded_points > maxPointsToExceed):
            break;
        empty_data_template_xml = string.Template("""<?xml version="1.0" encoding="utf-8"?>
                                       <logs xmlns="http://www.witsml.org/schemas/1series" version="$ver">
                                          <log uidWell="$uidWell" uidWellbore="$uidWellbore" uid="$uid">
                                             <nameWell>$nameWell</nameWell>
                                             <nameWellbore>$nameWellbore</nameWellbore>
                                             <name>$name</name>
                                             <indexType>$indexType</indexType>
                                             <direction>increasing</direction>
                                             <indexCurve>$indexMnemonic</indexCurve>
                                           """).substitute(ver           = get("server_schema_version"),
                                                           uidWell       = uidWell,
                                                           uidWellbore   = uidWellbore,
                                                           uid           = uidLog,
                                                           nameWell      = nameWell,
                                                           nameWellbore  = nameWellbore,
                                                           name          = nameLog,
                                                           indexType     = indexType,
                                                           indexMnemonic = indexMnemonic);
        ns = "http://www.witsml.org/schemas/1series";
        EF = objectify.ElementMaker(annotate=False, namespace=ns, nsmap={None : ns})
        ###
        update_xml = empty_data_template_xml;
        header_mnemonics = [indexMnemonic]
        header_uoms = [indexUnit]
        ###
        crv = string.Template('''
                        <logCurveInfo uid="$uid">
                            <mnemonic>$mnemonic</mnemonic>
                            <unit>$uom</unit>
                            <typeLogData>$typeLogData</typeLogData>
                        </logCurveInfo>
                        ''').substitute(uid      =  indexMnemonic,
                                        mnemonic =  indexMnemonic,
                                        uom      = indexUnit,
                                        typeLogData = indexDataType
                                        );
        if (first_upload):
                update_xml += crv; 
        ###
        for crv_index in range(curve_count):
                curve_mnemonic = curves[crv_index];
                curve_uom = 'm'
                curve_type = "int"
                                
                ###
                header_mnemonics.append(curve_mnemonic)
                header_uoms.append(curve_uom)
                ###
                                
                crv = string.Template('''
                    <logCurveInfo uid="$uid">
                        <mnemonic>$mnemonic</mnemonic>
                        <unit>$uom</unit>
                        <typeLogData>$typeLogData</typeLogData>
                    </logCurveInfo>
                    ''').substitute(uid         = curve_mnemonic,
                                    mnemonic    = curve_mnemonic,
                                    uom         = curve_uom,
                                    typeLogData = curve_type
                                    );
                if (first_upload):    
                    update_xml += crv; 
        ###
        update_xml += "<logData>\n"
        ###
        update_xml+="<mnemonicList>"+(",".join(header_mnemonics))+"</mnemonicList>\n"
        update_xml+="<unitList>"+(",".join(header_uoms))+"</unitList>\n"    
        ###
        collected_nodes = 0;
        collected_points = 0;
        for rwi in range(rows_per_request):
            
            if (indexType == "measured depth"):
                virtual_index += 0.1;
            else:
                virtual_index = add_seconds_to_timestamp(virtual_index, 1)
                
            data_row = [str(virtual_index)]; 
            
            for crv_i in range(curve_count):
                data_value = int(random.random() * 9 )
                data_row.append( str( data_value ) );    
                collected_points+=1;
            collected_nodes+=1;
            
            data_row_str = ",".join(data_row);
            update_xml+="<data>"+data_row_str+"</data>\n"
            
        update_xml += "</logData>\n</log>\n</logs>"    
        update_query = update_xml
        ###
        if (first_upload):
            WMLS_AddToStore(WMLTYPEIN_LOG, update_query  );
            check_ReturnValue_Success()
        else:
            WMLS_UpdateInStore(WMLTYPEIN_LOG, update_query  );
            check_ReturnValue_Success()
        ###
        uploaded_points += collected_points;
        uploaded_nodes += collected_nodes
        print "uploaded "+str(uploaded_points)+" points to witsml store"
        print "node count: "+str(uploaded_nodes)+" "
        first_upload = False;
    return True

