#----------------------------------------------------------------------------
# WS - DynamicData DB Network
# Version 2.0.7 (20150925)
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
# python WS_DynamicData_DB_Network.py -settingfile settingfile.config -logfile logfile.config
# 
# Example
# python WS_DynamicData_DB_Network.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/ws_db/config_algorithms/ws_dynamicdata_db-network_algorithm_local.config 
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_datacreator/ws_db/config_logs/ws_dynamicdata_db-network_logging_local.config
# 
#
# Version
# 2.0.7 (20150925) --> Updated code to save 3d variable
# 2.0.6 (20150812) --> Added code to multiprocess scripting
# 2.0.5 (20150812) --> Added argument(s) parser
# 2.0.4 (20150806) --> Added CSV reader/writer
# 2.0.3 (20150729) --> Updated codes, classes and methods
# 2.0.2 (20150702) --> Added get data using sql DB
# 2.0.1 (20150410) --> Fixed some bugs
# 2.0.0 (20150325) --> Release 2.0
# 1.0.1 (20140401) --> Starting version used in DRIHM2US project
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
        sSettingsFile = 'ws_dynamicdata_db-network_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'ws_dynamicdata_db-network_logging.config'
    
    return(sScriptName, sSettingsFile, sLoggingFile)

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #----------------------------------------------------------------------------
    # Script version 
    sProgramVersion = '2.0.7'
    sProjectName = 'WS'
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
    oLogStream.info('['+sProjectName+' DynamicData - DB NETWORK (Version '+sProgramVersion+')]')
    oLogStream.info('['+sProjectName+'] Start Program ... ')
    iExitStatus = 0
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load DynamicaData setting(s)
    oLogStream.info('[' + sProjectName + '] DynamicData - Set DB NETWORK configuration ... ')
    
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
        from src.GetGeoData import GetAnalyzedData
        
        from Cpl_Apps_WS_DynamicData_DB_Network import Cpl_Apps_WS_DynamicData_DB_Network
        
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
        oLogStream.info('[' + sProjectName + '] DynamicData - Set DB NETWORK configuration ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Set DB NETWORK configuration ... FAILED',1,1)
        #----------------------------------------------------------------------------
        
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] DynamicData - Initialize DB NETWORK ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Get vegetation data
        oDataVegType = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['VegetationType']['VarSource']))
    
        # Get terrain data
        oDataTerrain = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Terrain']['VarSource'])) 
        
        # Get terrain derived data
        oDataAnalyzed = GetAnalyzedData(join(oDataInfo.oInfoSettings.oPathInfo['DataStatic'], 
                                             oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Terrain']['VarSource']), 
                                             oDataInfo.oInfoSettings.oParamsInfo['DomainName'])
        
        # Get time data
        oDataTime = GetTime(timenow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow'], 
                            timestep=int(oDataInfo.oInfoSettings.oParamsInfo['TimeStep']),
                            timeperiodpast=int(oDataInfo.oInfoSettings.oParamsInfo['TimePeriod']),
                            timerefworld=oDataInfo.oInfoSettings.oParamsInfo['TimeWorldRef'])
        #----------------------------------------------------------------------------
    
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] DynamicData - Initialize DB NETWORK ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Initialize DB NETWORK ... FAILED',1,2)
        #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Run DynamicData
    oLogStream.info('[' + sProjectName + '] DynamicData - Execute DB NETWORK ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Dynamic Data
        oCpl_DynamicData = Cpl_Apps_WS_DynamicData_DB_Network(oDataTime=oDataTime, oDataGeo=oDataTerrain, oDataAnalyzed=oDataAnalyzed, oDataInfo=oDataInfo)
        
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
        oLogStream.info('[' + sProjectName + '] DynamicData - Execute DB NETWORK ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] DynamicData - Execute DB NETWORK ... FAILED',1,3)
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
    
    oLogStream.info('['+sProjectName+'] DynamicData - DB NETWORK (Version '+sProgramVersion+')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
    
    GetException('',0,0)
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------






