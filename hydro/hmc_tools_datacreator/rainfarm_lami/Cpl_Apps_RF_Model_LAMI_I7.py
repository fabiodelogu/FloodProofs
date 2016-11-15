"""
Class Features

Name:          Cpl_Apps_RF_Model_LAMI_I7
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20150923'
Version:       '1.1.0'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os, hashlib, pickle
import numpy as np

from os.path import join

import src.Lib_Data_IO_Utils as Lib_Data_IO_Utils

from src.GetTime import convertTimeLOCxGMT
from src.GetException import GetException

from src.Drv_Model_RainFarm import Drv_Model_RainFarm

from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_Data_Zip import Drv_Data_Zip
from src.Drv_Data_Type import Drv_Data_Type
from src.Lib_Data_IO_Utils import getFileHistory, writeFileHistory

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Cpl_Apps_RF_Model_LAMI_I7:

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataTime=None, oDataGeo=None, oDataInfo=None):
        
        # Data settings and data reference 
        self.oDataTime = oDataTime
        self.oDataGeo = oDataGeo
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
                    sFileCacheBIN_CHECK = os.path.join(sPathData_CHECK, 'RF_LAMI-I7_FILEBIN_' + sTimeSave + '_' + sVarCompOUT + '.history')
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
                    sFileCacheNC_CHECK = os.path.join(sPathData_CHECK, 'RF_LAMI-I7_FILENC_' + sTimeSave + '_' + sVarCompOUT + '.history')
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
    # Method to get dynamic data
    def getDynamicData(self, sTime):
        
        #------------------------------------------------------------------------------------- 
        # Get information
        oDrv_DataType = Drv_Data_Type(oDataGeo=self.oDataGeo, oDataInfo=self.oDataInfo)
        sPathDataSource = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        oVarsInfoIN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        oVarsSave = self.oVarsSave
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET DATA AT TIME: ' + sTime + ' ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Time information
        sYearLoad = sTimeLoad[0:4]; sMonthLoad = sTimeLoad[4:6]; sDayLoad = sTimeLoad[6:8]; sHHLoad = sTimeLoad[8:10]; sMMLoad = sTimeLoad[10:12];
        sYearSave = sTimeSave[0:4]; sMonthSave = sTimeSave[4:6]; sDaySave = sTimeSave[6:8]; sHHSave = sTimeSave[8:10]; sMMSave = sTimeSave[10:12];
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Cycling on variable type definition (input)
        for sVarType in oVarsInfoIN:
            
            #------------------------------------------------------------------------------------- 
            # Cycling on variable name definition (input)
            a1oFileDrvIN = {}; a1oDataSelect = {};
            for sVarName in oVarsInfoIN[sVarType]:
                
                #------------------------------------------------------------------------------------- 
                # FilenameIN definition
                sFileNameIN = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, oVarsInfoIN[sVarType][sVarName]['VarSource']), 
                                                       {'$yyyy' : sYearSave,'$mm' : sMonthSave,'$dd' : sDaySave, 
                                                        '$HH' : sHHSave,'$MM' : sMMSave})
                # File and variable info
                oLogStream.info( ' -----> Variable: ' + sVarName + ' ... ')
                oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... ')
                #------------------------------------------------------------------------------------- 
                
                #------------------------------------------------------------------------------------- 
                # Check variable saving condition
                if oVarsSave[sVarName] is False:
                
                    #------------------------------------------------------------------------------------- 
                    # Check input file(s) availability
                    bFileExistIN = Lib_Data_IO_Utils.checkFileExist(sFileNameIN)
                    if bFileExistIN is True:
                        
                        #-------------------------------------------------------------------------------------
                        # Check variable availability
                        if not sFileNameIN in a1oFileDrvIN:
                            # Save file input driver(s)
                            a1oFileDrvIN[sFileNameIN] = Drv_Data_IO(sFileNameIN,'r', str.lower(sVarType))
                            
                            # Get retrieve method selection
                            oData_GetMethod = getattr(oDrv_DataType, 'getVar' + oVarsInfoIN[sVarType][sVarName]['VarType'])
                            
                            # Get data selection
                            a1oDataSelect[sFileNameIN] = oData_GetMethod(a1oFileDrvIN[sFileNameIN].oFileWorkspace,
                                                                         oVarsInfoIN[sVarType][sVarName]['VarOp'],
                                                                         None, None, None)
                            # Info
                            oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... OK ')
                        else:
                            pass
                        #-------------------------------------------------------------------------------------
            
                    else:
                        
                        #-------------------------------------------------------------------------------------
                        # Exit code(s)
                        oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... SKIPPED --- FILE INPUT NOT FOUND ')
                        oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE NOT FOUND ')
                        GetException(' -----> WARNING: file input is not available!', 2, 1)
                        #-------------------------------------------------------------------------------------
                
                else:
                    
                    #-------------------------------------------------------------------------------------
                    # Exit code(s)
                    oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... SKIPPED --- FILE INPUT FOUND ')
                    oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE COMPUTED PREVIOUSLY ')
                    #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Save in global workspace available data dynamic
        self.a1oDataSelect = a1oDataSelect
        # Info
        oLogStream.info( ' ====> GET DATA AT TIME: ' + sTimeSave + ' ... OK ')
        #-------------------------------------------------------------------------------------
        
        ######################################################################################
        ### DEBUG START SAVE DATI INIZIALI ###
        #import shelve
        #sFileIN = 'lami_'+sTime+'.data'
        #oWorkspace = shelve.open(sFileIN)
        #oWorkspace['workspace'] = a1oDataSelect
        #oWorkspace.close()
        
        #import scipy.io as io
        #sFileIN2 = 'lami_'+sTime+'.mat'
        #io.savemat(sFileIN2,a1oDataSelect[sFileNameIN]['Data'])
        
        ### DEBUG END SAVE DATI INIZIALI ###
        ######################################################################################

    # End method
    #-------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------- 
    # Dynamic data apps
    def computeDynamicData(self, sTime):
        
        ######################################################################################
        ### DEBUG START LOAD DATI INIZIALI ###
        #import shelve
        #sFileIN = 'lami_'+sTime+'.data'
        #oWorkspace = shelve.open(sFileIN)
        #self.a1oDataSelect = oWorkspace['workspace']
        #self.bSavingFileCTS = True; self.bSavingTimeRTS = True
        ### DEBUG END LOAD DATI INIZIALI ###
        ######################################################################################

        #------------------------------------------------------------------------------------- 
        # Get information
        sPathDataSource = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        sPathDataCache = self.oDataInfo.oInfoSettings.oPathInfo['DataCache']
        
        oVarsInfoIN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        oParamsRun = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']
        
        # Get data
        oDataGeo = self.oDataGeo
        a1oDataSelect = self.a1oDataSelect
        oVarsSave = self.oVarsSave
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> COMPUTE DATA AT TIME: ' + sTimeSave + ' ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Time information
        sYearLoad = sTimeLoad[0:4]; sMonthLoad = sTimeLoad[4:6]; sDayLoad = sTimeLoad[6:8]; sHHLoad = sTimeLoad[8:10]; sMMLoad = sTimeLoad[10:12];
        sYearSave = sTimeSave[0:4]; sMonthSave = sTimeSave[4:6]; sDaySave = sTimeSave[6:8]; sHHSave = sTimeSave[8:10]; sMMSave = sTimeSave[10:12];
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Cycling on variable type definition (input)
        self.oVarData = {}; sTimeFrom_IN = None; sTimeTo_IN = None;
        for sVarType in oVarsInfoIN:
            
            #------------------------------------------------------------------------------------- 
            # Cycling on variable name definition
            for sVarName in oVarsInfoIN[sVarType]:
                
                #------------------------------------------------------------------------------------- 
                # FilenameIN definition
                sFileNameIN = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, oVarsInfoIN[sVarType][sVarName]['VarSource']), 
                                                       {'$yyyy' : sYearSave,'$mm' : sMonthSave,'$dd' : sDaySave, 
                                                        '$HH' : sHHSave,'$MM' : sMMSave})
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
                        # Cycling on timestep to interpolate variable using selected method
                        if a1oDataSelect[sFileNameIN]:
                             
                            #-------------------------------------------------------------------------------------
                            # Compute data time steps
                            if isinstance(a1oDataSelect[sFileNameIN]['Time'], basestring):
                                iDataLen = 1;
                            else:
                                iDataLen = len(a1oDataSelect[sFileNameIN]['Time'])
                            #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            # Cycling on data time dimension
                            iT = 0; 
                            a3dDataXYT_IN = np.zeros([a1oDataSelect[sFileNameIN]['GeoX'].shape[0], 
                                                      a1oDataSelect[sFileNameIN]['GeoX'].shape[1], 
                                                      iDataLen])
                            for iT in range(0,iDataLen):
                                 
                                #-------------------------------------------------------------------------------------
                                # Define time var
                                if iDataLen == 1:
                                    sTimeVar = str(a1oDataSelect[sFileNameIN]['Time'])
                                else:
                                    sTimeVar = str(a1oDataSelect[sFileNameIN]['Time'][iT])
                                 
                                # Initialize dictin time step key
                                if not sTimeVar in self.oVarData:
                                    self.oVarData[sTimeVar] = {}
                                #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                                # Store data in 3D array
                                a2dDataXY = a1oDataSelect[sFileNameIN]['Data'][sTimeVar][sVarName]
                                # Check data
                                a2dDataXY[a2dDataXY<=0.01] = 0.0
                                # Store data
                                #a3dDataXYT_IN[:,:,iT] = np.flipud(a2dDataXY)
                                a3dDataXYT_IN[:,:,iT] = a2dDataXY
                                
                                # Get time period information
                                if iT == 0:
                                    sTimeFrom_IN = sTimeVar
                                elif iT == iDataLen - 1:
                                    sTimeTo_IN = sTimeVar
                                #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                            # Driver RF model
                            oDrvModel = Drv_Model_RainFarm(a3dDataXYT_IN, 
                                                           sTimeFrom_IN, sTimeTo_IN, 
                                                           a1oDataSelect[sFileNameIN]['GeoX'], a1oDataSelect[sFileNameIN]['GeoY'],
                                                           oDataGeo.oGeoData.a2dGeoX, oDataGeo.oGeoData.a2dGeoY, 
                                                           oDataGeo.oGeoData.dGeoXStep, oDataGeo.oGeoData.dGeoXStep, 
                                                           oParamsRun['DomainEXT'],
                                                           oParamsRun['EnsembleN'],
                                                           oParamsRun['CSsf'], oParamsRun['CTsf'],
                                                           oParamsRun['RatioS'], oParamsRun['RatioT'], 
                                                           oParamsRun['SlopeS'], oParamsRun['SlopeT'], 
                                                           oParamsRun['Multicore'], 
                                                           sPathDataCache)
                            
                            # Execute RF model (in single or multi-core mode)
                            oWorkspace_RF = oDrvModel.main()
                            #-------------------------------------------------------------------------------------

                            #-------------------------------------------------------------------------------------
                            # Info
                            oLogStream.info( ' -----> Getting data: ' + sFileNameIN + ' ... OK ')
                            oLogStream.info( ' -----> Variable: ' + sVarName + ' ... OK ')
                            #-------------------------------------------------------------------------------------
                                 
                        else:
                             
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            oLogStream.info( ' -----> Getting data: ' + sFileNameIN + ' ... SKIPPED --- DATA NOT AVAILABLE ')
                            oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE UNDEFINED IN INPUT FILE ')
                            GetException(' -----> WARNING: variable is undefined in data!', 2, 1)
                            #-------------------------------------------------------------------------------------
#                         
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
        # Save in global workspace available data dynamic
        self.oVarData = oWorkspace_RF
        # Info
        oLogStream.info( ' ====> COMPUTE DATA AT TIME: ' + sTimeSave + ' ... OK')
        #------------------------------------------------------------------------------------- 

        # End cycle(s) on variable type(s)
        #-------------------------------------------------------------------------------------
        
    # End method
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to save dynamic data
    def saveDynamicData(self, sTime):
        
        #------------------------------------------------------------------------------------- 
        # Get information
        sPathData_OUT = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicOutcome']
        sPathData_CACHE = self.sPathCache
        oVarsInfo_OUT = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic
        oVarsSave_OUT = self.oVarsSave
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))

        # Get static and dynamic RF field(s)
        oVarData_Dynamic = self.oVarData['dynamic']
        oVarData_Static = self.oVarData['static']
        
        # Get RF parameters
        dNt = float(oVarData_Static['iNt'])         # disaggregated step
        dNtl = float(oVarData_Static['iNtl'])       # raw step
        dNDelta = float(oVarData_Static['iNDelta']) # delta data
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTimeSave + ' ...  ')
        #------------------------------------------------------------------------------------- 
        
        #-------------------------------------------------------------------------------------
        # Cache definition
        sTime_CACHE = sTimeSave
        sYear_CACHE = sTime_CACHE[0:4]; sMonth_CACHE = sTime_CACHE[4:6]; sDay_CACHE = sTime_CACHE[6:8];
        sHH_CACHE = sTime_CACHE[8:10]; sMM_CACHE = sTime_CACHE[10:12];
        sPathData_CACHE = Lib_Data_IO_Utils.defineFolderName(sPathData_CACHE,
                                                     {'$yyyy' : sYear_CACHE,'$mm' : sMonth_CACHE,'$dd' : sDay_CACHE, 
                                                      '$HH' : sHH_CACHE,'$MM' : sMM_CACHE})
        #-------------------------------------------------------------------------------------

        #------------------------------------------------------------------------------------- 
        # Check workspace field(s)
        if np.any(oVarData_Dynamic):
            
            #-------------------------------------------------------------------------------------
            # Cycle(s) on ensemble(s)
            for sEnsembleN in oVarData_Dynamic:
                
                #-------------------------------------------------------------------------------------
                # Get data ensemble 
                oVarData_Ensemble = oVarData_Dynamic[sEnsembleN]
                sEnsembleN = str(int(sEnsembleN)).zfill(3)
                
                # Ensemble Info
                oLogStream.info( ' -----> Save ensemble N: ' + sEnsembleN + ' ... ')
                #-------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Cycle(s) on get var name
                for sVarName in oVarData_Ensemble:
                    
                    #-------------------------------------------------------------------------------------
                    # Check variable save condition
                    if oVarsSave_OUT[sVarName] is False:
                    
                        #-------------------------------------------------------------------------------------
                        # Get data
                        oVarData = oVarData_Ensemble[sVarName]
                        # Data length
                        iVarLen = len(oVarData)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Cycle(s) on get time step
                        iVarTimeIndex = 0;  a1oVarTime = [];
                        a3dVarData = np.zeros([self.oDataGeo.oGeoData.iRows, self.oDataGeo.oGeoData.iCols, iVarLen])
                        for sVarTime in sorted(oVarData):
                        
                            # Get data 
                            a2dVarData = oVarData[sVarTime]
                            #a2dVarData[self.oDataGeo.a2bGeoDataNan] = self.oDataGeo.dNoData
                            a3dVarData[:,:, iVarTimeIndex] = a2dVarData
                            
                            # Get time
                            a1oVarTime.append(sVarTime)
                            
                            # Counter to get data
                            iVarTimeIndex = iVarTimeIndex + 1
                        #-------------------------------------------------------------------------------------
                    
                        #-------------------------------------------------------------------------------------
                        # SAVE DATA IN BINARY FORMAT (START)
                        # Cycle(s) on time step(s)
                        a1bFileBIN_CHECK = []; a1sFileNameBIN_OUT = [];
                        for iStep_BIN, sTime_BIN in enumerate(a1oVarTime):
                            
                            #------------------------------------------------------------------------------------- 
                            # Time information
                            sYear_BIN = sTime_BIN[0:4]; sMonth_BIN = sTime_BIN[4:6]; sDay_BIN = sTime_BIN[6:8];
                            sHH_BIN = sTime_BIN[8:10]; sMM_BIN = sTime_BIN[10:12];
                            
                            # Pathname BIN OUT
                            sPathNameBIN_OUT = Lib_Data_IO_Utils.defineFolderName(sPathData_OUT,
                                                                         {'$yyyy' : sYear_BIN,'$mm' : sMonth_BIN,'$dd' : sDay_BIN, 
                                                                          '$HH' : sHH_BIN,'$MM' : sMM_BIN, '$ENS' : sEnsembleN})
                            # Time Info
                            oLogStream.info( ' -----> Save time step (BINARY): ' + sTime_BIN)
                            #------------------------------------------------------------------------------------- 
                            
                            #-------------------------------------------------------------------------------------
                            # FilenameOUT binary definition
                            sFileNameBIN_OUT = Lib_Data_IO_Utils.defineFileName(join(sPathNameBIN_OUT, oVarsInfo_OUT['Binary'][sVarName]['VarSource']), 
                                                                     {'$yyyy' : sYear_BIN,'$mm' : sMonth_BIN,'$dd' : sDay_BIN, 
                                                                      '$HH' : sHH_BIN,'$MM' : sMM_BIN})
                            
                            # Check output file(s) availability 
                            bFileExistBIN_OUT = Lib_Data_IO_Utils.checkFileExist(sFileNameBIN_OUT + '.' + 
                                                                                 oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save']['Zip'])
                            
                            # Info
                            oLogStream.info( ' ------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... ')
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
                                        oDrvBIN_WriteMethod(a3dVarData[:,:,iStep_BIN], 
                                                            oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save'])
                                        
                                        # Close binary file
                                        oDrvBIN_OUT.oFileWorkspace.closeFile()
                                        
                                        # Zip file
                                        Drv_Data_Zip(sFileNameBIN_OUT, 'z', 
                                                     oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save']['Zip'], True)
                                        
                                        # Info
                                        a1sFileNameBIN_OUT.append(sFileNameBIN_OUT + '.' + oVarsInfo_OUT['Binary'][sVarName]['VarOp']['Op_Save']['Zip'])
                                        a1bFileBIN_CHECK.append(True)
                                        oLogStream.info( ' ------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... OK ')
                                        #-------------------------------------------------------------------------------------
                                    
                                    else:
                                        
                                        #-------------------------------------------------------------------------------------
                                        # Exit code
                                        a1bFileBIN_CHECK.append(False)
                                        GetException(' ------> WARNING: field not found in outcome workspace!', 2, 1)
                                        oLogStream.info( ' ------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... FAILED --- FIELD NOT FOUND IN OUTCOME WORKSPACE')
                                        #-------------------------------------------------------------------------------------
                                        
                                    #-------------------------------------------------------------------------------------
                                
                                else:
                                        
                                    #-------------------------------------------------------------------------------------
                                    # Exit code
                                    a1bFileBIN_CHECK.append(True)
                                    oLogStream.info( ' ------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... PREVIOUSLY SAVED')
                                    #-------------------------------------------------------------------------------------
                                
                                #-------------------------------------------------------------------------------------
                            
                            except:
                                
                                #-------------------------------------------------------------------------------------
                                # Exit code
                                a1bFileBIN_CHECK.append(False) 
                                # Info
                                GetException(' ------> WARNING: errors occurred in saving file! Check your output data!', 2, 1)
                                oLogStream.info( ' ------> Saving file output (BINARY): ' + sFileNameBIN_OUT + ' ... FAILED --- ERRORS OCCURRED IN SAVING DATA!')
                                #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                        
                        # Cycle(s) on time steps (END)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check saved data BIN
                        if np.all(np.asarray(a1bFileBIN_CHECK) == True ):
                            # Create cache handle
                            sFileCacheBIN_CHECK = os.path.join(sPathData_CACHE, 'RF_LAMI-I7_FILEBIN_' + sTimeSave + '_' + sVarName + '_' + sEnsembleN + '.history')
                            # Save history file for BIN
                            writeFileHistory(sFileCacheBIN_CHECK, zip(a1sFileNameBIN_OUT))
                            
                            #with open(sFileCacheBIN_CHECK, 'wb') as oFile:
                            #    pickle.dump(a1bFileBIN_CHECK, oFile, pickle.HIGHEST_PROTOCOL)
                        else:
                            # Info warning
                            GetException(' ------> WARNING: some files are not saved on disk! Check your data input!', 2, 1)
                        
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
                                                                      '$HH' : sVarHH_NC,'$MM' : sVarMM_NC, '$ENS' : sEnsembleN})
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
                                    oDrvNC_OUT.oFileWorkspace.writeTime(a1oVarTime, 'f8', 'time', dNtl/dNt)
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
                            sFileCacheNC_CHECK = os.path.join(sPathData_CACHE, 'RF_LAMI-I7_FILENC_' + sTimeSave + '_' + sVarName +'.history')
                            # Save history file for NC
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
                        oLogStream.info( ' -----> Save ensemble N: ' + sEnsembleN + ' ... OK')
                        oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTimeSave + ' ...  OK ')
                        #-------------------------------------------------------------------------------------
                
                    else:
                        
                        #-------------------------------------------------------------------------------------
                        # Info
                        oLogStream.info( ' -----> Save ensemble N: ' + sEnsembleN + ' ... OK')
                        oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTimeSave + ' ...  SKIPPED --- FILE SAVE PREVIOUSLY ')
                        #-------------------------------------------------------------------------------------
                        
                    #-------------------------------------------------------------------------------------
                
                # End cycle(s) on variable(s)
                #-------------------------------------------------------------------------------------
                
            # End cycle(s) on ensemble(s)
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
