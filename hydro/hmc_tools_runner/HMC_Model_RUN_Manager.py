#----------------------------------------------------------------------------
# HYDROLOGICAL MODEL CONTINUUM - RUN Manager
# Version 1.6.2 (20151022)
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
#                          1: Error in "Set model"
#                          2: Error in "Initialize model"
#                          3: Error in "Run model"
#
# General example usage: 
# python HMC_Model_RUN_Manager.py -settingfile settingsfile.config -logfile logfile.config
#
# Example:
# python HMC_Model_RUN_Manager.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_local_history_ws-db.config 
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_local_history_ws-db.config
# -time 201511091200
#
# python HMC_Model_RUN_Manager.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_local_realtime_nwp-lami-i7.config 
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_local_realtime_nwp-lami-i7.config 
# -time 201511160700
#
# python HMC_Model_RUN_Manager.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_local_realtime_nwp-ecmwf-0125.config 
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_local_realtime_nwp-ecmwf-0125.config
# -time 201511161300
#
# python HMC_Model_RUN_Manager.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_local_realtime_rf-lami-i7.config 
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_local_realtime_rf-lami-i7.config 
# -time 201511160700
#
# python HMC_Model_RUN_Manager.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_local_realtime_subfor.config 
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_local_realtime_subfor.config 
# -time 201512051400
#
# Version
# 1.6.2 (20151022) --> Updated functions, names and other stuff
# 1.6.1 (20151002) --> Corrected info file writing function
# 1.6.0 (20150928) --> Updated code style using updated data and algorithm structure
# 1.5.1 (20150903) --> Updated code style and other stuff
# 1.5.0 (20150707) --> Release 1.5 to Marche project
# 1.0.0 (20140401) --> Starting version used in DRIHM2US project
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Method to get script argument(s)
def GetArgs():
    
    import argparse
    
    sScriptName=''; sSettingsFile=''; sLoggingFile=''; sTimeNow = ''
    
    oParser = argparse.ArgumentParser()
    oParser.add_argument('-settingfile', action="store", dest="sSettingFile")
    oParser.add_argument('-logfile', action="store", dest="sLoggingFile")
    oParser.add_argument('-time', action="store", dest="sTimeNow")
    oParserValue = oParser.parse_args()
    
    sScriptName = oParser.prog
    
    if oParserValue.sSettingFile:
        sSettingsFile = oParserValue.sSettingFile
    else:
        sSettingsFile = 'hmc_model_run-manager_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'hmc_model_run-manager_logging.config'
        
    if oParserValue.sTimeNow:
        sTimeNow = oParserValue.sTimeNow
    else:
        sTimeNow = ''
    
    return(sScriptName, sSettingsFile, sLoggingFile, sTimeNow)#-------------------------------------------------------------------------------------

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #----------------------------------------------------------------------------
    # Script version 
    sProgramVersion = '1.6.2'
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
    oLogStream.info('['+sProjectName+' Model - RUN MANAGER (Version '+sProgramVersion+')]')
    oLogStream.info('['+sProjectName+'] Start Program ... ')
    iExitStatus = 0
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load DynamicaData setting(s)
    oLogStream.info('[' + sProjectName + '] Model - Set RUN MANAGER configuration ... ')
    
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
        
        from Cpl_Apps_HMC_Model_RUN_Manager import Cpl_Apps_HMC_Model_RUN_Manager
        
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
        oLogStream.info('[' + sProjectName + '] Model - Set RUN MANAGER configuration ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Set RUN MANAGER configuration ... FAILED',1,1)
        #----------------------------------------------------------------------------
        
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Initialize DynamicData
    oLogStream.info('[' + sProjectName + '] Model - Initialize RUN MANAGER  ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------    
        # Get time data
        oDataTime = GetTime(timenow=oDataInfo.oInfoSettings.oParamsInfo['TimeNow'], 
                            timestep=int(oDataInfo.oInfoSettings.oParamsInfo['TimeStep']),
                            timeperiodpast=int(oDataInfo.oInfoSettings.oParamsInfo['TimePeriodObs']),
                            timeperiodfut=int(oDataInfo.oInfoSettings.oParamsInfo['TimePeriodFor']),
                            timerefworld=oDataInfo.oInfoSettings.oParamsInfo['TimeWorldRef'])
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Initialize RUN MANAGER  ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Initialize RUN MANAGER  ... FAILED',1,2)
        #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load DynamicaData setting(s)
    oLogStream.info('[' + sProjectName + '] Model - Execute RUN MANAGER  ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Model execution coupler
        oCpl_ModelExecution = Cpl_Apps_HMC_Model_RUN_Manager(oDataInfo, oDataTime)
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # Cycle(s) on ensemble
        for iEns, sEns in enumerate(oCpl_ModelExecution.oDataEnsemble.values()):
            
            #----------------------------------------------------------------------------
            # Built model run
            oCpl_ModelExecution.Builder(sEns)
            #----------------------------------------------------------------------------
                
            #----------------------------------------------------------------------------
            # Execute model run
            oCpl_ModelExecution.Runner(sEns)
            #----------------------------------------------------------------------------
                
            #----------------------------------------------------------------------------
            # Finalize model run
            oCpl_ModelExecution.Finalizer(sEns)
            #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Execute RUN MANAGER ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Execute RUN MANAGER ... FAILED',1,3)
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
    
    oLogStream.info('['+sProjectName+'] Model - RUN MANAGER (Version '+sProgramVersion+')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
    
    GetException('',0,0)
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------







