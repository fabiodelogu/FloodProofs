"""
Class Features

Name:          Cpl_Apps_Radar_DynamicData_RRM_SRI
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151210'
Version:       '1.0.0'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os
import numpy as np

from os.path import join

import src.Lib_Data_Apps as Lib_Data_Apps
import src.Lib_Data_Analysis_Interpolation as Lib_Data_Analysis_Interpolation
import src.Lib_Data_IO_Utils as Lib_Data_IO_Utils

from src.GetException import GetException
from src.Drv_Data_Type import Drv_Data_Type
from src.Drv_Data_IO import Drv_Data_IO
from src.Drv_Data_Zip import Drv_Data_Zip
from src.Lib_Data_IO_Utils import getFileHistory, writeFileHistory

from src.GetTime import convertTimeLOCxGMT, computeTimePeriod, computeJDate

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Cpl_Apps_Radar_DynamicData_RRM_SRI:

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
        # Info
        oLogStream.info( ' ====> CHECK DATA AT TIME: ' + sTime + ' ... ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get path information
        sPathData_CHECK = self.oDataInfo.oInfoSettings.oPathInfo['DataCache']
        
        # Get outcome variable information
        oVarsInfo_CHECK = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic

        # Get time information
        iTimeStep_CHECK = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeStep'])
        iTimeUpd_CHECK = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeUpd'])
        a1oTimeSteps_CHECK = self.oDataTime.a1oTimeSteps
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cache definition
        sTime_CHECK = sTime
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
        oLogStream.info( ' ====> CHECK DATA AT TIME: ' + sTime_CHECK + ' ... ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cycle(s) on type file(s)
        a1sFileAll_CHECK = []
        for sFileType_CHECK in oVarsInfo_CHECK:
            
            #-------------------------------------------------------------------------------------
            # Cycle(s) to check variable(s)
            a2bSaveVar_CHECK = {};
            #-------------------------------------------------------------------------------------
        
            #-------------------------------------------------------------------------------------
            # Cycle(s) on variable name(s)
            for sVarName_CHECK in oVarsInfo_CHECK[sFileType_CHECK]:
                
                #------------------------------------------------------------------------------------- 
                # Check variable component(s)
                if ( oVarsInfo_CHECK[sFileType_CHECK][sVarName_CHECK]['VarOp']['Op_Load']['Comp'].has_key('OUT') ):
                
                    #-------------------------------------------------------------------------------------
                    # Get variable OUT component(s)
                    oVarCompOUT_CHECK = oVarsInfo_CHECK[sFileType_CHECK][sVarName_CHECK]['VarOp']['Op_Load']['Comp']['OUT']
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Cycle(s) on outcome variable(s)
                    for sVarCompOUT_CHECK in oVarCompOUT_CHECK.values():
                        
                        #-------------------------------------------------------------------------------------
                        # Initialize dictionary for each new variable(s)
                        if not sVarCompOUT_CHECK in a2bSaveVar_CHECK:
                            a2bSaveVar_CHECK[sVarCompOUT_CHECK] = {}
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Storage variable checking
                        a1bVarCache_CHECK = []

                        # Check file
                        sFileCache_CHECK = os.path.join(sPathData_CHECK, 'Radar_RRM-SRI_FILENC_' + sTime_CHECK + '_' + sVarCompOUT_CHECK + '.history')
                        bFileCache_CHECK = os.path.isfile(sFileCache_CHECK)
                        
                        # Check file status
                        if bFileCache_CHECK is True:
                            a1sFileName_CHECK = getFileHistory(sFileCache_CHECK)
                            for sFileName_CHECK in a1sFileName_CHECK[0]:
                                
                                bFileName_CHECK = os.path.isfile(sFileName_CHECK)
                                a1sFileAll_CHECK.append(sFileName_CHECK)
                            
                                if bFileName_CHECK is True:
                                    a1bVarCache_CHECK.append(True) 
                                else:
                                    a1bVarCache_CHECK.append(False) 
                        else:
                            a1bVarCache_CHECK.append(False)
                        #-------------------------------------------------------------------------------------
                    
                        #-------------------------------------------------------------------------------------
                        # Final check for each step
                        if np.all(a1bVarCache_CHECK) == True:    
                            a2bSaveVar_CHECK[sVarCompOUT_CHECK] = True
                        else:
                            a2bSaveVar_CHECK[sVarCompOUT_CHECK] = False
                        #-------------------------------------------------------------------------------------
                else:
                    pass
                #-------------------------------------------------------------------------------------
        
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Return check status 
        oLogStream.info( ' ====> CHECK DATA AT TIME: ' + sTime + ' ... OK')
        # Return variable(s)
        self.oVarsInfo_CHECK = a2bSaveVar_CHECK
        self.sPathCache = sPathData_CHECK
        #-------------------------------------------------------------------------------------
        
    #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------  
    # Method to get data 
    def getDynamicData(self, sTime):
                
        #------------------------------------------------------------------------------------- 
        # Get global information 
        oDrv_DataType = Drv_Data_Type(oDataGeo=self.oDataGeo, oDataInfo=self.oDataInfo)
        
        sPathDataSource = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicSource']
        oVarsInfoIN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        oVarsInfoOUT = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic
        oParamsInfo = self.oDataInfo.oInfoSettings.oParamsInfo
        
        oVarsSave = self.oVarsInfo_CHECK
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
        
        # Time information
        sYearLoad = sTimeLoad[0:4]; sMonthLoad = sTimeLoad[4:6]; sDayLoad = sTimeLoad[6:8]; sHHLoad = sTimeLoad[8:10]; sMMLoad = sTimeLoad[10:12];
        sYearSave = sTimeSave[0:4]; sMonthSave = sTimeSave[4:6]; sDaySave = sTimeSave[6:8]; sHHSave = sTimeSave[8:10]; sMMSave = sTimeSave[10:12];
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET DATA AT TIME: ' + sTime + ' ... ')
        #------------------------------------------------------------------------------------- 
        
        #-------------------------------------------------------------------------------------
        # Cycling on variable type definition (input)
        self.oVarData = {}
        for sVarType in oVarsInfoIN:
            
            #------------------------------------------------------------------------------------- 
            # Cycling on variable name definition (input)
            a1oFileDrvIN = {};  a1oDataSelect = {};
            for sVarName in oVarsInfoIN[sVarType]:
                
                oVarInfo = oVarsInfoIN[sVarType][sVarName]
                iVarTimeStep = int(oVarInfo['VarTimeStep'])
                iDataTimeStep = oParamsInfo['TimeStep']
                
                iDataTotalN = iDataTimeStep/iVarTimeStep
                
                oVarCompIN = oVarInfo['VarOp']['Op_Load']['Comp']['IN']
                oVarCompOUT = oVarInfo['VarOp']['Op_Load']['Comp']['OUT']

                if sVarName.lower() in oVarCompIN.values():
                    iVarIndexIN = oVarCompIN.values().index(sVarName.lower())
                    
                    sVarCompOUT = oVarCompOUT.values()[iVarIndexIN]
                    sVarCompIN = oVarCompIN.values()[iVarIndexIN]
                else:
                    GetException(' -----> WARNING: Variable are not defined! Check your settings!', 2, 1)
                    sVarCompOUT = None; sVarCompIN = None;
                
                #-------------------------------------------------------------------------------------
                # Get time period information
                a1oTimeFile = computeTimePeriod(sTimeLoad, iVarTimeStep, iDataTotalN) ### determinare i valori dal file di configurazione
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Cyling on subperiod step(s)
                for sTimeFile in a1oTimeFile:
                    
                    #-------------------------------------------------------------------------------------
                    # Get time information
                    sJDFile = str(computeJDate(sTimeFile)); sJDFile = sJDFile.zfill(3)
                    
                    sYearFile = sTimeFile[0:4]; sMonthFile = sTimeFile[4:6]; sDayFile = sTimeFile[6:8]; 
                    sHHFile = sTimeFile[8:10]; sMMFile = sTimeFile[10:12];
                    #-------------------------------------------------------------------------------------

                    #-------------------------------------------------------------------------------------
                    # Define FileNameIN
                    sFileNameIN = Lib_Data_IO_Utils.defineFileName(join(sPathDataSource, oVarsInfoIN[sVarType][sVarName]['VarSource']), 
                                                             {'$VAR'  : sVarCompIN,
                                                              '$YY' : sYearFile[2:4], '$JD': sJDFile, 
                                                              '$yyyy' : sYearFile, '$mm' : sMonthFile, '$dd' : sDayFile, 
                                                              '$HH' : sHHFile, '$MM' : sMMFile})
                    #------------------------------------------------------------------------------------- 
                    
                    #-------------------------------------------------------------------------------------
                    # File and variable info
                    oLogStream.info( ' -----> Variable: ' + sVarName + ' ... ')
                    oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... ')
                    #-------------------------------------------------------------------------------------

                    #------------------------------------------------------------------------------------- 
                    # Check input file(s) availability
                    bFileExistIN = Lib_Data_IO_Utils.checkFileExist(sFileNameIN)
                    if (bFileExistIN is True) and (oVarsSave[sVarCompOUT] is False):
                         
                        #-------------------------------------------------------------------------------------
                        # Check variable availability
                        if not sFileNameIN in a1oFileDrvIN:
                             
                            # Input file driver
                            a1oFileDrvIN[sFileNameIN] = Drv_Data_IO(sFileNameIN,'r', str.lower(sVarType))
                            # Variable get method
                            oData_GetMethod = getattr(oDrv_DataType, 'getVar' + oVarsInfoIN[sVarType][sVarCompIN]['VarType'])
                            # Get data selection
                            a1oDataSelect[sFileNameIN] = oData_GetMethod(a1oFileDrvIN[sFileNameIN].oFileWorkspace,
                                                                         oVarsInfoIN[sVarType][sVarCompIN]['VarOp'],
                                                                         -9999.0, sTimeLoad, None)
                            # Info
                            oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... OK ')
                        else:
                            pass
                        #-------------------------------------------------------------------------------------
         
                else:
                     
                    #-------------------------------------------------------------------------------------
                    # Exit code(s)
                    if (bFileExistIN is False) and (oVarsSave[sVarCompOUT] is False):
                         
                        #-------------------------------------------------------------------------------------
                        # Exit code(s)
                        oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... SKIPPED --- FILE INPUT NOT FOUND ')
                        oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE NOT FOUND ')
                        GetException(' -----> WARNING: file input is not available!', 2, 1)
                        #-------------------------------------------------------------------------------------
                     
                    elif (bFileExistIN is True) and (oVarsSave[sVarCompOUT] is True):
                         
                        #-------------------------------------------------------------------------------------
                        # Exit code(s)
                        oLogStream.info( ' -----> Opening input file: ' + sFileNameIN + ' ... SKIPPED --- FILE PROCESSED PREVIOUSLY ')
                        oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE SAVED PREVIOUSLY ')
                        #-------------------------------------------------------------------------------------
                         
                #-------------------------------------------------------------------------------------
             
            #-------------------------------------------------------------------------------------
         
        #-------------------------------------------------------------------------------------
        # Info
        oLogStream.info( ' ====> GET DATA AT TIME: ' + sTimeSave + ' ... OK ')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Info start parsering data
        oLogStream.info( ' ====> PARSER DATA AT TIME: ' + sTimeSave + ' ...  ')
        
        # Cycling on variable type definition (input)
        a2oDataWorspace = {}
        for sFormatType in oVarsInfoIN:
            
            #------------------------------------------------------------------------------------- 
            # Cycling on variable name definition (input)
            for sVarName in oVarsInfoIN[sFormatType]:
                
                #-------------------------------------------------------------------------------------
                # Get variable information
                oVarInfo = oVarsInfoIN[sFormatType][sVarName]  
                #-------------------------------------------------------------------------------------
                
                oVarCompIN = oVarInfo['VarOp']['Op_Load']['Comp']['IN']
                oVarCompOUT = oVarInfo['VarOp']['Op_Load']['Comp']['OUT']
                
                if sVarName in oVarCompIN.values():
                    iVarIndexIN = oVarCompIN.values().index(sVarName)
                    sVarCompOUT = oVarCompOUT.values()[iVarIndexIN]
                    sVarCompIN = oVarCompIN.values()[iVarIndexIN]
                else:
                    GetException(' -----> WARNING: Variable are not defined! Check your settings!', 2, 1)
                    sVarCompOUT = None; sVarCompIN = None;
                
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
                    a2dDataCum = np.array([])
                    for sFileName in a1oDataSelect:
                        
                        #-------------------------------------------------------------------------------------
                        # Get data dims
                        iDataStepN = len(a1oDataSelect)
                        
                        if iDataStepN < iDataTotalN:
                            GetException(' -----> WARNING: some data in period are not available!', 2, 1)
                        else:pass
                        
                        # Get data
                        a3dData = a1oDataSelect[sFileName]['Data'][sVarCompIN.lower()]
                        iDimX = a3dData.shape[2]; iDimY = a3dData.shape[1]; iDimT = a3dData.shape[0];
                        a2dData = np.zeros([iDimX, iDimY])
                        for iTime in range(0, iDimT):
                            a2dDataStep = a3dData[iTime,:,:]
                            a2dData = a2dData + a2dDataStep
                        a2dData[a2dData < 0.0] = 0.0
                        a2dData = a2dData*(iVarTimeStep/iDataTimeStep); # from mm/h each 10 min to mm
                        
#                         if not a2dDataCum:
#                             a2dDataCum = np.zeros([iDimX, iDimY])
#                         a2dDataCum = a2dDataCum + a2dData
                        
                        # Get geographical information
                        a1dGeoX = a1oDataSelect[sFileName]['GeoX']
                        a1dGeoX = np.repeat(a1dGeoX, iDimY)
                        a2dGeoX = np.transpose(np.reshape(a1dGeoX, [iDimX, iDimY]))
                        
                        a1dGeoY = a1oDataSelect[sFileName]['GeoY']
                        a1dGeoY = np.repeat(a1dGeoY, iDimY)
                        a2dGeoY = np.flipud(np.reshape(a1dGeoY, [iDimX, iDimY]))
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Store result(s)
                        a2oDataWorspace[sFileName] = {}
                        a2oDataWorspace[sFileName]['Data'] = {}
                        a2oDataWorspace[sFileName]['Data'][sTimeSave] = {}
                        a2oDataWorspace[sFileName]['Data'][sTimeSave][sVarCompIN] = {}
                        a2oDataWorspace[sFileName]['Data'][sTimeSave][sVarCompIN] = a2dData
                        a2oDataWorspace[sFileName]['GeoX'] = {}
                        a2oDataWorspace[sFileName]['GeoX'] = a2dGeoX
                        a2oDataWorspace[sFileName]['GeoY'] = {}
                        a2oDataWorspace[sFileName]['GeoY'] = a2dGeoY
                        a2oDataWorspace[sFileName]['GeoZ'] = None
                        
                        # End parsering data
                        #-------------------------------------------------------------------------------------
                    
                    # End filename(s)
                    #-------------------------------------------------------------------------------------
                    
                else:
                    
                    #-------------------------------------------------------------------------------------
                    # Exit code
                    oLogStream.info( ' -----> Parsering file(s) at time : ' + sTimeSave + ' ... SKIPPED --- DATA INPUT NOT FOUND ')
                    oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE UNDEFINED IN DATA INPUT ')
                    GetException(' -----> WARNING: variable is undefined in data input!', 2, 1)
                    a2oDataWorspace = None
                    #-------------------------------------------------------------------------------------
          
            # End variable name
            #-------------------------------------------------------------------------------------
        
        # End format type
        #-------------------------------------------------------------------------------------
            
        #-------------------------------------------------------------------------------------
        # Info end parsering data
        oLogStream.info( ' ====> PARSER DATA AT TIME: ' + sTimeSave + ' ...  OK')
        
        # Save in global workspace available data dynamic
        self.a2oDataWorspace = a2oDataWorspace
        #-------------------------------------------------------------------------------------
        
        
    #-------------------------------------------------------------------------------------
    # Method to compute data 
    def computeDynamicData(self, sTime):
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> COMPUTE DATA AT TIME: ' + sTime + ' ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get information
        oVarsInfo_IN = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic
        oVarsInfo_OUT = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic
        
        # Get geographical data
        oDataGeo = self.oDataGeo
        # Get variable data
        a2oDataWorspace = self.a2oDataWorspace
        
        # Get time reference information
        sTimeLoad = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefLoad))
        sTimeSave = convertTimeLOCxGMT(sTime, int(self.oDataTime.iTimeRefSave))
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Cycling on data type
        oVarData = {}
        for sVarType in oVarsInfo_IN:
            
            #-------------------------------------------------------------------------------------
            # Get variable IN
            oVarsType_IN = oVarsInfo_IN[sVarType]
            #-------------------------------------------------------------------------------------
            
            #------------------------------------------------------------------------------------- 
            # Cycling on variable name definition
            for sVarName in oVarsType_IN:
                
                #-------------------------------------------------------------------------------------
                # Info
                oLogStream.info( ' -----> Variable: ' + sVarName + ' ... ')
        
                # Get variable component(s)
                oVarNameComp_IN = oVarsType_IN[sVarName]['VarOp']['Op_Load']['Comp']['IN']
                oVarNameComp_OUT = oVarsType_IN[sVarName]['VarOp']['Op_Load']['Comp']['OUT']
                 
                if sVarName in oVarNameComp_IN.values():
                    iVarIndex_IN = oVarNameComp_IN.values().index(sVarName)
                    sVarComp_OUT = oVarNameComp_OUT.values()[iVarIndex_IN]
                    sVarComp_IN = oVarNameComp_IN.values()[iVarIndex_IN]
                else:
                    GetException(' -----> WARNING: Variable are not defined! Check your settings!', 2, 1)
                    sVarComp_OUT = None; sVarComp_IN = None;
                #-------------------------------------------------------------------------------------
                
                #------------------------------------------------------------------------------------- 
                # Check data workspace availability
                if a2oDataWorspace:
                    
                    #------------------------------------------------------------------------------------- 
                    # Get data and compute cumulated variable
                    a2dVarData_CUM = None
                    for sFileName in a2oDataWorspace:
                        
                        # Get data
                        oFileData = a2oDataWorspace[sFileName]
                        a1oVarsData = oFileData['Data']
                        a2dGeoX = oFileData['GeoX']
                        a2dGeoY = oFileData['GeoY']
                        
                        for sFileTime in a1oVarsData:
                            
                            a2dVarData_IN = a1oVarsData[sFileTime][sVarComp_IN]
                            
                            if a2dVarData_CUM == None:
                                a2dVarData_CUM = np.zeros([a2dGeoX.shape[0], a2dGeoY.shape[1]])
                            else:pass
                            a2dVarData_CUM = a2dVarData_CUM + a2dVarData_IN
                    #------------------------------------------------------------------------------------- 
                    
                    #------------------------------------------------------------------------------------- 
                    # Interpolate variable
                    oVarInfo_OUT = oVarsInfo_OUT[sVarType][sVarComp_OUT]
                
                    # Get interpolate method selection
                    oData_InterpMethod = getattr(Lib_Data_Analysis_Interpolation, 
                                         oVarInfo_OUT['VarOp']['Op_Math']['Interpolation']['Func'])

                    oVarData_OUT = oData_InterpMethod(oDataGeo, a2dVarData_CUM, a2dGeoX, a2dGeoY)
                    #------------------------------------------------------------------------------------- 
                    
                    #------------------------------------------------------------------------------------- 
                    # Cycle(s) on variable key(s) and value(s)
                    for sVarKeys_OUT in oVarData_OUT.keys():
                        
                        if sVarKeys_OUT in oVarNameComp_OUT:
                            
                            # Get component variable name
                            sVarName_OUT = oVarNameComp_OUT[sVarKeys_OUT]
                            # Get component variable data
                            a2dVarData_OUT = oVarData_OUT[sVarKeys_OUT]
                            
                            # Initialize dictionary dynamic variable name key
                            if not sVarName_OUT in oVarData:
                                oVarData[sVarName_OUT] = {}
                                
                            # Initialize dictionary dynamic time key
                            if not sTimeSave in oVarData[sVarName_OUT]:
                                oVarData[sVarName_OUT][sTimeSave] = {}
                            
                            # Debug
                            #plt.figure(1)
                            #plt.imshow(a2dVarData_CUM); plt.colorbar()
                            #plt.figure(2)
                            #plt.imshow(a2dVarData_OUT)
                            #plt.show()
                            
                            print(sVarName_OUT)
                            
                            oVarData[sVarName_OUT][sTimeSave] = a2dVarData_OUT
                            
                        else:
                            pass

                    # Info
                    oLogStream.info( ' -----> Variable: ' + sVarName + ' ... OK')    
                    #------------------------------------------------------------------------------------- 
                
                else:
                    
                    #-------------------------------------------------------------------------------------
                    # Exit code
                    oLogStream.info( ' -----> Variable: ' + sVarName + ' ... SKIPPED --- VARIABLE UNDEFINED IN INPUT FILE ')
                    GetException(' -----> WARNING: variable is undefined in data!', 2, 1)
                    #-------------------------------------------------------------------------------------
                    
                #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
                
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> COMPUTE DATA AT TIME: ' + sTime + ' ... OK ')
        self.oData_OUT = oVarData
        #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to save data
    def saveDynamicData(self, sTime):
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTime + ' ...  ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get information
        sPathData_OUT = self.oDataInfo.oInfoSettings.oPathInfo['DataDynamicOutcome']
        sPathCache_OUT = self.sPathCache
        
        oVarsInfo_OUT = self.oDataInfo.oInfoVarDynamic.oDataOutputDynamic
        oVarsData_OUT = self.oData_OUT
        
        # Get domain name
        sDomainName_OUT = self.oDataInfo.oInfoSettings.oParamsInfo['DomainName']
        #------------------------------------------------------------------------------------- 

        #------------------------------------------------------------------------------------- 
        # Check workspace field(s)
        if np.any(oVarsData_OUT):
            
            #-------------------------------------------------------------------------------------
            # Cycle(s) on get var name
            for sVarName_OUT in oVarsData_OUT:
            
                #-------------------------------------------------------------------------------------
                # Info variable name
                oLogStream.info( ' -----> Save variable: ' + sVarName_OUT + ' ... ')
                #-------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Time information
                sVarTime_OUT = sTime
                sVarYear_OUT = sVarTime_OUT[0:4]; sVarMonth_OUT = sVarTime_OUT[4:6]; sVarDay_OUT = sVarTime_OUT[6:8];
                sVarHH_OUT = sVarTime_OUT[8:10]; sVarMM_OUT = sVarTime_OUT[10:12];

                # Pathname NC OUT
                sPathName_OUT = Lib_Data_IO_Utils.defineFolderName(sPathData_OUT,
                                                             {'$yyyy' : sVarYear_OUT,'$mm' : sVarMonth_OUT,'$dd' : sVarDay_OUT, 
                                                              '$HH' : sVarHH_OUT,'$MM' : sVarMM_OUT})
                # Time Info
                oLogStream.info( ' ------> Save time step (NC): ' + sVarTime_OUT)
                #------------------------------------------------------------------------------------- 
                
                #-------------------------------------------------------------------------------------
                # Get data
                a2VarData_OUT = oVarsData_OUT[sVarName_OUT][sVarTime_OUT]
                a2VarData_OUT[self.oDataGeo.a2bGeoDataNan] = self.oDataGeo.dNoData
                iVarLen_OUT = 1
                # Save time information (for loading and saving function)
                a1oVarTime_OUT = []; a1oVarTime_OUT.append(sVarTime_OUT)
                #-------------------------------------------------------------------------------------
                
                #------------------------------------------------------------------------------------- 
                # Filename NC OUT
                sFileName_OUT = Lib_Data_IO_Utils.defineFileName(join(sPathName_OUT, oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarSource']), 
                                                         {'$yyyy' : sVarYear_OUT,'$mm' : sVarMonth_OUT,'$dd' : sVarDay_OUT, 
                                                          '$HH' : sVarHH_OUT,'$MM' : sVarMM_OUT})
                
                # Check output file(s) availability 
                bFileExist_OUT = Lib_Data_IO_Utils.checkFileExist(sFileName_OUT + '.' + 
                                                                    oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Zip'])
                
                # Info
                oLogStream.info( ' -------> Saving file output (NC): ' + sFileName_OUT + ' ... ')
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Check errors in code
                a1bFileCheck_OUT = []; a1sFileName_OUT = []
                try:
                    
                    #-------------------------------------------------------------------------------------
                    # Open NC file (in write or append mode)
                    bVarExist_OUT = False;
                    if bFileExist_OUT is False:
                        
                        #-------------------------------------------------------------------------------------
                        # Open NC file in write mode
                        oDrv_OUT = Drv_Data_IO(sFileName_OUT, 'w')
                        bVarExist_OUT = False;
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Write global attributes (common and extra)
                        oDrv_OUT.oFileWorkspace.writeFileAttrsCommon(self.oDataInfo.oInfoSettings.oGeneralInfo)
                        oDrv_OUT.oFileWorkspace.writeFileAttrsExtra(self.oDataInfo.oInfoSettings.oParamsInfo,
                                                                       self.oDataGeo.a1oGeoInfo)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Write geo-system information
                        oDrv_OUT.oFileWorkspace.writeGeoSystem(self.oDataInfo.oInfoSettings.oGeoSystemInfo, 
                                                                  self.oDataGeo.oGeoData.a1dGeoBox)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Declare variable dimensions
                        sDimVarX = oVarsInfo_OUT['NetCDF']['Terrain']['VarDims']['X']
                        oDrv_OUT.oFileWorkspace.writeDims(sDimVarX, self.oDataGeo.oGeoData.iCols)
                        sDimVarY = oVarsInfo_OUT['NetCDF']['Terrain']['VarDims']['Y']
                        oDrv_OUT.oFileWorkspace.writeDims(sDimVarY, self.oDataGeo.oGeoData.iRows)
                        sDimVarT = 'time'; 
                        oDrv_OUT.oFileWorkspace.writeDims(sDimVarT, iVarLen_OUT)
                        # Declare extra dimension(s)
                        oDrv_OUT.oFileWorkspace.writeDims('nsim', 1)
                        oDrv_OUT.oFileWorkspace.writeDims('ntime', 2)
                        oDrv_OUT.oFileWorkspace.writeDims('nens', 1)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Write time information
                        oDrv_OUT.oFileWorkspace.writeTime(a1oVarTime_OUT, 'f8', 'time', iVarLen_OUT/iVarLen_OUT)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Try to save longitude
                        sVarGeoX = 'Longitude'
                        oLogStream.info( ' -------> Saving variable: ' + sVarGeoX + ' ... ')
                        try:

                            #-------------------------------------------------------------------------------------
                            # Get longitude
                            oDrvNC_WriteMethod = getattr(oDrv_OUT.oFileWorkspace,  
                                                         oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarOp']['Op_Save']['Func'])
                            oDrvNC_WriteMethod(sVarGeoX, self.oDataGeo.oGeoData.a2dGeoX, 
                                               oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarAttributes'], 
                                               oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarOp']['Op_Save']['Format'], 
                                               oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarDims']['Y'], 
                                               oVarsInfo_OUT['NetCDF'][sVarGeoX]['VarDims']['X'])
                            # Info
                            a1bFileCheck_OUT.append(True)
                            oLogStream.info( ' -------> Saving variable: ' + sVarGeoX + ' ... OK ')
                            #-------------------------------------------------------------------------------------
                        
                        except:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            a1bFileCheck_OUT.append(False)
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
                            oDrvNC_WriteMethod = getattr(oDrv_OUT.oFileWorkspace,  
                                                         oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarOp']['Op_Save']['Func'])
                            oDrvNC_WriteMethod(sVarGeoY, self.oDataGeo.oGeoData.a2dGeoY, 
                                               oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarAttributes'], 
                                               oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarOp']['Op_Save']['Format'], 
                                               oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarDims']['Y'], 
                                               oVarsInfo_OUT['NetCDF'][sVarGeoY]['VarDims']['X'])
                            # Info
                            a1bFileCheck_OUT.append(True)
                            oLogStream.info( ' -------> Saving variable: ' + sVarGeoY + ' ... OK ')
                            #-------------------------------------------------------------------------------------
                        
                        except:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            a1bFileCheck_OUT.append(False)
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
                             
                            oDrvNC_WriteMethod = getattr(oDrv_OUT.oFileWorkspace, 
                                                         oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarOp']['Op_Save']['Func'])
                            oDrvNC_WriteMethod(sVarTerrain, a2dData, 
                                               oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarAttributes'],
                                               oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarOp']['Op_Save']['Format'], 
                                               oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarDims']['Y'], 
                                               oVarsInfo_OUT['NetCDF'][sVarTerrain]['VarDims']['X'])
                            # Info
                            a1bFileCheck_OUT.append(True)
                            oLogStream.info( ' -------> Saving variable: ' + sVarTerrain + ' ... OK ')
                            #-------------------------------------------------------------------------------------
                        
                        except:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            a1bFileCheck_OUT.append(False)
                            GetException(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                            oLogStream.info( ' -------> Saving variable: ' + sVarTerrain + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                            #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Try to save 3d variable
                        oLogStream.info( ' -------> Saving variable: ' + sVarName_OUT + ' ... ')
                        try:
                        
                            #-------------------------------------------------------------------------------------
                            # Get data dynamic
                            oDrvNC_WriteMethod = getattr(oDrv_OUT.oFileWorkspace, 
                                                         oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Func'])
                            oDrvNC_WriteMethod(sVarName_OUT, a2VarData_OUT, 
                                               oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarAttributes'], 
                                               oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Format'],
                                               oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarDims']['Y'], 
                                               oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarDims']['X'])
                        
                            # Info
                            a1bFileCheck_OUT.append(True)
                            oLogStream.info( ' -------> Saving variable: ' + sVarName_OUT + ' ... OK ')
                            #-------------------------------------------------------------------------------------
                        
                        except:
                            
                            #-------------------------------------------------------------------------------------
                            # Exit code
                            a1bFileCheck_OUT.append(False)
                            GetException(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                            oLogStream.info( ' -------> Saving variable: ' + sVarName_OUT + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                            #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Close NetCDF file
                        oDrv_OUT.oFileWorkspace.closeFile()
                        
                        # Zip file
                        Drv_Data_Zip(sFileName_OUT, 
                                     'z', 
                                     oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Zip'], 
                                     True)
                        
                        # Info
                        a1sFileName_OUT.append(sFileName_OUT + '.' + oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Zip'])
                        oLogStream.info( ' ------> Saving file output NetCDF: ' + sFileName_OUT + ' ... OK')
                        #-------------------------------------------------------------------------------------
                        
                    else:
                        
                        #-------------------------------------------------------------------------------------
                        # Unzip NC file (if file is compressed)
                        Drv_Data_Zip(sFileName_OUT + '.' +  oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Zip'],
                                     'u', 
                                     oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Zip'], 
                                     True)
                        
                        # Open NC file in append mode
                        oDrv_OUT = Drv_Data_IO(sFileName_OUT, 'a')
                        bVarExistNC_OUT = oDrv_OUT.oFileWorkspace.checkVarName(sVarName_OUT)
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Check variable availability
                        oLogStream.info( ' -------> Saving variable: ' + sVarName_OUT + ' ... ')
                        if bVarExistNC_OUT is False:
                        
                            #-------------------------------------------------------------------------------------
                            # Try to save 3d variable
                            try:
                            
                                #-------------------------------------------------------------------------------------
                                # Get data dynamic
                                oDrvNC_WriteMethod = getattr(oDrv_OUT.oFileWorkspace, 
                                                             oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Func'])
                                oDrvNC_WriteMethod(sVarName_OUT, a2VarData_OUT,  
                                                   oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarAttributes'], 
                                                   oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Format'], 
                                                   oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarDims']['Y'], 
                                                   oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarDims']['X'])
                            
                                # Info
                                a1bFileCheck_OUT.append(True)
                                oLogStream.info( ' -------> Saving variable: ' + sVarName_OUT + ' ... OK ')
                                #-------------------------------------------------------------------------------------
                            
                            except:
                                
                                #-------------------------------------------------------------------------------------
                                # Exit code
                                a1bFileCheck_OUT.append(False)
                                GetException(' -----> WARNING: variable not found in outcome workspace!', 2, 1)
                                oLogStream.info( ' -------> Saving variable: ' + sVarName_OUT + ' ... FAILED --- VARIABLE NOT FOUND IN OUTCOME WORKSPACE ')
                                #-------------------------------------------------------------------------------------
                            
                            #-------------------------------------------------------------------------------------
                        
                        else:
                            #-------------------------------------------------------------------------------------
                            # Info
                            oLogStream.info( ' -------> Saving variable: ' + sVarName_OUT + ' ... SAVED PREVIOUSLY')
                            a1bFileCheck_OUT.append(True)
                            #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        
                        #-------------------------------------------------------------------------------------
                        # Close NetCDF file
                        oDrv_OUT.oFileWorkspace.closeFile()
                        
                        # Zip file
                        Drv_Data_Zip(sFileName_OUT, 
                                     'z', 
                                     oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Zip'], 
                                     True)
                        
                        # Info
                        a1sFileName_OUT.append(sFileName_OUT + '.' + oVarsInfo_OUT['NetCDF'][sVarName_OUT]['VarOp']['Op_Save']['Zip'])
                        oLogStream.info( ' ------> Saving file output NetCDF: ' + sFileName_OUT + ' ... OK')
                        #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                        
                except:
                    
                    #-------------------------------------------------------------------------------------
                    # Exit code
                    a1bFileCheck_OUT.append(False)
                    # Info
                    GetException(' ------> WARNING: errors occurred in saving file! Check your output data!', 2, 1)
                    oLogStream.info( ' ------> Saving file output (NC): ' + sFileName_OUT + ' ... FAILED --- ERRORS OCCURRED IN SAVING DATA!')
                    #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Check saved data NC
                if np.all(np.asarray(a1bFileCheck_OUT) == True ):
                    # Create hash handle
                    sFileCache_OUT = os.path.join(sPathCache_OUT, 'Radar_RRM-SRI_FILENC_' + sVarTime_OUT + '_' + sVarName_OUT +'.history')
                    
                    # Adding filename(s) IN
                    for sFileName_IN in sorted(self.a2oDataWorspace): a1sFileName_OUT.append(sFileName_IN)
                    
                    # Save hystory file for NC
                    writeFileHistory(sFileCache_OUT, zip(a1sFileName_OUT))
                else:
                    # Info warning
                    GetException(' ------> WARNING: some files are not saved on disk! Check your data input!', 2, 1)
                
                # SAVE DATA IN NC FORMAT (END)
                #-------------------------------------------------------------------------------------
                
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Info
            oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTime + ' ...  OK ')
            #-------------------------------------------------------------------------------------
            
        else:
            
            #-------------------------------------------------------------------------------------
            # Info
            oLogStream.info( ' ====> SAVE DATA AT TIME: ' + sTime + ' ...  SKIPPED - All data are empty! Check your input files!')
            #-------------------------------------------------------------------------------------
        
        
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------
    
