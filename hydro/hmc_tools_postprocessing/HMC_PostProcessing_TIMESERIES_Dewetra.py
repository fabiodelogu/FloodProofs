#----------------------------------------------------------------------------
# HYDROLOGICAL MODEL CONTINUUM - PostProcessing TIMESERIES Dewetra
# Version 1.0.2 (20160212)
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
# Function Argument(s): -settingfile -logfile -time
#
# Function returns:
# iExitStatus             Function code error
#                          0: OK
#                          1: Error in "Set model"
#                          2: Error in "Initialize model"
#                          3: Error in "Run model"
#
# General example usage: 
# python HMC_PostProcessing_TIMESERIES_Dewetra.py -settingfile settingsfile.config -logfile logfile.config
#
# Example:
# python HMC_PostProcessing_TIMESERIES_Dewetra.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_postprocessing/config_algorithms/hmc_postprocessing_timeseries-dewetra_algorithm_local_history_ws-db.config
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_postprocessing/config_logs/hmc_postprocessing_timeseries-dewetra_logging_local_history_ws-db.config
# -time 201512100400
# 
# python HMC_PostProcessing_TIMESERIES_Dewetra.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_postprocessing/config_algorithms/hmc_postprocessing_timeseries-dewetra_algorithm_local_realtime_nwp-lami-i7.config
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_postprocessing/config_logs/hmc_postprocessing_timeseries-dewetra_logging_local_realtime_nwp-lami-i7.config
# -time 201511160700
#
# python HMC_PostProcessing_TIMESERIES_Dewetra.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_postprocessing/config_algorithms/hmc_postprocessing_timeseries-dewetra_algorithm_local_realtime_rf-lami-i7_mp.config
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_postprocessing/config_logs/hmc_postprocessing_timeseries-dewetra_logging_local_realtime_rf-lami-i7_mp.config
# -time 201511181600
#
# Version
# 1.0.2 (20160212) --> Added checking for alarm and alert discharge values
# 1.0.1 (20151201) --> Added observed data in timeseries
# 1.0.0 (20151123) --> First Release
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Method to get script argument(s)
def GetArgs():
    
    import argparse
    
    sScriptName=''; sSettingsFile=''; sLoggingFile=''; sTimeNow=''
    
    oParser = argparse.ArgumentParser()
    oParser.add_argument('-settingfile', action="store", dest="sSettingFile")
    oParser.add_argument('-logfile', action="store", dest="sLoggingFile")
    oParser.add_argument('-time', action="store", dest="sTimeNow")
    oParserValue = oParser.parse_args()
    
    sScriptName = oParser.prog
    
    if oParserValue.sSettingFile:
        sSettingsFile = oParserValue.sSettingFile
    else:
        sSettingsFile = 'hmc_postprocessing_timeseries_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'hmc_postprocessing_timeseries_logging.config'
        
    if oParserValue.sTimeNow:
        sTimeNow = oParserValue.sTimeNow
    else:
        sTimeNow = ''
        
    return(sScriptName, sSettingsFile, sLoggingFile, sTimeNow)

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #----------------------------------------------------------------------------
    # Script version 
    sProgramVersion = '1.0.2'
    sProjectName = 'HMC'
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Get script argument(s)
    [sScriptName, sSettingsFile, sLoggingFile, sTimeNow] = GetArgs()
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
    oLogStream.info('['+sProjectName+' PostProcessing - TIMESERIES Dewetra (Version '+sProgramVersion+')]')
    oLogStream.info('['+sProjectName+'] Start Program ... ')
    iExitStatus = 0
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load DynamicaData setting(s)
    oLogStream.info('[' + sProjectName + '] PostProcessing - Set TIMESERIES Dewetra configuration ... ')
    
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
         
        from Cpl_Apps_HMC_PostProcessing_TIMESERIES_Dewetra import Cpl_Apps_HMC_PostProcessing_TIMESERIES_Dewetra
        
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
        oDataInfo = GetSettings(join(sPathMain, sSettingsFile), sTimeNow)
        #----------------------------------------------------------------------------
    
        #----------------------------------------------------------------------------
        # Time information
        dStartTime = time.time()
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] PostProcessing - Set TIMESERIES Dewetra configuration ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] PostProcessing - Set TIMESERIES Dewetra configuration ... FAILED',1,1)
        #----------------------------------------------------------------------------
        
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] Model - Initialize TIMESERIES Dewetra  ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------    
        # Get time data
        oDataTime = GetTime(timenow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow'], 
                            timestep=int(oDataInfo.oInfoSettings.oParamsInfo['TimeStep']),
                            timerefworld=oDataInfo.oInfoSettings.oParamsInfo['TimeWorldRef'])
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Initialize TIMESERIES Dewetra  ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Initialize TIMESERIES Dewetra  ... FAILED',1,2)
        #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load DynamicaData setting(s)
    oLogStream.info('[' + sProjectName + '] Model - Execute TIMESERIES Dewetra ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Model execution coupler
        oCpl_PostProcessing = Cpl_Apps_HMC_PostProcessing_TIMESERIES_Dewetra(oDataInfo, oDataTime)
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # Built post processing algorithm
        oCpl_PostProcessing.Builder()
        
        # Execute post processing algorithm
        oCpl_PostProcessing.Runner()
        
        # Finalize post processing algorithm
        oCpl_PostProcessing.Finalizer()
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Execute TIMESERIES Dewetra ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Execute TIMESERIES Dewetra ... FAILED',1,3)
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
    
    oLogStream.info('['+sProjectName+' PostProcessing - TIMESERIES Dewetra (Version '+sProgramVersion+')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
    
    GetException('',0,0)
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------







