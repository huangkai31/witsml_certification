#******************************************************************************
# Copyright (c) 2012 Witsml Energistics   .
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#******************************************************************************

# System imports
import os
import sys

import wtl.utils
from sets import Set 
import wtl.control_prim
import wtl.testlog as testlog

# global variables
_set = wtl.utils.set_variable_value
_get = wtl.utils.get_variable_value
_log = testlog.log
_partial_success =  wtl.control_prim.partial_success


class LogVerify: 
    """ Evaluates the acquired log ( via the tools GetFromStore ) for consistency. 
        Provides two entry methods, 
           test_full_log - assumes an optionsIn=all
           test_header_only_log - assumes an optionsIn=header-only 
        """    
    
    xmlValue = None
    
    setupFlag = False
    
    MNEMONIC_NAME = "Mnemonic"
    LOG_NULL_NAME = 'LogNullName'
    CURVE_NULL_NAME = 'CurveNullName'
    CURVE_DATA_TYPE_NAME = "CurveDataType"
    CURVE_ARRAY_DIM_NAME = "CurveArrayDim"
    IS_INDEX_CURVE = "IsIndexCurve"
    
    def __init__(self, value=None):
        """
        Initialization of the returned value 
        
        Parameters:
          value:  Value to be used for the XmlValue in response
        """
        self.setupFlag = False
        
        self.xmlValue = value
     
    # public methods
    def test_full_log(self, verbose=False, strict=False):
        """ Expecting a log acquired from returnElements=all, if a failure occurs, we quit 
         
            Parameters:
              verbose: output messages 
              strict:  if true, run extra validation, false if not        

            Returns:
              True if all pass, or False otherwise        
        """
        self.setupFlag = False   
        self._test_full_log_private(verbose, strict)  
    
    def test_header_only_log(self, verbose=False, strict=False):
        """ Expecting a log acquired from returnElements=header-only, if a failure occurs, we quit 
            Parameters:
              verbose: output messages 
              strict:  if true, run extra validation, false if not             
                     
           Returns:
              True if all pass, or False otherwise          
        """
        self.setupFlag = False            
        self._test_header_only_log(verbose, strict)         
     
    def test_requestLatestValues_full_log(self, numberOfExpectedValues=1, verbose=False, strict=False):
        """ Expecting a log acquired from returnElements=all and requestLatestValues=numberOfExpectedValues, if a failure occurs, we quit 
         
            Parameters:
              numberOfExpectedValues: expected number of values
              verbose: output messages 
              strict:  if true, run extra validation, false if not        

           Returns:
              True if all pass, or False otherwise          
        """
        self.setupFlag = False            
        self._test_requestLatestValues_full_log_private(numberOfExpectedValues, False, verbose, strict)  
        
    def test_requestLatestValues_full_log_max(self, numberOfExpectedValues=1, verbose=False, strict=False):
        """ Expecting a log acquired from returnElements=all and requestLatestValues<=numberOfExpectedValues, if a failure occurs, we quit 
         
            Parameters:
              numberOfExpectedValues: expected number of values
              verbose: output messages 
              strict:  if true, run extra validation, false if not        

           Returns:
              True if all pass, or False otherwise          
        """ 
        self.setupFlag = False           
        self._test_requestLatestValues_full_log_private(numberOfExpectedValues, True, verbose, strict)           
     
    def test_dataOnly_log(self, verbose=False, strict=False):
        """ Expecting a log acquired from returnElements=data-only, if a failure occurs, we quit 
         
            Parameters:
              verbose: output messages 
              strict:  if true, run extra validation, false if not        

            Returns:
              True if all pass, or False otherwise        
        """
        self.setupFlag = False            
        self._test_dataOnly_log_private(verbose, strict) 
     
    def test_dataOnly_log_extended(self, curveListDict, verbose=False, strict=False):
        """ Expecting a log acquired from returnElements=data-only, if a failure occurs, we quit.
            This method relies on the caller to supply addition info ( i.e. above what is in the content of a data-only return
            to provide more robust checks.) that is obtained via get_CurveInfo_Dictionary()
         
            Parameters:
              curveListDict:  curve info dictionary
              verbose: output messages 
              strict:  if true, run extra validation, false if not        

            Returns:
              True if all pass, or False otherwise        
        """
        self.setupFlag = False            
        self._test_dataOnly_log_private(verbose, strict, curveListDict)      
     
    def get_CurveInfo_Dictionary(self, verbose=None, strict=False): 
        """ Access the current Log and return a dictionary of info of it's logCurveInfo data
         
            Parameters:
              verbose: output messages 
              strict:  if true, run extra validation, false if not        

            Returns:
              Dictionary of logCurveInfo          
        
        """
        self.setupFlag = False
        # make sure the current log passes at least the header only tests
        passFail = self._test_header_only_log(verbose, strict)
        if not(passFail):  return None
       
        curveListDict = self._test_get_CurveInfo_Dictionary(verbose)
        return curveListDict    

             
     
    # start usage of other library methods
    def _get_XMLout_Element_String(self, tag, startElement=None):
       return self.xmlValue.get_element_text_value(tag,startElement)
    
    def _get_XMLout_Attribute_String(self, tag, attribute, startElement=None):
       return self.xmlValue.get_attribute(tag, attribute, startElement )
    
    def _get_XMLout_RecurringElement_List(self, tag, startElement=None):
       return self.xmlValue.get_recurring_element_list(tag, startElement)
       
    def _get_logData_NumberOfNodes_Int(self):
       return self.xmlValue.get_log_data_number_of_nodes()  
       
    def _get_logData_IndexValue_String(self, n):
        return self.xmlValue.get_log_data_index_value(n)   
    
    def _get_logData_DataValue_String(self, n, mnemonic):
        return self.xmlValue.get_log_data_data_value(n,mnemonic)   
    
    def _get_log_data(self):
        return self.xmlValue.get_log_data();
    
    def _get_log_curve_array_length(self, mnemonic):
        return self.xmlValue.get_log_curve_array_length(mnemonic) 
       
    def _check_XMLout_ElementValue(self, tag, expected_value, _start_element=None):
        return self.xmlValue.check_element_value(tag, expected_value, _start_element ) 
       
    def _getGlobalElementNode(self, xpath_string, object_index=None):
        """ Retrieves embedded Nodes from the log document """
        xpath_string = wtl.utils.process_string(xpath_string)
        elements = self.xmlValue.get_element(xpath_string, object_index)
        return elements
    
    def _getLogNullValue(self):
        return self._get_XMLout_Element_String('/logs/log[$logIndex$]/nullValue')
    
    def _getCurveNullValue(self, mnemonic ):
        _set('mnemonicVar', mnemonic)
        return self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/nullValue')
    
    def _getCurveDataType(self, mnemonic):
       _set('mnemonicVar', mnemonic)
       return self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/typeLogData')
   
    def _getIndexCurveNameFromCurveListDict(self, curveListDict):
        """Get the Index curve name from the curveListDict """
        for mnemonic in curveListDict:
            curveInfoDict = curveListDict[mnemonic]
            if ( curveInfoDict[self.IS_INDEX_CURVE] ):
                return curveInfoDict[self.MNEMONIC_NAME]
        return None
               
    def _getCurveNullFromCurveListDict(self, callersMnemonic, curveListDict):
        """Get the Curve Null from the curveListDict """
        for mnemonic in curveListDict:
            if ( mnemonic == callersMnemonic):
                curveInfoDict = curveListDict[mnemonic]
                return curveInfoDict[self.CURVE_NULL_NAME]
        return None
    
    def _getCurveDataTypeFromCurveListDict(self, callersMnemonic, curveListDict):
        """Get the Curve Data Type from the curveListDict """
        for mnemonic in curveListDict:
            if ( mnemonic == callersMnemonic):
                curveInfoDict = curveListDict[mnemonic]
                return curveInfoDict[self.CURVE_DATA_TYPE_NAME]
        return None  
    
    def _getCurveArrayLengthFromCurveListDict(self, callersMnemonic, curveListDict):
        """Get the Curve Data Type from the curveListDict """
        for mnemonic in curveListDict:
            if ( mnemonic == callersMnemonic):
                curveInfoDict = curveListDict[mnemonic]
                return curveInfoDict[self.CURVE_ARRAY_DIM_NAME]
        return None       
    
    def _getLogNullFromCurveListDict(self, callersMnemonic, curveListDict):
        """Get the Log Null from the curveListDict """
        for mnemonic in curveListDict:
            if ( mnemonic == callersMnemonic):
                curveInfoDict = curveListDict[mnemonic]
                return curveInfoDict[self.LOG_NULL_NAME]
        return None                    
    # end usage of other library methods   
   
            
    # local methods
    def _isDepthBasedLog(self, indexType):
        """ Is this a depth based log """
        if indexType == 'measured depth':
            return True
        elif indexType == 'vertical depth':
            return True
        else:
            return False
       
    def _isTimeBasedLog(self, indexType):
        """ Is this a time based log """
        if indexType == 'date time':
            return True
        else:
            return False       
      
    def _test_get_CurveInfo_Dictionary(self, verbose):  
        """ Access the current Log and return a dictionary of info of it's logCurveInfo data """
        # make sure the current log passes at least the header only tests
        # look thru all log curves to see if they are defined in the mnemonic List
        logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')
        logNullValue = self._getLogNullValue()
        curveListDict = {}        
        for mnemonic in logCurveInfoMnemonics:
            curveInfoDict = {}
            curveInfoDict[self.MNEMONIC_NAME] = mnemonic
            curveInfoDict[self.LOG_NULL_NAME] = logNullValue
            curveNullValue = self._getCurveNullValue(mnemonic)
            curveInfoDict[self.CURVE_NULL_NAME] = curveNullValue
            curveDataType = self._getCurveDataType(mnemonic)
            curveInfoDict[self.CURVE_DATA_TYPE_NAME] = curveDataType
            curveArrayDim = self._get_log_curve_array_length(mnemonic)
            curveInfoDict[self.CURVE_ARRAY_DIM_NAME] = curveArrayDim
            isIndexCurve = mnemonic == _get('indexCurve')
            curveInfoDict[self.IS_INDEX_CURVE] = isIndexCurve
            curveListDict[mnemonic] = curveInfoDict
            
        return curveListDict
    
    
    
    def _test_dataOnly_log_private(self, verbose, strict, curveListDict=None):
        """ Expect a data-only log, i.e. with only logData"""
              
        """ non expected header info ?? """
        test = '_test_dataOnly_log_private:'
        passFail = self._setup(False,verbose)
        if not(passFail):  return False
        
        passFail = self._test_mnemonicsAreUnique(verbose)                    
        if not(passFail):  return False  
        
        passFail = self._log_dataOnly_numberOfCurve_Test(verbose)
        if not(passFail):  return False      
        
        indexCurveMnemonic = None
        if ( curveListDict is not None ):
            indexCurveMnemonicTemp = self._getIndexCurveNameFromCurveListDict(curveListDict)          
            if ( indexCurveMnemonicTemp is None ):
                self._Fail("setup", "IndexCurve is not defined")
                return False
            else:
                """data-only may not have the index curve. """                
                mnList = _get('mnenmonicList').split(",")                 
                if ( indexCurveMnemonicTemp in mnList ):
                    indexCurveMnemonic = indexCurveMnemonicTemp
                else:
                    if verbose:
                        _log(test + ' index curve ' +  indexCurveMnemonicTemp + ' is not defined in mnemonicList')                                  
        
        if ( indexCurveMnemonic is not None ):
            _set("indexCurve",indexCurveMnemonic)
            _set("logCurveInfoMnemonicList", _get( 'mnenmonicList'))
            passFail = self.test_index_curve(verbose)
            if not(passFail):  return False
                   
            
        passFail = self._log_dataOnly_checkNullValues_Test(verbose,indexCurveMnemonic)
        if not(passFail):  return False
        
        if ( curveListDict is not None ):
            passFail = self._test_get_dataContainsCorrectDataType(verbose, curveListDict) 
            if not(passFail):  return False
        
        return True;        
      
    def _test_full_log_private(self, verbose, strict):
        """ Expect a full log, i.e. with logCurveInfo and logData"""
        passFail = self._setup(True,verbose)
        if not(passFail):  return False
        
        if self._isTimeBasedLog(_get( 'indexType')) == False:
           # depth based processing 
           if strict:
             passFail = self._log_Datum_defined(verbose)
             if not(passFail):  return False
                
           passFail = self._test_get_direction_of_data_matches_header_depth(verbose)
           if not(passFail): return False
               
           passFail = self._log_validate_start_end_index_depth(verbose)
           if not(passFail):  return False
        
           passFail = self.test_log_curve_info_min_max_depth(verbose)
           if not(passFail):  return False
        
           if strict:
              passFail = self.test_log_curve_info_min_max_depth_uom(verbose)
              if not(passFail):  return False
           
           passFail = self.test_log_curve_first_last_value_depth(verbose)
           if not(passFail):  return False 
                   
        else:
            passFail = self._test_get_direction_of_data_matches_header_time(verbose) 
            if not(passFail):  return False
                        
            passFail = self._log_validate_start_end_index_time(verbose)       
            if not(passFail):  return False
            
            passFail = self.test_log_curve_info_min_max_time(verbose)
            if not(passFail):  return False            
        
            passFail = self.test_log_curve_first_last_value_time(verbose)
            if not(passFail):  return False  
                 
        passFail = self.test_log_curve_array_header(verbose)         
        if not(passFail):  return False 
                         
        passFail = self.test_log_curve_array_data(verbose)
        if not(passFail):  return False                     
                    
        passFail = self.test_index_curve(verbose)
        if not(passFail):  return False        
        
        passFail = self._test_do_log_curve_info_mnemonics_match_mnemonicList(verbose)
        if not(passFail):  return False
        
        curveListDict = self._test_get_CurveInfo_Dictionary(verbose)
        
        passFail = self._test_get_dataContainsCorrectDataType(verbose, curveListDict)
        if not(passFail):  return False
        
        passFail = self._test_mnemonicsAreUnique(verbose)
        if not(passFail):  return False         
                
        return True
        
     
    def _test_requestLatestValues_full_log_private(self, numberOfExpectedValues, isMax, verbose, strict):
        """ Expect a full log, i.e. with logCurveInfo and logData in a requestLatestValue mode"""
        passFail = self._setup(True, verbose)
        
        # log should still pass normal log requirements
        passFail = self._test_full_log_private(verbose, strict) 
        if not(passFail):  return False 
        
        # verify there are the correct number of values
        passFail = self._log_check_requestLatestValue(numberOfExpectedValues, isMax, verbose, strict)
        if not(passFail):  return False 
 
        return True
                    
    
                
    def _test_header_only_log(self, verbose, strict ):
        """ Expect a header only log, i.e. with logCurveInfo and no logData"""
        passFail = True
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
   
        passFail = self.test_index_curve(verbose)
        if not(passFail):  return False 
                              
        if self._isTimeBasedLog(_get( 'indexType')) == False:                                     
            passFail = self._log_validate_start_end_index_depth(verbose)
            if not(passFail):  return False 
                       
            passFail = self.test_log_curve_info_min_max_depth(verbose)
            if not(passFail):  return False 
        
            if strict:
               passFail = self.test_log_curve_info_min_max_depth_uom(verbose)
               if not(passFail):  return False 
        
        else:
            passFail = self._log_validate_start_end_index_time(verbose)       
            if not(passFail):  return False 
            
            passFail = self.test_log_curve_info_min_max_time(verbose)
            if not(passFail):  return False 
                
        passFail = self.test_log_curve_array_header(verbose)         
        if not(passFail):  return False                 
                    
        return True
             
        
    def _setup(self, headerShouldExists, verbose):
        """ Initialize all variables for all tests"""
        if self.setupFlag == False:
            logsNode = self._getGlobalElementNode('logs')
            if logsNode is None:
                _Fail('self', 'This is not a log object')
                return False
                
            _set( 'logIndex', '1')
            
            if ( headerShouldExists == True ):
                
                _set( 'indexType', self._get_XMLout_Element_String('logs/log[$logIndex$]/indexType'))
                
                if self._isTimeBasedLog(_get( 'indexType')) == False:
                   startIndexString = self._get_XMLout_Element_String('logs/log[$logIndex$]/startIndex')
                   if ( startIndexString is not None ):
                       _set( 'startIndex', float(startIndexString))
                       _set( 'startIndexUom', self._get_XMLout_Attribute_String( 'logs/log[$logIndex$]/startIndex', 'uom' ) )
                   else:
                       self._Fail("setup", "startIndex is not defined")
                       return False
                   endIndexString = self._get_XMLout_Element_String('logs/log[$logIndex$]/endIndex')
                   if ( endIndexString is not None ):
                       _set( 'endIndex', float(endIndexString))
                       _set( 'endIndexUom', self._get_XMLout_Attribute_String( 'logs/log[$logIndex$]/endIndex', 'uom' ) )
                   else:
                       self._Fail("setup", "endIndex is not defined")  
                       return False                   
                   _set( 'stepIncrement', self._get_XMLout_Element_String( 'logs/log[$logIndex$]/stepIncrement') )
                else:
                   startIndexString = self._get_XMLout_Element_String('logs/log[$logIndex$]/startDateTimeIndex')
                   if ( startIndexString is not None ):                
                       _set( 'startDateTimeIndex', startIndexString)
                   else:
                       self._Fail("setup", "startDateTimeIndex is not defined")
                       return False                         
                   endIndexString = self._get_XMLout_Element_String('logs/log[$logIndex$]/endDateTimeIndex')   
                   if ( endIndexString is not None ):                               
                       _set( 'endDateTimeIndex', endIndexString)
                   else:
                       self._Fail("setup", "endDateTimeIndex is not defined")
                       return False                                   
                    
                _set( 'direction', self._get_XMLout_Element_String('logs/log[$logIndex$]/direction'))
                if _get('direction') is None:
                    if verbose:
                        _log('direction is not defined, which means its assumed to be increasing')
                    _set( 'direction', 'increasing')
                                      
                _set( 'indexCurve', self._get_XMLout_Element_String('logs/log[$logIndex$]/indexCurve'))     
                _set( 'logCurveInfoMnemonicList', self._get_XMLout_RecurringElement_List('logs/log[$logIndex$]/logCurveInfo/mnemonic'))
            
            _set( 'mnenmonicList', self._get_XMLout_Element_String('mnemonicList'))   
            _set( 'unitList', self._get_XMLout_Element_String('unitList'))

            logDataNodes = self._getGlobalElementNode('logs/log[$logIndex$]/logData')
            if logDataNodes is not None and len(logDataNodes) > 0:
                _set( 'logData' ,  self._getGlobalElementNode('logs/log[$logIndex$]/logData'))
                _set( 'numberOfDataRows', self._get_logData_NumberOfNodes_Int())
            else:
                _set( 'logData' , list())
                _set( 'numberOfDataRows', 0) 
               
        self.setupFlag = True
        return True
        
    def _log_dataOnly_numberOfCurve_Test(self, verbose):
        """ Do the number of mnemonics, units and values per row match """
        test = '_log_dataOnly_numberOfCurve_Test' 
        if len(_get('logData')) > 0: 
            # are the same number of entries 
            mnList = _get('mnenmonicList').split(",")
            unitList = _get('unitList').split(",")
            numberOfCurves = len(mnList)
            numberofUnits = len(unitList)
            if ( numberOfCurves != numberofUnits ):
                self._Fail(test, "Number of mnemonics " + str(numberOfCurves) + " != number of units " + str(numberofUnits))
                return False
            
            logData = self._get_log_data()
            numberOfValuesInEachRow = len(logData[0])
            if ( numberOfCurves != numberOfValuesInEachRow ):
                self._Fail(test, "Number of mnemonics " + str(numberOfCurves) + " != number of values " + str(numberOfValuesInEachRow))
                return False
                       
        return True        
      
    def _log_dataOnly_checkNullValues_Test(self, verbose, indexCurveMnemonic=None):
        """ Do each curve have a least one non null value.
        
            Parameters:
              verbose: output messages 
              indexCurveName:  indexCurveName           
        
        """
        test = '_log_dataOnly_checkNullValues_Test' 
        if len(_get('logData')) > 0: 
            mnList = _get('mnenmonicList').split(",")
            
            #check index curve has all non null values
            if ( indexCurveMnemonic is not None ):
                for row in range(_get("numberOfDataRows")):
                    valueString = self._get_logData_DataValue_String(row,indexCurveMnemonic)
                    isNull = self._isCurveValueNullPrivate(valueString, None, None, None )
                    if ( isNull == True ):
                        self._Fail(test, "Index curve is null at row " + str(row) )
                        return False                    
            
            # see if all curves have at least one value
            for mnemonic in mnList:
                foundValue = False
                for row in range(_get("numberOfDataRows")):
                   valueString = self._get_logData_DataValue_String(row, mnemonic)
                   isNull = self._isCurveValueNullPrivate(valueString, None, None, None )
                   if ( isNull == False ):
                       foundValue= True
                       break
                if ( foundValue == False):
                   self._Fail(test, "Curve " + mnemonic + " has all null values "  )
                   return False                      
                
        return True       
        
    def _log_check_requestLatestValue(self, numberOfExpectedValues, isMax, verbose, strict): 
        """ _log_check_requestLatestValue 
         
            Parameters:
              numberOfExpectedValues: expected number of values
              verbose: output messages 
              isMax:   if true, very number of values <= numberOfExpectedValues, if false, expect number == numberOfExpectedValues
              strict:  if true, run extra validation, false if not        

           Returns:
              True if all pass, or False otherwise          
        """          
        test = '_log_check_requestLatestValue'   
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
                
        # find index of curve first non null value
        numberOfRows = self._get_logData_NumberOfNodes_Int(); 
            
        mnList = _get('mnenmonicList').split(",")
        logNullValue = self._getLogNullValue()       
        indexCurveName = _get('indexCurve') 
        
        # what is the expected number of non-index curves            
        numberOfCurves = len(mnList)
        if indexCurveName is not None and indexCurveName in mnList:
           numberOfCurves -= 1      
             
        # number of rows should be less the the number of curves and the expected values, i.e. if 5 curves and 5 values then max <= 25
        maxExpectedRows = numberOfCurves * numberOfExpectedValues
        if numberOfRows <= maxExpectedRows:    
            for mnemonic in mnList:    
                if ( indexCurveName != mnemonic ): 
                    curveNullValue = self._getCurveNullValue(mnemonic)                          
                    curveDataType = self._getCurveDataType(mnemonic)                 
                    valueCount = 0 
                    for row in range(numberOfRows):                                
                        value = self._get_logData_DataValue_String(row,mnemonic)
                        curve_array_length = self._get_log_curve_array_length(mnemonic)
                        if self._isCurveValueNull(value,curveDataType,curveNullValue,logNullValue,curve_array_length) == False: 
                             valueCount += 1         
                    if ( isMax ):        
                        if valueCount > numberOfExpectedValues:
                            self._Fail(test, "Curve " + mnemonic + " number of values is " + str(valueCount) + " but expecting " + str(numberOfExpectedValues))
                            return False
                    else:
                        if valueCount != numberOfExpectedValues:
                            self._Fail(test, "Curve " + mnemonic + " number of values is " + str(valueCount) + " but expecting " + str(numberOfExpectedValues))
                            return False                        
                
        else:
            self._Fail(test, "With " + str(numberOfCurves) + " non index curves, numberOfRows " + str(numberOfRows) + " exceeds max expected rows " + str(maxExpectedRows))
            return False
            
        return True
        
    def _log_Datum_defined(self, verbose ):
        """ Is the Datum of the depth based log defined""" 
        test = '_log_Datum_defined'   
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
        
        if verbose:
           _log('doing ' + test )
        
        defaultDatumUid = self._get_XMLout_Attribute_String('logs/log[$logIndex$]/commonData/defaultDatum','uidRef')
        wellDatumUid = self._get_XMLout_Attribute_String('logs/log[$logIndex$]/logCurveInfo[mnemonic="$indexCurve$"]/wellDatum', 'uidRef')
        
        if defaultDatumUid is None and wellDatumUid is None:
            self._Fail(test, 'datum is not defined')
            return False
        
        if verbose:        
            _partial_success('passed ' + test)
            
        return True
        
    def _log_validate_start_end_index_depth(self, verbose):
        """ Are the indexes of a depth based log correct""" 
        test = '_log_validate_start_end_index_depth'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
       
        if verbose:
            _log('doing ' + test )
       
        #ensure startIndex and endIndex exist
        if ( _get('startIndex') is None ): 
            self._Fail(test, "startIndex is not defined ")
            return False
        if ( _get('endIndex') is None ): 
            self._Fail(test, 'endIndex is not defined'  )
            return False
        # ensure startIndex and endIndex have uom's
        if ( _get('startIndexUom') is None ): 
            self._Fail(test, 'startIndexUom is not defined '  )
            return False
        if ( _get('endIndexUom') is None ): 
            self._Fail(test, 'endIndexUom is not defined '  )
            return False
            
        # ensure startIndex endIndex values are correct
        if self._isDirectionUnknown(_get('direction')) == False:
           if self._isDirectionIncreasing(_get('direction')): 
             if ( _get('startIndex') > _get('endIndex') ):
                self._Fail(test, 'log is defined as increasing but startIndex > endIndex ' + str(_get('startIndex')) + " " + str(_get('endIndex')) )
                return False
           else: 
             if ( _get('startIndex') < _get('endIndex') ):
                self._Fail(test,'log is defined as decreasing but startIndex < endIndex ' + str(_get('startIndex')) + " " + str(_get('endIndex')) )
                return False
        else:
           if verbose:
              _log(test + " direction is unknown, skipping startIndex and endIndex comparison")
        
        
        #ensure startstart startIndexUom and endIndexUom are the same
        if ( _get('startIndexUom') != _get('endIndexUom') ):
            self._Fail(test, 'log.startIndexUom != log.endIndexUom' + _get('startIndexUom') + " " + _get('endIndexUom') )  
            return False  
        
        # does start index match first index value and last index in the data
        if len(_get('logData')) > 0:
           if self._compareDoubleEquals(float(self._get_XMLout_Element_String('startIndex')),float(self._get_logData_IndexValue_String(0))) == False:
                self._Fail(test,"log.startIndex  != first Index in logData/data " + self._get_XMLout_Element_String('startIndex') + " " + self._get_logData_IndexValue_String(0) )
                return False 
           else:
              if verbose:               
                  _partial_success("'log.startIndex' matches logData Section first value")             
        
           # does end index match last index value
           if self._compareDoubleEquals(float(self._get_XMLout_Element_String('endIndex')),float(self._get_logData_IndexValue_String(_get('numberOfDataRows')-1))) == False:
                self._Fail(test,"log.endIndex  != last Index in logData/data " + self._get_XMLout_Element_String('startIndex') + " " + self._get_logData_IndexValue_String(_get('numberOfDataRows')-1) )
                return False 
           else:
              if verbose:                
                  _partial_success("'log.endIndex' matches logData Section first value")             
                    
        if verbose:          
            _partial_success('passed ' + test) 
        return True
    
    def _log_validate_start_end_index_time(self, verbose):
        """ Are the indexes of a time based log correct""" 
        test = '_log_validate_start_end_index_time'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
       
        if verbose:
            _log('doing ' + test )
       
             
        #ensure startDateTimeIndex and endDateTimeIndex exist
        if ( _get('startDateTimeIndex') is None ): 
            self._Fail(test, "log.startDateTimeIndex is not defined")
            return False
        if ( _get('endDateTimeIndex') is None ): 
            self._Fail(test, 'log.endDateTimeIndex is not defined '  )
            return False

            
        # ensure startDateTimeIndex endDateTimeIndex values are correct  
        startTimeIndex = wtl.utils.iso_to_utc(_get('startDateTimeIndex'), True)
        endTimeIndex = wtl.utils.iso_to_utc(_get('endDateTimeIndex'), True)  
        
        # ensure startIndex endIndex values are correct
        if self._isDirectionUnknown(_get('direction')) == False:
           if self._isDirectionIncreasing(_get('direction')): 
               if ( startTimeIndex > endTimeIndex):
                   self._Fail(test,'log.startDateTimeIndex > log.endDateTimeIndex ' + _get('startDateTimeIndex') + " " + _get('endDateTimeIndex') )
                   return False
           else: 
               if ( startTimeIndex < endTimeIndex):
                   self._Fail(test,'log.startDateTimeIndex < log.endDateTimeIndex ' + _get('startDateTimeIndex') + " " + _get('endDateTimeIndex') )
                   return False
        else:
           if verbose:
              _log(test + " direction is unknown, skipping startIndex and endIndex comparison")
               
               
                                      
        # does start index match first index value and last index in the data
        if len(_get('logData')) > 0:
           startTimeData = wtl.utils.iso_to_utc(self._get_logData_IndexValue_String(0), True)
           endTimeData = wtl.utils.iso_to_utc(self._get_logData_IndexValue_String(_get('numberOfDataRows')-1), True)
           if ( startTimeIndex != startTimeData ):
             self._Fail(test,'log.startDateTimeIndex != first index value in logData/data' + _get('startDateTimeIndex') + " " + self._get_logData_IndexValue_String(0) )
             return False
         
           if ( endTimeIndex != endTimeData ):
             self._Fail(test,'log.endDateTimeIndex != last index value in logData/data' + _get('startDateTimeIndex') + " " + self._get_logData_IndexValue_String(_get('numberOfDataRows')-1) )
             return False        
          
        if verbose:          
            _partial_success('passed ' + test) 
        return True
    
     
    def _test_do_log_curve_info_mnemonics_match_mnemonicList(self, verbose):
        """ Do the logCurveInfo.mnemonics match the mnemonicList"""
        test = '_test_do_log_curve_info_mnemonics_match_mnemonicList'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
        
        if len(_get('logData')) > 0:
        
            if verbose:
                _log('doing ' + test )
        
            unitList = _get('unitList').split(",")
            mnList = _get('mnenmonicList').split(",")
            logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')
             
            # look thru all log curves to see if they are defined in the mnemonic List
            for mnemonic in logCurveInfoMnemonics:
                _set('mnemonicVar', mnemonic)
                uid = self._get_XMLout_Attribute_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]','uid')
                if (mnemonic is not None):
                    indexOfCurve = -1
                    try:
                        indexOfCurve = mnList.index(mnemonic)
                    except ValueError:
                        self._Fail(test,"logCurveInfo.mnenonic " + mnemonic + " not found in logData.mnemonicsList")
                        return False                    
                    unit = self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/unit')    
                    if (unit is not None):
                        if unitList[indexOfCurve] != unit:  
                            self._Fail(test,"logCurveInfo.unit " + unit + " does not match logData.unitList " + unitList[indexOfCurve] + " for mnenonic " + mnemonic )
                            return False
                    else :
                        if unitList[indexOfCurve] != '':  
                            self._Fail(test,"logCurveInfo.unit [blank] does not match unitList")
                            return False
                else :
                    self._Fail(test,"logCurveInfo.mnenonic is null for uid " + uid)
                    return False
            if verbose:                    
                _partial_success('passed ' + test)
        else:
            if verbose:            
                _partial_success('skipped ' + test)
            
        return True
        
    def test_index_curve(self, verbose):
        """ Does the Index curve exist in the logCurveInfo.mnemonics and mnemonicList"""
        test = 'test_index_curve'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
        
        if verbose:
            _log('doing ' + test )
         
        # see if indexCurve is in the log Curve Info
        indexCurveName = _get('indexCurve')
        if indexCurveName is None:
             self._Fail(test,"log.indexCurve is not defined " )
             return False
                     
        
        if len(_get('logData')) > 0:
            # see if is first curve in mnemonicList
            mnList = _get('mnenmonicList').split(",")
            if indexCurveName != mnList[0]:
                 self._Fail(test,"log.indexCurve is not the first mnemonic in logData.mnemonicList" + indexCurveName )
                 return False            
        
        # see if defined in logCurveInfo
        logCurveInfoMnemonicList = _get('logCurveInfoMnemonicList')
        try:
            indexOfCurve = logCurveInfoMnemonicList.index(indexCurveName)
        except ValueError:
             self._Fail(test,"log.indexCurve does not exist in logCurveInfo set " + indexCurveName )
             return False        
        
        if verbose:
            _partial_success('passed ' + test)  
        return True

 
    def test_log_curve_info_min_max_depth(self, verbose):
        """ Are the LogCurveInfo minIndex and maxIndex within the log startIndex and endIndex"""
        test = 'test_log_curve_info_min_max_depth'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
 
        if self._isDirectionUnknown(_get('direction')) == False:
            if verbose:
                _log('doing ' + test )
             
            logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')                
            direction = _get('direction')
             
            # look thru all log curves to see if their start end index are a subset of the log index
            for mnemonic in logCurveInfoMnemonics:
                _set('mnemonicVar', mnemonic)
                minIndex = float(self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/minIndex'))
                maxIndex = float(self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/maxIndex'))
                if self._isDirectionIncreasing(_get('direction')):
                    if ( minIndex < _get('startIndex') ):
                        self._Fail(test,"logCurveInfo.minIndex < log.startIndex " + str(minIndex) + " " + str(_get('startIndex')) + " for mnemonic " + mnemonic)
                        return False
                    if ( minIndex > _get('endIndex') ):
                        self._Fail(test,"logCurveInfo.minIndex > log.endIndex " + str(minIndex) + " " + str(_get('endIndex')) + " for mnemonic " + mnemonic)
                        return False
                    if ( maxIndex > _get('endIndex') ):
                        self._Fail(test,"logCurveInfo.maxIndex > log.endIndex " + str(maxIndex) + " " + str(_get('endIndex')) + " for mnemonic " + mnemonic)
                        return False                
                else:              
                    if ( minIndex > _get('startIndex') ):
                        self._Fail(test,"logCurveInfo.minIndex > log.startIndex " + str(minIndex) + " " + str(_get('startIndex')) + " for mnemonic " + mnemonic)
                        return False
                    if ( minIndex < _get('endIndex') ):
                        self._Fail(test,"logCurveInfo.minIndex < log.endIndex " + str(minIndex) + " " + str(_get('endIndex')) + " for mnemonic " + mnemonic)
                        return False      
                    if ( maxIndex < _get('endIndex') ):
                        self._Fail(test,"logCurveInfo.maxIndex < log.endIndex " + str(maxIndex) + " " + str(_get('endIndex')) + " for mnemonic " + mnemonic)
                        return False                           
                if ( maxIndex < minIndex ):
                    self._Fail(test,"logCurveInfo.maxIndex < logCurveInfo.minIndex " + str(maxIndex) + " " + str(minIndex) + " for mnemonic " + mnemonic)
                    return False
    
                if verbose:                      
                    _partial_success('passed ' + test) 
                    
        else:
           if verbose:
              _log(test + " direction is unknown, skipping test")
                    
        return True
      
    def test_log_curve_first_last_value_depth(self, verbose):
        """ Are the LogCurveInfo minIndex and maxIndex matching with the actual first and last value """
        test = 'test_log_curve_first_last_value_depth'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
 
        if self._isDirectionUnknown(_get('direction')) == False:
            if verbose:
                _log('doing ' + test )
             
            logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')
            logNullValue = self._getLogNullValue()                
                    
            # look thru all log curves to see if their start end index match the actual first and last non null value
            for mnemonic in logCurveInfoMnemonics:
                _set('mnemonicVar', mnemonic)
                minIndex = float(self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/minIndex'))
                maxIndex = float(self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/maxIndex'))
                curveNullValue = self._getCurveNullValue(mnemonic)
                curveDataType = self._getCurveDataType(mnemonic)
                
                # find index of curve first non null value
                numberOfRows = self._get_logData_NumberOfNodes_Int(); 
                indexValueOfFirstNonNull = None
                for row in range(numberOfRows):
                     value = self._get_logData_DataValue_String(row,mnemonic)
                     curve_array_length = self._get_log_curve_array_length(mnemonic)
                     if self._isCurveValueNull(value,curveDataType,curveNullValue,logNullValue,curve_array_length) == False:
                         indexValueOfFirstNonNull = float(self._get_logData_IndexValue_String(row))         
                         break
                     
                #logCurveInfo minIndex and maxIndex are direction independent.
                if ( self._isDirectionIncreasing(_get('direction'))):
                    if self._compareDoubleEquals(minIndex,indexValueOfFirstNonNull) == False:
                        self._Fail(test,"logCurveInfo.minIndex != first non null Index in logData/data " + str(minIndex) + " " + str(indexValueOfFirstNonNull) + " for mnemonic " + mnemonic)
                        return False 
                else:                   
                    if self._compareDoubleEquals(maxIndex,indexValueOfFirstNonNull) == False:
                        self._Fail(test,"logCurveInfo.maxIndex != Last non null Index in logData/data " + str(maxIndex) + " " + str(indexValueOfFirstNonNull) + " for mnemonic " + mnemonic)
                        return False                  
                     
                # find index of curve last non null value
                numberOfRows = self._get_logData_NumberOfNodes_Int(); 
                indexValueOfLastNonNull = -1
                reverseRange = range(numberOfRows)
                reverseRange.reverse()
                for row in reverseRange:
                     value = self._get_logData_DataValue_String(row,mnemonic)
                     curve_array_length = self._get_log_curve_array_length(mnemonic)
                     if self._isCurveValueNull(value,curveDataType,curveNullValue,logNullValue,curve_array_length) == False:
                         indexValueOfLastNonNull = float(self._get_logData_IndexValue_String(row))          
                         indexOfFirstNonNull = row
                         break  
                        
                if ( self._isDirectionIncreasing(_get('direction'))):                    
                    if self._compareDoubleEquals(maxIndex,indexValueOfLastNonNull) == False:
                        self._Fail(test,"logCurveInfo.maxIndex != last non null Index in logData/data " + str(maxIndex) + " " + str(indexValueOfLastNonNull) + " for mnemonic " + mnemonic)
                        return False 
                else:                  
                    if self._compareDoubleEquals(minIndex,indexValueOfLastNonNull) == False:
                        self._Fail(test,"logCurveInfo.maxIndex != first non null Index in logData/data " + str(minIndex) + " " + str(indexValueOfLastNonNull) + " for mnemonic " + mnemonic)
                        return False                 
                       
                if verbose:              
                    _partial_success('passed ' + test) 
        else:
           if verbose:
              _log(test + " direction is unknown, skipping test")  
                                
        return True
      
    def test_log_curve_first_last_value_time(self, verbose):
        """ Are the LogCurveInfo minDateTimeIndex and maxDateTimeIndex matching with the actual first and last value """
        test = 'test_log_curve_first_last_value_time'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
 
        if self._isDirectionUnknown(_get('direction')) == False: 
 
            if verbose:
                _log('doing ' + test )
             
            logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')                
                  
            logNullValue = self._getLogNullValue()        
                            
            # look thru all log curves to see if their start end index match the actual first and last non null value
            for mnemonic in logCurveInfoMnemonics:
                _set('mnemonicVar', mnemonic)
                minIndex = wtl.utils.iso_to_utc(self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/minDateTimeIndex'))
                maxIndex = wtl.utils.iso_to_utc(self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/maxDateTimeIndex'))
                curveNullValue = self._getCurveNullValue(mnemonic)
                curveDataType = self._getCurveDataType(mnemonic)
                            
                # find index of curve first non null value
                numberOfRows = self._get_logData_NumberOfNodes_Int(); 
                indexValueOfFirstNonNull = None
                for row in range(numberOfRows):
                     value = self._get_logData_DataValue_String(row,mnemonic)
                     curve_array_length = self._get_log_curve_array_length(mnemonic)
                     if self._isCurveValueNull(value,curveDataType,curveNullValue,logNullValue,curve_array_length) == False:
                         indexValueOfFirstNonNull = wtl.utils.iso_to_utc(self._get_logData_IndexValue_String(row))         
                         break
                     
                #logCurveInfo minIndex and maxIndex are direction independent.
                if ( self._isDirectionIncreasing(_get('direction'))):                 
                    if ( minIndex != indexValueOfFirstNonNull):
                        self._Fail(test,"logCurveInfo.minDateTimeIndex != first non null Index in logData/data " + str(minIndex) + " " + str(indexValueOfFirstNonNull) + " for mnemonic " + mnemonic)
                        return False 
                else:                   
                    if ( maxIndex != indexValueOfFirstNonNull):
                        self._Fail(test,"logCurveInfo.maxDateTimeIndex != Last non null Index in logData/data " + str(maxIndex) + " " + str(indexValueOfFirstNonNull) + " for mnemonic " + mnemonic)
                        return False                                     
                     
                # find index of curve last non null value
                numberOfRows = self._get_logData_NumberOfNodes_Int(); 
                indexValueOfLastNonNull = -1
                reverseRange = range(numberOfRows)
                reverseRange.reverse()
                for row in reverseRange:
                     value = self._get_logData_DataValue_String(row,mnemonic)
                     curve_array_length = self._get_log_curve_array_length(mnemonic)
                     if self._isCurveValueNull(value,curveDataType,curveNullValue,logNullValue,curve_array_length) == False:
                         indexValueOfLastNonNull = wtl.utils.iso_to_utc(self._get_logData_IndexValue_String(row))          
                         break  
                     
                if ( self._isDirectionIncreasing(_get('direction'))):                     
                    if ( maxIndex != indexValueOfLastNonNull):
                        self._Fail(test,"logCurveInfo.maxDateTimeIndex != last non null Index in logData/data " + str(maxIndex) + " " + str(indexValueOfLastNonNull) + " for mnemonic " + mnemonic)
                        return False 
                else:                  
                    if ( minIndex != indexValueOfLastNonNull):
                        self._Fail(test,"logCurveInfo.minDateTimeIndex != first non null Index in logData/data " + str(minIndex) + " " + str(indexValueOfLastNonNull) + " for mnemonic " + mnemonic)
                        return False                                   
                       
            if verbose:                      
                _partial_success('passed ' + test) 
        else:
           if verbose:
              _log(test + " direction is unknown, skipping test")
                                
        return True

    def test_log_curve_array_header(self, verbose):
        """Verify all array type curves headers are correct"""
        test = 'test_log_curve_array_header'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False         
        logCurveInfoNodes = self._getGlobalElementNode('logs/log/logCurveInfo')
        

        for curveIndex in range(len(logCurveInfoNodes)):
            mnemonic = self._get_XMLout_Element_String('logs/log[$logIndex$]/logCurveInfo[%d]/mnemonic'%(curveIndex+1))
            axises = self._get_XMLout_RecurringElement_List('logs/log[$logIndex$]/logCurveInfo[%d]/axisDefinition'%(curveIndex+1))
            if ( axises is not None and len(axises)>0):
                orderList = []                
                for axisIndex in range(len(axises)):
                    axisCount = self._get_XMLout_Element_String('logs/log[$logIndex$]/logCurveInfo[%d]/axisDefinition[%d]/count'%((curveIndex+1),(axisIndex+1)))
                    if ( axisCount is not None ):
                        if ( int(axisCount) < 2):
                            self._Fail(test,"mnemonic %s axis.count <2, %s "%mnemonic,axisCount)
                            return False             
                    else:
                        self._Fail(test,"mnemonic %s axis.axisCount is not defined"%(mnemonic))
                        return False                             
                                     
                    axisOrder = self._get_XMLout_Element_String('logs/log[$logIndex$]/logCurveInfo[%d]/axisDefinition[%d]/order'%((curveIndex+1),(axisIndex+1)))
                    if ( axisOrder is not None ):
                        orderList.append(axisOrder)
                    else:
                        self._Fail(test,"mnemonic %s axis.order is not defined"%(mnemonic))
                        return False                             
                        
                    doubleValues =  self._get_XMLout_Element_String('logs/log[$logIndex$]/logCurveInfo[%d]/axisDefinition[%d]/doubleValues'%((curveIndex+1),(axisIndex+1)))
                    stringValues =  self._get_XMLout_Element_String('logs/log[$logIndex$]/logCurveInfo[%d]/axisDefinition[%d]/stringValues'%((curveIndex+1),(axisIndex+1)))
                    if doubleValues is not None:
                        doubleList = doubleValues.split(' ')
                        if ( len(doubleList) < 2 ):
                             self._Fail(test,"mnemonic %s axis.doubleList length incorrect, is %d expecting >= 2 value %s"%(mnemonic,len(doubleList),doubleValues))
                             return False                             
                        elif len(doubleList) > int(axisCount):
                             self._Fail(test,"mnemonic %s axis.doubleList length incorrect, is %d expecting %s value %s"%(mnemonic,len(doubleList),axisCount,doubleValues))
                             return False                             
                            
                    elif stringValues is not None:  
                        stringList = stringValues.split(' ')
                        if ( len(stringList) < 2 ):
                             self._Fail(test,"mnemonic %s axis.doubleList length incorrect, is %d expecting >= 2 value %s"%(mnemonic,len(doubleList),stringValues))
                             return False                             
                        elif len(stringList) > int(axisCount):
                             self._Fail(test,"mnemonic %s axis.doubleList length incorrect, is %d expecting %s value %s"%(mnemonic,len(doubleList),axisCount,stringValues))
                             return False  
                         
                if ( len(orderList) ):
                    uniqueOrderList = Set(orderList)
                    if ( len(uniqueOrderList) != len(orderList) ):
                        self._Fail(test,"Duplicate order in axisDefinition %s"%(str(orderList)))
                        return False                                       
                    orderList.sort()
                    for orderIndex in range(len(orderList)):
                        if ( (orderIndex+1) != int(orderList[orderIndex])):
                            self._Fail(test,"Incorrect orders in axisDefinition %s"%(str(orderList)))
                            return False                          
                
        if verbose:                      
            _partial_success('passed ' + test) 
        return True
                           
    def test_log_curve_array_data(self, verbose):
        """Verify all array type curves have the correct number of indexes"""
        test = 'test_log_curve_array_data'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False        
        numberOfRows = self._get_logData_NumberOfNodes_Int(); 
        logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')
        for mnemonic in logCurveInfoMnemonics:
            curve_array_length = self._get_log_curve_array_length(mnemonic)
            if ( curve_array_length > 1):
                if verbose:
                  _log('doing array ' + mnemonic + " " + test )                
                for row in range(numberOfRows):
                    value = self._get_logData_DataValue_String(row,mnemonic)     
                    if value is not None and len(value) > 0:   
                        curveValueList = value.split(' ')
                        if ( len(curveValueList) != curve_array_length):
                            self._Fail(test,"log curve data array length != not match header mnemonic " + mnemonic + " row " + str(row) + " array length " + str(curve_array_length)  + " data length " + str(len(curveValueList)) + " data " + value)
                            return False               
                    
        if verbose:                      
            _partial_success('passed ' + test)     
            
        return True            
                
                     
    def test_log_curve_info_min_max_time(self, verbose):
        """ Are the LogCurveInfo minDateTimeIndex and maxDateTimeIndex within the log startDateTimeIndex and endDateTimeIndex"""
        test = 'test_log_curve_info_min_max_time'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
 
        if self._isDirectionUnknown(_get('direction')) == False: 
 
            if verbose:
                _log('doing ' + test )
             
            logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')                
                    
            startTimeIndex = wtl.utils.iso_to_utc(_get('startDateTimeIndex'), True)
            endTimeIndex = wtl.utils.iso_to_utc(_get('endDateTimeIndex'), True)                
                    
            # look thru all log curves to see if their start end index are a subset of the log index
            for mnemonic in logCurveInfoMnemonics:
                _set('mnemonicVar', mnemonic)
                curveMinIndex = wtl.utils.iso_to_utc(self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/minDateTimeIndex'), True)
                curveMaxIndex = wtl.utils.iso_to_utc(self._get_XMLout_Element_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/maxDateTimeIndex'), True)
                if self._isDirectionIncreasing(_get('direction')):
                    if ( curveMinIndex < startTimeIndex ):
                        self._Fail(test,"logCurveInfo.minDateTimeIndex < log.startDateTimeIndex " + str(curveMinIndex) + " " + str(startTimeIndex) + " for mnemonic " + mnemonic)
                        return False
                    if ( curveMinIndex > endTimeIndex ):
                        self._Fail(test,"logCurveInfo.minDateTimeIndex > log.endIndex " + str(curveMinIndex) + " " + str(endTimeIndex) + " for mnemonic " + mnemonic)
                        return False
                    if ( curveMinIndex > curveMaxIndex ):
                        self._Fail(test,"logCurveInfo.maxDateTimeIndex < logCurveInfo.minDateTimeIndex " + str(curveMinIndex) + " " + str(curveMaxIndex) + " for mnemonic " + mnemonic)
                        return False
                    if ( curveMaxIndex > endTimeIndex ):
                        self._Fail(test,"logCurveInfo.maxDateTimeIndex > log.endDateTimeIndex " + str(curveMaxIndex) + " " + str(endTimeIndex) + " for mnemonic " + mnemonic)
                        return False
                else:              
                    if ( curveMinIndex > startTimeIndex ):
                        self._Fail(test,"logCurveInfo.minDateTimeIndex > log.startDateTimeIndex " + str(curveMinIndex) + " " + str(startTimeIndex) + " for mnemonic " + mnemonic)
                        return False
                    if ( curveMinIndex < endTimeIndex ):
                        self._Fail(test,"logCurveInfo.minDateTimeIndex < log.endDateTimeIndex " + str(curveMinIndex) + " " + str(endTimeIndex) + " for mnemonic " + mnemonic)
                        return False      
                    if ( curveMaxIndex < endTimeIndex ):
                        self._Fail(test,"logCurveInfo.maxDateTimeIndex < log.endDateTimeIndex " + str(curveMaxIndex) + " " + str(endTimeIndex) + " for mnemonic " + mnemonic)
                        return False                           
                if ( curveMaxIndex < curveMinIndex ):
                    self._Fail(test,"logCurveInfo.maxDateTimeIndex < logCurveInfo.minDateTimeIndex " + str(curveMaxIndex) + " " + str(curveMinIndex) + " for mnemonic " + mnemonic)
                    return False
                      
            if verbose:                      
                _partial_success('passed ' + test) 
        else:
           if verbose:
              _log(test + " direction is unknown, skipping test")    
                          
        return True
                     
                          
    def test_log_curve_info_min_max_depth_uom(self, verbose):
        """ Are the LogCurveInfo minIndex uom and maxIndex uom the same as the log startIndex uom and endIndex uom"""        
        test = 'test_log_curve_info_min_max_depth_uom'  
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
        
        if verbose:
            _log('doing ' + test )
        
        logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')
                       
        # look thru all log curves to see if their minIndex and maxIndex uom's match log 
        for mnemonic in logCurveInfoMnemonics:
            _set('mnemonicVar', mnemonic)
            curveMinIndexUom = self._get_XMLout_Attribute_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/minIndex','uom')
            curveMaxIndexUom = self._get_XMLout_Attribute_String('/logs/log[$logIndex$]/logCurveInfo[mnemonic="$mnemonicVar$"]/maxIndex','uom')            
            if ( curveMinIndexUom != _get('startIndexUom')):
                self._Fail(test,"logCurveInfo.minIndex@uom != log.startIndexUom " + curveMinIndexUom + " " + _get('startIndexUom') + " for mnemonic " + mnemonic)        
                return False
            if ( curveMaxIndexUom != _get('startIndexUom')):
                self._Fail(test,"logCurveInfo.maxIndex@uom != log.startIndexUom " + curveMaxIndexUom + " " + _get('startIndexUom') + " for mnemonic " + mnemonic)        
                return False
               
        if verbose:               
            _partial_success('passed ' + test)             
        return True    
           
     
    def _test_get_dataContainsCorrectDataType(self, verbose, curveListDict):
        """ Do each of the data rows have data that matches the Log Curve datatype 
            Parameters:
                      verbose:  extended logging output
                      curveListDict:  dictionary of logCurveInfo details        
        """
        test = '_test_get_dataContainsCorrectDataType'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
        
        if verbose:
            _log('doing ' + test )
        
        mnList = _get('mnenmonicList').split(",")
        
        numberOfRows = self._get_logData_NumberOfNodes_Int(); 
        for row in range(numberOfRows):
            for mnemonic in mnList:
                _set('mnemonicVar', mnemonic)
                value = self._get_logData_DataValue_String(row,mnemonic)
                logNullValue = self._getLogNullFromCurveListDict(mnemonic, curveListDict)
                curveNullValue = self._getCurveNullFromCurveListDict(mnemonic, curveListDict)
                curveDataType = self._getCurveDataTypeFromCurveListDict(mnemonic, curveListDict) 
                curve_array_length = self._getCurveArrayLengthFromCurveListDict(mnemonic, curveListDict)               
                if self._isCurveValueNull(value,curveDataType,curveNullValue,logNullValue,curve_array_length) == False:
                    if curve_array_length > 1:
                        curveValueList = value.split(' ')
                        for curve_value in curveValueList:
                            try:
                                if curveDataType == 'double' or curveDataType == 'float':
                                   floatValue = float(curve_value) 
                                elif curveDataType == 'int' or curveDataType == 'byte' or curveDataType == 'long' or curveDataType == 'short':
                                   intValue = int(curve_value) 
                                elif curveDataType == 'date time' :
                                     dtlhs = wtl.utils.iso_to_utc(curve_value, True)                                                 
                                elif curveDataType == '':
                                     i = 0; # skip nulls
                            except:
                                self._Fail(test,"Invalid dataType:  row " + str(row) + "  mnemonic " + mnemonic + " index " + str(curve_index) + " value " + str(curve_value) + " expecting " + curveDataType)
                                return False 
                    else: 
                        try:
                            if curveDataType == 'double' or curveDataType == 'float':
                               floatValue = float(value) 
                            elif curveDataType == 'int' or curveDataType == 'byte' or curveDataType == 'long' or curveDataType == 'short':
                               intValue = int(value) 
                            elif curveDataType == 'date time' :
                                 dtlhs = wtl.utils.iso_to_utc(value, True)                                                 
                            elif curveDataType == '':
                                 i = 0; # skip nulls
                        except:
                            self._Fail(test,"Invalid dataType:  row " + str(row) + "  mnemonic " + mnemonic + " value " + str(value) + " expecting " + curveDataType)
                            return False                         
             
        if verbose:                
            _partial_success('passed ' + test)             
        return True
     
    def _test_get_direction_of_data_matches_header_depth(self, verbose ):
        """ Does the data indexing match the direction"""
        test = '_test_get_direction_of_data_matches_header_depth'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
        
        if verbose:
            _log('doing ' + test )
        
        direction = _get('direction')
        stepIncrement = _get('stepIncrement')
        
        if self._isDirectionUnknown(_get('direction')) == False:
            numberOfRows = self._get_logData_NumberOfNodes_Int(); 
            lastIndexValue = -1            
            for row in range(numberOfRows):
                indexValue = self._get_logData_IndexValue_String(row);
                if row != 0:
                    if self._isDirectionIncreasing(direction):
                        if lastIndexValue >= float(indexValue):
                            self._Fail(test,"Invalid indexValue:  row " + str(row) + " lastIndex " + str(lastIndexValue) + "  indexValue " + indexValue)
                            return False
                    else:
                       if lastIndexValue <= float(indexValue):
                            self._Fail(test,"Invalid indexValue:  row " + str(row) + " lastIndex " + str(lastIndexValue) + "  indexValue " + indexValue)
                            return False
                    # see if step increment is correct
                    if stepIncrement is not None and float(stepIncrement) != 0:
                        diff = abs(lastIndexValue - float(indexValue))
                        if self._compareDoubleEquals(float(stepIncrement),diff) == False:
                            self._Fail(test,"Difference between indexes != stepIncrement:  row " + str(row) + " stepIncrement " + stepIncrement + " Diff " + str(diff) + "  lastIndex " + str(lastIndexValue) + "  indexValue " + indexValue)
                            return False
                       
                lastIndexValue = float(indexValue)     
               
            if verbose:                      
                _partial_success('passed ' + test)  
        else:
            if verbose:                      
                _partial_success('direction unknown, skipping ' + test)   
                           
        return True

    def _test_get_direction_of_data_matches_header_time(self, verbose ):
        """ Does the data indexing match the direction"""
        test = '_test_get_direction_of_data_matches_header_time'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
        
        if verbose:
            _log('doing ' + test )
        
        direction = _get('direction')

        if self._isDirectionUnknown(_get('direction')) == False:            
            numberOfRows = self._get_logData_NumberOfNodes_Int(); 
            lastIndexDate = None           
            for row in range(numberOfRows):
                indexValue = self._get_logData_IndexValue_String(row);
                if row == 0:
                    lastIndexDate = wtl.utils.iso_to_utc(indexValue, True)
                else:
                    indexDate = wtl.utils.iso_to_utc(indexValue, True)                    
                    if self._isDirectionIncreasing(direction):
                        if lastIndexDate >= indexDate:
                            self._Fail(test,"Invalid indexValue:  row " + str(row) + " lastIndex " + str(lastIndexDate) + "  indexValue " + indexValue)
                            return False
                    else:
                       if lastIndexDate <= indexDate:
                            self._Fail(test,"Invalid indexValue:  row " + str(row) + " lastIndex " + str(lastIndexDate) + "  indexValue " + indexValue)
                            return False
                    lastIndexDate = indexDate
               
            if verbose:                      
                _partial_success('passed ' + test)  
        else:
            if verbose:                      
                _partial_success('direction unknown, skipping ' + test)                 
                
        return True

    def _test_mnemonicsAreUnique(self, verbose):
        """ Are the mnemonics unique in the mnemonisList"""
        test = '_test_mnemonicsAreUnique'
        passFail = self._setup(True, verbose)
        if not(passFail):  return False
 
        if verbose:
            _log('doing ' + test )       
        
        mnList = _get('mnenmonicList').split(",")
        uniqueMnList = Set(mnList)
        if len(mnList) != len(uniqueMnList ):
             self._Fail(test,"Mnemonics are not unique " + ','.join(mnList) )
             return False   
         
        if verbose:         
            _partial_success('passed ' + test)
        return True         
                  

    def _Fail( self, test, message ):
          #message = 'FAILED ' + test + ': ' +  message
          message = 'FAILED: ' +  message
          _log(message )
          wtl.control_prim.fail(message)

    def _indexOfCurveInMnemonicList(self, mnemonic):
            indexOfCurve = -1
            mnList = _get('mnenmonicList').split(",")
            logCurveInfoMnemonics = _get('logCurveInfoMnemonicList')
            try:
                indexOfCurve = mnList.index(mnemonic)
            except ValueError:
                _log("mnemonic not found in mnemonicList " + mnemonic )
    
            return indexOfCurve

    def _isCurveValueNull(self, valueString, curveDataType, curveNullValue, logNullValue, curveArrayLength ):
        """ Is this curve value null """
        if curveArrayLength == 1:
            return self._isCurveValueNullPrivate(valueString, curveDataType, curveNullValue, logNullValue )
        else:
            # all elements of array must be null before the curve is null
            curveValueList = valueString.split(' ');
            for curveValue in curveValueList:
                curveIsNull = self._isCurveValueNullPrivate(curveValue, curveDataType, curveNullValue, logNullValue )
                if ( curveIsNull == False):
                    return False;
            return True;
              
        
    def _isCurveValueNullPrivate(self, valueString, curveDataType, curveNullValue, logNullValue ):
        """ Is this curve value null """
        isNull = False
        if valueString is not None and len(valueString) > 0:
            if  curveNullValue is not None or logNullValue is not None:
               try: 
                   if curveDataType == 'double' or dataType == 'float':
                      floatValue = float(valueString)
                      nullValue = None;
                      if curveNullValue is not None:
                          nullValue = float(curveNullValue)
                      elif logNullValue is not None:
                          nullValue = float(logNullValue)
                      if self._compareDoubleEquals(floatValue,nullValue) == True:
                          isNull = True  
                   elif curveDataType == 'int' or dataType == 'byte' or dataType == 'long' or dataType == 'short':
                      intValue = int(valueString) 
                      nullValue = None;
                      if curveNullValue is not None:
                          nullValue = int(curveNullValue)
                      elif logNullValue is not None:
                          nullValue = int(logNullValue)
                      if self._compareDoubleEquals(intValue,nullValue) == True:
                          isNull = True                   
                   elif curveDataType == 'date time' :
                      dtlhs = wtl.utils.iso_to_utc(valueString, True) 
                      nullValue = None;
                      if curveNullValue is not None:
                          nullValue = wtl.utils.iso_to_utc(curveNullValue, True)
                      elif logNullValue is not None:
                          nullValue = wtl.utils.iso_to_utc(logNullValue, True)
                      if (dtlhs == nullValue):
                          isNull = True                                                                   
                   elif dataType == '':
                          i = 0; # skip nulls
               except Exception as e:
                     _log("error convert nullValue " + str(e) )               
        else:
            isNull = True;
        return isNull;           
             
    def _compareDoubleEquals(self, first, second, error_margin=1):
        min_val = first * (10000 - error_margin) /10000
        max_val = first * (10000 + error_margin) /10000
        if ( first >= 0 ):
            if (second >= min_val) and (second <= max_val):
                  return True;     
            else:
                  return False; 
        else:
            # negative
            if (second <= min_val) and (second >= max_val):
                  return True;     
            else:
                  return False;             

    def _isDirectionIncreasing(self, direction):
        return direction == 'increasing'

    def _isDirectionDecreasing(self, direction):
        return direction == 'decreasing'

    def _isDirectionUnknown(self, direction):
        return direction == 'unknown'
