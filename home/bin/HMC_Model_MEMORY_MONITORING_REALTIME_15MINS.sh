#!/bin/bash

#-----------------------------------------------------------------------------------------
# Script settings
sScriptRun='HMC_Model_MEMORY_MONITORING_REALTIME_15MINS'
sScriptVersion='1.0.0'
sScriptDate='2016/04/28'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get process information
sProcName='HMC_Model_V2'
sPathName='/home/dpc-marche/log/'
sFileName='HMC_Model_MEMORY_MONITORING_REPORT.log'
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Get time information
sTimeNow=$(date +"%Y%m%d%H%M")
sYYYY=${sTimeNow:0:4} ; sMM=${sTimeNow:4:2} ; sDD=${sTimeNow:6:2} ; sHH=${sTimeNow:8:2}

# Define log file with full path
sFileLog=$sPathName/$sFileName
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
# Overwrite file 
if [[ $sHH == "04" ]]; then
    echo " Delete daily report file! Overwriting file ..."
    echo ' ' > $sFileLog
    echo " Delete daily report file! Overwriting file ... OK"
else
    echo " Add information to daily report file"
fi
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# Write report file

# Info start
echo " Write Report File ... "

# Write information to report file
echo '=============================================================' >> $sFileLog
echo ' REPORT AT TIME '$sTimeNow' ' >> $sFileLog

echo ' --------- PROCESS MONITORING AT TIME '$sTimeNow' ' >> $sFileLog
echo 'USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND' >> $sFileLog
ps aux | grep $sProcName >> $sFileLog

echo ' ' >> $sFileLog

echo ' --------- PROCESS MEMORY USAGE AT TIME '$sTimeNow' ' >> $sFileLog
ps -eo size,pid,user,command --sort -size | grep $sProcName | awk '{ hr=$1/1024 ; printf("%13.2f Mb ",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf("%s ",$x) } print "" }' >> $sFileLog 

echo ' ' >> $sFileLog

echo ' --------- MEMORY INFO AT TIME '$sTimeNow' ' >> $sFileLog
cat /proc/meminfo >> $sFileLog
echo '=============================================================' >> $sFileLog

echo ' ' >> $sFileLog

# Info end
echo " Write Report File ... OK"
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------
# End - Script 
echo "-------------------------------------------------------------"
echo " ... end script!"
echo " Bye, Bye"
echo "-------------------------------------------------------------"
#-----------------------------------------------------------------------------------------

