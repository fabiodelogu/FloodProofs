#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='HMC_Model_CLEANER_DATA_REALTIME_RUN_HOURLY'
sScriptVersion='1.0.0'
sScriptDate='2015/12/10'
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
# Script to remove old run
echo " Step - Remove old run ... "

echo " ------> RUN: realtime_ws-db ... "
rm -r "/hydro/run/realtime_ws-db/data/"
mkdir "/hydro/run/realtime_ws-db/data/"
rm -r "/hydro/run/realtime_ws-db/exec/"
mkdir "/hydro/run/realtime_ws-db/exec/"
rm -r "/hydro/run/realtime_ws-db/cache/"
mkdir "/hydro/run/realtime_ws-db/cache/"
rm -r "/hydro/run/realtime_ws-db/temp/"
mkdir "/hydro/run/realtime_ws-db/temp/"
echo " ------> RUN: realtime_ws-db ... OK"

echo " ------> RUN: realtime_radar-sri ... "
rm -r "/hydro/run/realtime_radar-sri/data/"
mkdir "/hydro/run/realtime_radar-sri/data/"
rm -r "/hydro/run/realtime_radar-sri/exec/"
mkdir "/hydro/run/realtime_radar-sri/exec/"
rm -r "/hydro/run/realtime_radar-sri/cache/"
mkdir "/hydro/run/realtime_radar-sri/cache/"
rm -r "/hydro/run/realtime_radar-sri/temp/"
mkdir "/hydro/run/realtime_radar-sri/temp/"
echo " ------> RUN: realtime_radar-sri ... OK"

echo " Step - Remove old run ... OK"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------


