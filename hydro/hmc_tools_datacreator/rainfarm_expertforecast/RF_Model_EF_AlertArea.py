#----------------------------------------------------------------------------
# RF - Model Expert Forecast Alert Area
# Version 3.0.2 (20150924)
# Author(s):    Fabio Delogu            (fabio.delogu@cimafoundation.org)
#               Simone Gabellani        (simone.gabellani@cimafoundation.org)
#               Francesco Silvestro     (francesco.silvestro@cimafoundation.org)
#               Nicola Rebora           (nicola.rebora@cimafoundation.org)
#
# Python 2.7
#
# References external libraries:
# numpy-scipy:        http://www.scipy.org/SciPy
# python-netcdf:      http://netcdf4-python.googlecode.com/svn/trunk/docs/netCDF4-module.html
# python-gdal:        https://pypi.python.org/pypi/GDAL/
#
# Function Argument(s): -settingfile -logfile
#
# Function returns:
# iExitStatus             Function code error
#                          0: OK
#                          1: Error in "Set model"
#                          2: Error in "Initialize model"
#                          3: Error in "Execute model"
#
# General example usage: 
# python RF_Model_EF_AlertArea.py -settingfile settingfile.config -logfile logfile.config
# 
# Example:
# python RF_Model_EF_AlertArea.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/rainfarm_expertforecast/config_algorithms/rf_model_ef-alertarea_algorithm_local.config
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/rainfarm_expertforecast/config_logs/rf_model_ef-alertarea_logging_local.config
#
# Version
# 3.0.2  (20150924) --> Added methods to manage multiple nc and binary files
# 3.0.1  (20150923) --> Added multiprocessing mode, nearest regrid method and completed check, get, compute and save methods
# 3.0.0  (20150823) --> Release based on last DRIHM release 2.5.11
# 2.5.11 (20150722) --> Corrected array XY orders
# 2.5.10 (20150203) --> Added control about 2d and 3d null variable(s)
# 2.5.9  (20150202) --> Added exit code and moved log file in results folder
# 2.5.8  (20141114) --> Added conditions for undefined fields (meso-nh ok, issues using arome for disaggregating fields)
# 2.5.7  (20141113) --> Added log file
# 2.5.6  (20140728) --> Added creation of mask using geographical bounding box
# 2.5.5  (20140723) --> Corrected bug for time disaggregation 
# 2.5.2  (20140717) --> Corrected bug for volume re-distribution for time steps (interp)
# 2.5.0  (20140523) --> Corrected bugs for input and output netcdf file(s)
# 2.5.0  (20140522) --> New release using classes and correct fields info and features
# 2.0.2  (20140512) --> Corrected bugs in time downscaler
# 2.0.1  (20140408) --> First release based on Rainfarm 1.0
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Method to get script argument(s)
def GetArgs():
    
    import argparse
    
    sScriptName = ''; sSettingsFile =''; sLoggingFile=''
    
    oParser = argparse.ArgumentParser()
    oParser.add_argument('-settingfile', action="store", dest="sSettingFile")
    oParser.add_argument('-logfile', action="store", dest="sLoggingFile")
    oParserValue = oParser.parse_args()
    
    sScriptName = oParser.prog
    
    if oParserValue.sSettingFile:
        sSettingsFile = oParserValue.sSettingFile
    else:
        sSettingsFile = 'rf_model_ef-alertarea_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'rf_model_ef-alertarea_logging.config'
    
    return(sScriptName, sSettingsFile, sLoggingFile)

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #----------------------------------------------------------------------------
    # Script version 
    sProgramVersion = '3.0.2'
    sProjectName = 'RF'
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Get script argument(s)
    [sScriptName, sSettingsFile, sLoggingFile] = GetArgs()
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Log initialization
    import logging
    import logging.config
    logging.config.fileConfig(sLoggingFile)
    oLogStream = logging.getLogger('sLogger')
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Start Program
    oLogStream.info('['+sProjectName+' Model - EF ALERT AREA (Version '+sProgramVersion+')]')
    oLogStream.info('['+sProjectName+'] Start Program ... ')
    iExitStatus = 0
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load DynamicaData setting(s)
    oLogStream.info('[' + sProjectName + '] Model - Set EF ALERT AREA configuration ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Complete library
        import os.path
        import time
        
        # Partial Library
        from os.path import join
        
        # Import classes
        import src.GetAncillaryData as GetAncillaryData
        from src.GetException import GetException
        from src.GetSettings import GetSettings
        from src.GetTime import GetTime
        
        from src.GetGeoData import GetGeoData
        
        from Cpl_Apps_RF_Model_EF_AlertArea import Cpl_Apps_RF_Model_EF_AlertArea
        
        # Debug
        import matplotlib.pylab as plt
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # Path main
        sPathMain = os.getcwd() + '/'  # Setting PathMain
        os.path.abspath(sPathMain)  # Entering in path main folder
        #----------------------------------------------------------------------------
    
        #----------------------------------------------------------------------------
        # Get settings data
        oDataInfo = GetSettings(join(sPathMain, sSettingsFile))
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # Time information
        dStartTime = time.time()
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Set EF ALERT AREA configuration ... OK')
        #----------------------------------------------------------------------------
        
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Set EF ALERT AREA configuration ... FAILED',1,1)
        #----------------------------------------------------------------------------
        
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] Model - Initialize EF ALERT AREA  ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Get terrain data
        oDataTerrain = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Terrain']['VarSource'])) 
                                       
        # Get alert area data                          
        oDataAA = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['AlertArea']['VarSource'])) 
                                       
        # Get ancillary data
        oDataAncillary = GetAncillaryData.ExpertForecast_RF_VM(join(oDataInfo.oInfoSettings.oPathInfo['DataAncillary'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['MAT']['VM']['VarSource'])) 
        
        # Get time data
        oDataTime = GetTime(timenow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow'], 
                            timestep=int(oDataInfo.oInfoSettings.oParamsInfo['TimeStep']),
                            timeperiodpast=int(oDataInfo.oInfoSettings.oParamsInfo['TimePeriod']),
                            timerefHH = '12',
                            timerefworld=oDataInfo.oInfoSettings.oParamsInfo['TimeWorldRef'])
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Initialize EF ALERT AREA ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Initialize EF ALERT AREA ... FAILED',1,2)
        #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Run DynamicData
    oLogStream.info('[' + sProjectName + '] Model - Execute EF ALERT AREA ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Dynamic Data
        oCpl_DynamicData = Cpl_Apps_RF_Model_EF_AlertArea(oDataTime=oDataTime, oDataGeo=oDataTerrain, oDataInfo=oDataInfo, 
                                                          oDataAA=oDataAA, oDataAncillary=oDataAncillary)
        
        # Cycle on time steps
        for sTime in oDataTime.a1oTimeSteps:
            
            # Check dynamic data availability
            oCpl_DynamicData.checkDynamicData(sTime)
            
            # Get dynamic data
            oCpl_DynamicData.getDynamicData(sTime)
            
            # Compute dynamic data
            oCpl_DynamicData.computeDynamicData(sTime)
            
            # Save dynamic data
            oCpl_DynamicData.saveDynamicData(sTime)
        
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Execute EF ALERT AREA ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Execute EF ALERT AREA ... FAILED',1,3)
        #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Note about script parameter(s)
    oLogStream.info('NOTE - Algorithm parameter(s)')
    oLogStream.info('Script: ' + str(sScriptName) )
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # End Program
    dTimeElapsed = round(time.time() - dStartTime,1);
    
    oLogStream.info('['+sProjectName+'] Model - EF ALERT AREA (Version '+sProgramVersion+')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
    
    GetException('',0,0)
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------
