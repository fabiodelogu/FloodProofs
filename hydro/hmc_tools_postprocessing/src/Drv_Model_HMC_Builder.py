"""
Class Features

Name:          Drv_Model_HMC_Builder
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151022'
Version:       '1.6.2'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os, csv, pickle
import datetime
import subprocess
import numpy as np

from os.path import join
from os.path import isfile
from os.path import split

import Lib_Data_IO_Utils as Lib_Data_IO_Utils
from Lib_Data_IO_Utils import getFileHistory, writeFileHistory

from Drv_Data_IO import Drv_Data_IO
from Drv_Model_HMC_IO import Drv_Model_HMC_IO

from GetGeoData import GetGeoData
from GetException import GetException

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Drv_Model_HMC_Builder:

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, sDomainName, sRunName, oDataInfo, oDataTime, sEnsembleName):
        
        # Global variable(s)
        self.sDomainName = sDomainName
        self.sRunName = sRunName
        self.oDataInfo = oDataInfo
        self.oDataTime = oDataTime
        
        self.sEnsembleName = sEnsembleName
        
    #-------------------------------------------------------------------------------------  
    
    #------------------------------------------------------------------------------------- 
    # Method to define run tags
    def defineRunTags(self):
    
        # Create tags dictionary
        oTagsDict = {}
        oTagsDict['$UC'] = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']['uc']
        oTagsDict['$UH'] = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']['uh']
        oTagsDict['$CT'] = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']['ct']
        oTagsDict['$CF'] = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']['cf']
        oTagsDict['$CPI'] = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']['cpi']
        oTagsDict['$VMAX'] = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']['vmax']
        oTagsDict['$SLOPEMAX'] = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']['slopemax']
        oTagsDict['$RF'] = self.oDataInfo.oInfoSettings.oParamsInfo['RunParams']['rf']
        oTagsDict['$RUN'] = self.sRunName       # Run name
        oTagsDict['$DOMAIN'] = self.sDomainName # Domain name
        oTagsDict['$TYPE'] = self.sEnsembleName  # Deterministic = '' or Ensemble member ID = xxx
        oTagsDict['$FILEEXEC'] = Lib_Data_IO_Utils.defineString(
                                    self.oDataInfo.oInfoSettings.oParamsInfo['FileExecName'],
                                    oTagsDict)
        
        self.oRunTags = oTagsDict
    #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------
    # Method to define run type
    def defineRunName(self):
        
        #-------------------------------------------------------------------------------------
        # Get parameter(s)
        sRunCommand = self.oDataInfo.oInfoSettings.oParamsInfo['RunCommand']

        # Get path(s)
        sPathRun = self.oDataInfo.oInfoSettings.oPathInfo['Run']
        sPathLib = self.oDataInfo.oInfoSettings.oPathInfo['Library']

        sPathCache = self.oDataInfo.oInfoSettings.oPathInfo['DataCache']
        sPathTemp = self.oDataInfo.oInfoSettings.oPathInfo['DataTemp']
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Update run command
        sRunCommand = Lib_Data_IO_Utils.defineString(sRunCommand, self.oRunTags)
        self.oDataInfo.oInfoSettings.oParamsInfo['RunCommand'] = sRunCommand
        
        # Update path library
        sPathLib = Lib_Data_IO_Utils.defineString(sPathLib, self.oRunTags)
        self.oDataInfo.oInfoSettings.oPathInfo['Library'] = sPathLib
        
        # Update path run
        sPathRun = Lib_Data_IO_Utils.defineString(sPathRun, self.oRunTags)
        self.oDataInfo.oInfoSettings.oPathInfo['Run'] = sPathRun
        
        # Update path cache
        sPathCache = Lib_Data_IO_Utils.defineString(sPathCache, self.oRunTags)
        self.oDataInfo.oInfoSettings.oPathInfo['DataCache'] = sPathCache
        
        # Update path temp
        sPathTemp = Lib_Data_IO_Utils.defineString(sPathTemp, self.oRunTags)
        self.oDataInfo.oInfoSettings.oPathInfo['DataTemp'] = sPathTemp
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to define run time
    def defineRunTimeNow(self):
        
        #-------------------------------------------------------------------------------------
        # Get parameter(s)
        sTimeNow_PARAMS = self.oDataInfo.oInfoSettings.oParamsInfo['TimeNow']
        sTimeNow_DEFINED = self.oDataTime.sTimeNow
        
        oLogStream.info( ' -----> Select time now ... ')
        
        if sTimeNow_PARAMS == '':
            oLogStream.info( ' ------> Updating time now (realtime mode) ... ')
            self.oDataInfo.oInfoSettings.oParamsInfo['TimeNow'] = sTimeNow_DEFINED
            oLogStream.info( ' ------> Updating time now (realtime mode) ... OK')
            oLogStream.info( ' -----> Select time now ... OK')
        elif sTimeNow_PARAMS == sTimeNow_DEFINED:
            oLogStream.info( ' ------> Updating time now (history mode) ... OK')
            oLogStream.info( ' -----> Select time now ... OK')
        else:
            oLogStream.info( ' -----> Select time now ... FAILED')
            GetException(' -----> ERROR: time now ambiguous! Change value in info settings!',1,1)
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to select restart time run
    def selectTimeRestart(self):
        
        # Info
        oLogStream.info( ' -----> Select time restart ... ')
        
        # Get time restart settings
        oTimeRestartSettings = self.oDataInfo.oInfoSettings.oParamsInfo['TimeRestart']
        iTimePeriodObs = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimePeriodObs'])
        iTimeStep = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeStep'])
        iTimeRestartFlag = int(self.oDataInfo.oInfoSettings.oParamsInfo['RunFlag']['flag_restart'])
        
        # Get time information
        oTimeNow = self.oDataTime.oTimeNow;
        oTimeFrom = self.oDataTime.oTimeFrom; oTimeTo = self.oDataTime.oTimeTo;
        
        # Check restart flag
        if iTimeRestartFlag == 1:
            
            # Info
            oLogStream.info( ' -----> Select time restart ... ACTIVATED')
            
            # Check timeday and timehh
            if oTimeRestartSettings['TimeDay'] and oTimeRestartSettings['TimeHH']:
                
                if oTimeRestartSettings['TimeDay'] > 0:
                    GetException(' -----> ERROR: time day must be negative or zero! Change value in info settings!',1,1)
                else:
                    pass
                
                # Get time restart starting from time now
                oTimeRestart = oTimeNow
                oTimeRestart = oTimeRestart.replace(hour = int(oTimeRestartSettings['TimeHH']), 
                                                    minute = 0, second = 0, microsecond = 0)
                # Compute time restart for oTimeRestartSettings['TimeDay'] (<0)
                oTimeRestart = oTimeRestart + datetime.timedelta(seconds = int(oTimeRestartSettings['TimeDay'])*24*iTimeStep)
                
                if oTimeRestart > oTimeFrom:
                    
                    oTimeRestart = oTimeFrom.replace(hour = int(oTimeRestartSettings['TimeHH']), 
                                                     minute = 0, second = 0, microsecond = 0)
                    oTimeFrom = oTimeRestart
                    
                elif oTimeRestart < oTimeFrom:
                    oTimeFrom = oTimeRestart
                else:
                    pass
                
                # Update time steps list
                oTimeStep = oTimeFrom
                oTimeDelta = datetime.timedelta(seconds = iTimeStep)
                
                a1oTimeStepsUpd = []
                while oTimeStep <= oTimeTo:
                    a1oTimeStepsUpd.append(oTimeStep.strftime('%Y%m%d%H%M'))
                    oTimeStep += oTimeDelta
                    
            else:
                # Set time restart equal to time from
                oTimeRestart = oTimeFrom
                a1oTimeStepsUpd = self.oDataTime.a1oTimeSteps

        else:
            
            # Info
            oLogStream.info( ' -----> Select time restart ... NOT ACTIVATED!')
            oLogStream.info( ' ------> Restart time based on time now and time observed steps!')
            oTimeRestart = oTimeFrom
            a1oTimeStepsUpd = self.oDataTime.a1oTimeSteps
        
        # Info restart time
        oLogStream.info( ' -----> Restart time : ' + str(oTimeRestart.strftime('%Y%m%d%H%M')) )
        
        # Save time restart information
        self.oDataTime.oTimeRestart = oTimeRestart
        self.oDataTime.oTimeFrom = oTimeFrom
        self.oDataTime.a1oTimeSteps = a1oTimeStepsUpd

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to define corrivation time model
    def computeTc(self):
        
        #-------------------------------------------------------------------------------------
        # Check static data availability
        if self.oDataStatic:
        
            #-------------------------------------------------------------------------------------
            # Get Info
            a2dGeoZ = self.oDataStatic['GeoZ']
            a2dGeoX = self.oDataStatic['GeoX']; a2dGeoY = self.oDataStatic['GeoY']
            dGeoXCellSize = float(self.oDataStatic['GeoInfo']['GeoRef']['cellsize'])
            dGeoYCellSize = float(self.oDataStatic['GeoInfo']['GeoRef']['cellsize'])
            dGeoNODATA = float(self.oDataStatic['GeoInfo']['GeoRef']['NODATA_value'])
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Dynamic values (NEW)
            dR = 6378388        # (Radius)
            dE = 0.00672267     # (Ellipsoid)
            
            # dx = (R * cos(lat)) / (sqrt(1 - e2 * sqr(sin(lat)))) * PI / 180
            a2dDX = ( dR*np.cos( a2dGeoY*np.pi/180 ) )/(np.sqrt(1 - dE*np.sqrt(np.sin( a2dGeoY*np.pi/180 ))))*np.pi/180                                 
            # dy = (R * (1 - e2)) / pow((1 - e2 * sqr(sin(lat))),1.5) * PI / 180
            a2dDY = ( dR*(1 - dE) )/ np.power((1 - dE*np.sqrt(np.sin( a2dGeoY/180) )), 1.5 )*np.pi/180
            
            a2dGeoAreaKm = ((a2dDX/(1/dGeoXCellSize)) * (a2dDY/(1/dGeoYCellSize))) / 1000000 # [km^2]
            a2dGeoAreaM = ((a2dDX/(1/dGeoXCellSize)) * (a2dDY/(1/dGeoYCellSize))) # [m^2]
            
            # Area, Mean Dx and Dy values (meters)
            dGeoDxMean = np.sqrt(np.nanmean(a2dGeoAreaM)); 
            dGeoDyMean = np.sqrt(np.nanmean(a2dGeoAreaM));

            # Compute domain pixels and area
            iGeoPixels = np.sum((a2dGeoZ != dGeoNODATA))
            dGeoArea = float(iGeoPixels)*dGeoDxMean*dGeoDyMean/1000000 
            
            # Concentration time [hour]
            iGeoTc = np.int(0.27*np.sqrt(0.6*dGeoArea) + 0.25)
            
            # Pass value to global workspace
            self.iTc = iGeoTc
            #-------------------------------------------------------------------------------------

        else:
            #-------------------------------------------------------------------------------------
            # Exit if static data is not available
            GetException(' -----> WARNING: concentration time not evaluated! Check your static data!',2,1)
            self.iTc = 0
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to select file model executable
    def defineFileExec(self):
        
        # Import library
        import shutil
        
        # Info
        oLogStream.info( ' -----> Executable file definition ... ')
        
        # Get information
        sPathLibraryRaw = self.oDataInfo.oInfoSettings.oPathInfo['Library']
        sPathRunRaw = self.oDataInfo.oInfoSettings.oPathInfo['Run']
        sFileNameExecRaw = self.oDataInfo.oInfoSettings.oParamsInfo['FileExecName']

        # Define path(s) and executable(s)
        sPathLibrary = Lib_Data_IO_Utils.defineString(sPathLibraryRaw, self.oRunTags)
        sPathRun = Lib_Data_IO_Utils.defineString(sPathRunRaw, self.oRunTags)
        sFileNameExec = Lib_Data_IO_Utils.defineString(sFileNameExecRaw, self.oRunTags)
        
        # Copy executable file from library to run folder
        if isfile(join(sPathLibrary, sFileNameExecRaw)):
            
            if isfile(join(sPathRun,sFileNameExec)):
                os.remove(join(sPathRun,sFileNameExec))
            else:
                pass
            # Info
            oLogStream.info( ' -----> Copy executable file from source to run folder ... ')
            shutil.copy(join(sPathLibrary, sFileNameExecRaw), join(sPathRun,sFileNameExec))
            oLogStream.info( ' -----> Copy executable file from source to run folder ... OK')
        else:
            # Info
            oLogStream.info( ' -----> Executable file definition ... FAILED! ')
            GetException(' -----> ERROR: run file raw not available in library folder! Check your library folder!',1,1)
        
        # Check file availability in folder run
        if not isfile(join(sPathLibrary, sFileNameExecRaw)):
            # Info
            oLogStream.info( ' -----> Executable file definition ... FAILED! ')
            GetException(' -----> ERROR: run file raw not copied in run folder! Check your library and run folder(s)!',1,1)
        else:
            # Update executable name in workspace
            self.oDataInfo.oInfoSettings.oParamsInfo['FileExecName'] = sFileNameExec
            # Info
            oLogStream.info( ' -----> Executable file definition ... OK ')
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to define file info
    def defineFileStaticInfo(self):
        
        # Import library
        import shutil
        
        # Info
        oLogStream.info( ' -----> Info file definition ... ')
        
        # Get information
        sPathRunRaw = self.oDataInfo.oInfoSettings.oPathInfo['Run']
        sFilePathRaw = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Info']['FilePath']
        sFileNameRaw = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Info']['FileName']
        
        # Define path(s) and executable(s)
        sPathRun = Lib_Data_IO_Utils.defineString(sPathRunRaw, self.oRunTags)
        sFilePath = Lib_Data_IO_Utils.defineString(sFilePathRaw, self.oRunTags)
        sFileName = Lib_Data_IO_Utils.defineString(sFileNameRaw, self.oRunTags)
        
        # Create run folder
        Lib_Data_IO_Utils.createFolder(sPathRun)
        
        # Copy executable file from library to run folder
        if isfile(join(sFilePath, sFileNameRaw)):
            
            if isfile(join(sPathRun,sFileName)):
                os.remove(join(sPathRun,sFileName))
            else:
                pass
            oLogStream.info( ' -----> Copy info file from source to run folder ... ')
            shutil.copy(join(sFilePath, sFileNameRaw), join(sPathRun,sFileName))
            oLogStream.info( ' -----> Copy info file from source to run folder ... OK')
        else:
            # Info
            oLogStream.info( ' -----> Info file definition ... FAILED')
            GetException(' -----> ERROR: info file raw not available in static info folder! Check your info folder!',1,1)
        
        # Check file availability in folder run
        if not isfile(join(sPathRun, sFileName)):
            # Info
            oLogStream.info( ' -----> Info file definition ... FAILED')
            GetException(' -----> ERROR: info file raw not copied in run folder! Check your info and run folder(s)!',1,1)
  
        else:
            # Update executable name in workspace
            self.oDataInfo.oInfoVarStatic.oDataInputStatic['Info']['FilePath'] = sPathRun # copy in run folder
            self.oDataInfo.oInfoVarStatic.oDataInputStatic['Info']['FileName'] = sFileName
            # Info
            oLogStream.info( ' -----> Info file definition ... OK')

    #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    # Method to define info file
    def getFileStaticInfo(self):
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET AND UPDATE FILE INFO ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get variable(s) information
        sPathRun = self.oDataInfo.oInfoSettings.oPathInfo['Run']
        sFilePath = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Info']['FilePath']
        sFileName = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Info']['FileName']
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Define filename
        sFileName = Lib_Data_IO_Utils.defineString(join(sFilePath, sFileName), self.oRunTags)
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Open file
        oFileDrv = Drv_Model_HMC_IO(sFileName, self.oDataInfo)
        
        # Get data from file
        oFileDataDefault = oFileDrv.getInfoData()['Data']

        # Update info file fields -- NB: file history must be in folder because previously created by dynamic gridded data subroutine
        oFileKeysUpd = oFileDrv.updateInfoData(self.oDataInfo, self.oDataTime, 
                                               self.oDataStatic, self.oRunTags, 
                                               getFileHistory(self.sFileHistory_NOW)[0]) 

        # Update info file data
        oFileDataUpd = oFileDrv.parseInfoData(oFileDataDefault, oFileKeysUpd)
        
        # Info
        oLogStream.info( ' ====> GET AND UPDATE FILE INFO ... OK')
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Save file in run path
        oLogStream.info( ' ====> SAVE FILE INFO ... ')
        oFileDrv.saveInfoData(join(sPathRun, split(sFileName)[1]), oFileDataUpd)
        oLogStream.info( ' ====> SAVE FILE INFO ... OK')
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to select static point file(s) 
    def getFileStaticPoint(self):
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET STATIC POINT FILE(S) ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get variable(s) information
        oFileVars = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FileVars']
        sFilePath = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FilePath']
        sFileName = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FileName']
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Cycling on name variable(s)
        for sVarKey, sVarName in oFileVars.items():
            
            #------------------------------------------------------------------------------------- 
            # Update run tags
            oRunTags = Lib_Data_IO_Utils.joinDict(self.oRunTags, {'$VAR' : sVarName})
            #------------------------------------------------------------------------------------- 
            
            #------------------------------------------------------------------------------------- 
            # Define file name 
            sFileNameVar = Lib_Data_IO_Utils.defineString(join(sFilePath, sFileName), oRunTags)
            
            # Initialize data driver
            oFileDrv = Drv_Model_HMC_IO(sFileNameVar, self.oDataInfo)
            
            # Check var availability
            bVarExist = oFileDrv.checkStaticVar(sVarName)
            if bVarExist is True:
                pass
            else:
                GetException(' -----> WARNING: variable point name not found! (VarName: ' + sVarName + ')',2,1)
                GetException(' -----> WARNING: file reference: ' + sFileNameVar,2,1)
            #------------------------------------------------------------------------------------- 
            
        #------------------------------------------------------------------------------------- 
            
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET STATIC POINT FILE(S) ... OK')
        #------------------------------------------------------------------------------------- 

    #------------------------------------------------------------------------------------- 
    
    #------------------------------------------------------------------------------------- 
    # Method to select static gridded file(s)
    def getFileStaticGridded(self):
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET STATIC GRIDDED FILE(S) ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get variable(s) information
        oFileVars = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Gridded']['FileVars']
        sFilePath = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Gridded']['FilePath']
        sFileName = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Gridded']['FileName']
        #------------------------------------------------------------------------------------- 

        #------------------------------------------------------------------------------------- 
        # Cycling on name variable(s)
        oDataStatic = None
        for sVarKey, sVarName in oFileVars.items():
            
            #------------------------------------------------------------------------------------- 
            # Update run tags
            oRunTags = Lib_Data_IO_Utils.joinDict(self.oRunTags, {'$VAR' : sVarName})
            #------------------------------------------------------------------------------------- 

            #------------------------------------------------------------------------------------- 
            # Define file name 
            sFileNameVar = Lib_Data_IO_Utils.defineString(join(sFilePath, sFileName), oRunTags)
            
            # Initialize data driver
            oFileDrv = Drv_Model_HMC_IO(sFileNameVar, self.oDataInfo)
            
            # Check variable availability
            bVarExist = oFileDrv.checkStaticVar(sVarName)
            
            # Availability condition
            if bVarExist is True:
            
                # Check terrain variable
                if (sVarKey == 'terrain'):
                    
                    # Get static data
                    oDataStatic = oFileDrv.getStaticData()
                    # Return data 
                    self.oDataStatic = oDataStatic
                    
                else:
                    pass
            else:
                GetException(' -----> WARNING: variable gridded name not found! (VarName: ' + sVarName + ')',2,1)
                GetException(' -----> WARNING: file reference: ' + sFileNameVar,2,1)
            #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Check data static workspace
        if not oDataStatic:
            GetException(' -----> ERROR: Terrain or DEM data not found! Check your static input file(s)!',1,1)

        # Info
        oLogStream.info( ' ====> GET STATIC GRIDDED FILE(S) ... OK')
        #------------------------------------------------------------------------------------- 
        
    #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------
    # Method to select input point file(s)
    def getFileDynamicPoint(self):
        
        pass
        
    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to select data type
    def selectUpdDynamicGridded(self):
        
        #------------------------------------------------------------------------------------- 
        # Get cache folder
        sPathCache = self.oDataInfo.oInfoSettings.oPathInfo['DataCache']
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get run initialization code (0 or 1)
        iRunInit = int(self.oDataInfo.oInfoSettings.oParamsInfo['RunInit'])
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get variable information
        oVarsDynamic_OBS = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded']['OBS']
        oVarsDynamic_FOR = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded']['FOR']
        
        iVarRes_OBS = int(oVarsDynamic_OBS['VarResolution'])
        iVarStep_OBS = int(oVarsDynamic_OBS['VarStep'])
        
        iVarRes_FOR = int(oVarsDynamic_FOR['VarResolution'])
        iVarStep_FOR = int(oVarsDynamic_FOR['VarStep'])
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get time steps
        a1oTimeData_ALL = self.oTimeData
        a1oTimeStep_ALL = sorted(self.oTimeData.keys())
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get time information
        iTimeStep_NOW = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeStep'])
        iTimeCheck_NOW = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeCheck'])
        
        # Time NOW
        sTime_NOW = str(self.oDataInfo.oInfoSettings.oParamsInfo['TimeNow']);  
        oTime_NOW = datetime.datetime.strptime(sTime_NOW,'%Y%m%d%H%M')
        oTimeDelta_NOW = datetime.timedelta(seconds = iTimeStep_NOW)
        
        # Time PREVIOUS STEP
        oTime_PS = oTime_NOW - oTimeDelta_NOW; sTime_PS = oTime_PS.strftime('%Y%m%d%H%M')
        
        sYear_NOW = sTime_NOW[0:4]; sMonth_NOW = sTime_NOW[4:6]; sDay_NOW = sTime_NOW[6:8];
        sHH_NOW = sTime_NOW[8:10]; sMM_NOW = sTime_NOW[10:12];
        
        sYear_PS = sTime_PS[0:4]; sMonth_PS = sTime_PS[4:6]; sDay_PS = sTime_PS[6:8];
        sHH_PS = sTime_PS[8:10]; sMM_PS = sTime_PS[10:12];
        #------------------------------------------------------------------------------------- 
        
        #-------------------------------------------------------------------------------------
        # [OBS] Define step to reprocess
        oTimeDelta_OBS = datetime.timedelta(seconds = iVarRes_OBS)
        oTimeFrom_OBS = oTime_NOW - datetime.timedelta(seconds = iVarRes_OBS*iTimeCheck_NOW); 
        oTimeTo_OBS = oTime_NOW
 
        a1oTimeSteps_OBS = []
        while oTimeFrom_OBS <= oTimeTo_OBS:
            a1oTimeSteps_OBS.append(oTimeFrom_OBS.strftime('%Y%m%d%H%M'))
            oTimeFrom_OBS += oTimeDelta_OBS
        
        # [FOR] Define step to reprocess
        oTimeDelta_FOR = datetime.timedelta(seconds = iVarRes_FOR)
        oTimeFrom_FOR = oTime_NOW + datetime.timedelta(seconds = iVarRes_FOR); 
        oTimeTo_FOR = oTimeFrom_FOR + datetime.timedelta(seconds = iVarRes_FOR*iVarStep_FOR); 
 
        a1oTimeSteps_FOR = []
        while oTimeFrom_FOR <= oTimeTo_FOR:
            a1oTimeSteps_FOR.append(oTimeFrom_FOR.strftime('%Y%m%d%H%M'))
            oTimeFrom_FOR += oTimeDelta_FOR
        a1oTimeSteps_FOR = [a1oTimeSteps_FOR[0]]
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Define cache folder for time now and time ps
        sRunType = str(self.oRunTags['$TYPE'])
        
        # Define cache file PS
        sPathHistory_PS = Lib_Data_IO_Utils.defineFolderName(sPathCache,
                                                     {'$yyyy' : sYear_PS,'$mm' : sMonth_PS,'$dd' : sDay_PS, 
                                                      '$HH' : sHH_PS,'$MM' : sMM_PS, '$RUN' : str(self.oRunTags['$RUN'])})
        
        if sRunType == '':
            sFileHistory_PS = os.path.join(sPathHistory_PS, 
                                           'RUN_DATAFORCING_' + sTime_PS + '_' + str(self.oRunTags['$RUN']) + '.history')
        else:
            sFileHistory_PS = os.path.join(sPathHistory_PS, 
                            'RUN_DATAFORCING_' + sTime_PS + '_' + str(self.oRunTags['$RUN']) + 
                            '_' + str(self.oRunTags['$TYPE']) + '.history')
        
        # Define cache file NOW
        sPathHistory_NOW = Lib_Data_IO_Utils.defineFolderName(sPathCache,
                                             {'$yyyy' : sYear_NOW,'$mm' : sMonth_NOW,'$dd' : sDay_NOW, 
                                              '$HH' : sHH_NOW,'$MM' : sMM_NOW, '$RUN' : str(self.oRunTags['$RUN'])})
        if sRunType == '':
            sFileHistory_NOW = os.path.join(sPathHistory_NOW, 
                                            'RUN_DATAFORCING_' + sTime_NOW + '_' + str(self.oRunTags['$RUN']) + '.history')
        else:
            sFileHistory_NOW = os.path.join(sPathHistory_NOW, 
                                'RUN_DATAFORCING_' + sTime_NOW + '_' + str(self.oRunTags['$RUN']) +
                                '_' + str(self.oRunTags['$TYPE']) + '.history')
        
        # Initialize run historical or whole initialization mode
        if iRunInit == 0:
            
            # Check if exist actual history file
            if not os.path.exists(sFileHistory_PS):
                
                # Redefine reference history file
                if os.path.exists(sFileHistory_NOW):
                    sFileHistory_PS = sFileHistory_NOW
            
            # Load cache file
            if os.path.exists(sFileHistory_PS):
                
                # Open history file
                [a1oFileTimeSave_PS, a1oFileType_PS, 
                     a1oFileTimeRef_PS, a1oFileName_PS, 
                     a1oFileExist_PS, a1oFileStatus_PS] = getFileHistory(sFileHistory_PS)
                bFileHystory = True
                
                # Cycle(s) on time steps
                for sTimeStep_ALL in a1oTimeStep_ALL:
                    
                    if sTimeStep_ALL in a1oFileTimeSave_PS:
                        
                        # Define time reference PS
                        iTimeIndex_REF = int(a1oFileTimeSave_PS.index(sTimeStep_ALL))
                        sTimeFile_REF = a1oFileTimeRef_PS[iTimeIndex_REF]
                        sFileExist_REF = a1oFileExist_PS[iTimeIndex_REF]
                        
                        oTimeStep_ALL = datetime.datetime.strptime(sTimeStep_ALL,'%Y%m%d%H%M')
                        oTimeFile_REF = datetime.datetime.strptime(sTimeFile_REF,'%Y%m%d%H%M')
                        
                        if sFileExist_REF == 'True':
                            
                            # OBS Check
                            if oTimeStep_ALL <= oTime_NOW:
            
                                if not [sStr for sStr in a1oTimeSteps_OBS if sTimeStep_ALL in sStr]:
                                    a1oTimeData_ALL[sTimeStep_ALL]['OBS'] = None
                                else:
                                    pass
                            else:
                                pass
                            
                            # FOR Check
                            if oTimeStep_ALL > oTime_NOW:
                                
                                if [sStr for sStr in a1oTimeSteps_FOR if sTimeStep_ALL in sStr]:
                                    
                                    sTimeStep_FOR_CS = a1oTimeData_ALL[sTimeStep_ALL]['FOR'][0]
                                    
                                    oTimeStep_FOR_CS = datetime.datetime.strptime(sTimeStep_FOR_CS,'%Y%m%d%H%M')
                                    oTimeStep_FOR_PS = oTimeFile_REF
                                    
                                    if oTimeStep_FOR_CS <= oTimeStep_FOR_PS:
                                        a1oTimeData_ALL[sTimeStep_ALL]['FOR'] = None
                                        
                                else:pass
                            else:pass
                        else:pass
                    else:pass
            else: bFileHystory = False; 
        else:bFileHystory = False; 
        #-------------------------------------------------------------------------------------   
        
        #------------------------------------------------------------------------------------- 
        # Return
        self.oTimeData = a1oTimeData_ALL
        self.sFileHistory_PS = sFileHistory_PS
        self.sFileHistory_NOW = sFileHistory_NOW
        #------------------------------------------------------------------------------------- 
  
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to select data time 
    def selectTimeDynamicGridded(self):
        
        oDataTime = self.oDataTime
        a1oTimeSteps = self.oDataTime.a1oTimeSteps;
        
        oVarsDynamic_OBS = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded']['OBS']
        oVarsDynamic_FOR = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded']['FOR']
        
        iVarRes_OBS = int(oVarsDynamic_OBS['VarResolution'])
        iVarRecStep_OBS = int(oVarsDynamic_FOR['VarRecurrency']['Step'])
        oVarRecHour_FOR = oVarsDynamic_FOR['VarRecurrency']['Hour']
        iVarStep_OBS = int(oVarsDynamic_OBS['VarStep'])
        
        iVarRes_FOR = int(oVarsDynamic_FOR['VarResolution'])
        iVarRecStep_FOR = int(oVarsDynamic_FOR['VarRecurrency']['Step'])
        oVarRecHour_FOR = oVarsDynamic_FOR['VarRecurrency']['Hour']
        iVarStep_FOR = int(oVarsDynamic_FOR['VarStep'])

        sTimeNow = self.oDataInfo.oInfoSettings.oParamsInfo['TimeNow']; oTimeNow = datetime.datetime.strptime(sTimeNow,'%Y%m%d%H%M')
        
        oTimeData = {}
        for sTimeStep in a1oTimeSteps:
            
            oTimeStep = datetime.datetime.strptime(sTimeStep,'%Y%m%d%H%M')
            
            if not sTimeStep in oTimeData:
                oTimeData[sTimeStep] = {}
                oTimeData[sTimeStep]['OBS'] = {}
                oTimeData[sTimeStep]['FOR'] = {}
            
            if oTimeStep <= oTimeNow:
                
                sTimeStep_OBS = oTimeStep.strftime('%Y%m%d%H%M')
                
                oTimeData[sTimeStep]['OBS'] = sTimeStep_OBS
                oTimeData[sTimeStep]['FOR'] = None

            elif oTimeStep > oTimeNow:
                
                iHHStep = int(sTimeStep[8:10]);
                for sHHValue in oVarRecHour_FOR:
                    iHHValue = int(sHHValue)
                    if iHHStep > iHHValue:
                        iHHSel = iHHValue

                oTimeStep_FOR = oTimeStep.replace(hour = iHHSel, minute = 0, second = 0, microsecond = 0)
                
                oTimeDelta_FOR = datetime.timedelta(seconds = iVarRes_FOR*iVarStep_FOR)
                
                oTimeTo_FOR = oTimeStep_FOR

                oTimeFrom_FOR = oTimeTo_FOR - oTimeDelta_FOR
                oTimeFrom_FOR = oTimeFrom_FOR.replace(hour = iHHSel, minute = 0, second = 0, microsecond = 0)
                
                oTimeStep_FOR = datetime.timedelta(seconds = iVarRecStep_FOR)
                
                a1oTimeSteps_FOR = []
                while oTimeFrom_FOR <= oTimeTo_FOR:
                    oTimeDiff = oTimeStep - oTimeFrom_FOR
                    if oTimeDiff < oTimeDelta_FOR:           
                        a1oTimeSteps_FOR.append(oTimeFrom_FOR.strftime('%Y%m%d%H%M')) 
                    else:
                        pass
                    oTimeFrom_FOR += oTimeStep_FOR
                
                oTimeData[sTimeStep]['OBS'] = None
                oTimeData[sTimeStep]['FOR'] = sorted(a1oTimeSteps_FOR,reverse=True)
                
                break # only first date for FOR data
        
        self.oTimeData = oTimeData
                
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to select input gridded file(s)
    def getFileDynamicGridded(self):
        
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET DYNAMIC GRIDDED FILE(S) ... ')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Get geosystem data
        oGeoSystemInfo = self.oDataInfo.oInfoSettings.oGeoSystemInfo
        oGeneralInfo = self.oDataInfo.oInfoSettings.oGeneralInfo
        oParamsInfo = self.oDataInfo.oInfoSettings.oParamsInfo
        
        # Cache folder 
        sPathCache = self.oDataInfo.oInfoSettings.oPathInfo['DataCache']
        sPathTemp = self.oDataInfo.oInfoSettings.oPathInfo['DataTemp']

        # Get time information
        iTimeStep_NOW = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeStep'])
        sTime_NOW = self.oDataInfo.oInfoSettings.oParamsInfo['TimeNow']; oTime_NOW = datetime.datetime.strptime(sTime_NOW,'%Y%m%d%H%M')

        # Get time/data information
        a1oTimeData_IN = self.oTimeData
        a1oTimeStep_IN = sorted(self.oTimeData.keys())
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Define cache folder for time now
        sYear_NOW = sTime_NOW[0:4]; sMonth_NOW = sTime_NOW[4:6]; sDay_NOW = sTime_NOW[6:8];
        sHH_NOW = sTime_NOW[8:10]; sMM_NOW = sTime_NOW[10:12];
        sPathCache_NOW = Lib_Data_IO_Utils.defineFolderName(sPathCache,
                                                     {'$yyyy' : sYear_NOW,'$mm' : sMonth_NOW,'$dd' : sDay_NOW, 
                                                      '$HH' : sHH_NOW,'$MM' : sMM_NOW, '$RUN' : str(self.oRunTags['$RUN'])})
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Cycling on time steps
        a1oFileName_OUT = []; a1oFileExist_OUT = []; a1oFileTime_OUT = []; a1oFileType_OUT = []; a1oFileTime_CHECK = []; a1oFileStatus_OUT = []
        a1sTime_SELECT = []; a1sVarType_SELECT = []; a1sVarStatus_SELECT = []
        for iIndex_IN, sTime_IN in enumerate(a1oTimeStep_IN):
            
            #------------------------------------------------------------------------------------- 
            # Initialize variable status
            a1sVarStatus_SELECT.append(False)
            a1sTime_SELECT.append('UNDEFINED')
            a1sVarType_SELECT.append('UNDEFINED')
            #------------------------------------------------------------------------------------- 
            
            #------------------------------------------------------------------------------------- 
            # Time information
            sYear_IN = sTime_IN[0:4]; sMonth_IN = sTime_IN[4:6]; sDay_IN = sTime_IN[6:8];
            sHH_IN = sTime_IN[8:10]; sMM_IN = sTime_IN[10:12];
            oTime_IN = datetime.datetime.strptime(sTime_IN,'%Y%m%d%H%M')

            # Time Info
            oLogStream.info( ' ====> TIME STEP INPUT: ' + sTime_IN + ' ... ')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Check variable(s) type (OBS or FOR)
            if oTime_IN <= oTime_NOW:
                
                #-------------------------------------------------------------------------------------
                # Variable type
                sVarType_IN = 'OBS'
                # Get dynamic time information
                oTimeData_IN = a1oTimeData_IN[sTime_IN][sVarType_IN]
                # Get dynamic variable information
                oVarsDynamic = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded'][sVarType_IN]['VarName']
                oVarsDims = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded'][sVarType_IN]['VarDims']
                #-------------------------------------------------------------------------------------
 
            elif oTime_IN > oTime_NOW:
                
                #-------------------------------------------------------------------------------------
                # Variable type
                sVarType_IN = 'FOR'
                # Get dynamic time information
                oTimeData_IN = a1oTimeData_IN[sTime_IN][sVarType_IN]
                # Get dynamic variable information
                oVarsDynamic = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded'][sVarType_IN]['VarName']
                oVarsDims = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded'][sVarType_IN]['VarDims']
                #-------------------------------------------------------------------------------------
                
            # Info variable type
            sVarType_SELECT = sVarType_IN
            oLogStream.info(' -----> VarType: ' + sVarType_SELECT)
            
            # Update variable status
            a1sTime_SELECT[iIndex_IN] = sTime_IN; a1sVarType_SELECT[iIndex_IN] = sVarType_SELECT
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Check if time of data must be processed
            if not oTimeData_IN is None:

                #-------------------------------------------------------------------------------------
                # Get time length
                if isinstance(oTimeData_IN, basestring):
                    a1oTime_CHECK = [oTimeData_IN] 
                else:
                    a1oTime_CHECK = oTimeData_IN
                
                # Get variable dimension(s)
                iVarDims = len(oVarsDims)
                #-------------------------------------------------------------------------------------
    
                #-------------------------------------------------------------------------------------
                # Check file availability
                a1oData_OUT = {}; 
                for sVarName_CHECK in oVarsDynamic:        
                    
                    #-------------------------------------------------------------------------------------
                    # Info
                    oLogStream.info(' ------> VarName: ' + sVarName_CHECK + ' ... ')
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Cycle(s) on time check
                    for sTime_CHECK in a1oTime_CHECK:
                        
                        # Define step and tags CHECK
                        sYear_CHECK = sTime_CHECK[0:4]; sMonth_CHECK = sTime_CHECK[4:6]; sDay_CHECK = sTime_CHECK[6:8];
                        sHH_CHECK = sTime_CHECK[8:10]; sMM_CHECK = sTime_CHECK[10:12];
                        oTime_CHECK = datetime.datetime.strptime(sTime_CHECK,'%Y%m%d%H%M')
                        
                        oTags_CHECK = Lib_Data_IO_Utils.joinDict(self.oRunTags, {'$yyyy' : sYear_CHECK, 
                                                                               '$mm' : sMonth_CHECK, '$dd' : sDay_CHECK, 
                                                                               '$HH' : sHH_CHECK, '$MM' : sMM_CHECK, 
                                                                               '$VAR' : sVarName_CHECK})
                        
                        # Define filename CHECK
                        sVarFilePath_CHECK = oVarsDynamic[sVarName_CHECK]['FilePath']
                        sVarFileName_CHECK = oVarsDynamic[sVarName_CHECK]['FileName']
                        sVarFileVar_CHECK = oVarsDynamic[sVarName_CHECK]['FileVar']
                        sFileName_CHECK = Lib_Data_IO_Utils.defineString(join(sVarFilePath_CHECK, sVarFileName_CHECK), oTags_CHECK)
                        
                        # Info
                        oLogStream.info(' -------> Select File: ' + sFileName_CHECK + ' ... ')
                        
                        # File availability CHECK
                        bFileExist_CHECK = Lib_Data_IO_Utils.checkFileExist(sFileName_CHECK)
                        if bFileExist_CHECK == True:
                            sFileName_SELECT = sFileName_CHECK; sVarName_SELECT = sVarName_CHECK;
                            oLogStream.info(' -------> Select File: ' + sFileName_SELECT + ' ... OK ')
                            break
                        else:
                            # Info
                            oLogStream.info( ' -------> Select File: ' + sFileName_CHECK + ' ... SKIPPED --- FILE NOT FOUND!')
                            GetException(' -------> WARNING: Select File: ' + sFileName_CHECK + ' ... SKIPPED --- FILE NOT FOUND!' ,2,1)
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Check file availability
                    if bFileExist_CHECK is True:
                        
                        # Info
                        oLogStream.info(' -------> Open File: ' + sFileName_SELECT + ' ... ')
                        
                        # Open file
                        oFileDrv_SELECT = Drv_Model_HMC_IO(sFileName_SELECT, self.oDataInfo, self.oDataStatic)
                        
                        # Get data 
                        oFileData_SELECT = oFileDrv_SELECT.getDynamicData(sVarFileVar_CHECK, sTime_IN, iVarDims)
                        
                        # Get data and time for select dictionary
                        oData_SELECT = oFileData_SELECT['Data']
                        oTime_SELECT = oFileData_SELECT['Time']
                        
                        if not (oData_SELECT == None and oTime_SELECT == None):
                            
                            for iTime_SELECT, sTime_SELECT in enumerate(oTime_SELECT):
            
                                if iVarDims == 2:
                                    a2dData_SELECT = oData_SELECT[:,:]
                                elif iVarDims == 3:
                                    a2dData_SELECT = oData_SELECT[:,:, iTime_SELECT]
                                
                                if not sTime_SELECT in a1oData_OUT:
                                    
                                    a1oData_OUT[sTime_SELECT] = {}
                                    a1oData_OUT[sTime_SELECT]['GeoX'] = oFileData_SELECT['GeoX']
                                    a1oData_OUT[sTime_SELECT]['GeoY'] = oFileData_SELECT['GeoY']
                                    a1oData_OUT[sTime_SELECT]['GeoZ'] = oFileData_SELECT['GeoZ']
                                    a1oData_OUT[sTime_SELECT]['Attributes'] = oFileData_SELECT['Attributes']
                                    a1oData_OUT[sTime_SELECT]['GeoInfo'] = {}
                                    a1oData_OUT[sTime_SELECT]['GeoInfo']['GeoBox'] = oFileData_SELECT['GeoInfo']['GeoBox']
                                    a1oData_OUT[sTime_SELECT]['GeoInfo']['GeoRef'] = oFileData_SELECT['GeoInfo']['GeoRef']
                                    
                                if not sVarName_SELECT in a1oData_OUT[sTime_SELECT]:
                                    a1oData_OUT[sTime_SELECT][sVarName_SELECT] = {}
                                
                                # Save data dynamic
                                a1oData_OUT[sTime_SELECT][sVarName_SELECT] = a2dData_SELECT
                                
                            # Info
                            oLogStream.info(' -------> Open File: ' + sFileName_SELECT + ' ... OK')
                                    
                        else:
                            # Info
                            oLogStream.info(' -------> Open File: ' + sFileName_SELECT + ' ... SKIPPED')
                            GetException(' -------> WARNING: Open File: ' + sFileName_SELECT + ' ... SKIPPED --- DATA NOT FOUND!' ,2,1)
                    else:
                        pass
                    #-------------------------------------------------------------------------------------
                
                # Info
                oLogStream.info(' ------> VarName: ' + sVarName_CHECK + ' ... OK')
                oLogStream.info( ' ====> TIME STEP INPUT: ' + sTime_IN + ' ... OK')
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Cycle(s) to save data in 2D format (starting from 2D or 3D variable(s)
                for sTime_OUT in sorted(a1oData_OUT):
                    
                    #-------------------------------------------------------------------------------------
                    # Info OUTPUT start
                    oLogStream.info( ' ====> TIME STEP OUTPUT: ' + sTime_OUT + ' ... ')
                    
                    sYear_OUT= sTime_OUT[0:4]; sMonth_OUT = sTime_OUT[4:6]; sDay_OUT = sTime_OUT[6:8];
                    sHH_OUT = sTime_OUT[8:10]; sMM_OUT = sTime_OUT[10:12];
                    
                    iTimeIndex_OUT = a1oTimeStep_IN.index(sTime_OUT)
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Define filename OUT
                    sFileName_OUT = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded']['FileName']
                    sFilePath_OUT = self.oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded']['FilePath']
                    
                    oTags_OUT = Lib_Data_IO_Utils.joinDict(self.oRunTags, {'$yyyy' : sYear_OUT, 
                                                       '$mm' : sMonth_OUT, '$dd' : sDay_OUT, 
                                                       '$HH' : sHH_OUT, '$MM' : sMM_OUT })
                    
                    sFilePath_OUT = Lib_Data_IO_Utils.defineString(sFilePath_OUT, oTags_OUT)
                    sFileName_OUT = Lib_Data_IO_Utils.defineString(join(sFilePath_OUT, sFileName_OUT), oTags_OUT)
                    
                    # Create folder OUT
                    Lib_Data_IO_Utils.createFolder(sFilePath_OUT)
                    #-------------------------------------------------------------------------------------
                    
                    #-------------------------------------------------------------------------------------
                    # Save data 
                    oLogStream.info( ' -------> Save File: ' + sFileName_OUT + ' ...  ')
                    try:
                        
                        # Get data 
                        oData_OUT = a1oData_OUT[sTime_OUT]
                        # Save data in output file
                        oFileDrv_OUT = Drv_Model_HMC_IO(sFileName_OUT, self.oDataInfo)
                        oFileDrv_OUT.saveDynamicData(oData_OUT, oParamsInfo, oGeneralInfo, oGeoSystemInfo)
    
                        # SAVE DATA IN NC FORMAT (END)
                        a1oFileName_OUT.append(sFileName_OUT); a1oFileExist_OUT.append('True'); 
                        a1oFileTime_OUT.append(sTime_OUT); a1oFileType_OUT.append(sVarType_IN)
                        a1oFileTime_CHECK.append(sTime_CHECK); a1oFileStatus_OUT.append('NEW')
                        oLogStream.info( ' -------> Save File: ' + sFileName_OUT + ' ...  OK')
                        oLogStream.info( ' ====> TIME STEP OUTPUT: ' + sTime_OUT + ' ... OK')
                        
                        a1sVarStatus_SELECT[iTimeIndex_OUT] = True
                        
                    except:
                        
                        # Info
                        a1oFileName_OUT.append(sFileName_OUT); a1oFileExist_OUT.append('False'); 
                        a1oFileTime_OUT.append(sTime_OUT); a1oFileType_OUT.append(sVarType_IN)
                        a1oFileTime_CHECK.append(sTime_CHECK); a1oFileStatus_OUT.append('FAIL')
                        oLogStream.info( ' -------> Save File: ' + sFileName_OUT + ' ... FAILED --- CHECK INPUT DATA')
                        GetException(' -------> Save File: ' + sFileName_OUT + ' ... FAILED --- CHECK INPUT DATA' ,2,1)
                        oLogStream.info( ' ====> TIME STEP OUTPUT: ' + sTime_OUT + ' ... FAILED')
                        
                        a1sVarStatus_SELECT[iTimeIndex_OUT] = False
                    
                    #-------------------------------------------------------------------------------------
                    
                #-------------------------------------------------------------------------------------
            
            else:
                
                #-------------------------------------------------------------------------------------
                # Get file history previous step
                sFileHistory_PS = self.sFileHistory_PS

                # Load cache file
                if os.path.exists(sFileHistory_PS):
                    
                    oLogStream.info( ' ====> TIME STEP INPUT: ' + sTime_IN + ' ... SKIPPED --- STEP PREVIOSLY PROCESSED!')
                    
                    # Open history file
                    [a1oFileTimeSave_PS, a1oFileType_PS, 
                     a1oFileTimeRef_PS, a1oFileName_PS, 
                     a1oFileExist_PS, a1oFileStatus_PS] = getFileHistory(self.sFileHistory_PS)
                    
                    iIndexTimeSave_IN = []; sFileTimeRef_IN = ''
                    iIndexTimeSave_IN = a1oFileTimeSave_PS.index(sTime_IN)
                    sFileTimeRef_IN = a1oFileTimeRef_PS[iIndexTimeSave_IN]
                    
                    a1sVarStatus_SELECT[iIndex_IN] = True

                    a1iIndexTime_IN = np.array([]);
                    for iIndexTimeRef_PS, sFileTimeRef_PS in enumerate(a1oFileTimeRef_PS):
                        if sFileTimeRef_PS == sFileTimeRef_IN:
                            sFileType_IN = a1oFileType_PS[iIndexTimeRef_PS]
                            if sFileType_IN == sVarType_IN:
                                if iIndexTimeRef_PS >= iIndexTimeSave_IN:
                                    a1iIndexTime_IN = np.append(a1iIndexTime_IN, iIndexTimeRef_PS)
                                else:pass
                            else:pass
                        else:pass
                    
                    for iI in range(0, len(a1iIndexTime_IN)):
                        
                        iIndexTime_PS = int(a1iIndexTime_IN[iI])
                        
                        sTime_OUT = a1oFileTimeSave_PS[iIndexTime_PS]
                        oLogStream.info( ' ====> TIME STEP OUTPUT: ' + sTime_OUT + ' ... ')
                        
                        a1oFileName_OUT.append(a1oFileName_PS[iIndexTime_PS]); 
                        a1oFileExist_OUT.append(a1oFileExist_PS[iIndexTime_PS]); 
                        a1oFileTime_OUT.append(a1oFileTimeSave_PS[iIndexTime_PS]); 
                        a1oFileType_OUT.append(a1oFileType_PS[iIndexTime_PS])
                        a1oFileTime_CHECK.append(a1oFileTimeRef_PS[iIndexTime_PS])
                        a1oFileStatus_OUT.append('OLD')
                        
                        oLogStream.info( ' ====> TIME STEP OUTPUT: ' + sTime_OUT + ' ... SKIPPED --- STEP PREVIOSLY PROCESSED!')
                else:
                    pass    
                #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Zip variable status
        self.oDataStatus = zip(a1sTime_SELECT, a1sVarType_SELECT, a1sVarStatus_SELECT)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Store hystory file 
        if np.any(np.asarray(a1oFileExist_OUT) == 'True'):
            # Create hash handle
            
            sRunType = str(self.oRunTags['$TYPE'])
            if sRunType == '':
                sFileCache_OUT = os.path.join(sPathCache_NOW, 
                              'RUN_DATAFORCING_' + sTime_NOW + '_' + str(self.oRunTags['$RUN']) + '.history')
            else:
                sFileCache_OUT = os.path.join(sPathCache_NOW, 
                          'RUN_DATAFORCING_' + sTime_NOW + '_' + str(self.oRunTags['$RUN']) +
                          '_' + str(self.oRunTags['$TYPE']) + '.history')

            # Save hystory file
            writeFileHistory(sFileCache_OUT, zip(a1oFileTime_OUT, a1oFileType_OUT, 
                                                 a1oFileTime_CHECK, a1oFileName_OUT, 
                                                 a1oFileExist_OUT, a1oFileStatus_OUT))

            self.oFileHistory_NOW = sFileCache_OUT
   
        else:
            # Info warning
            GetException(' ------> WARNING: all files are not available! Check your settings and data!', 2, 1)
            
        #------------------------------------------------------------------------------------- 
            
        #------------------------------------------------------------------------------------- 
        # Info
        oLogStream.info( ' ====> GET DYNAMIC GRIDDED FILE(S) ... OK')
        #------------------------------------------------------------------------------------- 

    #-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
  
  
  
  
  
    
