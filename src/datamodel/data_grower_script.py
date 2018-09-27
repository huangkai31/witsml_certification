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

test(
     purpose = "Generate growing log and trajectorys",
     reference =  "",
     reference_text = "",
     functionality_required =   [],
    )

import time;
import string

from lxml import etree
from lxml import objectify


def grow_log( well_uid, wellbore_uid, log_uid ):
    print "growing log : "+ well_uid +"/"+ wellbore_uid+"/"+log_uid;
    
    set('well_uid', well_uid)
    set('wellbore_uid', wellbore_uid)
    set('log_uid', log_uid)
    
    #obtain log header
    WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <log uidWell="$well_uid$" uidWellbore='$wellbore_uid$' uid='$log_uid$'/>      
                                     </logs>
                                  """, OptionsIn={'returnElements':'header-only'})
    check_ReturnValue_Success()
    
    #determine if log is time-based or depth-based
    set("logIndexType", get_XMLout_Element_String("indexType"))
    log_variable('logIndexType')
    
    isTime = None
    indexStr = None
    indexStrElement = None
    if (get("logIndexType") == "date time" ):
        isTime = True
        indexStr = "endDateTimeIndex"
        indexStrElement = "startDateTimeIndex"
    elif (get("logIndexType") == "measured depth"):
        isTime = False
        indexStr = "endIndex"
        indexStrElement = "startIndex"
    else:
        print "unsupported log type: " + get("logIndexType")
        return  
    
    set("endIndex", get_XMLout_Element_String(indexStr))
    log_variable("endIndex")
    set("indexStrElement", indexStrElement)
    
    #obtain last row of log 
    WMLS_GetFromStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="UTF-8"?>
                                     <logs xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <log uidWell="$well_uid$" uidWellbore='$wellbore_uid$' uid='$log_uid$'>  
                                           <$indexStrElement$>$endIndex$</$indexStrElement$>    
                                       </log>
                                     </logs>
                                  """, OptionsIn={'returnElements':'all'})
    check_ReturnValue_Success()
   
    #increment the index
    if (isTime == True ):
        newIdx = timestamp_add_seconds(get_XMLout_Element_String("endDateTimeIndex"),1)       
    else:
        newIdx = float(get_XMLout_Element_String("endIndex")) + 0.01
                
    print "setting log : '"+log_uid+"'  end index to :",newIdx;
    
    #construct update query
    set("mnemonicList",get_XMLout_Element_String("mnemonicList") )
    set("unitList", get_XMLout_Element_String("unitList") )
    log_data_str = get_XMLout_Element_String("data")
    log_data_list = log_data_str.split(',')    
    log_data_list[0] = str(newIdx)
    set("data", ",".join(log_data_list))
        

    WMLS_UpdateInStore(WMLTYPEIN_LOG, """<?xml version="1.0" encoding="utf-8"?>
                                   <logs xmlns="http://www.witsml.org/schemas/1series"  version="$server_schema_version$">
                                      <log uidWell="$well_uid$" uidWellbore='$wellbore_uid$' uid='$log_uid$'>   
                                         <logData>
                                           <mnemonicList>$mnemonicList$</mnemonicList>
                                           <unitList>$unitList$</unitList>
                                           <data>$data$</data>
                                         </logData>
                                      </log>
                                   </logs>
                                """)  
    
    check_ReturnValue_Success()
    

def grow_trajectory( well_uid, wellbore_uid, traj_uid ):
    """
        Adds a new trajectoryStation to the specified trajectory
        
        Parameters:
          well_uid - uid of well of trajectory to update
          wellbore_uid - uid of wellbore of trajectory to update
          traj_uid - uid of trajectory to update
                     
        Returns:
          None
        """
    print "growing trajectory : "+ well_uid +"/"+ wellbore_uid+"/"+traj_uid;
    
    set('well_uid', well_uid)
    set('wellbore_uid', wellbore_uid)
    set('traj_uid', traj_uid)
    
    WMLS_GetFromStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
                                     <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
                                       <trajectory uidWell="$well_uid$" uidWellbore="$wellbore_uid$" uid="$traj_uid$">
                                       </trajectory> 
                                     </trajectorys>
                                  """,OptionsIn={'returnElements':'all'})
    check_ReturnValue_Success()
      
    
    mdMax = float(get_XMLout_Element_String("mdMx"))
    set('new_traj_depth', mdMax + 1)
    set('type_traj', get_XMLout_Element_String("typeTrajStation"))
    set('name_well',get_XMLout_Element_String('nameWell'))
    set('name_wellbore',get_XMLout_Element_String('nameWellbore'))
    set('name',get_XMLout_Element_String('name'))
    set('newuid', "AppendUid"+now())
    
    WMLS_UpdateInStore(WMLTYPEIN_TRAJECTORY, """<?xml version="1.0" encoding="UTF-8"?>
        <trajectorys xmlns="http://www.witsml.org/schemas/1series" version="$server_schema_version$">
            <trajectory uidWell="$well_uid$" uidWellbore="$wellbore_uid$" uid="$traj_uid$">
                <nameWell>$name_well$</nameWell>
                <nameWellbore>$name_wellbore$</nameWellbore>
                <name>$name$</name>
                <trajectoryStation uid="$newuid$">
                    <typeTrajStation>$type_traj$</typeTrajStation>
                    <md uom="ft">$new_traj_depth$</md>
                </trajectoryStation>
            </trajectory>
        </trajectorys>""")
    
    check_ReturnValue_Success()

growing_logs = [
               ( 
                "Energistics-well-0001",
                "Energistics-w1-wellbore-0001",
                "Energistics-w1-wb1-log-0001"
                )
        ]
growing_trajectories = [
               ( 
                "Energistics-well-0001",
                "Energistics-w1-wellbore-0001",
                "Energistics-w1-wb1-trajectory-0001"
                )
        ]

if __name__ == '__main__':
    
    #check to see if trajectory and log object types are supported.
    growlog = wtl.globals.is_function_object_supported('WMLS_UpdateInStore' , WMLTYPEIN_LOG)
    growtraj = wtl.globals.is_function_object_supported('WMLS_UpdateInStore' , WMLTYPEIN_TRAJECTORY)
    
    print "Grow Logs: " + str(growlog)
    print "Grow Trajectorys: " + str(growtraj)
    
    while 1:
        if (growlog is True):
            for growing_log in growing_logs:
                well_uid, wellbore_uid, log_uid = growing_log;
                grow_log( well_uid, wellbore_uid, log_uid );
            
        if (growtraj is True):
            for growing_traj in growing_trajectories:
                well_uid, wellbore_uid, traj_uid = growing_traj;
                grow_trajectory(well_uid, wellbore_uid, traj_uid);
        
        #sleep after each iteration    
        time.sleep(1.0);
