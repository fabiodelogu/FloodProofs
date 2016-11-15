"""
Class Features

Name:          Cpl_Apps_WS_DynamicData_DB_Network
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20150925'
Version:       '2.0.7'
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
class Cpl_Apps_WS_DynamicData_DB_Network:

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataTime=None, oDataGeo=None, oDataAnalyzed = None, oDataInfo=None):
        
        # Data settings and data reference 
        self.oDataTime = oDataTime
        self.oDataGeo = oDataGeo
        self.oDataAnalyzed = oDataAnalyzed
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
                    # BIN Check file
                    sFileCacheBIN_CHECK = os.path.join(sPathData_CHECK, 'WS_DB-NETWORK_FILEBIN_' + sTimeSave + '_' + sVarCompOUT + '.history')
                    bFileCacheBIN_CHECK = os.path.isfile(sFileCacheBIN_CHECK)
                    
                    # Check file status
                    if bFileCacheBIN_CHECK is True:
                        if bSaveTime_CHECK is True:
                            a1bVar_CHECK.append(False) 
                        else:
                            a1bVar_CHECK.append(True) 
                    else:
                        a1bVar_CHECK.append(False)

                    # NETCDF Check file
                    sFileCacheNC_CHECK = os.path.join(sPathData_CHECK, 'WS_DB-NETWORK_FILENC_' + sTimeSave + '_' + sVarCompOUT + '.history')
                    bFileCacheNC_CHECK = os.path.isfile(sFileCacheNC_CHECK)
                    
                    # Check file status
                    if bFileCacheNC_CHECK is True:
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
        oDrv_DataType = Drv_Data_Type(oDataGeo=self.oDataGeo, oDataAnalyzed=self.oDataAnalyzed ,oDataInfo=self.oDataInfo)
        
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
                                                                     -9999.0, sTimeLoad, None)
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
        
        #-------------------------------------------------------------------------------------
        # Save in global workspace available data dynamic
        self.a1oDataSelect = a1oDataSelect
        # Info
        oLogStream.info( ' ====> GET DATA AT TIME: ' + sTimeSave + ' ... OK ')
        #-------------------------------------------------------------------------------------
        
    # End method
    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to compute data
    def computeDynamicData(self, sTime):
        
        #------------------------------------------------------------------------------------- 
        # Get information
        oVarsInfoIN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        
        iEPSGCode = int(self.oDataInfo.oInfoSettings.oGeoSystemInfo['epsg_code'])
        sPathDataSource = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        sPathTemp = self.oDataInfo.oInfoSettings.oPathInfo['DataTemp']
        
        # Get data
        oDataGeo = self.oDataGeo
        oDataAnalyzed = self.oDataAnalyzed 
        a1oDataSelect = self.a1oDataSelect
        
        oVarsSave = self.oVarsSave
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
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
                
                #print('DEBUG VARIABLE')
                #sVarName = 'IncRadiation'
                #sVarName = 'AirTemperature'
                #sVarName = 'Rain'
                #sVarName = 'Wind'
                #sVarName = 'RelHumidity'
                #sVarName = 'SnowLevel'
                
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
                    # Check data) availability
                    if sFileNameIN in a1oDataSelect:
            
                        #-------------------------------------------------------------------------------------
                        # Get interpolate method selection
                        oData_InterpMethod = getattr(Lib_Data_Analysis_Interpolation, 
                                                     oVarsInfoIN[sVarType][sVarName]['VarOp']['Op_Math']['Interpolation']['Func'])
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Cycling on timestep to interpolate variable using selected method
                        if a1oDataSelect[sFileNameIN]:
                            
                            #-------------------------------------------------------------------------------------
                            # Compute data time steps
                            if isinstance(a1oDataSelect[sFileNameIN]['Time'], basestring):
                                iDataLen = 1
                            else:
                                iDataLen = len(a1oDataSelect[sFileNameIN]['Time'])
                            #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            # Get variable component(s)
                            oVarsComp = oVarsInfoIN[sVarType][sVarName]['VarOp']['Op_Load']['Comp']['OUT']
                            
                            # Get radius information
                            dRadiusX = oVarsInfoIN[sVarType][sVarName]['VarOp']['Op_Math']['Interpolation']['XRad']
                            dRadiusY = oVarsInfoIN[sVarType][sVarName]['VarOp']['Op_Math']['Interpolation']['YRad']
                            try:
                                dRadiusInfluence = oVarsInfoIN[sVarType][sVarName]['VarOp']['Op_Math']['Interpolation']['InfluenceRad']
                                dRadiusInfluence = float(int(Lib_Data_Apps.convertDeg2Km(dRadiusInfluence)*1000)) # Convert from degree to meters
                            except:
                                dRadiusInfluence = None
                            # Get data excluded information
                            try:
                                dDataExc = float(oVarsInfoIN[sVarType][sVarName]['VarOp']['Op_Math']['Interpolation']['DataExcluded'])
                            except:
                                dDataExc = None
                            # Get data fill information (for nodata domain value)
                            try:
                                oDataFill = oVarsInfoIN[sVarType][sVarName]['VarOp']['Op_Math']['Interpolation']['FillValue']
                            except:
                                oDataFill = None
                            #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            # Cycling on data time dimension
                            iT = 0;
                            for iT in range(0,iDataLen):
                                
                                #-------------------------------------------------------------------------------------
                                # Define time variable (according to number of steps)
                                if iDataLen == 1:
                                    sTimeVarLoad = str(a1oDataSelect[sFileNameIN]['Time'])
                                    sTimeVarSave = convertTimeLOCxGMT(sTimeVarLoad, -(self.oDataTime.iTimeRefLoad))
                                    
                                else:
                                    sTimeVarLoad = str(a1oDataSelect[sFileNameIN]['Time'][iT])
                                    sTimeVarSave = convertTimeLOCxGMT(sTimeVarLoad, -(self.oDataTime.iTimeRefLoad))
                                
                                oLogStream.info( ' -----> Var LoadTime: ' + sTimeVarLoad + ' --- Var SaveTime: ' + sTimeVarSave)
                                
                                # Initialize dictionary using variable and time
                                for sVarValues in oVarsComp.values():
                                    # Initialize dictionary dynamic variable name key
                                    if not sVarValues in self.oVarData:
                                        self.oVarData[sVarValues] = {}
                                        
                                    # Initialize dictionary dynamic time key
                                    if not sTimeVarSave in self.oVarData[sVarValues]:
                                        self.oVarData[sVarValues][sTimeVarSave] = {}
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Data interpolation
                                oLogStream.info( ' -----> Interpolating ' + sVarName + ' at time ' + sTimeVarLoad + ' ... ')
                                oDataInterp = oData_InterpMethod(oDataGeo,
                                                                 a1oDataSelect[sFileNameIN]['Data'][sTimeVarLoad][sVarName],
                                                                 a1oDataSelect[sFileNameIN]['GeoX'], 
                                                                 a1oDataSelect[sFileNameIN]['GeoY'], 
                                                                 a1oDataSelect[sFileNameIN]['GeoZ'], 
                                                                 dRadiusX, dRadiusY, dRadiusInfluence, 
                                                                 dDataExc, 
                                                                 iEPSGCode, sPathTemp, oDataAnalyzed)
                                
                                # Cycle(s) on variable key(s) and value(s)
                                for sVarKey in oVarsComp:
                                    
                                    # Get comp variable name
                                    sVarNameComp = oVarsComp[sVarKey]
                                    
                                    # Check to fill nodata value in domain area
                                    oDataInterp[sVarKey] = Lib_Data_Analysis_Interpolation.interpVarFillValue(oDataInterp[sVarKey], 
                                                                                                              oDataGeo, oDataFill)
                                    
                                    self.oVarData[sVarNameComp][sTimeVarSave] = oDataInterp[sVarKey]
                                    
                                    # Debug
                                    #plt.figure(1)
                                    #plt.imshow(oDataInterp[sVarKey]); plt.colorbar(); plt.clim(0, 20)
                                    #plt.figure(2)
                                    #plt.imshow(a2dVar); plt.colorbar(); plt.clim(0, 20)
                                    #plt.figure(3)
                                    #plt.imshow(self.oDataGeo.a2dGeoData); plt.colorbar()
                                    #plt.show()
                                
                                # Info
                                oLogStream.info( ' -----> Interpolating ' + sVarName + ' at time ' + sTimeVarLoad + ' ... OK')
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Info
                                oLogStream.info( ' -----> Variable: ' + sVarName + ' ... OK ')
                                #-------------------------------------------------------------------------------------
                                
                            #-------------------------------------------------------------------------------------
                            
                        else:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... SKIPPED --- FILE INPUT NOT LOADED ')
                            oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE UNDEFINED IN INPUT FILE ')
                            GetException(' -----> WARNING: variable is undefined in input file!', 2, 1)
                            #-------------------------------------------------------------------------------------
                    else:
                        
                        #-------------------------------------------------------------------------------------
                        # Exit code(s) for data not available
                        if not sFileNameIN in a1oDataSelect:
                            oLogStream.info( ' -----> Getting data: ' + sFileNameIN + ' ... SKIPPED --- DATA NOT AVAILABLE (CURRENT TIME)')
                            oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- DATA NOT AVAILABLE (CURRENT TIME)')
                            GetException(' -----> WARNING: data not available in workspace!', 2, 1)
                        else:
                            pass
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
                    a3dVarData = np.zeros([self.oDataGeo.oGeoData.iRows, self.oDataGeo.oGeoData.iCols, iVarLen])
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
                    # SAVE DATA IN BINARY FORMAT (START)
                    # Cycle(s) on time step(s)
                    a1bFileBIN_CHECK = []; a1sFileNameBIN_OUT = [];
                    for iVarStep_BIN, sVarTime_BIN in enumerate(a1oVarTime):
                        
                        #------------------------------------------------------------------------------------- 
                        # Time information
                        sVarYear_BIN = sVarTime_BIN[0:4]; sVarMonth_BIN = sVarTime_BIN[4:6]; sVarDay_BIN = sVarTime_BIN[6:8];
                        sVarHH_BIN = sVarTime_BIN[8:10]; sVarMM_BIN = sVarTime_BIN[10:12];
                        
                        # Pathname BIN OUT
                        sPathNameBIN_OUT = Lib_Data_IO_Utils.defineFolderName(sPathData_OUT,
                                                                     {'$yyyy' : sVarYear_BIN,'$mm' : sVarMonth_BIN,'$dd' : sVarDay_BIN, 
                                                                      '$HH' : sVarHH_BIN,'$MM' : sVarMM_BIN})
                        # Time Info
                        oLogStream.info( ' ------> Save time step (BINARY): ' + sVarTime_BIN)
                        #------------------------------------------------------------------------------------- 
                        
                        #-------------------------------------------------------------------------------------
                        # Filename BIN OUT
                        sFileNameBIN_OUT = Lib_Data_IO_Utils.defineFileName(join(sPathNameBIN_OUT, oVarsInfo_OUT['Binary'][sVarName]['VarSource']), 
                                                                 {'$yyyy' : sVarYear_BIN,'$mm' : sVarMonth_BIN,'$dd' : sVarDay_BIN, 
                                                                  '$HH' : sVarHH_BIN,'$MM' : sVarMM_BIN})
                        
                        # Check output file(s) availability 
                        bFileExistBIN_OUT = Lib_Data_IO_Utils.checkFileExist(sFileNameBIN_OUT + '.' + 
                                                                             oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save']['Zip'])
                        
                        # Info
                        oLogStream.info( ' -------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... ')
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check saving variable method
                        try:
                            
                            #-------------------------------------------------------------------------------------
                            # Check binary availability
                            if (bFileExistBIN_OUT is False) or (oVarsSave_OUT[sVarName] is False):
                            
                                #-------------------------------------------------------------------------------------
                                # Check variable name to select save function
                                if sVarName in oVarsInfo_OUT['Binary']:
                                
                                    #-------------------------------------------------------------------------------------
                                    # Open binary file
                                    oDrvBIN_OUT = Drv_Data_IO(sFileNameBIN_OUT, 'w')
                                    
                                    # Define write method
                                    oDrvBIN_WriteMethod = getattr(oDrvBIN_OUT.oFileWorkspace, 
                                                                   oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save']['Func'])
                                    
                                    # Save 2d array in a binary file
                                    oDrvBIN_WriteMethod(a3dVarData[:,:,iVarStep_BIN], 
                                                        oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save'])
                                    
                                    # Close binary file
                                    oDrvBIN_OUT.oFileWorkspace.closeFile()
                                    
                                    # Zip file
                                    Drv_Data_Zip(sFileNameBIN_OUT, 'z', 
                                                 oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save']['Zip'], True)
                                    
                                    # Info
                                    a1sFileNameBIN_OUT.append(sFileNameBIN_OUT + '.' + oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save']['Zip'])
                                    a1bFileBIN_CHECK.append(True)
                                    oLogStream.info( ' -------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... OK ')
                                    #-------------------------------------------------------------------------------------
                                
                                else:
                                    
                                    #-------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileBIN_CHECK.append(False)
                                    GetException(' -------> WARNING: field not found in outcome workspace!', 2, 1)
                                    oLogStream.info( ' -------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... FAILED --- FIELD NOT FOUND IN OUTCOME WORKSPACE')
                                    #-------------------------------------------------------------------------------------
                                    
                                #-------------------------------------------------------------------------------------
                            
                            else:
                                    
                                #-------------------------------------------------------------------------------------
                                # Exit code
                                a1bFileBIN_CHECK.append(True)
                                oLogStream.info( ' -------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... PREVIOUSLY SAVED')
                                #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                        
                        except:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            a1bFileBIN_CHECK.append(False) 
                            # Info
                            GetException(' -------> WARNING: errors occurred in saving file! Check your output data!', 2, 1)
                            oLogStream.info( ' -------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... FAILED --- ERRORS OCCURRED IN SAVING DATA!')
                            #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                    
                    # Cycle(s) on time steps (END)
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Check saved data BIN
                    if np.all(np.asarray(a1bFileBIN_CHECK) == True ):
                        # Create cache handle
                        sFileCacheBIN_CHECK = os.path.join(sPathData_CACHE, 'WS_DB-NETWORK_FILEBIN_' + sTimeSave + '_' + sVarName + '.history')
                        # Save hystory file for BIN
                        writeFileHistory(sFileCacheBIN_CHECK, zip(a1sFileNameBIN_OUT))
                        
                        #with open(sFileCacheBIN_CHECK, 'wb') as oFile:
                        #    pickle.dump(a1bFileBIN_CHECK, oFile, pickle.HIGHEST_PROTOCOL)
                    else:
                        # Info warning
                        GetException(' -------> WARNING: some files are not saved on disk! Check your data input!', 2, 1)
                    
                    # SAVE DATA IN BINARY FORMAT (END)
                    #-------------------------------------------------------------------------------------
            
                    #-------------------------------------------------------------------------------------
                    # SAVE DATA IN NC FORMAT (START)
                    
                    #-------------------------------------------------------------------------------------
                    # Time information
                    sVarTime_NC = sTimeSave
                    sVarYear_NC = sVarTime_NC[0:4]; sVarMonth_NC = sVarTime_NC[4:6]; sVarDay_NC = sVarTime_NC[6:8];
                    sVarHH_NC = sVarTime_NC[8:10]; sVarMM_NC = sVarTime_NC[10:12];
    
                    # Pathname NC OUT
                    sPathNameNC_OUT = Lib_Data_IO_Utils.defineFolderName(sPathData_OUT,
                                                                 {'$yyyy' : sVarYear_NC,'$mm' : sVarMonth_NC,'$dd' : sVarDay_NC, 
                                                                  '$HH' : sVarHH_NC,'$MM' : sVarMM_NC})
                    # Time Info
                    oLogStream.info( ' ------> Save time step (NC): ' + sVarTime_NC)
                    #------------------------------------------------------------------------------------- 
                    
                    #------------------------------------------------------------------------------------- 
                    # Filename NC OUT
                    sFileNameNC_OUT = Lib_Data_IO_Utils.defineFileName(join(sPathNameNC_OUT, oVarsInfo_OUT['NetCDF'][sVarName]['VarSource']), 
                                                             {'$yyyy' : sVarYear_NC,'$mm' : sVarMonth_NC,'$dd' : sVarDay_NC, 
                                                              '$HH' : sVarHH_NC,'$MM' : sVarMM_NC})
                    
                    # Check output file(s) availability 
                    bFileExistNC_OUT = Lib_Data_IO_Utils.checkFileExist(sFileNameNC_OUT + '.' + 
                                                                        oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Zip'])
                    
                    # Info
                    oLogStream.info( ' -------> Saving file output (NC): ' + sFileNameNC_OUT + ' ... ')
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Check errors in code
                    a1bFileNC_CHECK = []; a1sFileNameNC_OUT = []
                    try:
                        
                        #-------------------------------------------------------------------------------------
                        # Check if time condition(s) are true or false
                        if (oVarsSave_OUT[sVarName] is False):
                            
                            #-------------------------------------------------------------------------------------
                            # Open NC file (in write or append mode)
                            bVarExistNC_OUT = False;
                            if bFileExistNC_OUT is False:
                                
                                #-------------------------------------------------------------------------------------
                                # Open NC file in write mode
                                oDrvNC_OUT = Drv_Data_IO(sFileNameNC_OUT, 'w')
                                bVarExistNC_OUT = False;
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Write global attributes (common and extra)
                                oDrvNC_OUT.oFileWorkspace.writeFileAttrsCommon(self.oDataInfo.oInfoSettings.oGeneralInfo)
                                oDrvNC_OUT.oFileWorkspace.writeFileAttrsExtra(self.oDataInfo.oInfoSettings.oParamsInfo,
                                                                               self.oDataGeo.a1oGeoInfo)
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Write geo-system information
                                oDrvNC_OUT.oFileWorkspace.writeGeoSystem(self.oDataInfo.oInfoSettings.oGeoSystemInfo, 
                                                                          self.oDataGeo.oGeoData.a1dGeoBox)
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Declare variable dimensions
                                sDimVarX = oVarsInfo_OUT['NetCDF']['Terrain']['VarDims']['X']
                                oDrvNC_OUT.oFileWorkspace.writeDims(sDimVarX, self.oDataGeo.oGeoData.iCols)
                                sDimVarY = oVarsInfo_OUT['NetCDF']['Terrain']['VarDims']['Y']
                                oDrvNC_OUT.oFileWorkspace.writeDims(sDimVarY, self.oDataGeo.oGeoData.iRows)
                                sDimVarT = 'time'; 
                                oDrvNC_OUT.oFileWorkspace.writeDims(sDimVarT, iVarLen)
                                # Declare extra dimension(s)
                                oDrvNC_OUT.oFileWorkspace.writeDims('nsim', 1)
                                oDrvNC_OUT.oFileWorkspace.writeDims('ntime', 2)
                                oDrvNC_OUT.oFileWorkspace.writeDims('nens', 1)
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Write time information
                                oDrvNC_OUT.oFileWorkspace.writeTime(a1oVarTime, 'f8', 'time', iVarLen/iVarLen)
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Try to save longitude
                                sVarGeoX = 'Longitude'
                                oLogStream.info( ' -------> Saving variable: ' + sVarGeoX + ' ... ')
                                try:
    
                                    #-------------------------------------------------------------------------------------
                                    # Get longitude
                                    oDrvNC_WriteMethod = getattr(oDrvNC_OUT.oFileWorkspace,  
                                                                 oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarOp']['Op_Save']['Func'])
                                    oDrvNC_WriteMethod(sVarGeoX, self.oDataGeo.oGeoData.a2dGeoX, 
                                                       oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarAttributes'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarOp']['Op_Save']['Format'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarDims']['Y'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarDims']['X'])
                                    # Info
                                    a1bFileNC_CHECK.append(True)
                                    oLogStream.info( ' -------> Saving variable: ' + sVarGeoX + ' ... OK ')
                                    #-------------------------------------------------------------------------------------
                                
                                except:
                                    
                                    #-------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileNC_CHECK.append(False)
                                    GetException(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info( ' -------> Saving variable: ' + sVarGeoX + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                    #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Try to save latitude
                                sVarGeoY = 'Latitude'
                                oLogStream.info( ' -------> Saving variable: ' + sVarGeoY + ' ... ')
                                try:
                                
                                    #-------------------------------------------------------------------------------------
                                    # Get latitude
                                    oDrvNC_WriteMethod = getattr(oDrvNC_OUT.oFileWorkspace,  
                                                                 oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarOp']['Op_Save']['Func'])
                                    oDrvNC_WriteMethod(sVarGeoY, self.oDataGeo.oGeoData.a2dGeoY, 
                                                       oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarAttributes'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarOp']['Op_Save']['Format'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarDims']['Y'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarDims']['X'])
                                    # Info
                                    a1bFileNC_CHECK.append(True)
                                    oLogStream.info( ' -------> Saving variable: ' + sVarGeoY + ' ... OK ')
                                    #-------------------------------------------------------------------------------------
                                
                                except:
                                    
                                    #-------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileNC_CHECK.append(False)
                                    GetException(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info( ' -------> Saving variable: ' + sVarGeoY + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                    #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Try to save terrain
                                sVarTerrain = 'Terrain'
                                oLogStream.info( ' -------> Saving variable: ' + sVarTerrain + ' ... ')
                                try:                     
                                
                                    #-------------------------------------------------------------------------------------
                                    # Get terrain  
                                    a2dData = self.oDataGeo.a2dGeoData
                                    a2dData[self.oDataGeo.a2bGeoDataNan] = self.oDataGeo.dNoData
                                     
                                    oDrvNC_WriteMethod = getattr(oDrvNC_OUT.oFileWorkspace, 
                                                                 oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarOp']['Op_Save']['Func'])
                                    oDrvNC_WriteMethod(sVarTerrain, a2dData, 
                                                       oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarAttributes'],
                                                       oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarOp']['Op_Save']['Format'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarDims']['Y'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarDims']['X'])
                                    # Info
                                    a1bFileNC_CHECK.append(True)
                                    oLogStream.info( ' -------> Saving variable: ' + sVarTerrain + ' ... OK ')
                                    #-------------------------------------------------------------------------------------
                                
                                except:
                                    
                                    #-------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileNC_CHECK.append(False)
                                    GetException(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info( ' -------> Saving variable: ' + sVarTerrain + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                    #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Try to save 3d variable
                                oLogStream.info( ' -------> Saving variable: ' + sVarName + ' ... ')
                                try:
                                
                                    #-------------------------------------------------------------------------------------
                                    # Get data dynamic
                                    oDrvNC_WriteMethod = getattr(oDrvNC_OUT.oFileWorkspace, 
                                                                 oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Func'])
                                    oDrvNC_WriteMethod(sVarName, a3dVarData[:,:,0], 
                                                       oVarsInfo_OUT['NetCDF'][sVarName]['VarAttributes'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Format'],
                                                       oVarsInfo_OUT['NetCDF'][sVarName]['VarDims']['Y'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarName]['VarDims']['X'])
                                
                                    # Info
                                    a1bFileNC_CHECK.append(True)
                                    oLogStream.info( ' -------> Saving variable: ' + sVarName + ' ... OK ')
                                    #-------------------------------------------------------------------------------------
                                
                                except:
                                    
                                    #-------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileNC_CHECK.append(False)
                                    GetException(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                    oLogStream.info( ' -------> Saving variable: ' + sVarName + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                    #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Close NetCDF file
                                oDrvNC_OUT.oFileWorkspace.closeFile()
                                
                                # Zip file
                                Drv_Data_Zip(sFileNameNC_OUT, 
                                             'z', 
                                             oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Zip'], 
                                             True)
                                
                                # Info
                                a1sFileNameNC_OUT.append(sFileNameNC_OUT + '.' + oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Zip'])
                                oLogStream.info( ' ------> Saving file output NetCDF: ' + sFileNameNC_OUT + ' ... OK')
                                #-------------------------------------------------------------------------------------
                                
                            else:
                                
                                #-------------------------------------------------------------------------------------
                                # Unzip NC file (if file is compressed)
                                Drv_Data_Zip(sFileNameNC_OUT + '.' +  oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Zip'],
                                             'u', 
                                             oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Zip'], 
                                             True)
                                
                                # Open NC file in append mode
                                oDrvNC_OUT = Drv_Data_IO(sFileNameNC_OUT, 'a')
                                bVarExistNC_OUT = oDrvNC_OUT.oFileWorkspace.checkVarName(sVarName)
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Check variable availability
                                oLogStream.info( ' -------> Saving variable: ' + sVarName + ' ... ')
                                if bVarExistNC_OUT is False:
                                
                                    #-------------------------------------------------------------------------------------
                                    # Try to save 3d variable
                                    try:
                                    
                                        #-------------------------------------------------------------------------------------
                                        # Get data dynamic
                                        oDrvNC_WriteMethod = getattr(oDrvNC_OUT.oFileWorkspace, 
                                                                     oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Func'])
                                        oDrvNC_WriteMethod(sVarName, a3dVarData[:,:,0],  
                                                           oVarsInfo_OUT['NetCDF'][sVarName]['VarAttributes'], 
                                                           oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Format'], 
                                                           oVarsInfo_OUT['NetCDF'][sVarName]['VarDims']['Y'], 
                                                           oVarsInfo_OUT['NetCDF'][sVarName]['VarDims']['X'])
                                    
                                        # Info
                                        a1bFileNC_CHECK.append(True)
                                        oLogStream.info( ' -------> Saving variable: ' + sVarName + ' ... OK ')
                                        #-------------------------------------------------------------------------------------
                                    
                                    except:
                                        
                                        #-------------------------------------------------------------------------------------
                                        # Exit code
                                        a1bFileNC_CHECK.append(False)
                                        GetException(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                        oLogStream.info( ' -------> Saving variable: ' + sVarName + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                        #-------------------------------------------------------------------------------------
                                    
                                    #-------------------------------------------------------------------------------------
                                
                                else:
                                    #-------------------------------------------------------------------------------------
                                    # Info
                                    oLogStream.info( ' -------> Saving variable: ' + sVarName + ' ... SAVED PREVIOUSLY')
                                    a1bFileNC_CHECK.append(True)
                                    #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Close NetCDF file
                                oDrvNC_OUT.oFileWorkspace.closeFile()
                                
                                # Zip file
                                Drv_Data_Zip(sFileNameNC_OUT, 
                                             'z', 
                                             oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Zip'], 
                                             True)
                                
                                # Info
                                a1sFileNameNC_OUT.append(sFileNameNC_OUT + '.' + oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Zip'])
                                oLogStream.info( ' ------> Saving file output NetCDF: ' + sFileNameNC_OUT + ' ... OK')
                                #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            
                        else:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            a1bFileNC_CHECK.append(True)
                            oLogStream.info( ' ------> Saving file output NetCDF: ' + sFileNameNC_OUT + ' ... PREVIOUSLY SAVED ')
                            #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        
                    except:
                        
                        #-------------------------------------------------------------------------------------
                        # Exit code
                        a1bFileNC_CHECK.append(False) 
                        # Info
                        GetException(' ------> WARNING: errors occurred in saving file! Check your output data!', 2, 1)
                        oLogStream.info( ' ------> Saving file output (NC): ' + sFileNameNC_OUT + ' ... FAILED --- ERRORS OCCURRED IN SAVING DATA!')
                        #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
    
                    #-------------------------------------------------------------------------------------
                    # Check saved data NC
                    if np.all(np.asarray(a1bFileNC_CHECK) == True ):
                        # Create hash handle
                        sFileCacheNC_CHECK = os.path.join(sPathData_CACHE, 'WS_DB-NETWORK_FILENC_' + sTimeSave + '_' + sVarName +'.history')
                        # Save hystory file for NC
                        writeFileHistory(sFileCacheNC_CHECK, zip(a1sFileNameNC_OUT))
                        
                        #with open(sFileCacheNC_CHECK, 'wb') as oFile:
                        #    pickle.dump(a1bFileNC_CHECK, oFile, pickle.HIGHEST_PROTOCOL)
                    else:
                        # Info warning
                        GetException(' ------> WARNING: some files are not saved on disk! Check your data input!', 2, 1)
                    
                    # SAVE DATA IN NC FORMAT (END)
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
            







 
