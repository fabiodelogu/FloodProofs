#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='HMC_Model_CLEANER_DATA_REALTIME_RUN_DAILY'
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

echo " ------> RUN: realtime_nwp-lami-i7 ... "
rm -r "/hydro/run/realtime_nwp-lami-i7/data/"
mkdir "/hydro/run/realtime_nwp-lami-i7/data/"
rm -r "/hydro/run/realtime_nwp-lami-i7/exec/"
mkdir "/hydro/run/realtime_nwp-lami-i7/exec/"
rm -r "/hydro/run/realtime_nwp-lami-i7/cache/"
mkdir "/hydro/run/realtime_nwp-lami-i7/cache/"
rm -r "/hydro/run/realtime_nwp-lami-i7/temp/"
mkdir "/hydro/run/realtime_nwp-lami-i7/temp/"
echo " ------> RUN: realtime_nwp-lami-i7 ... OK"

echo " ------> RUN: realtime_nwp-ecmwf-0125 ... "
rm -r "/hydro/run/realtime_nwp-ecmwf-0125/data/"
mkdir "/hydro/run/realtime_nwp-ecmwf-0125/data/"
rm -r "/hydro/run/realtime_nwp-ecmwf-0125/exec/"
mkdir "/hydro/run/realtime_nwp-ecmwf-0125/exec/"
rm -r "/hydro/run/realtime_nwp-ecmwf-0125/cache/"
mkdir "/hydro/run/realtime_nwp-ecmwf-0125/cache/"
rm -r "/hydro/run/realtime_nwp-ecmwf-0125/temp/"
mkdir "/hydro/run/realtime_nwp-ecmwf-0125/temp/"
echo " ------> RUN: realtime_nwp-ecmwf-0125 ... OK"

echo " ------> RUN: realtime_rf-lami-i7 ... "
rm -r "/hydro/run/realtime_rf-lami-i7/data/"
mkdir "/hydro/run/realtime_rf-lami-i7/data/"
rm -r "/hydro/run/realtime_rf-lami-i7/exec/"
mkdir "/hydro/run/realtime_rf-lami-i7/exec/"
rm -r "/hydro/run/realtime_rf-lami-i7/cache/"
mkdir "/hydro/run/realtime_rf-lami-i7/cache/"
rm -r "/hydro/run/realtime_rf-lami-i7/temp/"
mkdir "/hydro/run/realtime_rf-lami-i7/temp/"
echo " ------> RUN: realtime_rf-lami-i7 ... OK"

echo " ------> RUN: realtime_rf-ecmwf-0125 ... "
rm -r "/hydro/run/realtime_rf-ecmwf-0125/data/"
mkdir "/hydro/run/realtime_rf-ecmwf-0125/data/"
rm -r "/hydro/run/realtime_rf-ecmwf-0125/exec/"
mkdir "/hydro/run/realtime_rf-ecmwf-0125/exec/"
rm -r "/hydro/run/realtime_rf-ecmwf-0125/cache/"
mkdir "/hydro/run/realtime_rf-ecmwf-0125/cache/"
rm -r "/hydro/run/realtime_rf-ecmwf-0125/temp/"
mkdir "/hydro/run/realtime_rf-ecmwf-0125/temp/"
echo " ------> RUN: realtime_rf-ecmwf-0125 ... OK"

echo " ------> RUN: realtime_ef-lami-i7 ... "
rm -r "/hydro/run/realtime_ef-lami-i7/data/"
mkdir "/hydro/run/realtime_ef-lami-i7/data/"
rm -r "/hydro/run/realtime_ef-lami-i7/exec/"
mkdir "/hydro/run/realtime_ef-lami-i7/exec/"
rm -r "/hydro/run/realtime_ef-lami-i7/cache/"
mkdir "/hydro/run/realtime_ef-lami-i7/cache/"
rm -r "/hydro/run/realtime_ef-lami-i7/temp/"
mkdir "/hydro/run/realtime_ef-lami-i7/temp/"
echo " ------> RUN: realtime_ef-lami-i7 ... OK"

echo " Step - Remove old run ... OK"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Script to remove lock files
echo " Step - Remove lock files ... "

rm -r "/home/dpc-marche/lock/"
mkdir "/home/dpc-marche/lock/"

echo " Step - Remove lock files ... OK"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------


