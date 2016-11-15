#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='NWP_DYNAMICDATA_ECMWF_0125_REALTIME'
sScriptVersion='1.0.1'
sScriptDate='2016/03/04'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Library
export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get information (-u to get gmt time)
#sTimeNow=$(date -u +"%Y%m%d%H00")
sTimeNow=$(date +"%Y%m%d%H00")
# Get script folder
sScriptFolder="/home/dpc-marche/bin"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Start - Script
echo "-------------------------------------------------------------"
echo " $sScriptName - Version $sScriptVersion - Date $sScriptDate"
echo "-------------------------------------------------------------"
echo ""
echo " Start script ... "
echo ""
echo " TIMENOW: " $sTimeNow
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Run - Script
python /hydro/hmc_tools_datacreator/nwp_ecmwf/NWP_DynamicData_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/nwp_ecmwf/config_algorithms/nwp_dynamicdata_ecmwf-0125_algorithm_server_realtime.config -logfile /hydro/hmc_tools_datacreator/nwp_ecmwf/config_logs/nwp_dynamicdata_ecmwf-0125_logging_server_realtime.config
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------
