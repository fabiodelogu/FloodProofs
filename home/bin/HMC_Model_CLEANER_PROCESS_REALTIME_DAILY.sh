#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='HMC_Model_CLEANER_PROCESS_REALTIME_DAILY'
sScriptVersion='1.0.0'
sScriptDate='2016/03/12'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get process information
process_name="HMC_Model_V2_r"
etime_max=43200
# Get time information
sTimeNow=$(date -u +"%Y%m%d%H%M")
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Start - Script
echo "-------------------------------------------------------------"
echo " $sScriptName - Version $sScriptVersion - Date $sScriptDate"
echo "-------------------------------------------------------------"
echo ""
echo " Start script ... "
echo " TIMENOW: " $sTimeNow
echo ""
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get pid information
#PIDS=$(ps -eo pid,cmd,etime | grep $process_name)
PIDS=$(ps -A | grep $process_name | awk '{print $1}')
CMDS=$(ps -eo pid,cmd,etime | grep $process_name | awk '{print $2}')

# Cycles on pid(s)
for pid in ${PIDS}; 
    
    do  
        echo "-------------------------------------------------------------"
        echo "------> PROCESS: "$process_name" PID: "$pid" ... "
        etime_pid=$(ps -p $pid -oetime= | tr '-' ':' | awk -F: '{ total=0; m=1; } { for (i=0; i < NF; i++) {total += $(NF-i)*m; m *= i >= 2 ? 24 : 60 }} {print total}')
        
        #name_pid=$(ps -p $pid -o comm=)
        name_pid=$(ls -l /proc/$pid | grep exe)
        
        echo 'PROCESS: '$name_pid' PID: ' $pid ' ETime: ' $etime_pid ' [seconds]'
        
        echo "Killing PID: "$pid" ... " 
        if (( $etime_pid > $etime_max )); then
            kill -HUP "$pid"
            echo "Killing PID: "$pid" ... OK (etime_pid "$etime_pid" > etime_max "$etime_max" [seconds] "
        else
            echo "Killing PID: "$pid" ... SKIPPED (etime_pid "$etime_pid" <= etime_max "$etime_max" [seconds] "
        fi
        
        echo "------> PROCESS: "$process_name" PID: "$pid" ... OK"
        
    done;
#-----------------------------------------------------------------------------------------    

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------
