#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='RS_DYNAMICDATA_DB_NETWORK_REALTIME'
sScriptVersion='1.0.1'
sScriptDate='2016/03/04'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Library
export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get information (-u to get gmt time)
sTimeNow=$(date -u +"%Y%m%d%H00")
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
python /hydro/hmc_tools_datacreator/rs_db/RS_DynamicData_DB_Network.py -settingfile /hydro/hmc_tools_datacreator/rs_db/config_algorithms/rs_dynamicdata_db-network_algorithm_server_realtime.config -logfile /hydro/hmc_tools_datacreator/rs_db/config_logs/rs_dynamicdata_db-network_logging_server_realtime.config
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------
