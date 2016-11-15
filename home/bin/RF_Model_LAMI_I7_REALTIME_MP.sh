#!/bin/bash


#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='RF_Model_LAMI-I7_REALTIME_MP'
sScriptVersion='1.0.2'
sScriptDate='2016/04/26'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Path(s)
sPathData='/hydro/data/dynamic_data/source/nwp/lami/'
sPathLock='/home/dpc-marche/lock/'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Declare filename(s)
sFileLockStart='rf_model_lami-i7_lock_realtime_mp_START.txt'
sFileLockEnd='rf_model_lami-i7_lock_realtime_mp_END.txt'
#declare -a a1sFileName=("YYYYMMDD-lami.t00z.ALB" "YYYYMMDD-lami.t00z.PRECI1" "YYYYMMDD-lami.t00z.RH2m" "YYYYMMDD-lami.t00z.SWH" "YYYYMMDD-lami.t00z.T2m" "YYYYMMDD-lami.t00z.VENTO10m")
declare -a a1sFileName=("YYYYMMDD-lami.t00z.PRECI1")
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
        # Lock File END
        sTimeStep=$(date +"%Y%m%d%H%S")
        echo "Script execution END" >> $sPathLock/$sFileLockEnd
        echo "Script name: $sScriptRun" >> $sPathLock/$sFileLockEnd
        echo "Script run time: $sTimeStep" >> $sPathLock/$sFileLockEnd
        echo "Script exe time: $sTimeExe" >> $sPathLock/$sFileLockEnd
        echo "Script execution correctly terminated" >> $sPathLock/$sFileLockEnd
        #-----------------------------------------------------------------------------------------
        
        #-----------------------------------------------------------------------------------------
        # Exit unexpected mode
        echo "---> Script execution ... OK"; 
        echo "---> All data are correctly processed";
        #-----------------------------------------------------------------------------------------
        
    else
        
        #-----------------------------------------------------------------------------------------
        # Exit
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












