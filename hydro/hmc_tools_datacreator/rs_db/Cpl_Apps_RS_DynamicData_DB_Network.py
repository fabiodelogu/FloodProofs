"""
Class Features

Name:          Cpl_Apps_RS_DynamicData_DB_Network
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151204'
Version:       '1.0.0'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os, pickle
import numpy as np

from os.path import join
from os.path import split

import src.Lib_Data_Analysis_Interpolation as Lib_Data_Analysis_Interpolation
import src.Lib_Data_IO_Utils as Lib_Data_IO_Utils
import src.Lib_Data_Apps as Lib_Data_Apps

from src.Drv_Data_DB import Drv_Data_DB
from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_Data_Zip import Drv_Data_Zip
from src.Drv_Data_Type import Drv_Data_Type

from src.GetTime import convertTimeLOCxGMT
from src.GetException import GetException
from src.Lib_Data_IO_Utils import getFileHistory, writeFileHistory

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Cpl_Apps_RS_DynamicData_DB_Network:

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataTime=None, oDataPoint=None, oDataInfo=None):
        
        # Data settings and data reference 
        self.oDataTime = oDataTime
        self.oDataPoint = oDataPoint
        self.oDataInfo = oDataInfo
        
    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------
    # Method to check data availability
    def checkDynamicData(self, sTime):
        
        #-------------------------------------------------------------------------------------
        # Get path information
        sPathData_CHECK = self.oDataInfo.oInfoSettings.oPathInfo['DataCache']
        
        # Get outcome variable information
        oVarsInfo_CHECK = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic

        # Get time information
        iTimeStep_CHECK = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeStep'])
        iTimeUpd_CHECK = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeUpd'])
        a1oTimeSteps_CHECK = self.oDataTime.a1oTimeSteps
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cache definition
        sTime_CHECK = sTimeSave
        sYear_CHECK = sTime_CHECK[0:4]; sMonth_CHECK = sTime_CHECK[4:6]; sDay_CHECK = sTime_CHECK[6:8];
        sHH_CHECK = sTime_CHECK[8:10]; sMM_CHECK = sTime_CHECK[10:12];
        sPathData_CHECK = Lib_Data_IO_Utils.defineFolderName(sPathData_CHECK,
                                                     {'$yyyy' : sYear_CHECK,'$mm' : sMonth_CHECK,'$dd' : sDay_CHECK, 
                                                      '$HH' : sHH_CHECK,'$MM' : sMM_CHECK})
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Condition to save file for reanalysis period (Reanalysis Time Steps = RTS)
        bSaveTime_CHECK = Lib_Data_IO_Utils.checkSavingTime(sTime_CHECK, a1oTimeSteps_CHECK, iTimeStep_CHECK, iTimeUpd_CHECK)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info
        oLogStream.info( ' ====> CHECK DATA AT TIME: ' + sTimeSave + ' ... ')
        oLogStream.info( ' -----> Data LoadTime: ' + sTimeLoad + ' --- Data SaveTime: ' + sTimeSave)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cycle(s) on type file(s)
        for sFileTypeIN in oVarsInfo_CHECK:
            
            #-------------------------------------------------------------------------------------
            # Cycle(s) to check variable(s)
            a2bSaveVar_CHECK = {};
            #-------------------------------------------------------------------------------------
        
            #-------------------------------------------------------------------------------------
            # Cycle(s) on variable name(s)
            for sVarName in oVarsInfo_CHECK[sFileTypeIN]:
                
                #-------------------------------------------------------------------------------------
                # Get variable IN and OUT component(s)
                oVarCompIN = oVarsInfo_CHECK[sFileTypeIN][sVarName]['VarOp']['Op_Load']['Comp']['IN']
                oVarCompOUT = oVarsInfo_CHECK[sFileTypeIN][sVarName]['VarOp']['Op_Load']['Comp']['OUT']
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Cycle(s) on outcome variable(s)
                for sVarCompOUT in oVarCompOUT.values():
                    
                    #-------------------------------------------------------------------------------------
                    # Initialize dictionary for each new variable(s)
                    if not sVarCompOUT in a2bSaveVar_CHECK:
                        a2bSaveVar_CHECK[sVarCompOUT] = {}
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Storage variable checking
                    a1bVar_CHECK = []
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # ASCII Check file
                    sFileCache_CHECK = os.path.join(sPathData_CHECK, 'RS_DB-NETWORK_FILEASCII_' + sTimeSave + '_' + sVarCompOUT + '.history')
                    bFileCache_CHECK = os.path.isfile(sFileCache_CHECK)
                    
                    # Check file status
                    if bFileCache_CHECK is True:
                        if bSaveTime_CHECK is True:
                            a1bVar_CHECK.append(False) 
                        else:
                            a1bVar_CHECK.append(True) 
                    else:
                        a1bVar_CHECK.append(False)
                    #-------------------------------------------------------------------------------------
                
                    #-------------------------------------------------------------------------------------
                    # Final check for each step
                    if np.all(a1bVar_CHECK) == True:    
                        a2bSaveVar_CHECK[sVarCompOUT] = True
                    else:
                        a2bSaveVar_CHECK[sVarCompOUT] = False
                    #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
        
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Return check status 
        oLogStream.info( ' ====> CHECK DATA AT TIME: ' + sTimeSave + ' ... OK')
        self.oVarsSave = a2bSaveVar_CHECK
        self.sPathCache = sPathData_CHECK
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Get DynamicData Obs
    def getDynamicData(self, sTime):
        

        #------------------------------------------------------------------------------------- 
        # Get information
        oDrv_DataType = Drv_Data_Type(oDataGeo=None, oDataAnalyzed=None, oDataInfo=self.oDataInfo)
        
        sPathDataSource = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        oVarsInfoIN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        oParamsInfo = self.oDataInfo.oInfoSettings.oParamsInfo
        
        oVarsSave = self.oVarsSave
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Time information
        sYearLoad = sTimeLoad[0:4]; sMonthLoad = sTimeLoad[4:6]; sDayLoad = sTimeLoad[6:8]; sHHLoad = sTimeLoad[8:10]; sMMLoad = sTimeLoad[10:12];
        sYearSave = sTimeSave[0:4]; sMonthSave = sTimeSave[4:6]; sDaySave = sTimeSave[6:8]; sHHSave = sTimeSave[8:10]; sMMSave = sTimeSave[10:12];
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Check database type
        if oParamsInfo['DB']['ID'] != 'DB_UNKNOWN':
            
            #------------------------------------------------------------------------------------- 
            # Info
            oLogStream.info( ' ====> RETRIEVE DATA AT TIME: ' + sTimeSave + ' ... ')
            oLogStream.info( ' -----> Data LoadTime: ' + sTimeLoad + ' --- Data SaveTime: ' + sTimeSave)
            #------------------------------------------------------------------------------------- 

            #------------------------------------------------------------------------------------- 
            # Cycling on variable type definition (input)
            for sVarType in oVarsInfoIN:
                
                #------------------------------------------------------------------------------------- 
                # Cycling on variable name definition (input)
                for sVarName in oVarsInfoIN[sVarType]:
                    
                    #-------------------------------------------------------------------------------------
                    # Info
                    oLogStream.info( ' -----> Retrieve variable ' + sVarName + ' ... ')
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Get variable info
                    oVarInfo = oVarsInfoIN[sVarType][sVarName]
                    # Define filename
                    sFileNameIN = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, oVarsInfoIN[sVarType][sVarName]['VarSource']), 
                                                             {'$VAR':sVarName,
                                                              '$yyyy':sYearLoad, '$mm':sMonthLoad, '$dd':sDayLoad, '$HH':sHHLoad, '$MM':sMMLoad})
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Check variable saving condition
                    if (oVarsSave[sVarName] is False):
                        
                        #-------------------------------------------------------------------------------------
                        # Create destination folder
                        Lib_Data_IO_Utils.createFolder(split(sFileNameIN)[0])
                        
                        # Input file driver
                        Drv_Data_DB(sTimeLoad, sFileNameIN, oVarInfo, oParamsInfo)
                        
                        # Info
                        oLogStream.info( ' -----> Retrieve variable ' + sVarName + ' ... OK ')
                        #-------------------------------------------------------------------------------------
                        
                    else:
                        
                        #-------------------------------------------------------------------------------------
                        # Info
                        oLogStream.info( ' -----> Retrieve variable ' + sVarName + ' ... SKIPPED --- FILES PREVIOUSLY SAVED')
                        #-------------------------------------------------------------------------------------
                        
                    #-------------------------------------------------------------------------------------
                     
                #------------------------------------------------------------------------------------- 
            
            #------------------------------------------------------------------------------------- 
            
            #------------------------------------------------------------------------------------- 
            # Info
            oLogStream.info( ' ====> RETRIEVE DATA AT TIME: ' + sTimeSave + ' ... OK ')
            #-------------------------------------------------------------------------------------     
                
        else:
            
            #-------------------------------------------------------------------------------------
            # DB UNKNOWN
            GetException(' -----> WARNING: Database set DB_UNKNOWN: Nothing to do!', 2, 1)
            oLogStream.info( ' ====> RETRIEVE DATA AT TIME: ' + sTimeSave + ' ... SKIPPED ')
            oLogStream.info( ' -----> SELECTED DATABASE: ' + str(oParamsInfo['DB']['ID']) )
            #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET DATA AT TIME: ' + sTimeSave + ' ... ')
        oLogStream.info( ' -----> Data LoadTime: ' + sTimeLoad + ' --- Data SaveTime: ' + sTimeSave)

        # Cycling on variable type definition (input)
        self.oVarData = {}
        for sVarType in oVarsInfoIN:
            
            #------------------------------------------------------------------------------------- 
            # Cycling on variable name definition (input)
            a1oFileDrvIN = {};  a1oDataSelect = {};
            for sVarName in oVarsInfoIN[sVarType]:
                
                #-------------------------------------------------------------------------------------
                # Define FileNameIN
                sFileNameIN = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, oVarsInfoIN[sVarType][sVarName]['VarSource']), 
                                                         {'$VAR'  : sVarName,
                                                          '$yyyy' : sYearLoad, '$mm' : sMonthLoad, '$dd' : sDayLoad, 
                                                          '$HH' : sHHLoad, '$MM' : sMMLoad})
                #------------------------------------------------------------------------------------- 
                
                #-------------------------------------------------------------------------------------
                # File and variable info
                oLogStream.info( ' -----> Variable: ' + sVarName + ' ... ')
                oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... ')
                #-------------------------------------------------------------------------------------

                #------------------------------------------------------------------------------------- 
                # Check input file(s) availability
                bFileExistIN = Lib_Data_IO_Utils.checkFileExist(sFileNameIN)
                if (bFileExistIN is True) and (oVarsSave[sVarName] is False):
                    
                    #-------------------------------------------------------------------------------------
                    # Check variable availability
                    if not sFileNameIN in a1oFileDrvIN:
                        
                        # Input file driver
                        a1oFileDrvIN[sFileNameIN] = Drv_Data_IO(sFileNameIN,'r', str.lower(sVarType))
                        # Variable get method
                        oData_GetMethod = getattr(oDrv_DataType, 'getVar' + oVarsInfoIN[sVarType][sVarName]['VarType'])
                        # Get data selection
                        a1oDataSelect[sFileNameIN] = oData_GetMethod(a1oFileDrvIN[sFileNameIN].oFileWorkspace,
                                                                     oVarsInfoIN[sVarType][sVarName]['VarOp'],
                                                                     -9999.0, sTimeLoad, None, True)
                        # Info
                        oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... OK ')
                    else:
                        pass
                    #-------------------------------------------------------------------------------------
        
                else:
                    
                    #-------------------------------------------------------------------------------------
                    # Exit code(s)
                    if (bFileExistIN is False) and (oVarsSave[sVarName] is False):
                        
                        #-------------------------------------------------------------------------------------
                        # Exit code(s)
                        oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... SKIPPED --- FILE INPUT NOT FOUND ')
                        oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE NOT FOUND ')
                        GetException(' -----> WARNING: file input is not available!', 2, 1)
                        #-------------------------------------------------------------------------------------
                    
                    elif (bFileExistIN is True) and (oVarsSave[sVarName] is True):
                        
                        #-------------------------------------------------------------------------------------
                        # Exit code(s)
                        oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... SKIPPED --- FILE PROCESSED PREVIOUSLY ')
                        oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE SAVED PREVIOUSLY ')
                        #-------------------------------------------------------------------------------------
                        
                #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
        
        # Info
        oLogStream.info( ' ====> GET DATA AT TIME: ' + sTimeSave + ' ... OK ')
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> PARSER DATA AT TIME: ' + sTimeSave + ' ... ')
        oLogStream.info( ' -----> Data LoadTime: ' + sTimeLoad + ' --- Data SaveTime: ' + sTimeSave)
        
        # Cycling on data selected (if available)
        oDataWorkspace = {}
        for sFileName in a1oDataSelect:
            
            # Get data defined by filename
            oDataSelect = a1oDataSelect[sFileName]
            oDataRaw = oDataSelect['Data'][sTimeLoad]
            
            # Cycling on available data
            oVarCode = []; oVarValueQ = []; oVarValueWL = [];
            for sVarName in oDataRaw:
                a1oDataVar = oDataRaw[sVarName]
                
                for oDataVar in a1oDataVar:
                    
                    oVarCode.append(int(oDataVar[1]))
                    oVarValueWL.append(float(oDataVar[5]))
                    oVarValueQ.append(float(oDataVar[6]))
            
            # Define variable type
            a1oVarCode = map(int, oVarCode)
            a1oVarValueQ = map(float, oVarValueQ)
            a1oVarValueWL = map(float, oVarValueWL)
            
            # Store data in workspace
            oDataWorkspace[sFileName] = {}
            oDataWorkspace[sFileName]['Data_Code'] = a1oVarCode
            oDataWorkspace[sFileName]['Data_Q'] = a1oVarValueQ
            oDataWorkspace[sFileName]['Data_WL'] = a1oVarValueWL
            oDataWorkspace[sFileName]['Time'] = sTimeSave
        
        # Save in global workspace available data dynamic
        self.oDataWorkspace = oDataWorkspace
        # Info
        oLogStream.info( ' ====> PARSER DATA AT TIME: ' + sTimeSave + ' ... OK ')
        #-------------------------------------------------------------------------------------
        
    # End method
    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to compute data
    def computeDynamicData(self, sTime):
        
        #------------------------------------------------------------------------------------- 
        # Get information
        oVarsInfoIN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        # Get info data
        iEPSGCode = int(self.oDataInfo.oInfoSettings.oGeoSystemInfo['epsg_code'])
        sPathDataSource = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        sPathTemp = self.oDataInfo.oInfoSettings.oPathInfo['DataTemp']
        
        # Get static data
        oDataPoint = self.oDataPoint
        # Get dynamic data
        oDataWorkspace = self.oDataWorkspace
        # Get historical data
        oVarsSave = self.oVarsSave
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get section data
        a1oSecCode = oDataPoint.a1oSecCode
        a1oSecName = oDataPoint.a1oSecName
        a1oSecDomain = oDataPoint.a1oSecDomain
        
        iSecN = len(a1oSecCode)
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> COMPUTE DATA AT TIME: ' + sTimeSave + ' ... ')
        oLogStream.info( ' -----> Data LoadTime: ' + sTimeLoad + ' --- Data SaveTime: ' + sTimeSave)
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Time information
        sYearLoad = sTimeLoad[0:4]; sMonthLoad = sTimeLoad[4:6]; sDayLoad = sTimeLoad[6:8]; sHHLoad = sTimeLoad[8:10]; sMMLoad = sTimeLoad[10:12];
        sYearSave = sTimeSave[0:4]; sMonthSave = sTimeSave[4:6]; sDaySave = sTimeSave[6:8]; sHHSave = sTimeSave[8:10]; sMMSave = sTimeSave[10:12];
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Cycling on variable type definition (input)
        self.oVarData = {}
        for sVarType in oVarsInfoIN:
            
            #------------------------------------------------------------------------------------- 
            # Cycling on variable name definition
            for sVarName in oVarsInfoIN[sVarType]:
                
                #------------------------------------------------------------------------------------- 
                # FilenameIN definition
                sFileNameIN = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, oVarsInfoIN[sVarType][sVarName]['VarSource']), 
                                                       {'$VAR'  : sVarName, 
                                                        '$yyyy' : sYearLoad, '$mm' : sMonthLoad, '$dd' : sDayLoad, 
                                                        '$HH' : sHHLoad,'$MM' : sMMLoad})
                # File and variable info
                oLogStream.info( ' -----> Variable: ' + sVarName + ' ... ')
                oLogStream.info( ' -----> Getting data: ' + sFileNameIN + ' ... ')
                #------------------------------------------------------------------------------------- 
                
                #-------------------------------------------------------------------------------------
                # Check saving condition(s)
                if (oVarsSave[sVarName] is False):
                    
                    #-------------------------------------------------------------------------------------
                    # Init dictionary
                    self.oVarData[sVarName] = {}
                    #-------------------------------------------------------------------------------------
                    
                    #------------------------------------------------------------------------------------- 
                    # Check data) availability
                    if sFileNameIN in oDataWorkspace:
            
                        #-------------------------------------------------------------------------------------
                        # Cycling on timestep to interpolate variable using selected method
                        if oDataWorkspace[sFileNameIN]:
                            
                            #-------------------------------------------------------------------------------------
                            # Compute data time steps
                            if isinstance(oDataWorkspace[sFileNameIN]['Time'], basestring):
                                iDataLen = 1
                            else:
                                iDataLen = len(oDataWorkspace[sFileNameIN]['Time'])
                            #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            # Get data
                            oVarData = oDataWorkspace[sFileNameIN]
                            oVarTime = oVarData['Time']
                            oVarCode = oVarData['Data_Code']
                            oVarQ = oVarData['Data_Q']
                            
                            self.oVarData[sVarName][oVarTime] = {}
                            #-------------------------------------------------------------------------------------

                            #-------------------------------------------------------------------------------------
                            # Get data for section(s)
                            a2dVarData = np.zeros([iSecN, 2]); a2dVarData[:] = -9999;
                            for iSN, oSecCode in enumerate(a1oSecCode):
                                
                                # Get section data
                                iSecCode = int(oSecCode)
                                sSecName = str(a1oSecName[iSN]); sSecDomain = str(a1oSecDomain[iSN])
                                
                                # Info
                                oLogStream.info( ' -----> GET DATA Section: ' + sSecName + ' Domain: ' + sSecDomain +  ' Code: ' + str(iSecCode))
                                
                                # Check for defined code(s)
                                if iSecCode != -9999:
                                    
                                    # Check section code availability in variable code(s)
                                    if iSecCode in oVarCode:
                                        
                                        # Search index of section code in variable code(s)
                                        iVarIndex = int(oVarCode.index(iSecCode))
                                        iVarCode = int(oVarCode[iVarIndex])
                                        
                                        # Check if variable code equal to section code
                                        if iVarCode == iSecCode:
                                            
                                            # Get data
                                            dVarQ = float(oVarQ[iVarIndex])
                                            
                                            # Store code and data in workspace
                                            a2dVarData[iSN, 0] = iVarCode
                                            a2dVarData[iSN, 1] = dVarQ
                                            #a2dVarData[iSN, 2] = iSN
                                            
                                        else:
                                            GetException(' -----> WARNING: section code != data code! Check your data!', 2, 1)
                                            a2dVarData[iSN, 0] = -9999.0
                                            a2dVarData[iSN, 1] = -9999.0
                                            #a2dVarData[iSN, 2] = iSN
                                    else:
                                        GetException(' -----> WARNING: section code are not in variable data!', 2, 1)
                                        a2dVarData[iSN, 0] = iSecCode
                                        a2dVarData[iSN, 1] = -9999.0
                                        #a2dVarData[iSN, 2] = iSN
                                        
                                else:
                                    GetException(' -----> WARNING: section code is not defined!', 2, 1)
                                    a2dVarData[iSN, 0] = iSecCode
                                    a2dVarData[iSN, 1] = -9999.0
                                    #a2dVarData[iSN, 2] = iSN
                            #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            # Save variable in global workspace
                            self.oVarData[sVarName][oVarTime] = a2dVarData
                            # Info
                            oLogStream.info( ' -----> Variable: ' + sVarName + ' ... OK ')
                            #-------------------------------------------------------------------------------------
                                
                        else:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... SKIPPED --- FILE INPUT NOT LOADED ')
                            oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE UNDEFINED IN INPUT FILE ')
                            GetException(' -----> WARNING: variable is undefined in input file!', 2, 1)
                            
                            self.oVarData[sVarName][oVarTime] = None
                            #-------------------------------------------------------------------------------------
                    else:
                        
                        #-------------------------------------------------------------------------------------
                        # Exit code(s) for data not available
                        if not sFileNameIN in oDataWorkspace:
                            oLogStream.info( ' -----> Getting data: ' + sFileNameIN + ' ... SKIPPED --- DATA NOT AVAILABLE (CURRENT TIME)')
                            oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- DATA NOT AVAILABLE (CURRENT TIME)')
                            GetException(' -----> WARNING: data not available in workspace!', 2, 1)
                        else:
                            pass
                        
                        self.oVarData[sVarName] = None 
                        #-------------------------------------------------------------------------------------    
                else:
                    
                    #-------------------------------------------------------------------------------------
                    # Exit code(s) for data previously computed
                    if oVarsSave[sVarName] is True:
                        oLogStream.info( ' -----> Getting data: ' + sFileNameIN + ' ... SKIPPED --- FILE SAVE PREVIOUSLY')
                        oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- FILE SAVE PREVIOUSLY')
                    else:
                        oLogStream.info( ' -----> Getting data: ' + sFileNameIN + ' ... SKIPPED --- SOMETHING HAS GONE WRONG')
                        oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- SOMETHING HAS GONE WRONG')
                        GetException(' -----> WARNING: data not computed! Check your input data', 2, 1)
                        
                    self.oVarData[sVarName] = None
                    #-------------------------------------------------------------------------------------
                  
                # End check input file availability
                #-------------------------------------------------------------------------------------
            
            # End cycle(s) on variable name(s)
            #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> COMPUTE DATA AT TIME: ' + sTimeSave + ' ... OK')
        #------------------------------------------------------------------------------------- 
        
        # End cycle(s) on variable type(s)
        #-------------------------------------------------------------------------------------
        
    # End method
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to save data
    def saveDynamicData(self, sTime):
        
        #------------------------------------------------------------------------------------- 
        # Get information
        sPathDataOutcome = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicOutcome']
        oVarsInfoOUT = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic
        #------------------------------------------------------------------------------------- 
        #------------------------------------------------------------------------------------- 
        # Get information
        sPathData_OUT = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicOutcome']
        sPathData_CACHE = self.sPathCache
        oVarsInfo_OUT = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic
        oVarsSave_OUT = self.oVarsSave
        
        # Get section data
        a1oSecCode = self.oDataPoint.a1oSecCode
        a1oSecName = self.oDataPoint.a1oSecName
        a1oSecDomain = self.oDataPoint.a1oSecDomain
        
        iSecN = len(a1oSecCode)

        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTimeSave + ' ...  ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Check workspace field(s)
        if np.any(self.oVarData):
            
            #-------------------------------------------------------------------------------------
            # Cycle(s) on get var name
            for sVarName in self.oVarData:
            
                #-------------------------------------------------------------------------------------
                # Info variable name
                oLogStream.info( ' -----> Save variable: ' + sVarName + ' ... ')
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Check variable save condition
                if oVarsSave_OUT[sVarName] is False:
                
                    #-------------------------------------------------------------------------------------
                    # Get data
                    oVarData = self.oVarData[sVarName]
                    # Data length
                    iVarLen = len(oVarData)
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Cycle(s) on get time step
                    iVarTimeIndex = 0;  a1oVarTime = []; a1oSaveTime = [];
                    
                    # Initialize variable(s) 
                    a3dVarData = np.zeros([iSecN, 2, iVarLen])
                    for sVarTime in sorted(oVarData):
                    
                        # Get data 
                        a2dVarData = oVarData[sVarTime]
                        #a2dVarData[self.oDataGeo.a2bGeoDataNan] = self.oDataGeo.dNoData
                        
                        a3dVarData[:,:, iVarTimeIndex] = a2dVarData
                            
                        # Save time information (for loading and saving function)
                        a1oVarTime.append(sVarTime)
 
                        # Counter to get data
                        iVarTimeIndex = iVarTimeIndex + 1
                    #-------------------------------------------------------------------------------------
            
                    #-------------------------------------------------------------------------------------
                    # SAVE DATA IN ASCII FORMAT
                    # Cycle(s) on time step(s)
                    a1bFile_CHECK = []; a1sFileName_OUT = [];
                    for iVarStep, sVarTime in enumerate(a1oVarTime):
                        
                        #------------------------------------------------------------------------------------- 
                        # Time information
                        sVarYear = sVarTime[0:4]; sVarMonth = sVarTime[4:6]; sVarDay = sVarTime[6:8];
                        sVarHH = sVarTime[8:10]; sVarMM = sVarTime[10:12];
                        
                        # Pathname BIN OUT
                        sPathName_OUT = Lib_Data_IO_Utils.defineFolderName(sPathData_OUT,
                                                                     {'$yyyy' : sVarYear,'$mm' : sVarMonth,'$dd' : sVarDay, 
                                                                      '$HH' : sVarHH,'$MM' : sVarMM})
                        # Time Info
                        oLogStream.info( ' ------> Save time step (ASCII): ' + sVarTime)
                        #------------------------------------------------------------------------------------- 
                        
                        #-------------------------------------------------------------------------------------
                        # Filename BIN OUT
                        sFileName_OUT = Lib_Data_IO_Utils.defineFileName(join(sPathName_OUT, oVarsInfo_OUT['ASCII'][sVarName]['VarSource']), 
                                                                 {'$yyyy' : sVarYear,'$mm' : sVarMonth,'$dd' : sVarDay, 
                                                                  '$HH' : sVarHH,'$MM' : sVarMM})
                        
                        # Check output file(s) availability 
                        bFileExist_OUT = Lib_Data_IO_Utils.checkFileExist(sFileName_OUT + '.' + 
                                                                             oVarsInfo_OUT['ASCII'][sVarName]['VarOp']['Op_Save']['Zip'])
                        
                        # Info
                        oLogStream.info( ' -------> Saving file output (ASCII): ' + sFileName_OUT + ' ... ')
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check saving variable method
                        try:
                            
                            #-------------------------------------------------------------------------------------
                            # Check binary availability
                            if (bFileExist_OUT is False) or (oVarsSave_OUT[sVarName] is False):
                            
                                #-------------------------------------------------------------------------------------
                                # Check variable name to select save function
                                if sVarName in oVarsInfo_OUT['ASCII']:
                        
                                    #-------------------------------------------------------------------------------------
                                    # Open binary file
                                    oDrv_OUT = Drv_Data_IO(sFileName_OUT, 'w')
                                    
                                    # Define write method
                                    oDrv_WriteMethod = getattr(oDrv_OUT.oFileWorkspace, 
                                                                   oVarsInfo_OUT['ASCII'][sVarName]['VarOp']['Op_Save']['Func'])
                                    
                                    # Save 2d array in a binary file
                                    oDrv_WriteMethod(a3dVarData[:,:,iVarStep], 
                                                        oVarsInfo_OUT['ASCII'][sVarName]['VarOp']['Op_Save']['Format'])
                                    
                                    # Close binary file
                                    oDrv_OUT.oFileWorkspace.closeFile()

                                    # Info
                                    a1sFileName_OUT.append(sFileName_OUT + '.' + oVarsInfo_OUT['ASCII'][sVarName]['VarOp']['Op_Save']['Zip'])
                                    a1bFile_CHECK.append(True)
                                    oLogStream.info( ' -------> Saving file output (ASCII): ' + sFileName_OUT + ' ... OK ')
                                    #-------------------------------------------------------------------------------------
                        
                                else:
                                    
                                    #-------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFile_CHECK.append(False)
                                    GetException(' -------> WARNING: field not found in outcome workspace!', 2, 1)
                                    oLogStream.info( ' -------> Saving file output (ASCII): ' + sFileName_OUT + ' ... FAILED --- FIELD NOT FOUND IN OUTCOME WORKSPACE')
                                    #-------------------------------------------------------------------------------------
                                    
                                #-------------------------------------------------------------------------------------
                            
                            else:
                                    
                                #-------------------------------------------------------------------------------------
                                # Exit code
                                a1bFile_CHECK.append(True)
                                oLogStream.info( ' -------> Saving file output (BINARY): ' + sFileName_OUT + ' ... PREVIOUSLY SAVED')
                                #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                        
                        except:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            a1bFile_CHECK.append(False) 
                            # Info
                            GetException(' -------> WARNING: errors occurred in saving file! Check your output data!', 2, 1)
                            oLogStream.info( ' -------> Saving file output (BINARY): ' + sFileName_OUT + ' ... FAILED --- ERRORS OCCURRED IN SAVING DATA!')
                            #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                    
                    # Cycle(s) on time steps (END)
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Check saved data BIN
                    if np.all(np.asarray(a1bFile_CHECK) == True ):
                        # Create cache handle
                        sFileCacheBIN_CHECK = os.path.join(sPathData_CACHE, 'RS_DB-NETWORK_FILEASCII_' + sTimeSave + '_' + sVarName + '.history')
                        # Save history file for BIN
                        writeFileHistory(sFileCacheBIN_CHECK, zip(a1sFileName_OUT))
                        
                    else:
                        # Info warning
                        GetException(' -------> WARNING: some files are not saved on disk! Check your data input!', 2, 1)
                    
                    # SAVE DATA IN BINARY FORMAT (END)
                    #-------------------------------------------------------------------------------------
                
                    #-------------------------------------------------------------------------------------
                    # Info
                    oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTimeSave + ' ...  OK ')
                    #-------------------------------------------------------------------------------------
            
                else:
                    
                    #-------------------------------------------------------------------------------------
                    # Info
                    oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTimeSave + ' ...  SKIPPED --- FILE SAVE PREVIOUSLY ')
                    #-------------------------------------------------------------------------------------
                    
                #-------------------------------------------------------------------------------------
            
            # End cycle(s) on variable(s)
            #-------------------------------------------------------------------------------------
            
        else:
            
            #-------------------------------------------------------------------------------------
            # Exit code(s)
            if np.all(oVarsSave_OUT.values()) == True:
                
                #-------------------------------------------------------------------------------------
                # Exit - Files previously computed
                oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTimeSave + ' ...  SKIPPED ---- ALL FIELD(S) COMPUTED PREVIOUSLY')
                #-------------------------------------------------------------------------------------
                
            else:
                
                #-------------------------------------------------------------------------------------
                # Exit - NoData
                oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTimeSave + ' ...  FAILED ---- ALL FIELD(S) IN OUTCOME WORKSPACE ARE UNDEFINED')
                GetException(' -----> WARNING: all field(s) in outcome workspace are undefined!', 2, 1)
                #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
                  
        #-------------------------------------------------------------------------------------
        
    # End method
    #-------------------------------------------------------------------------------------
    
# End class
#-------------------------------------------------------------------------------------
            







 
