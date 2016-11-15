"""
Class Features

Name:          Cpl_Apps_HMC_PostProcessing_TIMESERIES_Dewetra
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151110'
Version:       '1.0.0'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

import os, glob, re, datetime
import numpy as np

from operator import itemgetter

from src.GetException import GetException

import src.Lib_Data_IO_Utils as Lib_Data_IO_Utils
import src.Lib_Data_IO_Dewetra as Lib_Data_IO_Dewetra

# Debug
import matplotlib.pylab as plt
######################################################################################

#------------------------------------------------------------------------------------- 
# Method to define run tags
def defineTags(sDomainName, sRunName, sRunType, sTime):
    
    # Split time information
    sYear = sTime[0:4]; sMonth = sTime[4:6]; sDay = sTime[6:8];
    sHH = sTime[8:10]; sMM = sTime[10:12];
    
    # Create and fill tags dictionary
    oTagsDict = {}
    oTagsDict['$yyyy'] = sYear
    oTagsDict['$mm'] = sMonth
    oTagsDict['$dd'] = sDay
    oTagsDict['$HH'] = sHH
    oTagsDict['$MM'] = sMM
    oTagsDict['$DOMAIN'] = sDomainName
    oTagsDict['$RUN'] = sRunName
    oTagsDict['$TYPE'] = sRunType
       
    # Return tags dictionary
    return oTagsDict
    #------------------------------------------------------------------------------------- 
    
#------------------------------------------------------------------------------------- 

#-------------------------------------------------------------------------------------
# Class
class Cpl_Apps_HMC_PostProcessing_TIMESERIES_Dewetra:
    
    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, oDataInfo=None, oDataTime=None):
        
        #-------------------------------------------------------------------------------------
        # Get information
        self.oDataInfo = oDataInfo
        self.oDataTime = oDataTime
        
        # Get domain, run and description name
        self.sDomainName = self.oDataInfo.oInfoSettings.oParamsInfo['DomainName'].lower()
        self.sRunName = self.oDataInfo.oInfoSettings.oParamsInfo['RunName'].lower()
        #self.sRunDescription = self.oDataInfo.oInfoSettings.oParamsInfo['RunDescription'].lower()
        self.sRunDescription = self.oDataInfo.oInfoSettings.oParamsInfo['RunDescription']
        
        # Select type run
        self.TypeRun()
        #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Method to select run type (ensemble or single run)
    def TypeRun(self):
        
        #-------------------------------------------------------------------------------------
        # initialize ensemble dictionary
        oEnsembleList = {}
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Check if ensemble dictionary exists in settings
        if self.oDataInfo.oInfoSettings.oParamsInfo['RunEnsemble']:
            
            #-------------------------------------------------------------------------------------
            # Get ensemble dictionary
            oParamsRunEns = self.oDataInfo.oInfoSettings.oParamsInfo['RunEnsemble']
            
            # Get ensemble information
            bEnsRun = oParamsRunEns['EnsRun']
            iEnsMax = int(oParamsRunEns['EnsMax']); iEnsMin = int(oParamsRunEns['EnsMin'])
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Check ensemble run type
            if bEnsRun:
                
                #-------------------------------------------------------------------------------------
                # Compute ensemble element(s)
                iEnsN = iEnsMax - iEnsMin + 1
                sEnsDigit = '%03d'; #sEnsDigit = '%0' + str(len(str(iEnsMax))) + 'd'; 
                
                # Cycle(s) on ensemble element(s)
                iID = 1
                for iEnsN in range(iEnsMin, iEnsMax + 1):
                    
                    # Ensemble ID
                    sEns = str(sEnsDigit%(iEnsN));
                    # Ensemble dictionary
                    oEnsembleList['Run_ENSEMBLE_' + str(sEnsDigit%(iID))] = sEns
                    # Counter ensemble
                    iID = iID + 1
                    
                #-------------------------------------------------------------------------------------
                                    
            else:  
                
                #-------------------------------------------------------------------------------------
                # Single run
                oEnsembleList['Run_Deterministic'] = ''
                #-------------------------------------------------------------------------------------
                
            #--------------oTags-----------------------------------------------------------------------
            
        else:
            
            #-------------------------------------------------------------------------------------
            # Single run
            oEnsembleList['Run_Deterministic'] = ''
            #-------------------------------------------------------------------------------------
            
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Return ensemble list
        self.oDataEnsemble = oEnsembleList
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to execute run model
    def Runner(self):
        
        #------------------------------------------------------------------------------------- 
        # Get workspace info
        oWorkspaceInfo = self.oWorkspaceInfo
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Cycle(s) on run
        oWorspaceData = {}; oWorspaceObs = {}
        for sRunType in oWorkspaceInfo:
            
            #------------------------------------------------------------------------------------- 
            # Run information
            oRunInfo = oWorkspaceInfo[sRunType]
            # Initialize workspace on run
            oWorspaceData[sRunType] = {}; oWorspaceObs[sRunType] = {}; 
            #------------------------------------------------------------------------------------- 
            
            #------------------------------------------------------------------------------------- 
            # Cycle(s) on variable
            for sVarName in oRunInfo:
                
                #------------------------------------------------------------------------------------- 
                # Info start
                oLogStream.info(' --------> Create TS - RunType: ' + sRunType + ' VarName: ' + sVarName + ' ... ')
                #------------------------------------------------------------------------------------- 
                
                #------------------------------------------------------------------------------------- 
                # Variable information
                oVarInfo = oRunInfo[sVarName]
                a1oVarFile = oVarInfo['FileList_ARC']
                a1oObsFile = oVarInfo['FileList_OBS']
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Check data length (int or NONE) 
                if oVarInfo['FileList_ARC']:
                    
                    # Define data length
                    iDataDim = int(oVarInfo['Data_DIM'])
                    # Define time length
                    iTimeDim = int(len(oVarInfo['FileList_ARC']))
                    
                    # Initialize workspace on variable
                    oWorspaceData[sRunType][sVarName] = {}; oWorspaceObs[sRunType][sVarName] = {}
                    #------------------------------------------------------------------------------------- 
                    
                    print(iTimeDim)
                    print(iDataDim)
                    
                    #------------------------------------------------------------------------------------- 
                    # Cycle(s) on variable file(s)
                    a2dVarData = np.zeros([iTimeDim, iDataDim]); a2dVarData[:] = -9999
                    for iVarStep, sVarFile in enumerate(a1oVarFile):
                        # Check file string
                        if sVarFile != None:
                            # Get 1d data
                            if os.path.isfile(sVarFile):
                                a1dVarData = Lib_Data_IO_Dewetra.getData1D(sVarFile)
                                a2dVarData[iVarStep, :] = a1dVarData
                            else:pass
                        else:pass
                    
                    # Save data in 2d format
                    oWorspaceData[sRunType][sVarName] = a2dVarData
                    #------------------------------------------------------------------------------------- 
                    
                    #------------------------------------------------------------------------------------- 
                    # Cycle(s) on observation file(s)
                    a2dObsData = np.zeros([iTimeDim, iDataDim]); a2dObsData[:] = -9999
                    for iObsStep, sObsFile in enumerate(a1oObsFile):
                        # Check file string
                        if sObsFile != None:
                            # Get 1d data
                            if os.path.isfile(sObsFile):
                                a1dObsData = Lib_Data_IO_Dewetra.getData1D(sObsFile)[:,1]
                                a2dObsData[iObsStep, :] = a1dObsData
                            else:pass
                        else:pass
                        
                    # Save data in 2d format
                    oWorspaceObs[sRunType][sVarName] = a2dObsData
                    #------------------------------------------------------------------------------------- 
                    
                    #------------------------------------------------------------------------------------- 
                    # Info end
                    oLogStream.info(' --------> Create TS - RunType: ' + sRunType + ' VarName: ' + sVarName + ' ... OK')
                    #-------------------------------------------------------------------------------------
                    
                else:
                
                    #------------------------------------------------------------------------------------- 
                    # Info end
                    oLogStream.info(' --------> Create TS - RunType: ' + sRunType + ' VarName: ' + sVarName + ' ... FAILED')
                    GetException(' WARNING: SECQ TIMESERIES TimeFrom and TimeTo Undefined!',2,1)
                    
                    # Delete none key in dictionary data and obs
                    if sRunType in oWorspaceData: del oWorspaceData[sRunType]
                    if sRunType in oWorspaceObs: del oWorspaceObs[sRunType]
                    #------------------------------------------------------------------------------------- 
                
            #------------------------------------------------------------------------------------- 
        
        #-------------------------------------------------------------------------------------
        # Save variable(s) data to workspace
        self.oWorkspaceData = oWorspaceData
        self.oWorkspaceObs = oWorspaceObs
        #-------------------------------------------------------------------------------------

    #------------------------------------------------------------------------------------- 
    
    #------------------------------------------------------------------------------------- 
    # Method to execute run model
    def Finalizer(self):
        
        #-------------------------------------------------------------------------------------
        # Get run description
        sRunDescription = self.sRunDescription
        #-------------------------------------------------------------------------------------
        
        #------------------------------------------------------------------------------------- 
        # Get workspace info and data
        oWorkspace_INFO = self.oWorkspaceInfo
        oWorkspace_DATA = self.oWorkspaceData
        oWorkspace_OBS = self.oWorkspaceObs
        oWorkspace_SEC = self.oWorkspaceSection
        oWorkspace_DAM = self.oWorkspaceDam
        #------------------------------------------------------------------------------------- 
        
        #-------------------------------------------------------------------------------------
        # Get TimeNow
        sTimeNow = self.oDataInfo.oInfoSettings.oParamsInfo['TimeNow']
        iTimeStep = int(self.oDataInfo.oInfoSettings.oParamsInfo['TimeStep'])
        
        # Get section number
        iSectionN = len(oWorkspace_SEC);
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cycle(s) on section
        oSecWarning = []
        for iSection, oSection in enumerate(oWorkspace_SEC):
            
            #-------------------------------------------------------------------------------------
            # Get section and basin information
            sBasinName = str(oSection[2]); sSectionName = str(oSection[3])
            dSectionQAlarm = float(oSection[6]); dSectionQAlert = float(oSection[7])
            
            oLogStream.info(' --------> SECQ == BASIN: ' + sBasinName + ' - SECTION: ' + sSectionName + ' -----------------' )
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Get and read ensemble result(s)
            a2dDataSECQ_TS_SAVE = None; a1dObsSECQ_TS_SAVE = None
            sFilePathSECQ_WS = None; sFileNameSECQ_WS = None; sFileNameSECQ_WS_SAVE = None
            sFilePathSECQ_TS = None; sFileNameSECQ_TS = None; sFileNameSECQ_TS_SAVE = None
            sTimeFromSECQ_TS = None; sTimeToSECQ_TS = None
            for iRun_DATA, sRun_DATA in enumerate(oWorkspace_DATA):
                
                oLogStream.info(' --------> SECQ == RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA))
                
                #-------------------------------------------------------------------------------------
                # Initialize data array
                if a2dDataSECQ_TS_SAVE == None:
                    iTimeN = len(oWorkspace_INFO[sRun_DATA]['Section_Q']['FileTime_ARC'])
                    iEnsN = len(oWorkspace_DATA.keys())
                    a2dDataSECQ_TS_SAVE = np.zeros([iEnsN, iTimeN]); a2dDataSECQ_TS_SAVE[:] = -9998.0
                else:
                    pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Initialize data array
                if a1dObsSECQ_TS_SAVE == None:
                    iTimeN = len(oWorkspace_INFO[sRun_DATA]['Section_Q']['FileTime_ARC'])
                else:
                    pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Initialize filename warnings
                if not (sFilePathSECQ_WS and sFileNameSECQ_WS and sFileNameSECQ_WS_SAVE):
                    sFilePathSECQ_WS = oWorkspace_INFO[sRun_DATA]['Section_Q']['FilePath_WS']
                    sFileNameSECQ_WS = oWorkspace_INFO[sRun_DATA]['Section_Q']['FileName_WS']
                    
                    Lib_Data_IO_Utils.createFolder(sFilePathSECQ_WS)
                    sFileNameSECQ_WS_SAVE = Lib_Data_IO_Utils.defineString(os.path.join(sFilePathSECQ_WS, sFileNameSECQ_WS),
                                                               {'$BASIN': sBasinName, '$SECTION': sSectionName})
                else:
                    pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Initialize filename ts
                if not (sFilePathSECQ_TS and sFileNameSECQ_TS and sFileNameSECQ_TS_SAVE):
                    sFilePathSECQ_TS = oWorkspace_INFO[sRun_DATA]['Section_Q']['FilePath_TS']
                    sFileNameSECQ_TS = oWorkspace_INFO[sRun_DATA]['Section_Q']['FileName_TS']
                    
                    Lib_Data_IO_Utils.createFolder(sFilePathSECQ_TS)
                    sFileNameSECQ_TS_SAVE = Lib_Data_IO_Utils.defineString(os.path.join(sFilePathSECQ_TS, sFileNameSECQ_TS),
                                                               {'$BASIN': sBasinName, '$SECTION': sSectionName})
                else:
                    pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Initialize filename
                if not (sTimeFromSECQ_TS and sTimeToSECQ_TS):
                    try:
                        sTimeFromSECQ_TS = oWorkspace_INFO[sRun_DATA]['Section_Q']['FileTime_ARC'][0]
                        sTimeToSECQ_TS = oWorkspace_INFO[sRun_DATA]['Section_Q']['FileTime_ARC'][-1]
                    except:
                        GetException(' WARNING: SECQ TIMESERIES TimeFrom and TimeTo Undefined!',2,1)
                        sTimeFromSECQ_TS = None; sTimeToSECQ_TS = None;
                else:
                    pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Get ensemble result
                a2dDataSECQ = oWorkspace_DATA[sRun_DATA]['Section_Q']
                a2dObsSECQ = oWorkspace_OBS[sRun_DATA]['Section_Q']
                

                # Check data availability
                try:
                    # Store ensemble result(s)
                    a1dDataSECQ_TS = a2dDataSECQ[:, iSection]
                    # Skip last step to avoid writing issue of wrong integrating value
                    a1dDataSECQ_TS[-1] = -9999.0
                    
                    # Add control to delete NaN value (issue with writing method in hydro model) --> threshold == 10000 m^3/s
                    try:
                        GetException(' WARNING: SECQ TIMESERIES GET Data NOT VALID! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                        a1dDataSECQ_TS = [oF if oF<10000 else -9997.0 for oF in a1dDataSECQ_TS]
                    except:
                        a1dDataSECQ_TS = a1dDataSECQ_TS
                    try:
                        a2dDataSECQ_TS_SAVE[iRun_DATA, :] = a1dDataSECQ_TS
                    except:
                        GetException(' WARNING: SECQ TIMESERIES GET Data WITH DIFFERENT LENGTH! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                        iLenTS = len(a1dDataSECQ_TS)
                        
                        if (iLenTS > iTimeN):
                            a2dDataSECQ_TS_SAVE[iRun_DATA, 0:iTimeN] = a1dDataSECQ_TS[0:iTimeN]
                        else:
                            a2dDataSECQ_TS_SAVE[iRun_DATA, 0:iLenTS] = a1dDataSECQ_TS[0:iLenTS]

                except:
                    
                    GetException(' WARNING: SECQ TIMESERIES GET Data N/A! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                    a1dDataSECQ_TS_NONE = np.zeros([1, iTimeN]); a1dDataSECQ_TS_NONE[:] = -9998.0
                    a2dDataSECQ_TS_SAVE[iRun_DATA, :] = a1dDataSECQ_TS_NONE
                    
                # Check obs availability
                if a1dObsSECQ_TS_SAVE == None:
                    try:
                        # Store ensemble result(s)
                        a1dObsSECQ_TS = a2dObsSECQ[:, iSection]
                        a1dObsSECQ_TS_SAVE = a1dObsSECQ_TS
                        
                    except:
                        GetException(' WARNING: SECQ TIMESERIES GET OBS N/A! RUNTYPE '+ sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                        a1dObsSECQ_TS_SAVE = np.zeros([1, iTimeN]); a1dObsSECQ_TS_SAVE[:] = -9999.0
                else: pass
                #-------------------------------------------------------------------------------------
            #-------------------------------------------------------------------------------------

            #-------------------------------------------------------------------------------------
            # Save data in selected format
            if len(a2dDataSECQ_TS_SAVE) > 0:
                
                dDataSECQ_TS_MAX = np.max(a2dDataSECQ_TS_SAVE);
                
                if dSectionQAlarm > 0:
                    a2iIndexAlarm = np.where(a2dDataSECQ_TS_SAVE >= dSectionQAlarm)
                else:
                    a2iIndexAlarm = ( np.array([]), np.array([]) )
                
                if dSectionQAlert > 0:
                    a2iIndexAlert = np.where(a2dDataSECQ_TS_SAVE >= dSectionQAlert)
                else:
                    a2iIndexAlert = ( np.array([]), np.array([]) )
                    
                # Check alarm
                if len(a2iIndexAlarm[0]) == 0:
                    sThrAlarm = 'FALSE'
                else:
                    sThrAlarm = 'TRUE'
                    
                # Check alert
                if len(a2iIndexAlert[0]) == 0:
                    sThrAlert = 'FALSE'
                else:
                    sThrAlert = 'TRUE'
                
                # Compose warning line for each section
                sWarningLine = (sBasinName + ' ' + sSectionName + ' ' + str(dDataSECQ_TS_MAX) + ' ' +
                                str(dSectionQAlarm) + ' ' + sThrAlarm + ' ' + 
                                str(dSectionQAlert) + ' ' + sThrAlert)
                
            else:
                GetException(' WARNING: SECQ WARNING CHECKING N/A! RUNTYPE '+ sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                sWarningLine = (sBasinName +' '+ sSectionName +' NONE NONE NONE NONE NONE')
            
            # Store warnings
            oSecWarning.append(sWarningLine)
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Save data in selected format
            if len(a2dDataSECQ_TS_SAVE) > 0:
                Lib_Data_IO_Dewetra.saveTimeSeries(sFileNameSECQ_TS_SAVE, 
                                                   a2dDataSECQ_TS_SAVE, a1dObsSECQ_TS_SAVE, 
                                                   sTimeFromSECQ_TS, sTimeNow,
                                                   sRunDescription, 
                                                   iTimeStep/60, iEnsN)
            else:
                GetException(' WARNING: SECQ TIMESERIES SAVE Data N/A! RUNTYPE ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
            #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Save data warnings in selected format
        if len(oSecWarning) > 0:
            sLineHeader = 'Basin Section QMaxSim QAlarm Alarm QAlert Alert'
            Lib_Data_IO_Dewetra.saveWarnings(sFileNameSECQ_WS_SAVE, 
                                       sLineHeader, oSecWarning, 
                                       sTimeFromSECQ_TS, sTimeToSECQ_TS, sTimeNow,
                                       sRunDescription, iEnsN)
        else:
            GetException(' WARNING: SECQ WARNINGS SAVE Data N/A! RUNTYPE ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cycle(s) on dam(s)
        for iDam, oDam in enumerate(oWorkspace_DAM):
            
            #-------------------------------------------------------------------------------------
            # Get section and basin information
            sDamName = str(oDam[2]); sIntakeName = str(oDam[3])
            oLogStream.info(' --------> DAMV_DAML == DAM: ' + sDamName + ' - INTAKE: ' + sIntakeName + ' -----------------' )
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Get and read ensemble result(s)
            a2dDataDAMV_TS_SAVE = None; a2dDataDAML_TS_SAVE = None;
            a1dObsDAMV_TS_SAVE = None; a1dObsDAML_TS_SAVE = None
            sFileNameDAMV_TS_SAVE = None;  sFileNameDAML_TS_SAVE = None
            sFilePathDAMV_TS = None; sFileNameDAMV_TS = None;
            sFilePathDAML_TS = None; sFileNameDAML_TS = None;
            sTimeFromDAMV_TS = None; sTimeToDAMV_TS = None
            sTimeFromDAML_TS = None; sTimeToDAML_TS = None
            for iRun_DATA, sRun_DATA in enumerate(oWorkspace_DATA):
                
                oLogStream.info(' --------> DAMV_DAML == RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA))
                
                #-------------------------------------------------------------------------------------
                # Initialize data array
                if a2dDataDAMV_TS_SAVE == None:
                    iTimeN = len(oWorkspace_INFO[sRun_DATA]['Dam_V']['FileTime_ARC'])
                    iEnsN = len(oWorkspace_DATA.keys())
                    a2dDataDAMV_TS_SAVE = np.zeros([iEnsN, iTimeN]); a2dDataDAMV_TS_SAVE[:] = -9998.0
                else:
                    pass
                if a2dDataDAML_TS_SAVE == None:
                    iTimeN = len(oWorkspace_INFO[sRun_DATA]['Dam_L']['FileTime_ARC'])
                    iEnsN = len(oWorkspace_DATA.keys())
                    a2dDataDAML_TS_SAVE = np.zeros([iEnsN, iTimeN]); a2dDataDAML_TS_SAVE[:] = -9998.0
                else:
                    pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Initialize data array
                if a1dObsDAMV_TS_SAVE == None:
                    iTimeN = len(oWorkspace_INFO[sRun_DATA]['Dam_V']['FileTime_ARC'])
                else:
                    pass
                if a1dObsDAML_TS_SAVE == None:
                    iTimeN = len(oWorkspace_INFO[sRun_DATA]['Dam_L']['FileTime_ARC'])
                else:
                    pass
                #-------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Initialize filename
                if not (sFilePathDAMV_TS and sFileNameDAMV_TS and sFileNameDAMV_TS_SAVE):
                    sFilePathDAMV_TS = oWorkspace_INFO[sRun_DATA]['Dam_V']['FilePath_TS']
                    sFileNameDAMV_TS = oWorkspace_INFO[sRun_DATA]['Dam_V']['FileName_TS']
                    
                    Lib_Data_IO_Utils.createFolder(sFilePathDAMV_TS)
                    sFileNameDAMV_TS_SAVE = Lib_Data_IO_Utils.defineString(os.path.join(sFilePathDAMV_TS, sFileNameDAMV_TS),
                                                               {'$DAM': sDamName, '$INTAKE': sIntakeName})
                else:
                    pass
                if not (sFilePathDAML_TS and sFileNameDAML_TS and sFileNameDAML_TS_SAVE):
                    sFilePathDAML_TS = oWorkspace_INFO[sRun_DATA]['Dam_L']['FilePath_TS']
                    sFileNameDAML_TS = oWorkspace_INFO[sRun_DATA]['Dam_L']['FileName_TS']
                    
                    Lib_Data_IO_Utils.createFolder(sFilePathDAML_TS)
                    sFileNameDAML_TS_SAVE = Lib_Data_IO_Utils.defineString(os.path.join(sFilePathDAML_TS, sFileNameDAML_TS),
                                                               {'$DAM': sDamName, '$INTAKE': sIntakeName})
                else:
                    pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Initialize time from and to
                if not (sTimeFromDAMV_TS and sTimeToDAMV_TS):
                    try:
                        sTimeFromDAMV_TS = oWorkspace_INFO[sRun_DATA]['Dam_V']['FileTime_ARC'][0]
                        sTimeToDAMV_TS = oWorkspace_INFO[sRun_DATA]['Dam_V']['FileTime_ARC'][-1]
                    except:
                        GetException(' WARNING: DAMV TIMESERIES TimeFrom and TimeTo Undefined!',2,3)
                        sTimeFromDAMV_TS = None; sTimeToDAMV_TS = None;
                else:
                    pass
                if not (sTimeFromDAML_TS and sTimeToDAML_TS):
                    try:
                        sTimeFromDAML_TS = oWorkspace_INFO[sRun_DATA]['Dam_L']['FileTime_ARC'][0]
                        sTimeToDAML_TS = oWorkspace_INFO[sRun_DATA]['Dam_L']['FileTime_ARC'][-1]
                    except:
                        GetException(' WARNING: DAML TIMESERIES TimeFrom and TimeTo Undefined!',2,3)
                        sTimeFromDAML_TS = None; sTimeToDAML_TS = None;
                else:
                    pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Get DAMV ensemble result
                a2dDataDAMV = oWorkspace_DATA[sRun_DATA]['Dam_V']
                a2dObsDAMV = oWorkspace_OBS[sRun_DATA]['Dam_V']
                try:
                    # Store ensemble result(s)
                    a1dDataDAMV_TS = a2dDataDAMV[:, iDam]
                    # Skip last step to avoid writing issue of wrong integrating value
                    a1dDataDAMV_TS[-1] = -9999.0
                    
                    try:
                        a2dDataDAMV_TS_SAVE[iRun_DATA, :] = a1dDataDAMV_TS
                    except:
                        GetException(' WARNING: DAMV TIMESERIES GET Data WITH DIFFERENT LENGTH! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                        iLenTS = len(a1dDataDAMV_TS)
                        
                        if (iLenTS > iTimeN):
                            a2dDataDAMV_TS_SAVE[iRun_DATA, 0:iTimeN] = a1dDataDAMV_TS[0:iTimeN]
                        else:
                            a2dDataDAMV_TS_SAVE[iRun_DATA, 0:iLenTS] = a1dDataDAMV_TS[0:iLenTS]
                        
                except:
                    GetException(' WARNING: DAMV TIMESERIES GET Data N/A! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                    a1dDataDAMV_TS_NONE = np.zeros([1, iTimeN]); a1dDataDAMV_TS_NONE[:] = -9998.0
                    a2dDataDAMV_TS_SAVE[iRun_DATA, :] = a1dDataDAMV_TS_NONE

                    
                # Check obs availability
                if a1dObsDAMV_TS_SAVE == None:
                    try:
                        # Store ensemble result(s)
                        a1dObsDAMV_TS = a2dObsDAMV[:, iDam]
                        a1dObsDAMV_TS_SAVE = a1dObsDAMV_TS
                    except:
                        GetException(' WARNING: DAMV TIMESERIES GET OBS N/A! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                        a1dObsDAMV_TS_SAVE = np.zeros([1, iTimeN]); a1dObsDAMV_TS_SAVE[:] = -9999.0
                else:pass
                    
                # Get DAML ensemble result
                a2dDataDAML = oWorkspace_DATA[sRun_DATA]['Dam_L']
                a2dObsDAML = oWorkspace_OBS[sRun_DATA]['Dam_L']
                try:
                    # Store ensemble result(s)
                    a1dDataDAML_TS = a2dDataDAML[:, iDam]
                    # Skip last step to avoid writing issue of wrong integrating value
                    a1dDataDAML_TS[-1] = -9999.0
                    
                    try:
                        a2dDataDAML_TS_SAVE[iRun_DATA, :] = a1dDataDAML_TS
                    
                    except:
                        GetException(' WARNING: DAML TIMESERIES GET Data WITH DIFFERENT LENGTH! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                        iLenTS = len(a1dDataDAML_TS)
                        
                        if (iLenTS > iTimeN):
                            a2dDataDAML_TS_SAVE[iRun_DATA, 0:iTimeN] = a1dDataDAML_TS[0:iTimeN]
                        else:
                            a2dDataDAML_TS_SAVE[iRun_DATA, 0:iLenTS] = a1dDataDAML_TS[0:iLenTS]
                        
                except:

                    GetException(' WARNING: DAML TIMESERIES GET Data N/A! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                    a1dDataDAML_TS_NONE = np.zeros([1, iTimeN]); a1dDataDAML_TS_NONE[:] = -9998.0
                    a2dDataDAML_TS_SAVE[iRun_DATA, :] = a1dDataDAML_TS_NONE
                    
                # Check obs availability
                if a1dObsDAML_TS_SAVE == None:
                    try:
                        # Store ensemble result(s)
                        a1dObsDAML_TS = a2dObsDAML[:, iDam]
                        a1dObsDAML_TS_SAVE = a1dObsDAML_TS
                    except:
                        GetException(' WARNING: DAML TIMESERIES GET OBS N/A! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
                        a1dObsDAML_TS_SAVE = np.zeros([1, iTimeN]); a1dObsDAML_TS_SAVE[:] = -9999.0
                else:pass
                #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Save data DAMV in selected format
            if len(a2dDataDAMV_TS_SAVE) > 0:
                Lib_Data_IO_Dewetra.saveTimeSeries(sFileNameDAMV_TS_SAVE, 
                                                   a2dDataDAMV_TS_SAVE, a1dObsDAMV_TS_SAVE, 
                                                   sTimeFromDAMV_TS, sTimeNow,
                                                   sRunDescription, 
                                                   iTimeStep/60, iEnsN)
            else:
                GetException(' WARNING: DAMV TIMESERIES SAVE Data N/A! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
            
            # Save data DAMV in selected format
            if len(a2dDataDAML_TS_SAVE) > 0:
                    Lib_Data_IO_Dewetra.saveTimeSeries(sFileNameDAML_TS_SAVE, 
                                                       a2dDataDAML_TS_SAVE, a1dObsDAML_TS_SAVE, 
                                                       sTimeFromDAML_TS, sTimeNow,
                                                       sRunDescription, 
                                                       iTimeStep/60, iEnsN)
            else:
                GetException(' WARNING: DAML TIMESERIES SAVE Data N/A! RUN_NAME: ' + sRun_DATA + ' RUN_ID: ' + str(iRun_DATA) ,2,1)
            #-------------------------------------------------------------------------------------
    
        #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------
    # Method to select reference path(s)
    def Builder(self):
        
        #-------------------------------------------------------------------------------------
        # Get run information
        sRunName = self.sRunName
        sDomainName = self.sDomainName

        # Get TimeNow
        sTimeNow = self.oDataInfo.oInfoSettings.oParamsInfo['TimeNow']
        
        # Get static file information
        sFileStaticP = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FileName']
        sPathStaticP = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FilePath']
        oFileVarsP = self.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FileVars']
        #-------------------------------------------------------------------------------------
         
        #-------------------------------------------------------------------------------------
        # Get variable(s) settings
        oData_ARC = self.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic
        oData_TS = self.oDataInfo.oInfoVarDynamic.oDataTimeSeriesDynamic
        oData_WS = self.oDataInfo.oInfoVarDynamic.oDataWarningsDynamic
        
        # Get ensemble information
        oData_ENS = self.oDataEnsemble
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Define SECTION file
        sFileName_SEC = Lib_Data_IO_Utils.defineString(os.path.join(sPathStaticP,sFileStaticP),
                                {'$VAR' : str(oFileVarsP['section']),'$DOMAIN' : sDomainName})
        oFile_SEC = Lib_Data_IO_Dewetra.getData2D(sFileName_SEC)
        oData_SEC = Lib_Data_IO_Dewetra.parseDataSection(oFile_SEC)
        iNum_SEC = len(oData_SEC)
        
        # Define DAM file
        sFileName_DAM = Lib_Data_IO_Utils.defineString(os.path.join(sPathStaticP,sFileStaticP),
                                {'$VAR' : str(oFileVarsP['dam']),'$DOMAIN' : sDomainName})
        # Get DAM data
        oFile_DAM = Lib_Data_IO_Dewetra.getData2D(sFileName_DAM, 2)
        oData_DAM = Lib_Data_IO_Dewetra.parseDataDam(oFile_DAM)
        iNum_DAM = len(oData_DAM)
        
        # Data dimension(s)
        oVar_DIM = {}
        oVar_DIM['Section_Q'] = iNum_SEC; oVar_DIM['Dam_L'] = iNum_DAM;  oVar_DIM['Dam_V'] = iNum_DAM; 
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cycle(s) on run type
        oVarDict = {}
        for sRunType in oData_ENS:
            
            #-------------------------------------------------------------------------------------
            # Get run ID
            sRunID = oData_ENS[sRunType]
            oVarDict[sRunType] = {}
            
            # Data 
            oLogStream.info(' -----> Analyzing RUN: ' + sRunType)
            #-------------------------------------------------------------------------------------

            #-------------------------------------------------------------------------------------
            # Cycle on variable(s)
            for sVar_ARC in oData_ARC:
                
                # Data 
                oLogStream.info(' -----> Anayzing Var: ' + sVar_ARC + ' ... ')
                
                # Initialize dictionary with variable ARC
                oVarDict[sRunType][sVar_ARC] = {}
                
                # Define tags
                oTags = defineTags(sDomainName, sRunName, sRunID, sTimeNow)
                
                # Get archive information
                oVar_ARC = oData_ARC[sVar_ARC]
                # Get var dimension
                iVar_DIM = int(oVar_DIM[sVar_ARC])
                
                # RUN ARCHIVE DATA
                sFilePath_ARC = Lib_Data_IO_Utils.defineString(oVar_ARC['FilePath'], oTags).replace('//', '/');
                sFileExt_ARC = os.path.splitext(oVar_ARC['FileName'])[-1];
                # RUN ARCHIVE HISTORY DATA
                try:
                    sFilePath_ARC_HIS = Lib_Data_IO_Utils.defineString(oVar_ARC['FilePathHistory'], oTags).replace('//', '/');
                    sFileExt_ARC_HIS = os.path.splitext(oVar_ARC['FileNameHistory'])[-1];
                except:
                    sFilePath_ARC_HIS = ''; sFileExt_ARC_HIS = ''
                # OBSERVED DATA
                try:
                    sFilePath_OBS_RAW = oVar_ARC['FilePathObs']
                    sFileName_OBS_RAW = oVar_ARC['FileNameObs']
                except:
                    sFilePath_OBS_RAW = ''; sFileName_OBS_RAW = ''
                
                # Get ws information
                try:
                    oVar_WS = oData_WS[sVar_ARC]
                    sFilePath_WS = Lib_Data_IO_Utils.defineString(oVar_WS['FilePath'], oTags).replace('//', '/');
                    sFileName_WS = Lib_Data_IO_Utils.defineString(oVar_WS['FileName'], oTags).replace('//', '/');
                except:
                    oVar_WS = None; sFilePath_WS = ''; sFileName_WS = '';
                    
                # Get ts information
                oVar_TS = oData_TS[sVar_ARC]
                sFilePath_TS = Lib_Data_IO_Utils.defineString(oVar_TS['FilePath'], oTags).replace('//', '/');
                sFileName_TS = Lib_Data_IO_Utils.defineString(oVar_TS['FileName'], oTags).replace('//', '/');
                
                # Search all file ARC HISTORY
                a1oFileList_ARC_HIS = []; a1oFileTime_ARC_HIS = [];
                if os.path.exists(sFilePath_ARC_HIS):
                    for sFileName_ARC_HIS in glob.glob(sFilePath_ARC_HIS + '*' + sFileExt_ARC_HIS):
                        a1oFileList_ARC_HIS.append(sFileName_ARC_HIS)
                        
                        # Get time from file
                        oMatch = re.search(r'\d{4}\d{2}\d{2}\d{2}\d{2}', sFileName_ARC_HIS)
                        sTime = oMatch.group();
                        oTime = datetime.datetime.strptime(oMatch.group(), '%Y%m%d%H%M')
                        a1oFileTime_ARC_HIS.append(sTime)
                    
                    # Save filename and time
                    a1oFileList_ARC_HIS = sorted(a1oFileList_ARC_HIS)
                    a1oFileTime_ARC_HIS = sorted(a1oFileTime_ARC_HIS)
                    
                else:
                    GetException(' WARNING: file archive point history not available: ' + sFilePath_ARC_HIS ,2,1)
                    a1oFileTime_ARC_HIS = []; a1oFileList_ARC_HIS = []
                
                # Search all file ARC
                a1oFileList_ARC = []; a1oFileTime_ARC = [];
                if os.path.exists(sFilePath_ARC):
                    for sFileName_ARC in glob.glob(sFilePath_ARC + '*' + sFileExt_ARC):
                        a1oFileList_ARC.append(sFileName_ARC)
                        
                        # Get time from file
                        oMatch = re.search(r'\d{4}\d{2}\d{2}\d{2}\d{2}', sFileName_ARC)
                        sTime = oMatch.group();
                        oTime = datetime.datetime.strptime(oMatch.group(), '%Y%m%d%H%M')
                        a1oFileTime_ARC.append(sTime)
                    
                    # Save filename and time
                    a1oFileList_ARC = sorted(a1oFileList_ARC)
                    a1oFileTime_ARC = sorted(a1oFileTime_ARC)
                    
                else:
                    GetException(' WARNING: file archive point not available: ' + sFilePath_ARC ,2,1)
                    a1oFileTime_ARC = []; a1oFileList_ARC = []
                
                # Merge ARCHIVE and ARCHIVE HISTORY STEPS
                a1oFileTime_ARC_TOT = []; a1oFileList_ARC_TOT = []
                if (a1oFileList_ARC_HIS > 0):
                    a1oFileTime_ARC_NCommon = sorted(list(set(a1oFileTime_ARC_HIS) - set(a1oFileTime_ARC)))
                    a1oFileTime_ARC_Common = sorted(list(set(a1oFileTime_ARC).intersection(a1oFileTime_ARC_HIS)))
                    
                    a1oFileTime_ARC_HIS_SEL = []; a1oFileList_ARC_HIS_SEL = []
                    for sFileTime_ARC_NCommon in a1oFileTime_ARC_NCommon:
                        a1oFileTime_ARC_HIS_SEL.append(a1oFileTime_ARC_HIS[a1oFileTime_ARC_HIS.index(sFileTime_ARC_NCommon)])
                        a1oFileList_ARC_HIS_SEL.append(a1oFileList_ARC_HIS[a1oFileTime_ARC_HIS.index(sFileTime_ARC_NCommon)])
                    
                    a1oFileTime_ARC_TOT = sorted(a1oFileTime_ARC + a1oFileTime_ARC_HIS_SEL)
                    a1oFileList_ARC_TOT = sorted(a1oFileList_ARC + a1oFileList_ARC_HIS_SEL)
                
                else:
                    GetException(' WARNING: file archive point list empty' ,2,1)
                    a1oFileTime_ARC_TOT = sorted(a1oFileTime_ARC)
                    a1oFileList_ARC_TOT = sorted(a1oFileList_ARC)
                
                # Check time now and file found in time series ARC
                oTimeNow = datetime.datetime.strptime(sTimeNow,'%Y%m%d%H%M')
                try:
                    oTimeSeriesFirst = datetime.datetime.strptime(a1oFileTime_ARC_TOT[0],'%Y%m%d%H%M')
                    if oTimeNow == oTimeSeriesFirst:
                        GetException(' WARNING: TIMESERIESFIRST == TIMENOW (' + sVar_ARC + ')' ,2,1)
                        GetException(' WARNING: No history data available --> TIMENOW = TIMESERIESFIRST',2,1)
                    elif oTimeNow < oTimeSeriesFirst:
                        GetException(' WARNING: TIMESERIESFIRST >= TIMENOW (' + sVar_ARC + ')' ,2,1)
                        GetException(' WARNING: No history data available --> TIMENOW = TIMESERIESFIRST',2,1)
                        sTimeNowUpd = oTimeSeriesFirst.strftime('%Y%m%d%H%M')
                        self.oDataInfo.oInfoSettings.oParamsInfo['TimeNow'] = sTimeNowUpd
                    else:
                        pass
                except:
                    GetException(' WARNING: TIMESERIESFIRST NOT FOUND! CHECK YOUR RUN!',2,1)
                    oTimeSeriesFirst = None
                    
                # Search all file OBS (using ARCH TOT time information)
                a1oFileTime_OBS_STEP = []; a1oFileList_OBS_STEP = []; a1oFileTime_OBS_TOT = []; a1oFileList_OBS_TOT = []
                for sFileTime_OBS_STEP in a1oFileTime_ARC_TOT:
                    
                    # Get time information
                    sFileYear = sFileTime_OBS_STEP[0:4]; sFileMonth = sFileTime_OBS_STEP[4:6]; sFileDay = sFileTime_OBS_STEP[6:8];
                    sFileHH = sFileTime_OBS_STEP[8:10]; sFileMM = sFileTime_OBS_STEP[10:12];
                    
                    # Define tags as a function of time step
                    oTags_STEP = oTags
                    oTags_STEP['$yyyy'] = sFileYear
                    oTags_STEP['$mm'] = sFileMonth
                    oTags_STEP['$dd'] = sFileDay
                    oTags_STEP['$HH'] = sFileHH
                    oTags_STEP['$MM'] = sFileMM
                    
                    sFilePath_OBS_STEP = Lib_Data_IO_Utils.defineString(sFilePath_OBS_RAW, oTags_STEP).replace('//', '/');
                    sFileName_OBS_STEP = Lib_Data_IO_Utils.defineString(sFileName_OBS_RAW, oTags_STEP)
                    
                    if os.path.exists(os.path.join(sFilePath_OBS_STEP,sFileName_OBS_STEP)):
                        
                        a1oFileList_OBS_STEP.append(os.path.join(sFilePath_OBS_STEP, sFileName_OBS_STEP))
                        a1oFileTime_OBS_STEP.append(sFileTime_OBS_STEP)
                        
                    else:
                        #GetException(' WARNING: file archive point obs not available: ' + os.path.join(sFilePath_OBS_STEP,sFileName_OBS_STEP) ,2,1)
                        a1oFileList_OBS_STEP.append(None)
                        a1oFileTime_OBS_STEP.append(sFileTime_OBS_STEP)
                
                try:
                    # Set time information
                    a1oFile_OBS_TOT = zip(a1oFileTime_OBS_STEP, a1oFileList_OBS_STEP)
                    a1oFile_OBS_TOT = sorted(a1oFile_OBS_TOT, key=itemgetter(0))
                    
                    [a1oFileTime_OBS_TOT, a1oFileList_OBS_TOT] = zip(*a1oFile_OBS_TOT)
                    a1oFileTime_OBS_TOT = list(a1oFileTime_OBS_TOT)
                    a1oFileList_OBS_TOT = list(a1oFileList_OBS_TOT)
     
                    # Save variable information
                    oVarDict[sRunType][sVar_ARC]['FilePath_ARC'] = sFilePath_ARC
                    oVarDict[sRunType][sVar_ARC]['FileList_ARC'] = a1oFileList_ARC_TOT
                    oVarDict[sRunType][sVar_ARC]['FileTime_ARC'] = a1oFileTime_ARC_TOT
                    oVarDict[sRunType][sVar_ARC]['FileList_OBS'] = a1oFileList_OBS_TOT
                    oVarDict[sRunType][sVar_ARC]['FileTime_OBS'] = a1oFileTime_OBS_TOT
                    oVarDict[sRunType][sVar_ARC]['FilePath_TS'] = sFilePath_TS
                    oVarDict[sRunType][sVar_ARC]['FileName_TS'] = sFileName_TS
                    oVarDict[sRunType][sVar_ARC]['FilePath_WS'] = sFilePath_WS
                    oVarDict[sRunType][sVar_ARC]['FileName_WS'] = sFileName_WS
                    oVarDict[sRunType][sVar_ARC]['Data_DIM'] = iVar_DIM
                    
                    # Exit info
                    oLogStream.info(' -----> Anayzing Var: ' + sVar_ARC + ' ... OK')
                    
                except:
                    
                    # Save variable information
                    oVarDict[sRunType][sVar_ARC]['FilePath_ARC'] = None
                    oVarDict[sRunType][sVar_ARC]['FileList_ARC'] = None
                    oVarDict[sRunType][sVar_ARC]['FileTime_ARC'] = None
                    oVarDict[sRunType][sVar_ARC]['FileList_OBS'] = None
                    oVarDict[sRunType][sVar_ARC]['FileTime_OBS'] = None
                    oVarDict[sRunType][sVar_ARC]['FilePath_TS'] = None
                    oVarDict[sRunType][sVar_ARC]['FileName_TS'] = None
                    oVarDict[sRunType][sVar_ARC]['FilePath_WS'] = None
                    oVarDict[sRunType][sVar_ARC]['FileName_WS'] = None
                    oVarDict[sRunType][sVar_ARC]['Data_DIM'] = None
                
                    # Exit info
                    oLogStream.info(' -----> Anayzing Var: ' + sVar_ARC + ' ... FAILED')
                    GetException(' WARNING: Analyzing Var NOT FOUND! CHECK YOUR RUN! (RUNNAME: '+sRunType+')',2,1)

            #-------------------------------------------------------------------------------------
                            
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Save variable(s) information to workspace
        self.oWorkspaceDam = oData_DAM
        self.oWorkspaceSection = oData_SEC
        self.oWorkspaceInfo = oVarDict
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------
    
    
     
     
     
    
    
    
