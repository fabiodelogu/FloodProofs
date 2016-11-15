#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='HMC_Model_POSTPROCESSING_RF_DYNAMICUPDATE_REALTIME'
sScriptVersion='1.0.0'
sScriptDate='2016/03/11'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Path(s) for sending result(s)

# RF LAMI-I7
sDataArchivePath_01='/hydro/archive/realtime_rf-lami-i7'

sDataDDSPath_Grid_01=''
sDataTypePath_Grid_01=''

sDataDDSPath_Point1_01='/share/series/probabilisticlami'
sDataTypePath_Point1_01='/timeseries/section_q'

sDataDDSPath_Point2_01='/share/series/damsprobabilisticlami'
sDataTypePath_Point2_01='/timeseries/dam_volume'

# RF ECMWF-0125
sDataArchivePath_02='/hydro/archive/realtime_rf-ecmwf-0125'

sDataDDSPath_Grid_02=''
sDataTypePath_Grid_02=''

sDataDDSPath_Point1_02='/share/series/probabilisticecmwf'
sDataTypePath_Point1_02='/timeseries/section_q'

sDataDDSPath_Point2_02='/share/series/damsprobabilisticecmwf'
sDataTypePath_Point2_02='/timeseries/dam_volume'

# RF EXPERT-FORECAST-LAMI-I7
sDataArchivePath_03='/hydro/archive/realtime_ef-lami-i7'

sDataDDSPath_Grid_03=''
sDataTypePath_Grid_03=''

sDataDDSPath_Point1_03='/share/series/probabilisticexpertforecast'
sDataTypePath_Point1_03='/timeseries/section_q'

sDataDDSPath_Point2_03='/share/series/damsprobabilisticexpertforecast'
sDataTypePath_Point2_03='/timeseries/dam_volume'
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
iTimeHour=$(date -u +"%H")

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
# Script to postprocessing algorithm
echo " Step 1 - Post-Process model results for rf-lami-i7 ... "
if (( $iTimeHour >= 8 )); then
    
    # Get time
    sTimeNow_01=$(date -u +"%Y%m%d0700")
    
    # Execute post-processing script
    echo " ------ Execute post-processing script ... "
    python /hydro/hmc_tools_postprocessing/HMC_PostProcessing_TIMESERIES_Dewetra.py -settingfile /hydro/hmc_tools_postprocessing/config_algorithms/hmc_postprocessing_timeseries-dewetra_algorithm_server_realtime_rf-lami-i7_mp.config -logfile /hydro/hmc_tools_postprocessing/config_logs/hmc_postprocessing_timeseries-dewetra_logging_server_realtime_rf-lami-i7_mp.config -time $sTimeNow_01
    echo " ------ Execute post-processing script ... OK"
    
    # Send results to dds
    echo " ------ Send results to dds ... "
    /bin/bash $sScriptFolder/dpc-marche2dds_point.sh $sTimeNow_01 $sDataArchivePath_01 $sDataDDSPath_Point1_01 $sDataTypePath_Point1_01
    /bin/bash $sScriptFolder/dpc-marche2dds_point.sh $sTimeNow_01 $sDataArchivePath_01 $sDataDDSPath_Point2_01 $sDataTypePath_Point2_01
    echo " ------ Send results to dds ... OK"
    
    echo " Step 1 - Post-Process model results for rf-lami-i7 ... OK "
else
    echo " Step 1 - Post-Process model results for rf-lami-i7 ... SKIPPED"
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Script to postprocessing algorithm
echo " Step 2 - Post-Process model results for rf-ecmwf-0125 ... "
if (( $iTimeHour >= 9 )); then
    
    # Get time
    sTimeNow_02=$(date -u +"%Y%m%d0800")
    
    # Execute post-processing script
    echo " ------ Execute post-processing script ... "
    python /hydro/hmc_tools_postprocessing/HMC_PostProcessing_TIMESERIES_Dewetra.py -settingfile /hydro/hmc_tools_postprocessing/config_algorithms/hmc_postprocessing_timeseries-dewetra_algorithm_server_realtime_rf-ecmwf-0125_mp.config -logfile /hydro/hmc_tools_postprocessing/config_logs/hmc_postprocessing_timeseries-dewetra_logging_server_realtime_rf-ecmwf-0125_mp.config -time $sTimeNow_02
    echo " ------ Execute post-processing script ... OK"
    
    # Send results to dds
    echo " ------ Send results to dds ... "
    /bin/bash $sScriptFolder/dpc-marche2dds_point.sh $sTimeNow_02 $sDataArchivePath_02 $sDataDDSPath_Point1_02 $sDataTypePath_Point1_02
    /bin/bash $sScriptFolder/dpc-marche2dds_point.sh $sTimeNow_02 $sDataArchivePath_02 $sDataDDSPath_Point2_02 $sDataTypePath_Point2_02
    echo " ------ Send results to dds ... OK"
    
    echo " Step 2 - Post-Process model results for rf-ecmwf-0125 ... OK "
else
    echo " Step 2 - Post-Process model results for rf-ecmwf-0125 ... SKIPPED"
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Script to postprocessing algorithm
echo " Step 3 - Post-Process model results for rf-expertforecast-lami-i7 ... "
if (( $iTimeHour >= 13)); then
    
    # Get time
    sTimeNow_03=$(date -u +"%Y%m%d1200")
    
    # Execute post-processing script
    echo " ------ Execute post-processing script ... "
    python /hydro/hmc_tools_postprocessing/HMC_PostProcessing_TIMESERIES_Dewetra.py -settingfile /hydro/hmc_tools_postprocessing/config_algorithms/hmc_postprocessing_timeseries-dewetra_algorithm_server_realtime_ef-lami-i7_mp.config -logfile /hydro/hmc_tools_postprocessing/config_logs/hmc_postprocessing_timeseries-dewetra_logging_server_realtime_ef-lami-i7_mp.config -time $sTimeNow_03
    echo " ------ Execute post-processing script ... OK"
    
    # Send results to dds
    echo " ------ Send results to dds ... "
    /bin/bash $sScriptFolder/dpc-marche2dds_point.sh $sTimeNow_03 $sDataArchivePath_03 $sDataDDSPath_Point1_03 $sDataTypePath_Point1_03
    /bin/bash $sScriptFolder/dpc-marche2dds_point.sh $sTimeNow_03 $sDataArchivePath_03 $sDataDDSPath_Point2_03 $sDataTypePath_Point2_03
    echo " ------ Send results to dds ... OK"
    
    echo " Step 2 - Post-Process model results for rf-expertforecast-lami-i7 ... OK "
else
    echo " Step 2 - Post-Process model results for rf-expertforecast-lami-i7 ... SKIPPED"
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------









