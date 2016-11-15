#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='RF_Model_ECMWF-0125_REALTIME'
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
# Script to run model
echo " ------> ENSEMBLE 01 ==> RUN 01 - 05"
python /hydro/hmc_tools_datacreator/rainfarm_ecmwf/RF_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_algorithms/rf_model_ecmwf-0125_algorithm_server_realtime_mp01.config -logfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_logs/rf_model_ecmwf-0125_logging_server_realtime_mp01.config &
iPID_RM_01=$! 
sleep 10
echo "Process PID RM 01: " $iPID_RM_01
echo ""

python /hydro/hmc_tools_datacreator/rainfarm_ecmwf/RF_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_algorithms/rf_model_ecmwf-0125_algorithm_server_realtime_mp02.config -logfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_logs/rf_model_ecmwf-0125_logging_server_realtime_mp02.config &


python /hydro/hmc_tools_datacreator/rainfarm_ecmwf/RF_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_algorithms/rf_model_ecmwf-0125_algorithm_server_realtime_mp03.config -logfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_logs/rf_model_ecmwf-0125_logging_server_realtime_mp03.config &


python /hydro/hmc_tools_datacreator/rainfarm_ecmwf/RF_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_algorithms/rf_model_ecmwf-0125_algorithm_server_realtime_mp04.config -logfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_logs/rf_model_ecmwf-0125_logging_server_realtime_mp04.config &


python /hydro/hmc_tools_datacreator/rainfarm_ecmwf/RF_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_algorithms/rf_model_ecmwf-0125_algorithm_server_realtime_mp05.config -logfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_logs/rf_model_ecmwf-0125_logging_server_realtime_mp05.config &


python /hydro/hmc_tools_datacreator/rainfarm_ecmwf/RF_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_algorithms/rf_model_ecmwf-0125_algorithm_server_realtime_mp06.config -logfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_logs/rf_model_ecmwf-0125_logging_server_realtime_mp06.config &

python /hydro/hmc_tools_datacreator/rainfarm_ecmwf/RF_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_algorithms/rf_model_ecmwf-0125_algorithm_server_realtime_mp07.config -logfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_logs/rf_model_ecmwf-0125_logging_server_realtime_mp07.config &


python /hydro/hmc_tools_datacreator/rainfarm_ecmwf/RF_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_algorithms/rf_model_ecmwf-0125_algorithm_server_realtime_mp08.config -logfile /hydro/hmc_tools_datacreator/rainfarm_ecmwf/config_logs/rf_model_ecmwf-0125_logging_server_realtime_mp08.config &




















