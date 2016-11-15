"""
Class Features

Name:          Cpl_Apps_KF_DynamicData_EF_AirTemperature
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151123'
Version:       '1.0.0'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os, datetime
import numpy as np

from os.path import join
from os.path import split

import src.Lib_Data_Analysis_Interpolation as Lib_Data_Analysis_Interpolation
import src.Lib_Data_IO_Utils as Lib_Data_IO_Utils
import src.Lib_Data_Apps as Lib_Data_Apps

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
class Cpl_Apps_KF_DynamicData_EF_AirTemperature:

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataTime=None, oDataGeo=None, oDataAncillary=None, oDataInfo=None):
        
        # Data settings and data reference 
        self.oDataTime = oDataTime
        self.oDataGeo = oDataGeo
        self.oDataAncillary = oDataAncillary
        self.oDataInfo = oDataInfo
        
        self.oDataAnalyzed = None
        
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
                    # NETCDF Check file
                    sFileCacheNC_CHECK = os.path.join(sPathData_CHECK, 'KF_EF-AIRTEMPERATURE_FILENC_' + sTimeSave + '_' + sVarCompOUT + '.history')
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
        oDrv_DataType = Drv_Data_Type(oDataGeo=self.oDataGeo ,oDataInfo=self.oDataInfo)
        
        sPathDataSource = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        oVarsInfoIN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        oParamsInfo = self.oDataInfo.oInfoSettings.oParamsInfo
        
        # Get WS information
        oWS = self.oDataAncillary['WS']
        oGeoX = self.oDataAncillary['GeoX']
        oGeoY = self.oDataAncillary['GeoY']
        oGeoZ = self.oDataAncillary['GeoZ']
        
        # Get saved variable(s) information
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
        # Info start getting data
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
                # Get filename(s)
                oFileListIN = sorted(oVarsInfoIN[sVarType][sVarName]['VarSource']['IN'].keys())
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Cycling on filename(s)
                for sFileListIN in oFileListIN:
                    
                    #-------------------------------------------------------------------------------------
                    # Get FileNameIN
                    sFileNameIN = oVarsInfoIN[sVarType][sVarName]['VarSource']['IN'][sFileListIN]

                    # Define FileNameIN
                    sFileNameIN = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, sFileNameIN), 
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
                        if not sFileListIN in a1oFileDrvIN:
                            
                            # Input file driver
                            a1oFileDrvIN[sFileListIN] = Drv_Data_IO(sFileNameIN,'rU', str.lower(sVarType))
                            # Variable get method
                            oData_GetMethod = getattr(oDrv_DataType, 'getVar' + oVarsInfoIN[sVarType][sVarName]['VarType'])
                            # Get data selection
                            a1oDataSelect[sFileListIN] = oData_GetMethod(a1oFileDrvIN[sFileListIN].oFileWorkspace,
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
        
        #-------------------------------------------------------------------------------------
        # Info end getting data
        oLogStream.info( ' ====> GET DATA AT TIME: ' + sTimeSave + ' ... OK ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info start parsering data
        oLogStream.info( ' ====> PARSER DATA AT TIME: ' + sTimeSave + ' ...  ')
        
        # Get FileNameOUT
        sFileNameOUT = oVarsInfoIN[sVarType][sVarName]['VarSource']['OUT']

        # Define FileNameIN
        sFileNameOUT = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, sFileNameOUT), 
                                                 {'$VAR'  : sVarName,
                                                  '$yyyy' : sYearSave, '$mm' : sMonthSave, '$dd' : sDaySave, 
                                                  '$HH' : sHHSave, '$MM' : sMMSave})
        
        # Cycling on variable type definition (input)
        for sVarType in oVarsInfoIN:
            
            #------------------------------------------------------------------------------------- 
            # Cycling on variable name definition (input)
            for sVarName in oVarsInfoIN[sVarType]:
                
                #-------------------------------------------------------------------------------------
                # Get variable information
                oVarInfoIN = oVarsInfoIN[sVarType][sVarName]
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Check data select is not empty
                a1oTimeSteps = []; a1oDataSteps = []; a2oDataSteps = {}; a2oDataGeo = {}
                if a1oDataSelect:
                    
                    #-------------------------------------------------------------------------------------
                    # Get time initial step
                    sTimeData = sTimeSave
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Init variable(s)
                    a1oGeoX = []; a1oGeoY = []; a1oGeoZ = [];
                    for sFileListIN in sorted(oFileListIN):
                        
                        #-------------------------------------------------------------------------------------
                        # Select data
                        oDataSelect = a1oDataSelect[sFileListIN]['Data'][sTimeSave][sVarName]
                        
                        # Get type step
                        a1oDataTimeStepIN = sorted(oVarInfoIN['VarTimeStep']['IN'])
                        a1oDataTimeStepOUT = sorted(oVarInfoIN['VarTimeStep']['OUT'])
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Cycle(s) on WS information
                        for oWSInfo in oDataSelect:
                            
                            #-------------------------------------------------------------------------------------
                            # Get time information
                            oTimeFrom = datetime.datetime.strptime(sTimeData,'%Y%m%d%H%M')
                            oTimeFrom = oTimeFrom.replace(minute = 0, second = 0, microsecond = 0)
                            
                            # Get data
                            a1oWSInfo = oWSInfo.split('$');
                            a1oWSData = Lib_Data_IO_Utils.getNumber(a1oWSInfo, 'NA')

                            # Get geographical information
                            iWSIndex = oWS.index(a1oWSInfo[0])
                            if not a1oWSInfo[0] in a2oDataGeo:
                                a2oDataGeo[a1oWSInfo[0]] = {}
                                a2oDataGeo[a1oWSInfo[0]]['GeoX'] = oGeoX[iWSIndex]
                                a2oDataGeo[a1oWSInfo[0]]['GeoY'] = oGeoY[iWSIndex]
                                a2oDataGeo[a1oWSInfo[0]]['GeoZ'] = oGeoZ[iWSIndex]
                            else:pass
                            
                            # Get data information
                            if not a1oWSInfo[0] in a2oDataSteps:
                                a2oDataSteps[a1oWSInfo[0]] = None
                            else:pass
                            #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            # Cycle(s) on step type
                            for iStepIndex, sStepType in enumerate(a1oDataTimeStepIN):
                                
                                # Get time step
                                iTimeStepIN = int(oVarInfoIN['VarTimeStep']['IN'][sStepType])
                                iTimeStepOUT = int(oVarInfoIN['VarTimeStep']['OUT'][sStepType])
                                
                                # Define time period
                                oTimeTo = oTimeFrom + datetime.timedelta(seconds = iTimeStepIN)
                                oTimeDelta = datetime.timedelta(seconds = iTimeStepOUT)
                                
                                # Save data on time period
                                while oTimeFrom < oTimeTo:
                                    a1oTimeSteps.append(oTimeFrom.strftime('%Y%m%d%H%M'))
                                    oTimeFrom += oTimeDelta
                                    
                                    # Save data using time steps
                                    if a1oWSData[iStepIndex] == 'NA':
                                        a1oWSData[iStepIndex] = '-9999.0'
                                    else:pass
                                    a1oDataSteps.append(float(a1oWSData[iStepIndex]))
                                
                                oTimeFrom = oTimeTo
                            #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            # Store all values for all time steps and ws
                            if a2oDataSteps[a1oWSInfo[0]] == None:
                                a2oDataSteps[a1oWSInfo[0]] = a1oDataSteps
                            else:
                                a1oDataStepsOld = a2oDataSteps[a1oWSInfo[0]]
                                a1oDataStepsUpd = a1oDataStepsOld + a1oDataSteps
                                a2oDataSteps[a1oWSInfo[0]] = a1oDataStepsUpd
                            # Re-initialize data steps
                            a1oDataSteps = []
                            #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Get unique time steps 
                        a1oTimeSteps = sorted(list(set(a1oTimeSteps)))
                        sTimeData = oTimeFrom.strftime('%Y%m%d%H%M')
                        #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Initialize storing object
                    iWSLen = len(a2oDataSteps.keys())
                    
                    a1dGeoX = np.zeros([1,iWSLen]); a1dGeoY = np.zeros([1,iWSLen]); a1dGeoZ = np.zeros([1,iWSLen])
                    oDataObj = {}; a2oDataObj = []
                    
                    oDataObj[sFileNameOUT] = {}
                    oDataObj[sFileNameOUT]['Data'] = {}
                    
                    # Cycling on timestep(s)
                    for iTimeStep, sTimeStep in enumerate(a1oTimeSteps):
                        
                        oDataObj[sFileNameOUT]['Data'][sTimeStep] = {}
                        oDataObj[sFileNameOUT]['Data'][sTimeStep][sVarName] = {}
                        
                        a1dData = np.zeros([1,iWSLen])

                        # Cycling on keys
                        for iKey, sKey in enumerate(a2oDataSteps.keys()):
                            
                            # Get geographical information
                            if not 'GeoX' in oDataObj[sFileNameOUT]:
                                a1oDataGeo = a2oDataGeo[sKey]
                                dGeoX = float(a1oDataGeo['GeoX'])
                                a1dGeoX[0,iKey] = dGeoX
                            else:pass
                            if not 'GeoY' in oDataObj[sFileNameOUT]:
                                a1oDataGeo = a2oDataGeo[sKey]
                                dGeoY = float(a1oDataGeo['GeoY'])
                                a1dGeoY[0,iKey] = dGeoY
                            else:pass
                            if not 'GeoZ' in oDataObj[sFileNameOUT]:
                                a1oDataGeo = a2oDataGeo[sKey]
                                dGeoZ = float(a1oDataGeo['GeoZ'])
                                a1dGeoZ[0,iKey] = dGeoZ
                            else:pass
                            
                            # Get data information
                            a1oDataSteps = a2oDataSteps[sKey]
                            dData = float(a1oDataSteps[iTimeStep])
                            
                            if dData == -9999.0:
                                dData = np.nan
                            else:pass
                            
                            a1dData[0,iKey] = dData
                            
                        # Concatenate data
                        a1oFileData = list([sTimeStep]) + list(a1dData[0])
                        if not a2oDataObj:
                            a2oDataObj = a2oDataObj + [['WS'] + list(a2oDataSteps.keys())]
                            a2oDataObj = a2oDataObj + [['GeoX'] + list(a1dGeoX)]
                            a2oDataObj = a2oDataObj + [['GeoY'] + list(a1dGeoY)]
                            a2oDataObj = a2oDataObj + [['GeoZ'] + list(a1dGeoZ)]
                        else:pass
                        a2oDataObj = a2oDataObj + [a1oFileData]
                            
                        # Store data information
                        oDataObj[sFileNameOUT]['Data'][sTimeStep][sVarName] = a1dData
                        # Store geographical information
                        if not 'GeoX' in oDataObj[sFileNameOUT]:
                            oDataObj[sFileNameOUT]['GeoX'] = a1dGeoX
                        else:pass
                        if not 'GeoY' in oDataObj[sFileNameOUT]:
                            oDataObj[sFileNameOUT]['GeoY'] = a1dGeoY
                        else:pass
                        if not 'GeoZ' in oDataObj[sFileNameOUT]:
                            oDataObj[sFileNameOUT]['GeoZ'] = a1dGeoZ
                        else:pass
                        if not 'Time' in oDataObj[sFileNameOUT]:
                            oDataObj[sFileNameOUT]['Time'] = a1oTimeSteps
                        else:pass
                        #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Write raw data on disk
                    oFileDrv = Drv_Data_IO(sFileNameOUT, 'wb')
                    oFileDrv.oFileWorkspace.writeFileData(a2oDataObj)
                    oFileDrv.oFileWorkspace.closeFile()
                    #-------------------------------------------------------------------------------------

                else:
                    
                    #-------------------------------------------------------------------------------------
                    # Exit code
                    oLogStream.info( ' -----> Parsering file(s) at time : ' + sTimeSave + ' ... SKIPPED --- DATA INPUT NOT FOUND ')
                    oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE UNDEFINED IN DATA INPUT ')
                    GetException(' -----> WARNING: variable is undefined in data input!', 2, 1)
                    oDataObj = None
                    #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info end parsering data
        oLogStream.info( ' ====> PARSER DATA AT TIME: ' + sTimeSave + ' ...  OK')
        
        # Save data in global workspace
        self.oDataObj = oDataObj
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
        oDataAnalyzed = self.oDataAnalyzed
        oDataGeo = self.oDataGeo
        oDataObj = self.oDataObj
        
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
                                
                #------------------------------------------------------------------------------------- 
                # FilenameIN definition
                sFileNameIN = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, oVarsInfoIN[sVarType][sVarName]['VarSource']['OUT']), 
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
                    if sFileNameIN in oDataObj:
            
                        #-------------------------------------------------------------------------------------
                        # Get interpolate method selection
                        oData_InterpMethod = getattr(Lib_Data_Analysis_Interpolation, 
                                                     oVarsInfoIN[sVarType][sVarName]['VarOp']['Op_Math']['Interpolation']['Func'])
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Cycling on timestep to interpolate variable using selected method
                        if oDataObj[sFileNameIN]:
                            
                            #-------------------------------------------------------------------------------------
                            # Compute data time steps
                            if isinstance(oDataObj[sFileNameIN]['Time'], basestring):
                                iDataLen = 1
                            else:
                                iDataLen = len(oDataObj[sFileNameIN]['Time'])
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
                                    sTimeVarLoad = str(oDataObj[sFileNameIN]['Time'])
                                    sTimeVarSave = convertTimeLOCxGMT(sTimeVarLoad, -(self.oDataTime.iTimeRefLoad))
                                    
                                else:
                                    sTimeVarLoad = str(oDataObj[sFileNameIN]['Time'][iT])
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
                                                                 oDataObj[sFileNameIN]['Data'][sTimeVarLoad][sVarName][0],
                                                                 oDataObj[sFileNameIN]['GeoX'], 
                                                                 oDataObj[sFileNameIN]['GeoY'], 
                                                                 oDataObj[sFileNameIN]['GeoZ'], 
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
                        if not sFileNameIN in oDataObj:
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
                        a2dVarData[self.oDataGeo.a2bGeoDataNan] = self.oDataGeo.dNoData
                        
                        a3dVarData[:,:, iVarTimeIndex] = a2dVarData
                            
                        # Save time information (for loading and saving function)
                        a1oVarTime.append(sVarTime)
 
                        # Counter to get data
                        iVarTimeIndex = iVarTimeIndex + 1
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
                                    oDrvNC_WriteMethod(sVarName, a3dVarData[:,:,:], 
                                                       oVarsInfo_OUT['NetCDF'][sVarName]['VarAttributes'], 
                                                       oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Format'],
                                                       oVarsInfo_OUT['NetCDF'][sVarName]['VarDims']['time'],
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
                                        oDrvNC_WriteMethod(sVarName, a3dVarData[:,:,:],  
                                                           oVarsInfo_OUT['NetCDF'][sVarName]['VarAttributes'], 
                                                           oVarsInfo_OUT['NetCDF'][sVarName]['VarOp']['Op_Save']['Format'], 
                                                           oVarsInfo_OUT['NetCDF'][sVarName]['VarDims']['time'],
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
                        sFileCacheNC_CHECK = os.path.join(sPathData_CACHE, 'KF_EF-AIRTEMPERATURE_FILENC_' + sTimeSave + '_' + sVarName +'.history')
                        # Save hystory file for NC
                        writeFileHistory(sFileCacheNC_CHECK, zip(a1sFileNameNC_OUT))
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
            







 
