#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='HMC_Model_RUN_MANAGER_RF_LAMI-I7_HISTORY'
sScriptVersion='1.0.0'
sScriptDate='2015/11/10'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Set case study
sTimeNow='201603220600' # ---> yyyymmdd0000 
iDDSSync=1 # ---> value: 0,1
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Path(s) for sending result(s)
sScriptFolder="/home/dpc-marche/bin"

sDataArchivePath='/hydro/archive/history_rf-lami-i7'

sDataDDSPath_Grid=''
sDataTypePath_Grid=''

sDataDDSPath_Point1='/share/series/probabilisticlami'
sDataTypePath_Point1='/timeseries/section_q'

sDataDDSPath_Point2='/share/series/damsprobabilisticlami'
sDataTypePath_Point2='/timeseries/dam_volume'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Library
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/gdal-2.0.0/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/netcdf-4.1.2/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/hdf5-1.8.7/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/zlib-1.2.5/lib/
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/home/dpc-marche/library/hdf4-4.2.10/lib/

# Path executable(s)
export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/

# MODIS Reprojection Tool
MRT_HOME="/home/dpc-marche/library/MODIS_Reprojection_Tool/"
PATH="$PATH:/home/dpc-marche/library/MODIS_Reprojection_Tool/bin"
MRT_DATA_DIR="/home/dpc-marche/library/MODIS_Reprojection_Tool/data"
export MRT_HOME PATH MRT_DATA_DIR

# Set stack size to unlimited
ulimit -s unlimited
ulimit -a
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get information (-u to get gmt time)
#sTimeNow=$(date -u +"%Y%m%d%H00")
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
echo " DDS SYNC: " $iDDSSync
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Script to run model
echo " Step 1 - Collect data and run model ... "
echo " ------> ENSEMBLE 01 ==> RUN 01 - 03"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp01.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp01.config -time $sTimeNow &
iPID_RM_01=$!
sleep 10
echo "Process PID RM 01: " $iPID_RM_01
echo ""

echo " ------> ENSEMBLE 02 ==> RUN 04 - 06"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp02.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp02.config -time $sTimeNow &
iPID_RM_02=$!
sleep 10
echo "Process PID RM 02: " $iPID_RM_02
echo ""

echo " ------> ENSEMBLE 03 ==> RUN 07 - 09"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp03.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp03.config -time $sTimeNow &
iPID_RM_03=$!
sleep 10
echo "Process PID RM 03: " $iPID_RM_03
echo ""

echo " ------> ENSEMBLE 04 ==> RUN 10 - 12"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp04.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp04.config -time $sTimeNow &
iPID_RM_04=$!
sleep 10
echo "Process PID RM 04: " $iPID_RM_04
echo ""

echo " ------> ENSEMBLE 05 ==> RUN 13 - 15"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp05.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp05.config -time $sTimeNow &
iPID_RM_05=$!
sleep 10
echo "Process PID RM 05: " $iPID_RM_05
echo ""

echo " ------> ENSEMBLE 06 ==> RUN 16 - 18"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp06.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp06.config -time $sTimeNow &
iPID_RM_06=$!
sleep 10
echo "Process PID RM 06: " $iPID_RM_06
echo ""

echo " ------> ENSEMBLE 07 ==> RUN 19 - 21"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp07.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp07.config -time $sTimeNow &
iPID_RM_07=$!
sleep 10
echo "Process PID RM 07: " $iPID_RM_07
echo ""

echo " ------> ENSEMBLE 08 ==> RUN 22 - 24"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp08.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp08.config -time $sTimeNow &
iPID_RM_08=$!
sleep 10
echo "Process PID RM 08: " $iPID_RM_08
echo ""

echo " ------> ENSEMBLE 09 ==> RUN 25 - 27"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp09.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp09.config -time $sTimeNow &
iPID_RM_09=$!
sleep 10
echo "Process PID RM 09: " $iPID_RM_09
echo ""

echo " ------> ENSEMBLE 10 ==> RUN 28 - 30"
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp10.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp10.config -time $sTimeNow &
iPID_RM_10=$!
sleep 10
echo "Process PID RM 10: " $iPID_RM_10
echo ""

#echo " ------> ENSEMBLE 11 ==> RUN 31 - 33"
#python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp11.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp11.config -time $sTimeNow &
#iPID_RM_11=$!
#sleep 10
#echo "Process PID RM 11: " $iPID_RM_11
#echo ""

#echo " ------> ENSEMBLE 12 ==> RUN 34 - 36"
#python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp12.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp12.config -time $sTimeNow &
#iPID_RM_12=$!
#sleep 10
#echo "Process PID RM 12: " $iPID_RM_12
#echo ""

#echo " ------> ENSEMBLE 13 ==> RUN 37 - 39"
#python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp13.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp13.config -time $sTimeNow &
#iPID_RM_13=$!
#sleep 10
#echo "Process PID RM 13: " $iPID_RM_13
#echo ""

#echo " ------> ENSEMBLE 14 ==> RUN 40 - 42"
#python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_rf-lami-i7_mp14.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_rf-lami-i7_mp14.config -time $sTimeNow &
#iPID_RM_14=$!
#sleep 10
#echo "Process PID RM 14: " $iPID_RM_14
#echo ""

wait

echo " ------> CHECK RUN MODEL JOB"
jobs -l

echo " Step 1 - Collect data and run model ... OK"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Script to postprocessing algorithm
echo " Step 2 - Post-Process model results ... "
python /hydro/hmc_tools_postprocessing/HMC_PostProcessing_TIMESERIES_Dewetra.py -settingfile /hydro/hmc_tools_postprocessing/config_algorithms/hmc_postprocessing_timeseries-dewetra_algorithm_server_history_rf-lami-i7_mp.config -logfile /hydro/hmc_tools_postprocessing/config_logs/hmc_postprocessing_timeseries-dewetra_logging_server_history_rf-lami-i7_mp.config -time $sTimeNow
iPID_PP=$!
echo "Process PID PP: " $iPID_PP
echo ""

wait

echo " ------> CHECK POST PROCESS JOB"
jobs -l

echo " Step 2 - Post-Process model results ... OK"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Script to postprocessing result(s)
echo " Step 3 - Send results to dds ... "

if (( $iDDSSync == 1 )); then
    echo "running dpc-marche2dds with param: $sScriptFolder $sTimeNow $sDataArchivePath $sDataDDSPath_Point1 $sDataTypePath_Point1" >> /home/dpc-marche/log/dpc-marche2dds.log
    cd $sScriptFolder
    #/bin/bash $sScriptFolder/dpc-marche2dds_grid.sh $sTimeNow $sDataArchivePath $sDataDDSPath_Grid $sDataTypePath_Grid
    /bin/bash $sScriptFolder/dpc-marche2dds_point.sh $sTimeNow $sDataArchivePath $sDataDDSPath_Point1 $sDataTypePath_Point1
    /bin/bash $sScriptFolder/dpc-marche2dds_point.sh $sTimeNow $sDataArchivePath $sDataDDSPath_Point2 $sDataTypePath_Point2
    echo " Step 3 - Send results to dds ... OK"
else
    echo " Step 3 - Send results to dds ... SKIPPED"
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------
