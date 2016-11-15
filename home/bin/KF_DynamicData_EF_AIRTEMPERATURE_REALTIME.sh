#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='KF_DYNAMICDATA_EF_AIRTEMPERATURE_REALTIME'
sScriptVersion='1.0.2'
sScriptDate='2016/04/26'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Path(s)
sPathData='/hydro/data/dynamic_data/source/observation/kalman-filter/YYYY/MM/DD/'
sPathLock='/home/dpc-marche/lock/'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Declare filename(s)
sFileLockStart='kf_dynamicdata_ef-airtemperature_lock_realtime_START.txt'
sFileLockEnd='kf_dynamicdata_ef-airtemperature_lock_realtime_END.txt'

declare -a a1sFileName=("YYYYMMDD_TEMP_domani.txt" "YYYYMMDD_TEMP_dopodomani.txt" "YYYYMMDD_TEMP_oggi.txt")
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Library
export PATH=$PATH:/home/dpc-marche/library/gdal-2.0.0/bin/
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get information (-u to get gmt time)
sTimeNow=$(date  +"%Y%m%d%H00")
sTimeExe=$(date)
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
# Loop to search declared file(s)
iIndex=0
declare -a a1bFileCheck
for sFileName in "${a1sFileName[@]}"
do  
    
    iIndex=$((iIndex+1))
    
    sYYYY=${sTimeNow:0:4}
    sMM=${sTimeNow:4:2}
    sDD=${sTimeNow:6:2}
    
    sPathData=${sPathData/"YYYY"/$sYYYY}
    sPathData=${sPathData/"MM"/$sMM}
    sPathData=${sPathData/"DD"/$sDD}
    
    sFileName=${sFileName/"YYYY"/$sYYYY}
    sFileName=${sFileName/"MM"/$sMM}
    sFileName=${sFileName/"DD"/$sDD}

    echo "--> Searching $sFileName ... "
    
    sPathFile="$sPathData/$sFileName"
   
    if [ -f $sPathFile ]; then
        echo "---> File $sPathFile exists."
        a1bFileCheck+=true
        echo "--> Searching $sFileName ... OK"

    else
        echo "---> ATTENTION: file $sPathFile does not exist."
        a1bFileCheck+=false
        echo "--> Searching $sFileName ... FAILED"
    fi
    
    a1bFileCheck+=' '
   
done

# Check files availability
if [[ $a1bFileCheck =~ "false" ]]; then
    echo "--> ATTENTION: some file(s) are unavailable on disk";
    bFileCheck=false
else
    echo "--> All files are available on disk!";
    bFileCheck=true
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Script execution 
if $bFileCheck == true; then
    
    #-----------------------------------------------------------------------------------------
    # Start
    echo "---> Script execution ... ";  
    sPathFileStart=$sPathLock/$sFileLockStart  
    sPathFileEnd=$sPathLock/$sFileLockEnd 
    #-----------------------------------------------------------------------------------------
    
    #-----------------------------------------------------------------------------------------
    # Run check
    if [ -f $sPathFileStart ] && [ -f $sPathFileEnd ]; then
        
        #-----------------------------------------------------------------------------------------
        # Process completed condition
        echo "---> Script execution ... SKIPPED"; 
        echo "---> All data are correctly processed during a previously process!";
        #-----------------------------------------------------------------------------------------
    
    elif [ -f $sPathFileStart ] && [ ! -f $sPathFileEnd ]; then
        
        #-----------------------------------------------------------------------------------------
        # Process running condition
        echo "---> Script execution ... SKIPPED"; 
        echo "---> Script still running ... WAIT FOR PROCESS ENDING!";
        #-----------------------------------------------------------------------------------------
        
    elif [ ! -f $sPathFileStart ] && [ ! -f $sPathFileEnd ]; then
        
        #-----------------------------------------------------------------------------------------
        # Lock File START
        sTimeStep=$(date +"%Y%m%d%H%S")
        echo "Script execution START" >> $sPathLock/$sFileLockStart
        echo "Script name: $sScriptRun" >> $sPathLock/$sFileLockStart
        echo "Script run time: $sTimeStep" >> $sPathLock/$sFileLockStart
        echo "Script exe time: $sTimeExe" >> $sPathLock/$sFileLockStart
        echo "Script execution running..." >> $sPathLock/$sFileLockStart
        #-----------------------------------------------------------------------------------------

        #-----------------------------------------------------------------------------------------
        # Run - Script
        python /hydro/hmc_tools_datacreator/kf_expertforecast/KF_DynamicData_EF_AirTemperature.py -settingfile /hydro/hmc_tools_datacreator/kf_expertforecast/config_algorithms/kf_dynamicdata_ef-airtemperature_algorithm_server_realtime.config -logfile /hydro/hmc_tools_datacreator/kf_expertforecast/config_logs/kf_dynamicdata_ef-airtemperature_logging_server_realtime.config
        #-----------------------------------------------------------------------------------------

        #-----------------------------------------------------------------------------------------
        # Lock File END
        sTimeStep=$(date +"%Y%m%d%H%S")
        echo "Script execution END" >> $sPathLock/$sFileLockEnd
        echo "Script name: $sScriptRun" >> $sPathLock/$sFileLockEnd
        echo "Script run time: $sTimeStep" >> $sPathLock/$sFileLockEnd
        echo "Script exe time: $sTimeExe" >> $sPathLock/$sFileLockEnd
        echo "Script execution correctly terminated" >> $sPathLock/$sFileLockEnd
        #-----------------------------------------------------------------------------------------
        
        #-----------------------------------------------------------------------------------------
        # Exit
        echo "---> Script execution ... OK"; 
        echo "---> All data are correctly processed";
        #-----------------------------------------------------------------------------------------
        
    else
        
        #-----------------------------------------------------------------------------------------
        # Exit unexpected mode
        echo "---> Script execution ... FAILED"; 
        echo "---> Exit for unknown files condition!";
        #-----------------------------------------------------------------------------------------
        
    fi
    #-----------------------------------------------------------------------------------------

else

    #-----------------------------------------------------------------------------------------
    # Exit
    echo "---> Script execution ... FAILED"; 
    echo "---> Script interrupted! Some input files are unavailable!";
    #-----------------------------------------------------------------------------------------
    
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------
