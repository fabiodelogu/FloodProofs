#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='RF_Model_LAMI-I7_REALTIME'
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
python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_realtime_mp01.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_realtime_mp01.config &
iPID_RM_01=$! 
sleep 10
echo "Process PID RM 01: " $iPID_RM_01
echo ""

echo " ------> ENSEMBLE 02 ==> RUN 06 - 10"
python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_realtime_mp02.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_realtime_mp02.config &
iPID_RM_02=$! 
sleep 10
echo "Process PID RM 02: " $iPID_RM_02
echo ""

echo " ------> ENSEMBLE 03 ==> RUN 11 - 15"
python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_realtime_mp03.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_realtime_mp03.config &
iPID_RM_03=$! 
sleep 10
echo "Process PID RM 03: " $iPID_RM_03
echo ""

echo " ------> ENSEMBLE 04 ==> RUN 16 - 20"
python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_realtime_mp04.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_realtime_mp04.config &
iPID_RM_04=$! 
sleep 10
echo "Process PID RM 04: " $iPID_RM_04
echo ""

echo " ------> ENSEMBLE 05 ==> RUN 21 - 25"
python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_realtime_mp05.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_realtime_mp05.config &
iPID_RM_05=$! 
sleep 10
echo "Process PID RM 05: " $iPID_RM_05
echo ""

echo " ------> ENSEMBLE 06 ==> RUN 26 - 30"
python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_realtime_mp06.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_realtime_mp06.config &
iPID_RM_06=$! 
sleep 10
echo "Process PID RM 06: " $iPID_RM_06
echo ""

echo " ------> ENSEMBLE 07 ==> RUN 31 - 35"
python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_realtime_mp07.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_realtime_mp07.config &
iPID_RM_07=$! 
sleep 10
echo "Process PID RM 07: " $iPID_RM_07
echo ""

echo " ------> ENSEMBLE 08 ==> RUN 36 - 40"
python /hydro/hmc_tools_datacreator/rainfarm_lami/RF_Model_LAMI_I7.py -settingfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_algorithms/rf_model_lami-i7_algorithm_server_realtime_mp08.config -logfile /hydro/hmc_tools_datacreator/rainfarm_lami/config_logs/rf_model_lami-i7_logging_server_realtime_mp08.config &
iPID_RM_08=$! 
sleep 10
echo "Process PID RM 08: " $iPID_RM_08
echo ""

wait

echo " ------> CHECK RUN MODEL JOB"
jobs -l
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------
