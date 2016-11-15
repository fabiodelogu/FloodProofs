"""
Class Features

Name:          Drv_Model_HMC_Finalizer
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20151022'
Version:       '1.6.2'
"""

######################################################################################
# Logging
import logging
oLogStream = logging.getLogger('sLogger')

# Library
import os, datetime
import numpy as np

import Lib_Data_IO_Utils as Lib_Data_IO_Utils

from Drv_Data_Zip import Drv_Data_Zip
from Drv_Data_IO import Drv_Data_IO
from Drv_Model_HMC_IO import Drv_Model_HMC_IO

from GetGeoData import GetGeoData
from GetException import GetException

# Debug
import matplotlib.pylab as plt
######################################################################################

#-------------------------------------------------------------------------------------
# Class
class Drv_Model_HMC_Finalizer:
    
    #-------------------------------------------------------------------------------------
    # Method init class
    def __init__(self, sDomainName, sRunName, oDataInfo, oDrvBuilder, sEnsembleName):
        
        # Global variable(s)
        self.sDomainName = sDomainName
        self.sRunName = sRunName
        self.oDataInfo = oDataInfo
        self.oDrvBuilder = oDrvBuilder
        
        self.sEnsembleName = sEnsembleName

    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Method to collect output
    def collectDataOutput(self):
        
        #-------------------------------------------------------------------------------------
        # Get model and run parameter(s)
        iDtModel = int(self.oDrvBuilder.oDataInfo.oInfoSettings.oParamsInfo['RunDt']['dt_model'])
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get folder(s) information (STATIC, OUTPUT and STATE)
        sPathStaticP = self.oDrvBuilder.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FilePath']
        sPathOutputG = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Gridded']['FilePath']
        sPathOutputP_SecQ = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Point']['FilePath']  
        sPathOutputP_DamV = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Point']['FilePath']
        sPathOutputP_DamL = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Point']['FilePath']    
        sPathStateG = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataStateDynamic['Gridded']['FilePath']
        sPathStateP = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataStateDynamic['Point']['FilePath']  
         
        # Get folder(s) information (ARCHIVE)
        sPathArchiveG = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Gridded']['FilePath']
        sPathArchiveP_SecQ = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FilePath']['Path_SectionQ']
        sPathArchiveP_DamV = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FilePath']['Path_DamV']
        sPathArchiveP_DamL = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FilePath']['Path_DamL']
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get filename(s) information (STATIC, OUTPUT and STATE)
        sFileStaticP = self.oDrvBuilder.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FileName']
        sFileOutputG = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Gridded']['FileName']
        sFileOutputP_SecQ = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Point']['FileName']['File_SectionQ']
        sFileOutputP_DamV = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Point']['FileName']['File_DamV']
        sFileOutputP_DamL = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataOutputDynamic['Point']['FileName']['File_DamL']     
        sFileStateG = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataStateDynamic['Gridded']['FileName']
        sFileStateP = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataStateDynamic['Point']['FileName']   
        
        # Get filename(s) information (ARCHIVE)
        sFileArchiveP_SecQ = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FileName']['File_SectionQ']
        sFileArchiveP_DamV = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FileName']['File_DamV']
        sFileArchiveP_DamL = self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FileName']['File_DamL']   
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get variable(s) information
        oFileVarsP = self.oDrvBuilder.oDataInfo.oInfoVarStatic.oDataInputStatic['Point']['FileVars']
        
        iFileTimeResP_SecQ = int(self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FileTimeRes'])
        iFileTimeResP_DamV = int(self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FileTimeRes'])
        iFileTimeResP_DamL = int(self.oDrvBuilder.oDataInfo.oInfoVarDynamic.oDataArchiveDynamic['Point']['FileTimeRes'])
        
        # Get concentration time
        iTime_CONC = self.oDrvBuilder.iTc
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get run and domain names information
        sRunName = self.sRunName
        sDomainName = self.sDomainName
        sEnsembleName = self.sEnsembleName
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Get time information
        oDtModel = datetime.timedelta(seconds = iDtModel)
        
        a1oTime_STEPS = self.oDrvBuilder.oDataTime.a1oTimeSteps
        oTime_NOW = self.oDrvBuilder.oDataTime.oTimeNow; sTime_NOW = oTime_NOW.strftime('%Y%m%d%H%M')
        oTime_FROM = self.oDrvBuilder.oDataTime.oTimeFrom; sTime_FROM = oTime_FROM.strftime('%Y%m%d%H%M')
        oTime_TO = self.oDrvBuilder.oDataTime.oTimeTo; sTime_TO = oTime_TO.strftime('%Y%m%d%H%M')
        
        sYear_NOW = sTime_NOW[0:4]; sMonth_NOW = sTime_NOW[4:6]; sDay_NOW = sTime_NOW[6:8];
        sHH_NOW = sTime_NOW[8:10]; sMM_NOW = sTime_NOW[10:12];
        
        iTime_STEPS = len(a1oTime_STEPS)
        
        # Get time information upd (to include time concentration)
        oTime_DIFF = (datetime.datetime.strptime(sTime_TO, '%Y%m%d%H%M') - 
                     datetime.datetime.strptime(sTime_FROM, '%Y%m%d%H%M') +
                     oDtModel )
                     
        #iTime_STEPS = oTime_DIFF.total_seconds()/3600
        #iTime_DELTA = oTime_DIFF/iTime_STEPS
        
        # Update time steps (considering tc steps)
        oTime_FROM_UPD = oTime_FROM
        oTime_TO_UPD = oTime_TO + datetime.timedelta(seconds = iDtModel*iTime_CONC) + oDtModel
        oTime_STEP = oTime_FROM_UPD
        oTime_DELTA = datetime.timedelta(seconds = iDtModel)
        
        a1oTime_STEPS_UPD = []
        while oTime_STEP <= oTime_TO_UPD:
            a1oTime_STEPS_UPD.append(oTime_STEP.strftime('%Y%m%d%H%M'))
            oTime_STEP += oTime_DELTA
            
        iTime_UPD_STEPS = len(a1oTime_STEPS_UPD)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Define folder name(s) 
        sPathArchiveG_OUT = Lib_Data_IO_Utils.defineFolderName(sPathArchiveG,
                                {'$yyyy' : sYear_NOW,'$mm' : sMonth_NOW,'$dd' : sDay_NOW, 
                                '$HH' : sHH_NOW,'$MM' : sMM_NOW, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
        sPathArchiveP_SecQ_OUT = Lib_Data_IO_Utils.defineFolderName(sPathArchiveP_SecQ,
                                {'$yyyy' : sYear_NOW,'$mm' : sMonth_NOW,'$dd' : sDay_NOW, 
                                '$HH' : sHH_NOW,'$MM' : sMM_NOW, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
        sPathArchiveP_DamV_OUT = Lib_Data_IO_Utils.defineFolderName(sPathArchiveP_DamV,
                                {'$yyyy' : sYear_NOW,'$mm' : sMonth_NOW,'$dd' : sDay_NOW, 
                                '$HH' : sHH_NOW,'$MM' : sMM_NOW, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
        sPathArchiveP_DamL_OUT = Lib_Data_IO_Utils.defineFolderName(sPathArchiveP_DamL,
                                {'$yyyy' : sYear_NOW,'$mm' : sMonth_NOW,'$dd' : sDay_NOW, 
                                '$HH' : sHH_NOW,'$MM' : sMM_NOW, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Cycle(s) on time steps
        a2dData_SecQ_OUT = np.array([]); 
        a2dData_DamV_OUT = np.array([]); a2dData_DamL_OUT = np.array([]);
        for sTime_STEP in a1oTime_STEPS_UPD:
            
            #-------------------------------------------------------------------------------------
            # Info archive data
            oLogStream.info(' ====> TIME STEP ARCHIVE: ' + sTime_STEP + ' ... ')
            oTime_STEP = datetime.datetime.strptime(sTime_STEP,'%Y%m%d%H%M')
            
            if oTime_STEP > oTime_TO:
                oLogStream.info(' -----> Step greater than Simulation period')
            else:
                oLogStream.info(' -----> Step in Simulation period')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Time step information
            sYear_STEP = sTime_STEP[0:4]; sMonth_STEP = sTime_STEP[4:6]; sDay_STEP = sTime_STEP[6:8];
            sHH_STEP = sTime_STEP[8:10]; sMM_STEP = sTime_STEP[10:12];
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Define folder name OUTPUT GRIDDED step
            sPathOutputG_STEP = Lib_Data_IO_Utils.defineString(sPathOutputG,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            
            # Define folder name OUTPUT POINT step
            sPathOutputP_SecQ_STEP = Lib_Data_IO_Utils.defineString(sPathOutputP_SecQ,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            sPathOutputP_DamV_STEP = Lib_Data_IO_Utils.defineString(sPathOutputP_DamV,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            sPathOutputP_DamL_STEP = Lib_Data_IO_Utils.defineString(sPathOutputP_DamL,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            
            # Define folder name STATE GRIDDED and POINT step
            sPathStateG_STEP = Lib_Data_IO_Utils.defineString(sPathStateG,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            sPathStateP_STEP = Lib_Data_IO_Utils.defineString(sPathStateP,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            
            # Define file name ARCHIVE GRIDDED and POINT step
            #sPathArchiveG_STEP = Lib_Data_IO_Utils.defineString(sPathArchiveG,
            #                    {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
            #                    '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            #sPathArchiveP_SecQ_STEP = Lib_Data_IO_Utils.defineFolderName(sPathArchiveP_SecQ,
            #                        {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
            #                        '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            #sPathArchiveP_DamV_STEP = Lib_Data_IO_Utils.defineFolderName(sPathArchiveP_DamV,
            #                        {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
            #                        '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            #sPathArchiveP_DamL_STEP = Lib_Data_IO_Utils.defineFolderName(sPathArchiveP_DamL,
            #                        {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
            #                        '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName, '$TYPE' : sEnsembleName})
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Define file name OUTPUT GRIDDED step
            sFileOutputG_STEP = Lib_Data_IO_Utils.defineString(sFileOutputG,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName})
            
            # Define file name OUTPUT POINT step
            sFileOutputP_SecQ_STEP = Lib_Data_IO_Utils.defineString(sFileOutputP_SecQ,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName})
            sFileOutputP_DamV_STEP = Lib_Data_IO_Utils.defineString(sFileOutputP_DamV,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName})
            sFileOutputP_DamL_STEP = Lib_Data_IO_Utils.defineString(sFileOutputP_DamL,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName})
            
            # Define folder name STATE GRIDDED and POINT step
            sFileStateG_STEP = Lib_Data_IO_Utils.defineString(sFileStateG,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName})
            sFileStateP_STEP = Lib_Data_IO_Utils.defineString(sFileStateP,
                                     {'$yyyy' : sYear_STEP,'$mm' : sMonth_STEP,'$dd' : sDay_STEP, 
                                      '$HH' : sHH_STEP,'$MM' : sMM_STEP, '$RUN' : sRunName})
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Copy and get SECTION Q file
            oLogStream.info(' -----> Copy SECTION Q POINT file: ' + os.path.join(sPathOutputP_SecQ_STEP, sFileOutputP_SecQ_STEP) + ' ... ')
            
            sFileName_SecQ_STEP = os.path.join(sPathOutputP_SecQ_STEP, sFileOutputP_SecQ_STEP)
            #sFileName_SecQ_OUT = os.path.join(sPathArchiveP_SecQ_OUT, sFileOutputP_SecQ_STEP)
            sPathArchiveP_SecQ_OUT = sPathArchiveP_SecQ_OUT.replace('//','/')
            
            oDrvModel_IO = Drv_Model_HMC_IO(sFileName_SecQ_STEP, self.oDataInfo)
            #a1dData_SecQ_STEP = oDrvModel_IO.getModelData1D()
            oDrvModel_IO.copyModelData(sPathArchiveP_SecQ_OUT)
            
            # Concatenate array 1D array
            #if a2dData_SecQ_OUT.shape[0] == 0:
            #    a2dData_SecQ_OUT = a1dData_SecQ_STEP
            #else:
            #   a2dData_SecQ_OUT = np.vstack((a2dData_SecQ_OUT, a1dData_SecQ_STEP))
            
            oLogStream.info(' -----> Copy SECTION Q POINT file: ' + os.path.join(sPathOutputP_SecQ_STEP, sFileOutputP_SecQ_STEP) + ' ... OK')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Copy and get DAM VOLUME file
            oLogStream.info(' -----> Copy DAM VOLUME POINT file: ' + os.path.join(sPathOutputP_DamV_STEP, sFileOutputP_DamV_STEP) + ' ... ')
            
            sFileName_DamV_STEP = os.path.join(sPathOutputP_DamV_STEP, sFileOutputP_DamV_STEP)
            #sFileName_DamV_OUT = os.path.join(sPathArchiveP_DamV_OUT, sFileOutputP_DamV_STEP)
            sPathArchiveP_DamV_OUT = sPathArchiveP_DamV_OUT.replace('//','/')
            
            oDrvModel_IO = Drv_Model_HMC_IO(sFileName_DamV_STEP, self.oDataInfo)
            #a1dData_DamV_STEP = oDrvModel_IO.getModelData1D()
            oDrvModel_IO.copyModelData(sPathArchiveP_DamV_OUT)
            
            # Concatenate array 1D array
            #if a2dData_DamV_OUT.shape[0] == 0:
            #    a2dData_DamV_OUT = a1dData_DamV_STEP
            #else:
            #    a2dData_DamV_OUT = np.vstack((a2dData_DamV_OUT, a1dData_DamV_STEP))
            
            oLogStream.info(' -----> Copy DAM VOLUME POINT file: ' + os.path.join(sPathOutputP_SecQ_STEP, sFileOutputP_SecQ_STEP) + ' ... OK')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Copy and get DAM LEVEL file
            oLogStream.info(' -----> Copy DAM LEVEL POINT file: ' + os.path.join(sPathOutputP_DamV_STEP, sFileOutputP_DamV_STEP) + ' ... ')
            
            sFileName_DamL_STEP = os.path.join(sPathOutputP_DamL_STEP, sFileOutputP_DamL_STEP)
            #sFileName_DamL_OUT = os.path.join(sPathArchiveP_DamL_OUT, sFileOutputP_DamL_STEP)
            sPathArchiveP_DamL_OUT = sPathArchiveP_DamL_OUT.replace('//','/')
            
            oDrvModel_IO = Drv_Model_HMC_IO(sFileName_DamL_STEP, self.oDataInfo)
            #a1dData_DamL_STEP = oDrvModel_IO.getModelData1D()
            oDrvModel_IO.copyModelData(sPathArchiveP_DamL_OUT)
            
            # Concatenate array 1D array
            #if a2dData_DamL_OUT.shape[0] == 0:
            #    a2dData_DamL_OUT = a1dData_DamL_STEP
            #else:
            #    a2dData_DamL_OUT = np.vstack((a2dData_DamL_OUT, a1dData_DamL_STEP))
            
            oLogStream.info(' -----> Copy DAM LEVEL POINT file: ' + os.path.join(sPathOutputP_SecQ_STEP, sFileOutputP_SecQ_STEP) + ' ... OK')
            #-------------------------------------------------------------------------------------
          
            #-------------------------------------------------------------------------------------
            # Copy OUTPUT GRIDDED file
            oLogStream.info(' -----> Copy OUTPUT GRIDDED file: ' + os.path.join(sPathOutputG_STEP, sFileOutputG_STEP) + ' ... ')
            oDrvModel_IO = Drv_Model_HMC_IO(os.path.join(sPathOutputG_STEP, sFileOutputG_STEP), self.oDataInfo)
            oDrvModel_IO.copyModelData(sPathArchiveG_OUT, sFileOutputG_STEP, '.gz')
            oLogStream.info(' -----> Copy OUTPUT GRIDDED file: ' + os.path.join(sPathOutputG_STEP, sFileOutputG_STEP) + ' ... OK')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Copy STATE GRIDDED file
            oLogStream.info(' -----> Copy STATE GRIDDED file: ' + os.path.join(sPathStateG_STEP, sFileStateG_STEP) + ' ... ')
            oDrvModel_IO = Drv_Model_HMC_IO(os.path.join(sPathStateG_STEP, sFileStateG_STEP), self.oDataInfo)
            oDrvModel_IO.copyModelData(sPathArchiveG_OUT, sFileStateG_STEP, '.gz')
            oLogStream.info(' -----> Copy STATE GRIDDED file: ' + os.path.join(sPathStateG_STEP, sFileStateG_STEP) + ' ... OK')
            #-------------------------------------------------------------------------------------
            
            #-------------------------------------------------------------------------------------
            # Info archive data
            oLogStream.info(' ====> TIME STEP ARCHIVE: ' + sTime_STEP + ' ... OK')
            #-------------------------------------------------------------------------------------

        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Save information to global workspace
        #self.sPathArchiveG = sPathArchiveG_OUT
        #self.sPathArchiveP_SecQ = sPathArchiveP_SecQ_OUT
        #self.sPathArchiveP_DamV = sPathArchiveP_DamV_OUT
        #self.sPathArchiveP_DamL = sPathArchiveP_DamL_OUT
        #self.a1oTimeArchive = a1oTime_STEPS_UPD
        # Save data to global workspace
        #self.a2dDataArchive_SecQ = a2dData_SecQ_OUT
        #self.a2dDataArchive_DamV = a2dData_DamV_OUT
        #self.a2dDataArchive_DamL = a2dData_DamL_OUT
        #-------------------------------------------------------------------------------------
        
#-------------------------------------------------------------------------------------
    
    
    
    
    
    