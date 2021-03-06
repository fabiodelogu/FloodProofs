#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='HMC_Model_RUN_MANAGER_DB_NETWORK_HISTORY'
sScriptVersion='1.0.0'
sScriptDate='2015/11/10'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Set case study

sTimeNow='201603241200' # ---> yyyymmddHHMM 201312010000 201103150000 201311160000
iDDSSync=1 # ---> value: 0,1
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Path(s) for sending result(s)
sScriptFolder="/home/dpc-marche/bin"

sDataArchivePath='/hydro/archive/history_ws-db'

sDataDDSPath_Grid='/share/hmc/realtime_ws-db'
sDataTypePath_Grid='/gridded'

sDataDDSPath_Point1='/share/series/gaugeobservation'
sDataTypePath_Point1='/timeseries/section_q'

sDataDDSPath_Point2='/share/series/damsgaugeobservation'
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
# Get information
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
python /hydro/hmc_tools_runner/HMC_Model_RUN_Manager.py -settingfile /hydro/hmc_tools_runner/config_algorithms/hmc_model_run-manager_algorithm_server_history_ws-db.config -logfile /hydro/hmc_tools_runner/config_logs/hmc_model_run-manager_logging_server_history_ws-db.config -time $sTimeNow
echo " Step 1 - Collect data and run model ... OK"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Script to postprocessing result(s)
echo " Step 2 - Post-Process model results ... "
python /hydro/hmc_tools_postprocessing/HMC_PostProcessing_TIMESERIES_Dewetra.py -settingfile /hydro/hmc_tools_postprocessing/config_algorithms/hmc_postprocessing_timeseries-dewetra_algorithm_server_history_ws-db.config -logfile /hydro/hmc_tools_postprocessing/config_logs/hmc_postprocessing_timeseries-dewetra_logging_server_history_ws-db.config -time $sTimeNow
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

















