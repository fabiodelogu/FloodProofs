"""
Class Features

Name:          Drv_Model_HMC_IO
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151022'
Version:       '1.6.2'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os, csv, shutil, collections, datetime, time
import numpy as np

from random import randint
from operator import itemgetter
from itertools import groupby

import Lib_Data_IO_Utils as Lib_Data_IO_Utils

from Drv_Data_Zip import Drv_Data_Zip
from Drv_Data_IO import Drv_Data_IO

from GetGeoData import GetGeoData
from GetException import GetException

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Drv_Model_HMC_IO:

    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, sFileName, oSettings, oGeoInfo=None):

        # Global variable(s)
        self.sFilePath = os.path.split(sFileName)[0]
        self.sFileName = os.path.split(sFileName)[1]
        self.oSettings = oSettings
        self.oGeoInfo = oGeoInfo

        # Define filename 
        self.sFileNameExt, self.bFileNameZip = Drv_Data_Zip.removeZipExt(self.sFileName)
        
        # Select type file
        self.iTypeFile = np.nan
        if self.sFileNameExt.endswith('nc'):
            self.iTypeFile = 1;
        elif self.sFileNameExt.endswith('bin'):
            self.iTypeFile = 2      
        elif self.sFileNameExt.endswith('txt'):
            self.iTypeFile = 3     
        else:
            GetException(' -----> ERROR: undefined file input! Check your input file(s)',1,1)
    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------
    # Method to remove file from OUT folder (to avoid overwriting issue)
    def deleteModelData(self, sPathName_OUT, sFileName_OUT, sZipExt=None):
    
        if not sZipExt:
            sZipExt = '';
        else:pass
        
        sFileName_DEST = os.path.join(sPathName_OUT, sFileName_OUT + sZipExt)
        
        if os.path.exists(sFileName_DEST):
            os.remove(sFileName_DEST)
        else:pass
        
    #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------
    # Method to copy file from IN to OUT folder
    def copyModelData(self, sPathName_OUT, sFileName_OUT=None, sZipExt=None):
        
        if not sZipExt:
            sZipExt = '';
        
        # Check file type
        if (self.iTypeFile == 1):
        
            # Get IN information
            sPathName_IN = self.sFilePath; sFileName_IN = self.sFileName
            
            # Check if filename IN exists
            if os.path.exists(os.path.join(sPathName_IN, sFileName_IN + sZipExt)):
                
                # Define file SRC
                sFileName_SRC = os.path.join(sPathName_IN, sFileName_IN + sZipExt)
                
                # Check if DEST folder exists
                if not os.path.exists(sPathName_OUT):
                    os.makedirs(sPathName_OUT)
                else:
                    pass
                
                # Define file DEST
                if sFileName_OUT:
                    sFileName_DEST = os.path.join(sPathName_OUT, sFileName_OUT + sZipExt)
                else:
                    sFileName_DEST = os.path.join(sPathName_OUT, sFileName_IN + sZipExt)
                
                # Copy file from SRC to DEST
                shutil.copyfile(sFileName_SRC, sFileName_DEST)
                
            else:
                GetException(' -----> WARNING: gridded model file does not exist! Check your filesystem!',2,1)
                
        elif (self.iTypeFile == 3):
        
            # Get IN information
            sPathName_IN = self.sFilePath; sFileName_IN = self.sFileName
            
            # Check if filename IN exists
            if os.path.exists(os.path.join(sPathName_IN, sFileName_IN + sZipExt)):
                
                # Define file SRC
                sFileName_SRC = os.path.join(sPathName_IN, sFileName_IN + sZipExt)
                
                # Check if DEST folder exists
                if not os.path.exists(sPathName_OUT):
                    os.makedirs(sPathName_OUT)
                else:
                    pass
                
                # Define file DEST
                if sFileName_OUT:
                    sFileName_DEST = os.path.join(sPathName_OUT, sFileName_OUT + sZipExt )
                else:
                    sFileName_DEST = os.path.join(sPathName_OUT, sFileName_IN + sZipExt)
                
                # Copy file from SRC to DEST
                shutil.copyfile(sFileName_SRC, sFileName_DEST)
                
            else:
                GetException(' -----> WARNING: point model file does not exist! Check your filesystem!',2,1)
        
        else:
            GetException(' -----> WARNING: incorrect filetype I/O for gridded/point model file! Check your settings!',2,1)
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to get data 2D from output file
    def getModelData2D(self):
        
        # Initialize variable
        oTableData = np.array([]);
        
        # Check file type
        if (self.iTypeFile == 3):
        
            # Check file availability
            if os.path.exists(os.path.join(self.sFilePath, self.sFileName)):
            
                # Open ascii file
                oFile = open(os.path.join(self.sFilePath, self.sFileName), 'r')
                # Read data
                oTableData = [sRow.strip().split('\t') for sRow in oFile]
                
            else:
                GetException(' -----> WARNING: model file 2D does not exist! Check your filesystem!',2,1)
                oTableData = np.array([]);
        else:
            GetException(' -----> WARNING: incorrect type input for 2D model file! Check your settings!',2,1)
            oTableData = np.array([]);
            
        # Return variable
        return oTableData
            
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to get data 1D from output file
    def getModelData1D(self):
        
        # Initialize variable
        oVarData = np.array([]); 
        
        # Check file type
        if (self.iTypeFile == 3):
        
            # Check file availability
            if os.path.exists(os.path.join(self.sFilePath, self.sFileName)):
            
                # Open ascii file
                oFile = open(os.path.join(self.sFilePath, self.sFileName), 'r')
                # Read data
                oVarData = np.loadtxt(oFile, skiprows=0)
            
            else:
                GetException(' -----> WARNING: model file 1D does not exist! Check your filesystem!',2,1)
                oVarData = np.array([]);
        else:
            GetException(' -----> WARNING: incorrect type input for 1D model file! Check your settings!',2,1)
            oVarData = np.array([]);
        
        # Return variable
        return oVarData

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to save data 1D in specified format
    def saveModelData1D(self, 
                        a1dDataModel=None, a1dDataObs=None, 
                        sTimeFrom=None, sTimeNow=None,
                        sRunType=None, 
                        iTimeRes=0, iEnsN=0):
        
        # Define filename
        sFileName = os.path.join(self.sFilePath, self.sFileName)
        
        # Convert array from float to string
        a1sDataObs = a1dDataObs.tolist()
        a1sDataModel = a1dDataModel.tolist()
        
        # Save update information
        oModelData = {}
        
        # Flag information
        oModelData['Line_01'] = 'Procedure='+ str(sRunType) + ' \n'
        oModelData['Line_02'] = 'DateMeteoModel='+ str(sTimeNow) + ' \n'
        oModelData['Line_03'] = 'DateStart='+ str(sTimeFrom) + ' \n'
        oModelData['Line_04'] = 'Temp.Resolution='+ str(iTimeRes) + ' \n'
        oModelData['Line_05'] = 'SscenariosNumber='+ str(int(iEnsN)) + ' \n'
        oModelData['Line_06'] = (' '.join(map(str, a1sDataObs[0]))) + ' \n'
        oModelData['Line_07'] = (' '.join(map(str, a1sDataModel[0]))) + ' \n'
        
        # Dictionary sorting
        oModelDataOrd = collections.OrderedDict(sorted(oModelData.items()))
        
        # Open ASCII file (to save all data)
        oFileHandler = open(sFileName,'w');
        
        # Write data in ASCII file
        oFileHandler.writelines(oModelDataOrd.values())
        # Close ASCII file
        oFileHandler.close()
        
    #-------------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------------
    # Method to parse info file
    def parseInfoData(self, oFIData, oFIKeysUpd):
        
        #------------------------------------------------------------------------------------- 
        # Cycling to update value from settings file
        iL = 0; oInfoUpd = {};
        for sLineData in oFIData.values():
            
            sLineDataTest = sLineData.strip()
            
            if sLineDataTest:
                if not (sLineDataTest.startswith('!') or sLineDataTest.startswith('&') or sLineDataTest.startswith('/')):
                    
                    #print(sLineData)
                    
                    sKey, sValue = sLineData.split('=')
                    sKey = str(sKey.replace(' ', ''))
                    
                    if sKey in oFIKeysUpd.keys():
                        
                        # Get new value
                        oValue = oFIKeysUpd[sKey];
                        
                        sValue = ''
                        if isinstance(oValue, basestring):
                            sValue = str(oValue)
                        elif isinstance(oValue, np.float):
                            sValue = str(np.float32(oValue))
                        elif isinstance(oValue, np.int):
                            sValue = str(np.int32(oValue))
                        elif isinstance(oValue, list):
                            sValue = str(oValue).strip('[]')
                        else:
                            GetException(' -----> ERROR: incorrect type input!',1,1)
                        
                        # Update line
                        sLineDataUpdate = sKey + ' = ' + sValue;

                    else: 
                        sLineDataUpdate = sLineDataTest
                else:
                    # No update line
                    sLineDataUpdate = sLineDataTest
            else:
                # Empty line
                sLineDataUpdate = ''
            
            oInfoUpd[iL] = sLineDataUpdate + '\n'
            iL = iL + 1
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Return data
        return oInfoUpd
        #-------------------------------------------------------------------------------------
        
    #-------------------------------------------------------------------------------------
    
    #------------------------------------------------------------------------------------- 
    # Method to get info file updated dynamically fields
    def updateInfoData(self, oDataInfo, oDataTime, oDataStatic, oRunTags, oFileHistory):
        
        #-------------------------------------------------------------------------------------
        # Get data history
        oDataTimeStepHistory = oFileHistory[0]
        oDataTypeHistory = oFileHistory[1]
        oDataTimeRefHistory = oFileHistory[2]
        oDataStatusHistory = oFileHistory[4]
        oDataTypeElabHistory = oFileHistory[5]
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # To find skipped data
        a1oDataSkipTotal = []; a1oDataSkipConsecutive = []
        a1oDataSkipTotal = [iI for iI, sX in enumerate(oDataStatusHistory) if sX == "Skip"]
        
        for iK, sG in groupby(enumerate(a1oDataSkipTotal), lambda (iK,iX):iK-iX):
            a1oDataSkipConsecutive = map(itemgetter(1), sG)
        if a1oDataSkipConsecutive:
            a1oDataSkipDiff = list(set(a1oDataSkipTotal) - set(a1oDataSkipConsecutive))
        else:
            a1oDataSkipDiff = []
        
        if not a1oDataSkipDiff:
        
            try:
                iDataSkipStart = min(a1oDataSkipTotal)
            except:
                iDataSkipStart = None
                
            if iDataSkipStart != None:
                oDataTimeStepSelect = oDataTimeStepHistory[0:iDataSkipStart]
                oDataTypeSelect = oDataTypeHistory[0:iDataSkipStart]
                oDataTimeRefSelect = oDataTimeRefHistory[0:iDataSkipStart]
                oDataStatusSelect = oDataStatusHistory[0:iDataSkipStart]
                oDataTypeElabSelect = oDataTypeElabHistory[0:iDataSkipStart]
            else:
                oDataTimeStepSelect = oDataTimeStepHistory
                oDataTypeSelect = oDataTypeHistory
                oDataTimeRefSelect = oDataTimeRefHistory
                oDataStatusSelect = oDataStatusHistory
                oDataTypeElabSelect = oDataTypeElabHistory
        else:
            
            oDataTimeStepSelect = oDataTimeStepHistory
            oDataTypeSelect = oDataTypeHistory
            oDataTimeRefSelect = oDataTimeRefHistory
            oDataStatusSelect = oDataStatusHistory
            oDataTypeElabSelect = oDataTypeElabHistory
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get info structure
        oInfoParams = oDataInfo.oInfoSettings.oParamsInfo
        oInfoPath = oDataInfo.oInfoSettings.oPathInfo
        
        # Get data structure(s)
        oSI_G = oDataInfo.oInfoVarStatic.oDataInputStatic['Gridded']
        oSI_P = oDataInfo.oInfoVarStatic.oDataInputStatic['Point']
        oDI_G = oDataInfo.oInfoVarDynamic.oDataInputDynamic['Gridded']
        oDI_P = oDataInfo.oInfoVarDynamic.oDataInputDynamic['Point']
        oDO_G = oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Gridded']
        oDO_P = oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Point']
        oDS_G = oDataInfo.oInfoVarDynamic.oDataStateDynamic['Gridded']
        oDS_P = oDataInfo.oInfoVarDynamic.oDataStateDynamic['Point']
        oDR_G = oDataInfo.oInfoVarDynamic.oDataRestartDynamic['Gridded']
        oDR_P = oDataInfo.oInfoVarDynamic.oDataRestartDynamic['Point']
        
        # Get params
        sRunName = oInfoParams['RunName']
        sDomainName = oInfoParams['DomainName']
        sTimeCheck = oInfoParams['TimeCheck']
        sTimeNow = oInfoParams['TimeNow']
        iTimeStep = int(oInfoParams['TimeStep'])
        iTimePeriodObs = int(oInfoParams['TimePeriodObs'])
        iTimePeriodFor = int(oInfoParams['TimePeriodFor'])
        
        # Get model flags
        oInfoFlag = oInfoParams['RunFlag']
        iFlagOS = oInfoFlag['flag_os']
        iFlagRestart = oInfoFlag['flag_restart']
        iFlagDeepFlow = oInfoFlag['flag_flowdeep']
        iFlagS = oInfoFlag['flag_S']
        iFlagO = oInfoFlag['flag_O']
        iFlagDtPhysConv = oInfoFlag['flag_dtphysconv']
        iFlagSnow = oInfoFlag['flag_snow']
        iFlagSnowAssim = oInfoFlag['flag_snow_assim']
        iFlagUc = oInfoFlag['flag_uc']
        iFlagDebugSet = oInfoFlag['flag_debugset']
        iFlagDebugLevel = oInfoFlag['flag_debuglevel']
        iFlagLAI = oInfoFlag['flag_LAI']
        iFlagAlbedo = oInfoFlag['flag_albedo']
        
        # Get model dt
        oInfoDt = oInfoParams['RunDt']
        iDtModel = oInfoDt['dt_model']
        iDtPhysConv = oInfoDt['dt_physconv']
        # Get model other info
        oInfoDt = oInfoParams['RunOtherInfo']
        iScaleFactor = oInfoDt['scale_factor']
        iTcMax = oInfoDt['tc_max']
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get path(s)
        #sPathDataSG = oInfoPath['DataDynamicSourceGridded']
        #sPathDataSP = oInfoPath['DataDynamicSourcePoint']
        sPathRun = oInfoPath['Run']
        sPathLib = oInfoPath['Library']
        sPathTemp = oInfoPath['DataTemp']
        sPathCache = oInfoPath['DataCache']
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get time info and run length
        if oDataTimeStepSelect:
            iTimeLength = int(len(oDataTimeStepSelect))
            sTimeStart = oDataTimeStepSelect[0]
            sTimeRestart = oDataTimeStepSelect[0]
            sTimeStatus = oDataTimeStepSelect[0]
            sTimeFrom = oDataTimeStepSelect[0]; sTimeTo = oDataTimeStepSelect[-1]
        else: pass
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get updated restart time if restart flag is activated
        if iFlagRestart == 1:
            
            oTimeRestartUpd = oDataTime.oTimeRestartUpd
            sTimeRestartUpd = oTimeRestartUpd.strftime('%Y%m%d%H%M')

            sTimeRestart = sTimeRestartUpd
            sTimeStatus = sTimeRestartUpd
             
        else:pass
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get geographical info
        iGeoNCols = oDataStatic['GeoInfo']['GeoRef']['ncols']
        iGeoNRows = oDataStatic['GeoInfo']['GeoRef']['nrows']
        dGeoXllCorner = oDataStatic['GeoInfo']['GeoRef']['xllcorner']
        dGeoYllCorner = oDataStatic['GeoInfo']['GeoRef']['yllcorner']
        dGeoCellSize = oDataStatic['GeoInfo']['GeoRef']['cellsize']
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # File Type(s)
        iSI_G_FileType = oSI_G['FileType']; iSI_G_FileTimeRes = oSI_G['FileTimeRes'];
        sSI_G_FilePath = oSI_G['FilePath']; sSI_G_FileName = oSI_G['FileName']; 
        
        iSI_P_FileType = oSI_P['FileType']; iSI_P_FileTimeRes = oSI_P['FileTimeRes'];
        sSI_P_FilePath = oSI_P['FilePath']; sSI_P_FileName = oSI_P['FileName'];
        
        iDI_G_FileType = oDI_G['FileType']; iDI_G_FileTimeRes = oDI_G['FileTimeRes'];
        sDI_G_FilePath = oDI_G['FilePath']; sDI_G_FileName = oDI_G['FileName'];
        
        iDI_P_FileType = oDI_P['FileType']; iDI_P_FileTimeRes = oDI_P['FileTimeRes'];
        sDI_P_FilePath = oDI_P['FilePath']; sDI_P_FileName = oDI_P['FileName'];
        
        iDO_G_FileType = oDO_G['FileType']; iDO_G_FileTimeRes = oDO_G['FileTimeRes'];
        sDO_G_FilePath = oDO_G['FilePath']; sDO_G_FileName = oDO_G['FileName'];
        
        iDO_P_FileType = oDO_P['FileType']; iDO_P_FileTimeRes = oDO_P['FileTimeRes'];
        sDO_P_FilePath = oDO_P['FilePath']; sDO_P_FileName = oDO_P['FileName'];
        
        iDS_G_FileType = oDS_G['FileType']; iDS_G_FileTimeRes = oDS_G['FileTimeRes'];
        sDS_G_FilePath = oDS_G['FilePath']; sDS_G_FileName = oDS_G['FileName'];
        
        iDS_P_FileType = oDS_P['FileType']; iDS_P_FileTimeRes = oDS_P['FileTimeRes'];
        sDS_P_FilePath = oDS_P['FilePath']; sDS_P_FileName = oDS_P['FileName'];
        
        iDR_G_FileType = oDR_G['FileType']; iDR_G_FileTimeRes = oDR_G['FileTimeRes'];
        sDR_G_FilePath = oDR_G['FilePath']; sDR_G_FileName = oDR_G['FileName'];
        
        iDR_P_FileType = oDR_P['FileType']; iDR_P_FileTimeRes = oDR_P['FileTimeRes'];
        sDR_P_FilePath = oDR_P['FilePath']; sDR_P_FileName = oDR_P['FileName'];
        #-------------------------------------------------------------------------------------
                
        #-------------------------------------------------------------------------------------
        # Path(s)
        # Static input file (SI)
        sSI_G_FilePath = Lib_Data_IO_Utils.defineString(sSI_G_FilePath, oRunTags)
        sSI_G_File = Lib_Data_IO_Utils.defineString(os.path.join(sSI_G_FilePath, sSI_G_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(os.path.split(sSI_G_File)[0], '$yyyy')
        sSI_P_FilePath = Lib_Data_IO_Utils.defineString(sSI_P_FilePath, oRunTags)
        sSI_P_FilePath = sSI_P_FilePath.replace('//','/')
        sSI_P_File = Lib_Data_IO_Utils.defineString(os.path.join(sSI_P_FilePath, sSI_P_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(os.path.split(sSI_P_File)[0], '$yyyy')
        
        # Dynamic input file (DI)
        sDI_G_FilePath = Lib_Data_IO_Utils.defineString(sDI_G_FilePath, oRunTags)
        sDI_G_File = Lib_Data_IO_Utils.defineString(os.path.join(sDI_G_FilePath, sDI_G_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(os.path.split(sDI_G_File)[0], '$yyyy')
        sDI_P_FilePath = Lib_Data_IO_Utils.defineString(sDI_P_FilePath, oRunTags)
        sDI_P_FilePath = sDI_P_FilePath.replace('//','/')
        sDI_P_File = Lib_Data_IO_Utils.defineString(os.path.join(sDI_P_FilePath, sDI_P_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(os.path.split(sDI_P_File)[0], '$yyyy')
        
        # Dynamic output file (DO)
        sDO_G_FilePath = Lib_Data_IO_Utils.defineString(sDO_G_FilePath, oRunTags)
        sDO_G_File = Lib_Data_IO_Utils.defineString(os.path.join(sDO_G_FilePath, sDO_G_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(os.path.split(sDO_G_File)[0], '$yyyy')
        sDO_P_FilePath = Lib_Data_IO_Utils.defineString(sDO_P_FilePath, oRunTags)
        sDO_P_FilePath = sDO_P_FilePath.replace('//','/')
        #sDO_P_File = Lib_Data_IO_Utils.defineString(os.path.join(sDO_P_FilePath, sDO_P_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(sDO_P_FilePath, '$yyyy')
        
        # Dynamic restart file (DR)
        sDR_G_FilePath = Lib_Data_IO_Utils.defineString(sDR_G_FilePath, oRunTags)
        sDR_G_File = Lib_Data_IO_Utils.defineString(os.path.join(sDR_G_FilePath, sDR_G_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(os.path.split(sDR_G_File)[0], '$yyyy')
        sDR_P_FilePath = Lib_Data_IO_Utils.defineString(sDR_P_FilePath, oRunTags)
        sDR_P_FilePath = sDR_P_FilePath.replace('//','/')
        #sDR_P_File = Lib_Data_IO_Utils.defineString(os.path.join(sDR_P_FilePath, sDR_P_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(sDR_P_FilePath, '$yyyy')
        
        # Dynamic state file (DS)
        sDS_G_FilePath = Lib_Data_IO_Utils.defineString(sDS_G_FilePath, oRunTags)
        sDS_G_File = Lib_Data_IO_Utils.defineString(os.path.join(sDS_G_FilePath, sDS_G_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(os.path.split(sDS_G_File)[0], '$yyyy')
        sDS_P_FilePath = Lib_Data_IO_Utils.defineString(sDS_P_FilePath, oRunTags)
        sDS_P_FilePath = sDS_P_FilePath.replace('//','/')
        #sDS_P_File = Lib_Data_IO_Utils.defineString(os.path.join(sDS_P_FilePath, sDS_P_FileName), oRunTags)
        Lib_Data_IO_Utils.createFolder(sDS_P_FilePath, '$yyyy')
        #------------------------------------------------------------------------------------- 
        
        #------------------------------------------------------------------------------------- 
        # Save update information
        oFIKeysUpd = {}
        
        # Flag information
        oFIKeysUpd['iFlagDebugSet'] = iFlagDebugSet
        oFIKeysUpd['iFlagDebugLevel'] = iFlagDebugLevel
        oFIKeysUpd['iFlagOs'] = iFlagOS
        oFIKeysUpd['iFlagFlowDeep'] = iFlagDeepFlow
        oFIKeysUpd['iFlagRestart'] = iFlagRestart
        oFIKeysUpd['a1iFlagS'] = iFlagS
        oFIKeysUpd['a1iFlagO'] = iFlagO
        oFIKeysUpd['iFlagVarUc'] = iFlagUc
        oFIKeysUpd['iFlagVarDtPhysConv'] = iFlagDtPhysConv
        oFIKeysUpd['iFlagSnow'] = iFlagSnow
        oFIKeysUpd['iFlagSnowAssim'] = iFlagSnowAssim
        oFIKeysUpd['iFlagLAI'] = iFlagLAI
        oFIKeysUpd['iFlagAlbedo'] = iFlagAlbedo
        
        # File type(s) information
        oFIKeysUpd['iFlagTypeData_Static'] = iSI_G_FileType
        #oFIKeysUpd['iFlagTypeData_Static_Gridded'] = iSI_G_FileType
        #oFIKeysUpd['iFlagTypeData_Static_Point'] = iSI_P_FileType
        oFIKeysUpd['iFlagTypeData_Forcing_Gridded'] = iDI_G_FileType
        oFIKeysUpd['iFlagTypeData_Forcing_Point'] = iDI_P_FileType
        oFIKeysUpd['iFlagTypeData_Output_Gridded'] = iDO_G_FileType
        oFIKeysUpd['iFlagTypeData_Output_Point'] = iDO_P_FileType
        oFIKeysUpd['iFlagTypeData_State_Gridded'] = iDS_G_FileType
        oFIKeysUpd['iFlagTypeData_State_Point'] = iDS_P_FileType
        oFIKeysUpd['iFlagTypeData_Restart_Gridded'] = iDR_G_FileType
        oFIKeysUpd['iFlagTypeData_Restart_Point'] = iDR_P_FileType
        
        # Paths(s) information
        oFIKeysUpd['sPathData_Static_Gridded'] = "'" + sSI_G_FilePath + "'"
        oFIKeysUpd['sPathData_Static_Point'] = "'" + sSI_P_FilePath + "'"
        oFIKeysUpd['sPathData_Forcing_Gridded'] = "'" + sDI_G_FilePath + "'"
        oFIKeysUpd['sPathData_Forcing_Point'] = "'" + sDI_P_FilePath + "'"
        oFIKeysUpd['sPathData_Output_Gridded'] = "'" + sDO_G_FilePath + "'"
        oFIKeysUpd['sPathData_Output_Point'] = "'" + sDO_P_FilePath + "'"
        oFIKeysUpd['sPathData_State_Gridded'] = "'" + sDS_G_FilePath + "'"
        oFIKeysUpd['sPathData_State_Point'] = "'" + sDS_P_FilePath + "'"
        oFIKeysUpd['sPathData_Restart_Gridded'] = "'" + sDR_G_FilePath + "'"
        oFIKeysUpd['sPathData_Restart_Point'] = "'" + sDR_P_FilePath + "'"
        
        oFIKeysUpd['iSimLength'] = iTimeLength
        
        oFIKeysUpd['sTimeStart'] = sTimeStart
        oFIKeysUpd['sTimeStatus'] = sTimeStatus
        oFIKeysUpd['sTimeRestart'] = sTimeRestart
        
        # Geographical information
        oFIKeysUpd['a1dGeoForcing'] = str(dGeoYllCorner) + ', ' + str(dGeoXllCorner)
        oFIKeysUpd['a1dResForcing'] = str(dGeoCellSize) + ', ' + str(dGeoCellSize)
        oFIKeysUpd['a1iDimsForcing'] = str(iGeoNRows) + ', ' + str(iGeoNCols)
        
        # Time integration information
        oFIKeysUpd['iDtModel'] = iDtModel #iDI_G_FileTimeRes
        oFIKeysUpd['iDtPhysConv'] = iDtPhysConv
        
        oFIKeysUpd['iDtData_Forcing'] = iDI_G_FileTimeRes
        oFIKeysUpd['iDtData_Output_Gridded'] = iDO_G_FileTimeRes
        oFIKeysUpd['iDtData_Output_Point'] = iDO_P_FileTimeRes
        oFIKeysUpd['iDtData_State_Gridded'] = iDS_G_FileTimeRes
        oFIKeysUpd['iDtData_State_Point'] = iDS_P_FileTimeRes
        
        # Other information
        oFIKeysUpd['iScaleFactor'] = iScaleFactor
        oFIKeysUpd['iTcMax'] = iTcMax
        
        return oFIKeysUpd
        #------------------------------------------------------------------------------------- 

    #------------------------------------------------------------------------------------- 
    
    #-------------------------------------------------------------------------------------  
    # Method to get info data in ASCII format
    def getInfoData(self):
        
        # Select type file
        if self.iTypeFile == 3:
            
            # Get from ASCII file
            oFileDrv = Drv_Data_IO(os.path.join(self.sFilePath,self.sFileName),'r')
            oInfoData = oFileDrv.oFileWorkspace.readInfoFile()
            
        else:
            GetException(' -----> ERROR: incorrect info file type!',1,1)
        
        # Store information
        oFileObject = {}
        oFileObject['Data'] = oInfoData['Data']
        oFileObject['Attributes'] = None
        oFileObject['GeoX'] = None
        oFileObject['GeoY'] = None
        oFileObject['GeoZ'] = None
        oFileObject['Time'] = None
        oFileObject['GeoInfo'] = None
        
        return oFileObject

    #-------------------------------------------------------------------------------------  
    
    #-------------------------------------------------------------------------------------
    # Method to save info data
    def saveInfoData(self, sFileName, oFileData):
        
        # Delete old info file
        Lib_Data_IO_Utils.deleteFile(sFileName)
        
        # Open ASCII file (to save all data)
        oFileHandler = open(sFileName,'wb');
        # Write data in ASCII file
        oFileHandler.writelines(oFileData.values())
        # Close ASCII file
        oFileHandler.close()
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to check variable availability
    def checkStaticVar(self, sVarName):
        
        # Select type file
        bExist = False
        if self.iTypeFile == 1:
            
            # Get from NetCDF file
            oFileDrv = Drv_Data_IO(os.path.join(self.sFilePath,self.sFileName),'r') 
            bExist = oFileDrv.oFileWorkspace.checkVarName(sVarName)
            
        elif self.iTypeFile == 3:
            
            bExist = Lib_Data_IO_Utils.checkFileExist(os.path.join(self.sFilePath, self.sFileName))
            
        else:
            GetException(' -----> WARNING: incorrect static file type (variable method)!',2,1)
            bExist = False
        
        return bExist
           
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to get static data in NetCDF or ASCII format
    def getStaticData(self):
        
        # Select type file
        if self.iTypeFile == 1:
        
            # Get from NetCDF file
            oFileDrv = Drv_Data_IO(os.path.join(self.sFilePath,self.sFileName),'r')
            
            # Get data and information
            a2dGeoX = oFileDrv.oFileWorkspace.get2DVar('Longitude')
            a2dGeoY = oFileDrv.oFileWorkspace.get2DVar('Latitude')
            a2dGeoZ = oFileDrv.oFileWorkspace.get2DVar('Terrain')
            # Get attribute(s)
            oAttrs = oFileDrv.oFileWorkspace.getFileAttrsCommon()
            
            # Organize data in a right way
            a1oGeoRef = {}
            a1oGeoRef['ncols'] = oAttrs['ncols']
            a1oGeoRef['nrows'] = oAttrs['nrows']
            a1oGeoRef['cellsize'] = oAttrs['cellsize']
            a1oGeoRef['xllcorner'] = oAttrs['xllcorner']
            a1oGeoRef['yllcorner'] = oAttrs['yllcorner']
            a1oGeoRef['NODATA_value'] = oAttrs['nodata_value']
            
            dGeoXMin = np.nanmin(a2dGeoX); dGeoXMax = np.nanmax(a2dGeoX)
            dGeoYMax = np.nanmax(a2dGeoY); dGeoYMin = np.nanmin(a2dGeoY)
            a1dGeoBox = [dGeoXMin, dGeoYMax, dGeoXMax, dGeoYMin]
        
        elif self.iTypeFile == 3:
            
            # Get from ASCII file
            oDataTerrain = GetGeoData(os.path.join(self.sFilePath, self.sFileName))
            
            # Get data and information
            a2dGeoZ = oDataTerrain.a2dGeoData
            a2dGeoX = oDataTerrain.oGeoData.a2dGeoX
            a2dGeoY = oDataTerrain.oGeoData.a2dGeoY
            a1oGeoRef = oDataTerrain.a1oGeoInfo
            a1dGeoBox = oDataTerrain.oGeoData.a1dGeoBox
            
        else:
            GetException(' -----> ERROR: incorrect static file type (data method)!',1,1)
            
        # Store information
        oFileObject = {}
        oFileObject['Data'] = None
        oFileObject['Attributes'] = None
        oFileObject['GeoX'] = a2dGeoX
        oFileObject['GeoY'] = a2dGeoY
        oFileObject['GeoZ'] = a2dGeoZ
        oFileObject['Time'] = None
        oFileObject['GeoInfo'] = {}
        oFileObject['GeoInfo']['GeoBox'] = a1dGeoBox
        oFileObject['GeoInfo']['GeoRef'] = a1oGeoRef
        
        return oFileObject
        
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to get dynamic data 
    def getDynamicData(self, sVarName, sVarTime, iVarDims):
        
        # Initialize dictionary
        oData = None; oDataSel = None; 
        oAttrs = None; 
        oGeoX = None; oGeoY = None; oGeoZ = None; 
        oTime = None; oTimeSel = None
        a1oGeoRef = None; a1dGeoBox = None
        
        # Select type file
        if self.iTypeFile == 1:
            
            # Get info
            sFileName = self.sFileName
            sFilePath = self.sFilePath
            oLogStream.info(' -------> Open File: ' + os.path.join(sFilePath, sFileName) + ' ... ')
            
            # Create temp folder to unzip file (to manage multiprocess request)
            sRN1 = str(randint(0,1000)); sRN2 = str(randint(1001,5000));
            oTimeTemp = datetime.datetime.now(); sTimeTemp = oTimeTemp.strftime('%Y%m%d-%H%M%S_%f')
            sTempName = 'folder_temp_' + sTimeTemp.lower() + '_' + sRN1.lower() + '_' + sRN2.lower()
            sTempPath = os.path.join(sFilePath,sTempName); 
            
            # Create temp dirs
            os.makedirs(sTempPath)
        
            # Copy file in a temp folder
            if os.path.exists(os.path.join(sFilePath, sFileName)):
                shutil.copyfile(os.path.join(sFilePath, sFileName), os.path.join(sTempPath, sFileName))
            else:
                GetException(' -----> WARNING: file ' + os.path.join(sFilePath, sFileName) + ' does not exist (ATTEMPT 1)!',2, 1)
                GetException(' -----> Wait 60 seconds ... ',2,1)
                time.sleep(60)
                GetException(' -----> Wait 60 seconds ... OK',2,1)
                
                if os.path.exists(os.path.join(sFilePath, sFileName)):
                    shutil.copyfile(os.path.join(sFilePath, sFileName), os.path.join(sTempPath, sFileName))
                else:
                    GetException(' -----> WARNING: file ' + os.path.join(sFilePath, sFileName) + ' does not exist (ATTEMPT 2 - NOT MORE ATTEMPTS)!',2, 1)
                
            # Unzip file 
            try:
                if self.bFileNameZip is True:
                    if os.path.exists(os.path.join(sTempPath, sFileName)):
                        
                        Drv_Data_Zip(os.path.join(sTempPath,sFileName), 'u', None, False)
                        sFileName = self.sFileNameExt
                            
                    else:
                        GetException(' -----> WARNING: file copying from ' + os.path.join(sFilePath, sFileName) + ' to ' + os.path.join(sTempPath, sFileName) +' FAILED! First Attempt!',2,1)
                        GetException(' -----> Retring copyfile and unzipping file ... ',2,1)
                        
                        os.makedirs(sTempPath)
                        shutil.copyfile(os.path.join(sFilePath, sFileName), os.path.join(sTempPath, sFileName))
                        Drv_Data_Zip(os.path.join(sTempPath,sFileName), 'u', None, False)
                        sFileName = self.sFileNameExt

                else:
                    GetException(' -----> WARNING: UNZIP FILE AVAILABLE! TO AVOID ERRORS COPY ZIP FILE IN TEMP FOLDER!',2,1)
                    if os.path.exists(os.path.join(sTempPath, sFileName)):
                        
                        Drv_Data_Zip(os.path.join(sTempPath,sFileName), 'u', None, False)
                        sFileName = self.sFileNameExt
                            
                    else:
                        GetException(' -----> WARNING: file copying from ' + os.path.join(sFilePath, sFileName) + ' to ' + os.path.join(sTempPath, sFileName) +' FAILED! Second Attempt',2,1)
                        GetException(' -----> Retring copyfile and unzipping file ... ',2,1)
                        
                        os.makedirs(sTempPath)
                        shutil.copyfile(os.path.join(sFilePath, sFileName), os.path.join(sTempPath, sFileName))
                        Drv_Data_Zip(os.path.join(sTempPath,sFileName), 'u', None, False)
                        sFileName = self.sFileNameExt
            except:
            
                GetException(' -----> WARNING: errors in file copying from ' + os.path.join(sFilePath, sFileName) + ' to ' + os.path.join(sTempPath, sFileName) +' FAILED! Failure Previously!',2,1) 
                GetException(' -----> Wait 60 seconds ... ',2,1)
                time.sleep(60)
                GetException(' -----> Wait 60 seconds ... OK',2,1)
                
                # Compute a new random number to avoid copying issue of file
                sRN1 = str(randint(0,1000)); sRN2 = str(randint(5000,9999));
                oTimeTemp = datetime.datetime.now(); sTimeTemp = oTimeTemp.strftime('%Y%m%d-%H%M%S_%f')
                sTempName = 'folder_temp_' + sTimeTemp.lower() + '_' + sRN1.lower() + '_' + sRN2.lower()
                sTempPath = os.path.join(sFilePath,sTempName); 
                
                # Make a new folder
                os.makedirs(sTempPath)
                shutil.copyfile(os.path.join(sFilePath, sFileName), os.path.join(sTempPath, sFileName))
                Drv_Data_Zip(os.path.join(sTempPath,sFileName), 'u', None, False)
                sFileName = self.sFileNameExt
            
            # File IO driver
            oFileDrv = Drv_Data_IO(os.path.join(sTempPath,sFileName),'r')
            
            # Get time information
            oTime = oFileDrv.oFileWorkspace.getTime()
            iTimeStartIndex = oTime.index(sVarTime)

            # Check variable availability in file
            bFileVarExist = oFileDrv.oFileWorkspace.checkVarName(sVarName)
            bFileVarExistCheck = False
            if bFileVarExist is True:
            
                # Get data information
                if iVarDims == 2:
                    oDataSel = oFileDrv.oFileWorkspace.get2DVar(sVarName)
                    oTimeSel = oTime
                elif iVarDims == 3:
                    oData = oFileDrv.oFileWorkspace.get3DVar(sVarName)
                    oDataSel = oData[:,:,iTimeStartIndex:] 
                    oTimeSel = oTime[iTimeStartIndex:]
                    
                oGeoX = self.oGeoInfo['GeoX']
                oGeoY = self.oGeoInfo['GeoY']
                oGeoZ = self.oGeoInfo['GeoZ']
                
                a1dGeoBox = self.oGeoInfo['GeoInfo']['GeoBox']
                a1oGeoRef = self.oGeoInfo['GeoInfo']['GeoRef']
    
                oAttrs = oFileDrv.oFileWorkspace.getFileAttrsCommon()
                
                bFileVarExistCheck = True
            
            else: 
                GetException(' -----> WARNING: variable ' + sVarName +' is not available in file '+ os.path.join(sFilePath, sFileName) +'! Check your input!',2,1)
                bFileVarExistCheck = False
                
            # Remove all temporary files
            if os.path.exists(sTempPath):
                if os.listdir(sTempPath):
                    try:
                        shutil.rmtree(sTempPath)
                    except:
                        GetException(' -----> WARNING: deleting folder ' +sTempPath+ ' failed! Check your permission(s) and file system!',1,1)  
                else: pass
            else: pass

        elif self.iTypeFile == 2:
            
            oDataSel = sFileName
        
        else:
            GetException(' -----> ERROR: incorrect dynamic file type!',1,1)
            
        # Store information
        oFileObject = {}
        oFileObject['Data'] = oDataSel
        oFileObject['Attributes'] = oAttrs
        oFileObject['GeoX'] = oGeoX
        oFileObject['GeoY'] = oGeoY
        oFileObject['GeoZ'] = oGeoZ
        oFileObject['Time'] = oTimeSel
        oFileObject['GeoInfo'] = {}
        oFileObject['GeoInfo']['GeoBox'] = a1dGeoBox
        oFileObject['GeoInfo']['GeoRef'] = a1oGeoRef
        
        return oFileObject, bFileVarExistCheck

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to save dynamic data
    def saveDynamicData(self, oFileData, oSimInfo=None, oGeneralInfo=None, oGeoSystemInfo=None):
        
        #-------------------------------------------------------------------------------------
        # Get file information
        sFileName = self.sFileName
        sFilePath = self.sFilePath
        
        oGeoInfo = self.oGeoInfo
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Select type file
        if self.iTypeFile == 1:
            
            #-------------------------------------------------------------------------------------
            # Get info from global variable(s)
            oSettings = self.oSettings
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Open file
            oFileDrv = Drv_Data_IO(os.path.join(sFilePath, sFileName), 'w')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Set file attribute(s)
            if oGeneralInfo:
                oFileDrv.oFileWorkspace.writeFileAttrsCommon(oGeneralInfo)
            else:
                pass
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Cycling on variable(s)
            iCols = None; iRows = None; oVarAttr = None;
            a2dGeoX = np.array([]); a2dGeoY = np.array([]); a2dGeoZ = np.array([]); a1dGeoBox = np.array([]);
            for sVarName in oFileData:
                
                #-------------------------------------------------------------------------------------
                # Get variable workspace
                oVarData = oFileData[sVarName]
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Get and write variable dimension(s)
                if not iCols and not iRows:
                    
                    try:
                        iCols = np.int32(oFileData['GeoInfo']['GeoRef']['ncols'])
                        iRows = np.int32(oFileData['GeoInfo']['GeoRef']['nrows'])
                    except:
                        iRows = oGeoInfo['GeoZ'].shape[0]
                        iCols = oGeoInfo['GeoZ'].shape[1]
                        
                    # Write variable dimension(s)
                    oFileDrv.oFileWorkspace.writeDims('X', iCols)    
                    oFileDrv.oFileWorkspace.writeDims('Y', iRows) 
                    oFileDrv.oFileWorkspace.writeDims('time', 1)
                else:pass
                #-------------------------------------------------------------------------------------

                #-------------------------------------------------------------------------------------
                # Get and write geographical information     #### condizione da verificare per netcdf e arcgrid
                if not a1dGeoBox.size:
                    
                    try:
                        a1dGeoBox = oFileData['GeoInfo']['GeoBox']
                        a1dGeoRef = oFileData['GeoInfo']['GeoRef']
                    except:
                        a1dGeoBox = oGeoInfo['GeoInfo']['GeoBox']
                        a1dGeoRef = oGeoInfo['GeoInfo']['GeoRef']
                    
                    if not a1dGeoBox.size:
                        a1dGeoBox = oGeoInfo['GeoInfo']['GeoBox']
                    else: pass
                    
                    if not a1dGeoRef:
                        a1dGeoRef = oGeoInfo['GeoInfo']['GeoRef']
                    else: pass
                    
                    if oSimInfo:
                        oFileDrv.oFileWorkspace.writeFileAttrsExtra(oSimInfo, a1dGeoRef)
                    else:pass
                    if oGeoSystemInfo:
                        oFileDrv.oFileWorkspace.writeGeoSystem(oGeoSystemInfo, a1dGeoBox)
                    else:pass
                    
                else:pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Get attributes
                if not oVarAttr:
                    oVarAttr = oFileData['Attributes']
                else:pass
                #-------------------------------------------------------------------------------------
                
                #-------------------------------------------------------------------------------------
                # Write 2D variable(s) and skip other stuff
                if sVarName == 'GeoX':
                    
                    #oFileDrv.oFileWorkspace.write2DVar('Longitude', oVarData, [] , 'f4', 'Y', 'X')
                    oFileDrv.oFileWorkspace.write2DVar('Longitude', oGeoInfo['GeoX'], [] , 'f4', 'Y', 'X')
                    
                elif sVarName == 'GeoY':
                    
                    #oFileDrv.oFileWorkspace.write2DVar('Latitude', oVarData, [] , 'f4', 'Y', 'X') 
                    oFileDrv.oFileWorkspace.write2DVar('Latitude', oGeoInfo['GeoY'], [] , 'f4', 'Y', 'X') 
                    
                elif sVarName == 'GeoZ':
                    
                    #oFileDrv.oFileWorkspace.write2DVar('Terrain', oVarData, [] , 'f4', 'Y', 'X') 
                    oFileDrv.oFileWorkspace.write2DVar('Terrain', oGeoInfo['GeoZ'], [] , 'f4', 'Y', 'X') 
                    
                elif sVarName == 'Attributes':pass
                elif sVarName == 'GeoInfo':pass
                else:
                    if oVarAttr:
                        oFileDrv.oFileWorkspace.write2DVar(sVarName, oVarData, oVarAttr , 'f4', 'Y', 'X')
                    else:
                        oFileDrv.oFileWorkspace.write2DVar(sVarName, oVarData, [], 'f4', 'Y', 'X')
                #-------------------------------------------------------------------------------------
                
            #-------------------------------------------------------------------------------------
            # Close file
            oFileDrv.oFileWorkspace.closeFile()
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Zip file
            Drv_Data_Zip(os.path.join(sFilePath, sFileName), 'z', 'gz', True)
            #-------------------------------------------------------------------------------------
            
        elif self.iTypeFile == 2:
            
            #-------------------------------------------------------------------------------------
            # IMPOSTARE COPY FILE
            print('binary - solo copia')
            print('scrivere questa parte')
            #-------------------------------------------------------------------------------------
            
            pass
        
        #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
