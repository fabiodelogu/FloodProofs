#!/bin/bash


#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='NWP_DYNAMICDATA_ECMWF_0125_REALTIME'
sScriptVersion='1.0.2'
sScriptDate='2016/04/26'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Path(s)
sPathData='/hydro/data/dynamic_data/source/nwp/ecmwf0125/'
sPathLock='/home/dpc-marche/lock/'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Declare filename(s)
sFileLockStart='nwp_dynamicdata_ecmwf-0125_lock_realtime_START.txt'
sFileLockEnd='nwp_dynamicdata_ecmwf-0125_lock_realtime_END.txt'
declare -a a1sFileName=("YYYYMMDD-ecmwf0125.t00z.PRECI6" "YYYYMMDD-ecmwf0125.t00z.RH2m" "YYYYMMDD-ecmwf0125.t00z.T2m" "YYYYMMDD-ecmwf0125.t00z.VENTO10m")
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get information (-u to get gmt time)
sTimeNow=$(date +"%Y%m%d%H00")
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
echo ""
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
        # Script launcher
        # NWP
        python /hydro/hmc_tools_datacreator/nwp_ecmwf/NWP_DynamicData_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/nwp_ecmwf/config_algorithms/nwp_dynamicdata_ecmwf-0125_algorithm_server_realtime.config -logfile /hydro/hmc_tools_datacreator/nwp_ecmwf/config_logs/nwp_dynamicdata_ecmwf-0125_logging_server_realtime.config
        
        # ASTRORADIATION MODEL
        python /hydro/hmc_tools_datacreator/astrorad_ecmwf/ARad_Model_ECMWF_0125.py -settingfile /hydro/hmc_tools_datacreator/astrorad_ecmwf/config_algorithms/arad_model_ecmwf-0125_algorithm_server_realtime.config -logfile /hydro/hmc_tools_datacreator/astrorad_ecmwf/config_logs/arad_model_ecmwf-0125_logging_server_realtime.config
        #-----------------------------------------------------------------------------------------
        
        #-----------------------------------------------------------------------------------------
        # Lock File
        sTimeStep=$(date +"%Y%m%d%H%S")
        echo "Script execution" >> $sPathLock/$sFileLockEnd
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












