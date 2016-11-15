#-------------------------------------------------------------------------------------
# Radar - Data Dynamic RRM SRI
# Version 1.0.0 (20151201)
#
# Author(s):    Fabio Delogu        (fabio.delogu@cimafoundation.org)
#               Simone Gabellani    (simone.gabellani@cimafoundation.org)
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
# Example: 
# python Radar_DynamicData_RRM_SRI.py -settingfile settingfile.config -logfile logfile.config
#
# General example usage: 
# python Radar_DynamicData_RRM_SRI.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/radar_rrm/config_algorithms/radar_dynamicdata_rrm-sri_algorithm_local.config
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/radar_rrm/config_logs/radar_dynamicdata_rrm-sri_logging_local.config
#
# Versions:
# 1.0.0 (20151201) --> First Release
#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
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
        sSettingsFile = 'radar_dynamicdata_rrm-sri_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'radar_dynamicdata_rrm-sri_logging.config'
    
    return(sScriptName, sSettingsFile, sLoggingFile)

#-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #-------------------------------------------------------------------------------------
    # Versioning
    sProgramVersion = '1.0.0'
    sProjectName = 'Radar'
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Get script argument(s)
    [sScriptName, sSettingsFile, sLoggingFile] = GetArgs()
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Log initialization
    import logging
    import logging.config
    logging.config.fileConfig(sLoggingFile)
    oLogStream = logging.getLogger('sLogger')
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Start Program
    oLogStream.info('['+sProjectName+' DataDynamic - RRM SRI (Version '+sProgramVersion+')]')
    oLogStream.info('['+sProjectName+'] Start Program ... ')
    iExitStatus = 0
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Load LandData setting(s)
    oLogStream.info('[' + sProjectName + '] DataDynamic - Load RRM SRI configuration ... ')
    
    # Check section
    try:
    
        #-------------------------------------------------------------------------------------
        # Complete library
        import os
        import time
    
        # Partial library
        from sys import argv
        from os.path import join
        from os.path import abspath
        
        # Import classes
        from src.GetException import GetException
        from src.GetSettings import GetSettings
        from src.GetTime import GetTime
        from src.GetGeoData import GetGeoData
        
        from Cpl_Apps_Radar_DynamicData_RRM_SRI import Cpl_Apps_Radar_DynamicData_RRM_SRI
        
        # Debugging library
        # import matplotlib.pylab as plt
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Path main
        sPathMain = os.getcwd() + '/'  # Setting PathMain
        abspath(sPathMain)  # Entering in path main folder
        #-------------------------------------------------------------------------------------
    
        #-------------------------------------------------------------------------------------
        # Get information data
        oDataInfo = GetSettings(sSettingsFile)
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # Time information
        dStartTime = time.time()
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DataDynamic - Load RRM SRI configuration ... OK')
        #-------------------------------------------------------------------------------------
        
    except:
    
        #-------------------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DataDynamic - Load RRM SRI configuration ... FAILED',1,1)
        #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] DataDynamic - Initialize RRM SRI ... ')
    
    # Check section
    try:
        
        #-------------------------------------------------------------------------------------
        # Get terrain data
        oDataTerrain = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Terrain']['VarSource']))
        
        # Get time data
        oDataTime = GetTime(timenow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow'], 
                            timestep=int(oDataInfo.oInfoSettings.oParamsInfo['TimeStep']),
                            timeperiodpast=int(oDataInfo.oInfoSettings.oParamsInfo['TimePeriod']),
                            timerefworld=oDataInfo.oInfoSettings.oParamsInfo['TimeWorldRef'])
        #-------------------------------------------------------------------------------------
    
        #-------------------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DataDynamic - Initialize RRM SRI ... OK')
        #-------------------------------------------------------------------------------------
    
    except:
    
        #-------------------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DataDynamic - Initialize RRM SRI ... FAILED',1,2)
        #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] DataDynamic - Execute RRM SRI ... ')
    
    # Check section
    try:
        
        #-------------------------------------------------------------------------------------
        # Dynamic Data
        oCpl_DynamicData = Cpl_Apps_Radar_DynamicData_RRM_SRI(oDataTime=oDataTime, oDataGeo=oDataTerrain, oDataInfo=oDataInfo)
        
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
            
        #-------------------------------------------------------------------------------------
        
        #-------------------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DataDynamic - Execute RRM SRI ... OK')
        #-------------------------------------------------------------------------------------
    
    except:
    
        #-------------------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DataDynamic - Execute RRM SRI ... FAILED',1,3)
        #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # Note about script parameter(s)
    oLogStream.info('NOTE - Algorithm parameter(s)')
    oLogStream.info('Script: ' + str(sScriptName) )
    #-------------------------------------------------------------------------------------
    
    #-------------------------------------------------------------------------------------
    # End Program
    dTimeElapsed = round(time.time() - dStartTime,1);
    
    oLogStream.info('['+sProjectName+'] DataDynamic - RRM SRI (Version '+sProgramVersion+')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
    
    GetException('',0,0)
    #-------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------

















