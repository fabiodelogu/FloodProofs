#!/bin/bash

#
# Script che trasferisce dati da locale ad un server remoto
# /hydro/archive/realtime_ws-db/2015/12/02/14/gridded/

#source_base_path=/hydro/archive/realtime_nwp-lami-i7
DATE=$(echo $1)
YEAR=$(echo $1 | cut -c1-4)
MONTH=$(echo $1 | cut -c5-6)
DAY=$(echo $1 | cut -c7-8)
HH=$(echo $1 | cut -c9-10)

#source_base_path=/hydro/archive/realtime_nwp-lami-i7
#dds_base_path=/share/series/damsdeterministicecmwf 
#data_path=/timeseries/section_q
source_base_path=$2
dds_base_path=$3
data_path=$4

log_file="/home/dpc-marche/log/dpc-marche2dds.log"

echo "Running script dpc-marche2dds_grid with Parameters: $1 $2 $3 $4" >> $log_file

dds_host=10.198.26.11
dds_usr=root
dds_psw=rootroot

#echo "$YEAR $MONTH $DAY $HH" >> $log_file

FILES=$(find $source_base_path/$YEAR/$MONTH/$DAY/$HH$data_path/ -type f -name "hmc.output-grid.*2300.nc.gz")
for FILE in ${FILES}; do
    	#echo $FILE
    	filename_nopath=${FILE##*/}
    	#filename_datepart=${FILE##*-}
    	#echo $filename_datepart
	filename_year=$(echo $filename_nopath | cut -c17-20)
	filename_month=$(echo $filename_nopath | cut -c21-22)
	filename_day=$(echo $filename_nopath | cut -c23-24)
    	echo "$FILE $filename_datepart $filename_year $filename_month $filename_day" >> $log_file
    	if ! (sshpass -p $dds_psw ssh $dds_usr@$dds_host  [ -d $dds_base_path/$filename_year/$filename_month/$filename_day/2300 ])
    	then
		#echo "creating path: $dds_base_path/$filename_year/$filename_month/$filename_day/2300" >> $log_file
		sshpass -p $dds_psw ssh $dds_usr@$dds_host "mkdir -p $dds_base_path/$filename_year/$filename_month/$filename_day/2300"
    	fi
	#echo "transferring file $FILE" >> $log_file
   	sshpass -p $dds_psw rsync -ue ssh $FILE $dds_usr@$dds_host:$dds_base_path/$filename_year/$filename_month/$filename_day/2300/$filename_nopath
	#echo "unzipping file $FILE" >> $log_file
	sshpass -p $dds_psw ssh $dds_usr@$dds_host gunzip -f $dds_base_path/$filename_year/$filename_month/$filename_day/2300/$filename_nopath
	#echo "change owner to rdp" >> $log_file
    	sshpass -p $dds_psw ssh $dds_usr@$dds_host "chown -R rdp:rdp $dds_base_path/$filename_year"
done

FILES=$(find $source_base_path/$YEAR/$MONTH/$DAY/$HH$data_path/ -type f -name "hmc.output-grid.*1200.nc.gz")
for FILE in ${FILES}; do
    	#echo $FILE
    	filename_nopath=${FILE##*/}
    	#filename_datepart=${FILE##*-}
    	#echo $filename_datepart
	filename_year=$(echo $filename_nopath | cut -c17-20)
	filename_month=$(echo $filename_nopath | cut -c21-22)
	filename_day=$(echo $filename_nopath | cut -c23-24)
    	echo "$FILE $filename_datepart $filename_year $filename_month $filename_day" >> $log_file
    	if ! (sshpass -p $dds_psw ssh $dds_usr@$dds_host  [ -d $dds_base_path/$filename_year/$filename_month/$filename_day/1200 ])
    	then
		#echo "creating path: $dds_base_path/$filename_year/$filename_month/$filename_day/2300" >> $log_file
		sshpass -p $dds_psw ssh $dds_usr@$dds_host "mkdir -p $dds_base_path/$filename_year/$filename_month/$filename_day/1200"
    	fi
	#echo "transferring file $FILE" >> $log_file
   	sshpass -p $dds_psw rsync -ue ssh $FILE $dds_usr@$dds_host:$dds_base_path/$filename_year/$filename_month/$filename_day/1200/$filename_nopath
	#echo "unzipping file $FILE" >> $log_file
	sshpass -p $dds_psw ssh $dds_usr@$dds_host gunzip -f $dds_base_path/$filename_year/$filename_month/$filename_day/1200/$filename_nopath
	#echo "change owner to rdp" >> $log_file
    	sshpass -p $dds_psw ssh $dds_usr@$dds_host "chown -R rdp:rdp $dds_base_path/$filename_year"
done

echo "End Running script dpc-marche2dds_grid\n\n\n" >> $log_file

