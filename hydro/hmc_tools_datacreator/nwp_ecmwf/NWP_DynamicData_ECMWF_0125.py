#----------------------------------------------------------------------------
# NWP - DynamicData ECMWF 0125
# Version 2.0.4 (20150923)
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
# python NWP_DynamicData_ECMWF_0125.py -settingfile settingfile.config -logfile logfile.config
# 
# Example:
# python NWP_DynamicData_ECMWF_0125.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/nwp_ecmwf/config_algorithms/nwp_dynamicdata_ecmwf-0125_algorithm_local.config
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/nwp_ecmwf/config_logs/nwp_dynamicdata_ecmwf-0125_logging_local.config
#
# Version
# 2.0.4 (20150923) --> Updated code to save 3d variable
# 2.0.3 (20150812) --> Added code to multiprocess scripting
# 2.0.2 (20150812) --> Added argument(s) parser
# 2.0.0 (20150325) --> Release 2.0
# 1.0.1 (20140401) --> Starting version used in DRIHM2US project
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
        sSettingsFile = 'nwp_dynamicdata_ecmwf-0125_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'nwp_dynamicdata_ecmwf-0125_logging.config'
    
    return(sScriptName, sSettingsFile, sLoggingFile)

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #----------------------------------------------------------------------------
    # Script version 
    sProgramVersion = '2.0.4'
    sProjectName = 'NWP'
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
    oLogStream.info('['+sProjectName+' DynamicData - ECMWF 0125 (Version '+sProgramVersion+')]')
    oLogStream.info('['+sProjectName+'] Start Program ... ')
    iExitStatus = 0
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load DynamicaData setting(s)
    oLogStream.info('[' + sProjectName + '] DynamicData - Set ECMWF 0125 configuration ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Complete library
        import os.path
        import time
        
        # Partial Library
        from os.path import join
        
        # Import classes
        from src.GetException import GetException
        from src.GetSettings import GetSettings
        from src.GetTime import GetTime
        
        from src.GetGeoData import GetGeoData
        
        from Cpl_Apps_NWP_DynamicData_ECMWF_0125 import Cpl_Apps_NWP_DynamicData_ECMWF_0125

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
        oLogStream.info('[' + sProjectName + '] DynamicData - Set ECMWF 0125 configuration ... OK')
        #----------------------------------------------------------------------------
        
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Set ECMWF 0125 configuration ... FAILED',1,1)
        #----------------------------------------------------------------------------
        
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] DynamicData - Initialize ECMWF 0125 ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Get vegetation data
        oDataVegType = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['VegetationType']['VarSource']))
    
        # Get terrain data
        oDataTerrain = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Terrain']['VarSource'])) 
        
        # Get time data
        oDataTime = GetTime(timenow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow'], 
                            timestep=int(oDataInfo.oInfoSettings.oParamsInfo['TimeStep']),
                            timeperiodpast=int(oDataInfo.oInfoSettings.oParamsInfo['TimePeriod']),
                            timerefHH = '00',
                            timerefworld=oDataInfo.oInfoSettings.oParamsInfo['TimeWorldRef'])
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DynamicData - Initialize ECMWF 0125 ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Initialize ECMWF 0125 ... FAILED',1,2)
        #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Run DynamicData
    oLogStream.info('[' + sProjectName + '] DynamicData - Execute ECMWF 0125 ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Dynamic Data
        oCpl_DynamicData = Cpl_Apps_NWP_DynamicData_ECMWF_0125(oDataTime=oDataTime, oDataGeo=oDataTerrain, oDataInfo=oDataInfo)
        
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
        oLogStream.info('[' + sProjectName + '] DynamicData - Execute ECMWF 0125 ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Execute ECMWF 0125 ... FAILED',1,3)
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
    
    oLogStream.info('['+sProjectName+'] DynamicData - ECMWF 0125 (Version '+sProgramVersion+')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
    
    GetException('',0,0)
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------
