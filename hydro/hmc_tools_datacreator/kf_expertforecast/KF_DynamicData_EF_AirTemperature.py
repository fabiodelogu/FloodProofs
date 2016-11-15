#----------------------------------------------------------------------------
# KF - DynamicData Expert Forecast AirTemperature
# Version 1.0.0 (20151125)
# Author(s):    Fabio Delogu            (fabio.delogu@cimafoundation.org)
#               Simone Gabellani        (simone.gabellani@cimafoundation.org)
#               Francesco Silvestro     (francesco.silvestro@cimafoundation.org)
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
#                          1: Error in "Set algorithm"
#                          2: Error in "Initialize algorithm"
#                          3: Error in "Execute algorithm"
#
# General example usage: 
# python KF_DynamicData_EF_AirTemperature.py -settingfile settingfile.config -logfile logfile.config
# 
# Example
# python KF_DynamicData_EF_AirTemperature.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/kf_expertforecast/config_algorithms/kf_dynamicdata_ef-airtemperature_algorithm_local.config 
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/kf_expertforecast/config_logs/kf_dynamicdata_ef-airtemperature_logging_local.config
# 
#
# Version
# 1.0.0 (20151125) --> First release
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Method to get script argument(s)
def GetArgs():
    
    import argparse
    
    sScriptName=''; sSettingsFile=''; sLoggingFile=''
    
    oParser = argparse.ArgumentParser()
    oParser.add_argument('-settingfile', action="store", dest="sSettingFile")
    oParser.add_argument('-logfile', action="store", dest="sLoggingFile")
    oParserValue = oParser.parse_args()
    
    sScriptName = oParser.prog
    
    if oParserValue.sSettingFile:
        sSettingsFile = oParserValue.sSettingFile
    else:
        sSettingsFile = 'kf_dynamicdata_ef-airtemperature_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'kf_dynamicdata_ef-airtemperature_logging.config'
    
    return(sScriptName, sSettingsFile, sLoggingFile)

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #----------------------------------------------------------------------------
    # Script version 
    sProgramVersion = '1.0.0'
    sProjectName = 'KF'
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
    oLogStream.info('['+sProjectName+' DynamicData - EF AIRTEMPERATURE (Version '+sProgramVersion+')]')
    oLogStream.info('['+sProjectName+'] Start Program ... ')
    iExitStatus = 0
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load DynamicaData setting(s)
    oLogStream.info('[' + sProjectName + '] DynamicData - Set EF AIRTEMPERATURE configuration ... ')
    
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

        from Cpl_Apps_KF_DynamicData_EF_AirTemperature import Cpl_Apps_KF_DynamicData_EF_AirTemperature
        
        # Debug
        #import matplotlib.pylab as plt
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
        oLogStream.info('[' + sProjectName + '] DynamicData - Set EF AIRTEMPERATURE configuration ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Set EF AIRTEMPERATURE configuration ... FAILED',1,1)
        #----------------------------------------------------------------------------
        
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] DynamicData - Initialize EF AIRTEMPERATURE ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Get terrain data
        oDataTerrain = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Terrain']['VarSource'])) 
        
        # Get ancillary data
        oDataAncillary = GetAncillaryData.ExpertForecast_KF_WeatherStationRegistry(join(oDataInfo.oInfoSettings.oPathInfo['DataAncillary'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['CSV']['WeatherStation_Registry']['VarSource'])) 
        
        
        # Get time data
        oDataTime = GetTime(timenow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow'], 
                            timestep=int(oDataInfo.oInfoSettings.oParamsInfo['TimeStep']),
                            timeperiodpast=int(oDataInfo.oInfoSettings.oParamsInfo['TimePeriod']),
                            timerefHH = '03',
                            timerefworld=oDataInfo.oInfoSettings.oParamsInfo['TimeWorldRef'])
        #----------------------------------------------------------------------------
    
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DynamicData - Initialize EF AIRTEMPERATURE ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Initialize EF AIRTEMPERATURE ... FAILED',1,2)
        #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Run DynamicData
    oLogStream.info('[' + sProjectName + '] DynamicData - Execute EF AIRTEMPERATURE ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Dynamic Data
        oCpl_DynamicData = Cpl_Apps_KF_DynamicData_EF_AirTemperature(oDataTime=oDataTime, 
                                                                     oDataGeo=oDataTerrain, 
                                                                     oDataAncillary=oDataAncillary, oDataInfo=oDataInfo)
        
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
        oLogStream.info('[' + sProjectName + '] DynamicData - Execute EF AIRTEMPERATURE ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Execute EF AIRTEMPERATURE ... FAILED',1,3)
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
    
    oLogStream.info('['+sProjectName+'] DynamicData - EF AIRTEMPERATURE (Version '+sProgramVersion+')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
    
    GetException('',0,0)
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------






