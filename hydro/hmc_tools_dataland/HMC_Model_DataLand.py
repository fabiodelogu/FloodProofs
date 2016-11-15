#----------------------------------------------------------------------------
# HMC - StaticData LAND
# Version 2.0.4 (20150823)
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
# Function Argument(s):
#
# Function returns:
# iExitStatus             Function code error
#                          0: OK
#                          1: Error in "Load Library"
#                          2: Error in "Initialize LandData Tools"
#                          3: Error in "Run LandData Tools"
#
# General example usage: 
# python HMC_Model_DataLand.py -settingfile settingfile.config -logfile logfile.config
#
# Example:
# python HOC_DynamicData_OBS.py
# -settingfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_dataland/config_algorithms/hmc_model_dataland_algorithm_local.config 
# -logfile /home/fabio/Desktop/Project_RegioneMarche/hmc_tools_dataland/config_logs/hmc_model_dataland_logging_local.config
#
# Version:
# 2.0.4 (20150823) --> Added argument(s) parser
# 2.0.3 (20150528) --> Add data masking with internal or external mask
# 2.0.0 (20150310) --> Release 2.0
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
        sSettingsFile = 'hmc_model_dataland_algorithm.config'
    
    if oParserValue.sLoggingFile:
        sLoggingFile = oParserValue.sLoggingFile
    else:
        sLoggingFile = 'hmc_model_dataland_logging.config'
    
    return(sScriptName, sSettingsFile, sLoggingFile)

#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# Script Main
if __name__ == "__main__":

    #----------------------------------------------------------------------------
    # Script version 
    sProgramVersion = '2.0.4'
    sProjectName = 'HMC'
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
    oLogStream.info('['+sProjectName+' Model - DATALAND (Version '+sProgramVersion+')]')
    oLogStream.info('['+sProjectName+'] Start Program ... ')
    iExitStatus = 0
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Load LandData setting(s)
    oLogStream.info('[' + sProjectName + '] Model - Load DATALAND configuration ... ')
    
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
        from src.GetGeoData import GetGeoData
        from Cpl_Apps_HMC_Model_DataLand import Cpl_Apps_HMC_Model_DataLand
        
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
        oLogStream.info('[' + sProjectName + '] Model - Load DATALAND configuration ... OK')
        #----------------------------------------------------------------------------
        
        
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Load DATALAND configuration ... FAILED',1,1)
        #----------------------------------------------------------------------------
        
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Initialize LandData Tools
    oLogStream.info('[' + sProjectName + '] Model - Initialize DATALAND ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Get vegetation data
        oDataVegType = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStaticSource'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['VegetationType']['VarSource']))
        # Get terrain data
        oDataTerrain = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStaticSource'], 
                                       oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Terrain']['VarSource'])) 
        # Get mask data
        oDataMask = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStaticSource'], 
                                    oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['Mask']['VarSource']))
        
        # Get nature data
        oDataNature = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStaticSource'], 
                                    oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['NatureType']['VarSource']))
        
        # Get alert area data
        oDataAA = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStaticSource'], 
                                    oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['AlertArea']['VarSource']))
        
        # Get watermark data
        oDataWaterMark = GetGeoData(join(oDataInfo.oInfoSettings.oPathInfo['DataStaticSource'], 
                                         oDataInfo.oInfoVarStatic.oDataInputStatic['ASCII']['WaterMark']['VarSource']))
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Initialize DATALAND ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Initialize DATALAND ... FAILED',1,2)
        #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    
    #----------------------------------------------------------------------------
    # Run LandData Tools
    oLogStream.info('[' + sProjectName + '] Model - Execute DATALAND ... ')
    
    # Check section
    try:
        
        #----------------------------------------------------------------------------
        # Dynamic Data
        oCpl_DataLand = Cpl_Apps_HMC_Model_DataLand(oDataTerrain=oDataTerrain, oDataVegType=oDataVegType, 
                                                   oDataMask=oDataMask, oDataWaterMark=oDataWaterMark,
                                                   oDataNature=oDataNature, oDataAA=oDataAA,
                                                   oDataInfo=oDataInfo)
        
        # Compute static data
        oCpl_DataLand.computeStaticData()
        
        # Mask static data
        oCpl_DataLand.maskStaticData()
        
        # Save static data
        oCpl_DataLand.saveStaticData()  
        #----------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------
        # End section
        oLogStream.info('[' + sProjectName + '] Model - Execute DATALAND ... OK')
        #----------------------------------------------------------------------------
    
    except:
    
        #----------------------------------------------------------------------------
        # Algorithm exception(s)
        GetException('[' + sProjectName + '] Model - Execute DATALAND ... FAILED',1,3)
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
    
    oLogStream.info('['+sProjectName+'] Model - DATALAND (Version '+sProgramVersion+')]')
    oLogStream.info('End Program - Time elapsed: ' + str(dTimeElapsed) + ' seconds')
    
    GetException('',0,0)
    #----------------------------------------------------------------------------

#----------------------------------------------------------------------------







